"""Package the current main.py as the next numbered submission archive.

Each submission is frozen under submissions/<NNN>-<version>/ with the exact
bytes that go to Kaggle, a manifest recording how it was built, and a row in
submissions/INDEX.md.

Usage:
  python package_submission.py "<message>" [--version v21.3]
  python package_submission.py --reindex        # rebuild INDEX.md from manifests
"""
import argparse
import gzip
import hashlib
import io
import json
import re
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
SUBMISSIONS = HERE / "submissions"
INDEX = SUBMISSIONS / "INDEX.md"
DIR_PATTERN = re.compile(r"^(\d{3})-(.+)$")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def submission_dirs():
    if not SUBMISSIONS.is_dir():
        return []
    found = []
    for entry in sorted(SUBMISSIONS.iterdir()):
        if entry.is_dir() and DIR_PATTERN.match(entry.name):
            found.append(entry)
    return found


def next_index():
    indices = [int(DIR_PATTERN.match(d.name).group(1)) for d in submission_dirs()]
    return max(indices, default=0) + 1


def detect_version(main_text):
    match = re.search(r'"""(v[\d.]+)\b', main_text)
    return match.group(1) if match else None


def detect_params(main_text):
    params = {}
    for key in ("_BASE_PROTO_INDEX", "_MIRROR_THRESHOLD"):
        match = re.search(r"^%s = (.+)$" % key, main_text, re.M)
        if match:
            raw = match.group(1).strip()
            try:
                params[key.lstrip("_").lower()] = json.loads(raw.lower())
            except ValueError:
                params[key.lstrip("_").lower()] = raw
    return params


def write_archive(main_path, archive_path):
    """Write a reproducible main.py-at-root tar.gz: same input, same bytes."""
    payload = main_path.read_bytes()
    info = tarfile.TarInfo("main.py")
    info.size = len(payload)
    info.mtime = 0
    info.mode = 0o644
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        tar.addfile(info, io.BytesIO(payload))
    with open(archive_path, "wb") as handle:
        with gzip.GzipFile(filename="", mode="wb", fileobj=handle, mtime=0) as gz:
            gz.write(raw.getvalue())


def package(message, version):
    main_path = HERE / "main.py"
    if not main_path.is_file():
        raise SystemExit("main.py not found — run build_v212.py first")
    main_text = main_path.read_text(encoding="utf-8")
    compile(main_text, "main.py", "exec")  # never ship a file that will not import

    version = version or detect_version(main_text) or "unversioned"
    index = next_index()
    target = SUBMISSIONS / ("%03d-%s" % (index, version))
    if target.exists():
        raise SystemExit("%s already exists" % target)
    target.mkdir(parents=True)

    shutil.copy2(main_path, target / "main.py")
    archive_name = "submission-%03d.tar.gz" % index
    archive_path = target / archive_name
    write_archive(main_path, archive_path)

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
    if members != ["main.py"]:
        raise SystemExit("archive must contain exactly main.py at the root, got %r" % members)

    base = HERE / "public_v211.py"
    calibration_path = HERE / "calibration.json"
    manifest = {
        "index": index,
        "id": "%03d" % index,
        "version": version,
        "message": message,
        "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "archive": archive_name,
        "archive_sha256": sha256(archive_path),
        "main_sha256": sha256(main_path),
        "main_bytes": main_path.stat().st_size,
        "base_artifact": base.name if base.is_file() else None,
        "base_artifact_sha256": sha256(base) if base.is_file() else None,
        "params": detect_params(main_text),
        "calibration": json.loads(calibration_path.read_text()) if calibration_path.is_file() else None,
        "submitted": False,
        "result": None,
        "notes": "",
    }
    write_json(target / "manifest.json", manifest)
    reindex()

    print("packaged %s" % target)
    print("  main.py      %d bytes  %s" % (manifest["main_bytes"], manifest["main_sha256"][:16]))
    print("  %s  %s" % (archive_name, manifest["archive_sha256"][:16]))
    print()
    print("submit with:")
    print('  kaggle competitions submit kaggriculture -f %s -m "%s"'
          % (archive_path.relative_to(HERE), message))
    return target


def write_json(path, payload):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def reindex():
    rows = []
    for directory in submission_dirs():
        manifest_path = directory / "manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result = manifest.get("result") or ""
        submitted = manifest.get("submitted")
        status = "yes" if submitted else ("unknown" if submitted is None else "no")
        rows.append("| [%s](%s/) | %s | %s | %s | `%s` | %s | %s |" % (
            manifest.get("id", directory.name[:3]),
            directory.name,
            manifest.get("version", ""),
            (manifest.get("built_utc") or "")[:10],
            status,
            (manifest.get("main_sha256") or "")[:12],
            result,
            (manifest.get("message") or "").replace("|", "\\|"),
        ))

    lines = [
        "# Submissions",
        "",
        "One directory per submitted artifact, frozen at the exact bytes sent to",
        "Kaggle. Regenerate this table with `python package_submission.py --reindex`",
        "after editing any `manifest.json`.",
        "",
        "| # | Version | Built (UTC) | Submitted | main.py sha256 | Result | Message |",
        "|---|---|---|---|---|---|---|",
    ]
    lines.extend(rows or ["| — | | | | | | _no submissions packaged yet_ |"])
    lines += [
        "",
        "## Packaging a new submission",
        "",
        "```bash",
        "python build_v212.py <base_proto_index> <mirror_threshold>   # writes main.py",
        "python evaluate.py 3 all                                     # sanity-check it",
        'python package_submission.py "what changed"                  # freezes the next NNN',
        "```",
        "",
        "Archives are reproducible (tar/gzip timestamps pinned to 0), so re-packaging",
        "an unchanged `main.py` yields a byte-identical `.tar.gz`.",
        "",
        "After Kaggle accepts one, set `\"submitted\": true` and fill in `\"result\"`",
        "in that submission's `manifest.json`, then re-run `--reindex`.",
        "",
    ]
    with open(INDEX, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    print("wrote %s (%d submission%s)" % (INDEX, len(rows), "" if len(rows) == 1 else "s"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", nargs="?", help="what changed in this submission")
    parser.add_argument("--version", help="override the version label (default: parsed from main.py)")
    parser.add_argument("--reindex", action="store_true", help="rebuild INDEX.md and exit")
    args = parser.parse_args()

    SUBMISSIONS.mkdir(exist_ok=True)
    if args.reindex:
        reindex()
        return
    if not args.message:
        parser.error("a message is required (or pass --reindex)")
    package(args.message, args.version)


if __name__ == "__main__":
    main()
