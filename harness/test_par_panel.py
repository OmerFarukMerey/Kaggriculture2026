"""Regression checks for Kaggle file selection and invalid-game accounting."""
import tempfile
import unittest
from pathlib import Path

from par_panel import cell


class PanelExecutionTests(unittest.TestCase):
    def run_agents(self, first, second):
        with tempfile.TemporaryDirectory() as directory:
            a = Path(directory) / "a.py"
            b = Path(directory) / "b.py"
            a.write_text(first, encoding="utf-8")
            b.write_text(second, encoding="utf-8")
            return cell(("a", "b", str(a), str(b), 632149, 0))

    def test_file_selected_policy_is_used(self):
        source = (
            'def agent(obs, conf):\n    raise RuntimeError("obsolete entrypoint")\n'
            'def submitted_policy(obs, conf):\n    return {}\n'
        )
        result = self.run_agents(source, source)
        self.assertTrue(result["valid"], result["failures"])
        self.assertEqual(result["m"], 0)

    def test_terminal_action_error_is_not_scored_as_draw(self):
        broken = (
            'def agent(obs, conf):\n'
            '    if obs.step == 718: raise RuntimeError("terminal failure")\n'
            '    return {}\n'
        )
        result = self.run_agents(broken, 'def agent(obs, conf):\n    return {}\n')
        # Kaggriculture overwrites terminal ERROR with DONE and cash rewards.
        self.assertFalse(result["valid"])
        self.assertIsNone(result["m"])

    def test_factory_return_is_not_scored_as_valid_pass_policy(self):
        factory = (
            'def install(parent):\n'
            '    def policy(obs, conf): return {}\n'
            '    return policy\n'
        )
        result = self.run_agents(factory, 'def agent(obs, conf):\n    return {}\n')
        self.assertFalse(result["valid"])
        self.assertIsNone(result["m"])


if __name__ == "__main__":
    unittest.main()
