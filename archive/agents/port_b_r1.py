"""Pure-Python transpile of yhay81's "Three-Day Shop Router" (public Kaggle
notebook ``yhay81/three-day-shop-router``, Apache-2.0), ported from the C++
sources in that notebook: ``source/policy.cpp``,
``source/include/six_day_budget_guard.hpp``, ``source/include/runtime_types.hpp``,
``submission_bridge.cpp`` and the ctypes ``main.py``.

The original ships a compiled ``agent.so`` plus a ctypes bridge.  This file is a
single self-contained module with no native dependency: the two 719-turn tapes
are embedded zlib+base85, and the router, the segment logic and the SixDay
budget guard are re-implemented in Python with the same arithmetic.

What it reproduces:
  * two tapes of 719 encoded actions, byte-identical outside [360, 432)
  * at env step 360 ``select_route`` picks tape 1 when the FIRST unlocked shop is
    BAKERY and market FERTILIZER inventory <= 10232.5, or when it is PET_CAFE and
    the RIVAL farm has <= 64.5 planted tiles; otherwise tape 0
  * at every step that is a multiple of 72 the budget guard may append SELL
    orders to cover the coming 72-turn window's forecast purchase budget
  * step >= 719 returns a bare PASS

The extracted tape body hashes to
30b724c3c905d0c03e4ef38d36f96fb7acbd6abef5371abbedee36ea3717e09f, the same
sha256 the notebook's own manifest cell asserts for ``source/tape.inc``.
"""

import base64
import math
import zlib

# --------------------------------------------------------------------------- #
# runtime_types.hpp
# --------------------------------------------------------------------------- #

_ITEMS = (
    "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG",
    "MILK", "WOOL", "FERTILIZER", "GOOSE", "COW", "SHEEP",
)
_PRODUCTS = _ITEMS[:9]
N_ITEMS = 12
N_PRODUCTS = 9
N_CROPS = 5
MAX_UNITS = 40
BOARD = 10
MAX_SHOP_INSTANCES = 8

WHEAT, FERTILIZER, GOOSE = 0, 8, 9

_UNIT_OPS = (
    "PASS", "NORTH", "SOUTH", "EAST", "WEST", "PICKUP", "DROP",
    "PLACE", "PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG",
    "BUILD_COOP", "BUILD_PASTURE", "FEED", "COLLECT_FERTILIZER", "CARE",
)
OP_PLACE, OP_FERTILIZE, OP_FEED = 7, 11, 15
_ITEM_OPS = frozenset(("PLANT", "PICKUP", "PLACE"))

_MARKET_OPS = ("PASS", "HIRE", "BUY_LAND", "BUY_SEED", "BUY_PRODUCT",
               "BUY_ANIMAL", "SELL")
M_HIRE, M_BUY_LAND, M_BUY_SEED, M_BUY_PRODUCT, M_BUY_ANIMAL, M_SELL = 1, 2, 3, 4, 5, 6
_BARE_MARKET_OPS = frozenset(("HIRE", "BUY_LAND"))

_SHOPS = (
    "BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "ICE_CREAM_SHOP",
    "PET_CAFE", "PIZZA_SHOP", "SMOOTHIE_SHOP", "YARN_STORE",
)
_SHOP_ID = dict((name, index) for index, name in enumerate(_SHOPS))
SHOP_BAKERY, SHOP_PET_CAFE = 0, 4
_UNKNOWN_SHOP = 255

_KIND_ID = {
    None: 0, "EMPTY": 0, "SOIL": 0, "LOCKED": 1, "WEED": 2,
    "COOP": 3, "PASTURE": 4, "PLANT": 5,
}
T_PLANT = 5

CROP_SEED_COST = (10, 20, 50, 100, 80)
ANIMAL_COST = (300, 400, 500)
LAND_PRICES = (1000, 2000, 4000)

# struct Config: only episode_steps is ever overwritten from the real
# configuration in the original, and nothing reads it.  These two stay
# hardcoded there, so they stay hardcoded here.
MAX_ORDERS = 10
HIRE_MULT = 1


def _fib(n):
    """kag::fib -- fib(0)=1, fib(1)=1, fib(2)=2, fib(3)=3, fib(4)=5 ..."""
    previous, current = 1, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


# --------------------------------------------------------------------------- #
# tape.inc -- 2 routes x 719 encoded actions
# --------------------------------------------------------------------------- #

K_TURNS = 719
K_ROUTES = 2
K_SEGMENT_TURNS = 72
K_DECISION_STEP = 360

_TAPE_B85 = (
    "c-qZfTbAr74*aiG<PtyvZ1%sgsq|Bz2-$t_{g~5ds;8@*B*q3wp-?D)@+bZNlRxGAQ-AU&r|oz7(|&)hAN~Eg{QfMTEXN<%&-(qWeE*d{^3%>i"
    "_urrYk?(Ii|M2~yY_7jX%k$Ti`@_H2%kT8c{p;#KyqGUAAM4wHFMe9b5X%RBs@Ojs-?>k~Ov`=BUa{=6>TV(M1dp4p=E59(m6|CX(;U8c{|o+<"
    "pVRTZ9e&j?{P3xTPB0yB+A+c7|KC?{zu&Ga=9~Ac?ezLJo|;d0{8EPByZ>gru4CWZAHUcBCb{puuUO5`^zwUk8ZWu;P4Ii|&-LYX{pEG;=g;@<"
    "YjiyP)ay?D&w5>9H)4Tf94}@D-)4qcz;4avcl%ZQ8=9NnV*BrYuR3?g^1Fz`BmVu%{*s@+*X?R?Qy263`|7e?z5n)@KsT3{X>i#loQAt{XO_9f"
    "ZfpBq-d8kpU9RwwWWFZ_SM<j#%0C$6U(7@QPsT`paK-nL?VD(SEtnnt&ac|7LU!HnCDVcJHr)1-$go$Uok_0fZtn(1#PD+a^Vdwp9)Wqdt@EJK"
    "Xpl-wSed6%+$d$9iXY|vA~Cz#?#G<wxu~1;I?u%plM`MS`-SVYx@1MJLG}}=47Z~8+uHW$-E-SUJe)Xp?{@C)Z}S>u;)LjR#o(>=`4qNGM6B9>"
    "*kJnL=<XY=1@>%oR5RL$?v*?CTAN=y_J+23Q<CksUl=(__PUC9ul=Z<A{a5vS2p+Nnis^mRl~bo+^@{tlz9~E+}XS7&brPX-ElYSZadqT%-oH-"
    "A?LdhvZebppua8wXLsM1YF@z6*4*xbo}1IYANKH2F#PGBh&w>+A-kC!yI#Y%GMh;AsI0?O&k%FEu$e2Ha~foRR?NGQz-?XZSGQr$*Lb&YORw*Y"
    "D%`)$?lN;~9KZcS@A8c&q@EX6v&cEJ<clA&&sMm(cSWHu@4tvx`|h_gm`s{?l((|0_1XKipyCgV1-b^qI_dnXTc=3eCb!4Z@EGm+v2UeydXB|e"
    ")Py~X>UPX%=<>J&+$G*SiN;cL#XK!_yK{72b-V3KE$r?$-0!Tuvd8t<o6O<WEs!b~I#VKN)|!O<1?DFEf;fhExL})oY(jtFMi$wInX&0+yQpB3"
    "3})Q1N%k9L*yOiO9vton6B%8AG@l-qA-iU|+qC^>9{{KII^1qEGB_R1TeKH8cNTVdVIc#`be(ulct&Tsht2l;8vJzg==~wHUti`So15NzGfJF|"
    "JRvzk>~$ZmyAjgwo)uzf_Z|IxMB>bCqhr5ClQK6jk)f7-#g8}V_L!=h{tZ0U;WzfE*+<!KAYGR$7^dLiw~va4ag)bc@n>`LsA}?XYla_If5O-u"
    "$^P*B*=74Dr*p3oceA@O+x{^FTkS81b^X3)^}2nH0RKWgD&_xhj(-kw#-NosEz83|U)QJ~uflZsF*aCCGtlpcr)5?1+NqmXo>AldX&0aD$i)q@"
    "I>XktV>P?e|NLDsen|(O;f-K+GsI%gu<9I~GA2Uw@^-p;F&ps53W3k>S8IP5eru@%+Y4BW^OFK1Lq#CP;c4EVL^+pEtZKhL+r5oa3{hEgV!w8D"
    "bFpPSe?NY!5^Dx5R=-}@;_zk`SdM$<_e;0W-@vvGlXC&Ao%HsS$oBc+{P4(WCv!huv+sY^>(r6gCStc)<!8B0@&Zzs`1dB!X&+p5KMVPd+3esu"
    "SW3fx7`S@V?<$Ldx_1EUaJY>TSpx&ebQ~_`SQv9E)_~mh^)><17HR&-6>@mC>-68h!vYxU@-F!EdOu2>vdQytr{rbqQ$T#&_d*O(nGUQ>f(-vj"
    "b0C=Q-+fkHiPJcrk{*FjcM8dLO7;*<WMM*wXxHNLV~;n?U#bkju;=A`s<XvZY>CL7D#<<c=}1rH=r6>Qr|VcwB+~2T4NTK}=(AKFBk;Mj`;)`5"
    "Y@vo@d#=G}+0Vf$j-LKHxFK)P?{6$oty^A?m|jDdYaHx5%r=Ceqmu>4$$5X9%e(ykuR(Cl`+WPgIvhvsX4q`L*x@-J+xcMCY(x$VUL1cG7a-)&"
    "0olF1obR)zjy`X`ENa4gaxe)yRR@?HCBX+7XqeYB8j>81$8s9`#F{sg0~aR|6ky(ie8oomQb`hJfDgf%v6I(hr^7)<7tP;G1!s^>w!yBMx-%op"
    "thyxMF)fcw9P3{~kKQH$?Q*GK`A*y=U^e`6`BaCHl;x0@x|Zv9s2KL<U2PkSm^%~}L|BiqM|tT3>EEYSi4!+0ypS&|=Khu_hwD)(VE*lEWs_Nn"
    "5N3u2pBXpD^Amzbbl}%^XS~e3j;uGyJB>z6uqoRCvEg-SWMUy##6w^vYWWXv*y%YH6VoUFzIWq^pzU?$Q|?}SPFDa>*sdEkDjWOQi0Q_vs)xG<"
    "psU(bV|YpZQQZ6>E%XYm=}h6s^1?Ckkx35nXFT3>b^@+X_5Sx@)g09DlYN{B(tnMj>~2CMhR6sx>UQ<zFsaXCjFYLv#4OtbX~&k`-|6pNAM+Z#"
    "T)I#`($RaJRun-ezfe6kFlokw2LD;f&os{lz>1ySV|O$)Hy0(D5x@}`PD!)4N*A}0xs-Wv4+8+!R>(B6J^Sa|0V_+_#oUiLpQ!s4Q9}ANBRKjm"
    "&znsn$nYeVgK+PjF`mMKVI1~82<{ASTiI;3!RqkV*0;vW8!j8J{YR5^x>Z4fmQtuP#q+j+rtEKzO!?ycV&uq5?l@xo4xA{YNPiL@;?EWh_WwHC"
    "GCBKo9y1|CHHL4_Q$9JXwGXHu>)UxgII;YU8&W;>!lz?Fu4o{KknuD;a{zL8kXEv6VL1UPlN(P)SK>?F9p>7$UzI)mQ}#V58>(3@h+zN!2-_^1"
    "A-u0V=!?tXE|-s#`xU(pn{6&`s>?kgm=0;v*je@ogR&hv@4|e#!3&aUP0kr7R^r3xP7vYV=d+EzkL$_$fJEg(lW}n4l#bIqKBz+}&b{aZovHe{"
    "*LyAeY&{UNdOGCtA!$)_UY+}j4cnQO2aoT3b2ljK@I}=QpU7#0(g_1D*3OM_)j*61$(*Nk=-|j2DL3XsOcY5-2zepy(sH<=0_hTfwzz^bwt|1P"
    "-G`H@q$ovnXN0~E|FYw~Fze%ZgWK=o)%{f1;~?D^CmUWyf3W=R(}$Pbk}irfZ1GP4;p=u-C6HFv36`;6CS!&r0}6q9Qv;}v)%))LJN5PeG|UE$"
    "@8R$Udz|N*<Ox7$pXis-pH^2M<?ib{&~ZQ&79$-4VVc!VR>*#;hz3+%t*3X0>?AXL03+>TiCA}jmVg2<tYP=igv;Cm$FGqR5^>xHT+MmR(Vw{X"
    "nTt0^B+F&Jh{Bk%)h|e4*fg1=crytGS_zzCXF0td?oq7nt(It#ojq)2?`I)F{9uCt$7o>ROfRUnS!s57U0K99X-}p0P`^Lad;mF&P`snm=NlHn"
    "k@4vh@i(jPW_v_@9Bv=H*p{DYPFx=tCHi8kf4a$VWz376$Q%nxvkvFGyJcqfU;lNE*887F>!ZE&@p3)tC}!Ja%4o{~GZmInq2RKCc9dgyg{9mk"
    "Ksk+8b$Gmm{mOx^%jWYBn|l9M2}`&7#cWy!z?FIQ085?#*E9$4%k@}<SD6UL%+Q)-cD&2DCig_z1NkZOiJUG>0k_osX>Wgubz9O*`kQ!9i9zCh"
    "e$aejR>mF86OTv+_^riY>x%2V?JWtoF@0s=9SR5^cw8TA*LHCM12n)1&jh$ZiIoYicplxKAIZHFi7<ie2CP1s0}-Rl#+0W6l6T+}OQAX=k=TMJ"
    "f&m{EDcw<TSWU-@Y0Uur&rxDi+_U_d`Pm47454M1tqULbq%8ouB*vfJF??iy0c&3v)>R1JXo(ZZLt9AV-5<%rNZz?^Bp&lMeV+W%pR0wz(KQUT"
    "Fqb)dA&X&^x?k|d^k@(!<Z_mlQUD6FypOv^>m+QQ3W=Nik$h4UEUzrF*!O`Ld6+x*POa3;6=u|BeyN;d!DKy|D{Y@3px*iFY6*|qkpbnyGLR8e"
    "a_Wwxp2pHFg?T>-FO;y<3L{cItP|i(#pF+A>y(+})P3mluuh$&qm=SW@0UFhrtR<yK<Jq!v8uk$j8O!c=}Tx<iP_^<=B`_Fw;lx5zX-E*bdG1B"
    "v;wlHwRc}*+poW_J5fxo?8Nt&=y9acX)>=J|E%ZJ^Z;rG@z{_wTeeh|n9yWn%G&WpgOWU?=7BQHx4lk6s9EOozjj6=5L2)5j``)xCUYgAmMdmK"
    "(AaWCea8$tC`wpvb5Iz^Y50$8yvTYt;`V@8GVh2!tK0X$Ac6$zJr;-rz;gF^)x4KO-6f%K&Y}9{mr6oVYtXTKSSmoPqNuj>nNU8y;1ZAN#uN4j"
    ")w@TPKz$x6rLPpY;q2cN?-6E3vjoTgN?ahYP>zX&7_19+2aA7W5@8W2bA3Q~u~I~lc$sqB$j&M%fGww<k1>+s_d#OI*C{BOCs6WDPSJnC7#FtB"
    "l|K9v-s@?8)+t#iB%j3*xsBK>ut2G97`-^?(*~az(uNkF-%>(BpWNf*kUIm_7gBSAz#u?z8*3D9<T|tD>I9ep)GB5m4a0ZlaVrCI?HswA!s~lr"
    "O6L9`%9+u1%xpEcFDX7V1EN5*ni+5&R($i_PP@EYO_Gk1u*zUuOhMCiN$g_^fH4J^Qz$C_>tSY}FI?@ntk28oF*=uw<77Be=p!>5M!^H2xKO=3"
    "&Rh-MITy=@sk_VqeVx!#T7cVx63?SV2-WvR!l@nc7cT4az%49<?K-4W=FDO7o&^QldUUs$fa^gmH4wKsh!uKOG$NuUDz5gx_4%IbH~TZ+Ho(dO"
    "AqU0EQO0x)t#*&%TKyO4!}7V*B%}Q`SLxTo0As8DJF;Fjau4J@D16)TD^#w;4wpOP+fSkNlXVgkDgpZjCu6|7IS)Dpo{6S2<FdVDT&f_W4E4;P"
    "prm{sRpU?P6qmn<6JN4(&0#ey%FN^(O%}n;Y;&W%T70meQ#AlOEriMMWG3rshRw9pCIJVndb6|6i_0`=QI?>_dC+UNa&`+yKHM4K+ox)+amVQ)"
    "dtB_>1~@Q6p~Dn$e2%xR`p*FlI*_Cw6`#kj3x)@fW?^Lk+jKn4aO+5i{dEu4>5(psLNf`De?My1I5R#xP-Bek*)eUp#vqvsDnY&J|Blg)!54;&"
    "o-3nY_p^A{btUz%ZTrOW92@WrgzD8U{!t1(Hxi>}d8M|IBb``vlg`@djY;Yx2Bxd`95jgKmjgL|%S^u0Qr!mqf9XY3l#>~t@D-N7W@FeX0HBkU"
    "$eTdF1VRVd4;eH!08WI(0m^*37w&c@Hts@Xw#4jTfOR$E9w0Hsim6{|u=hQ*^gTu*x^p6E*gD3gi6)^v0~fg`3v=yIlC@wvurD&QUyWtO*RjH="
    "-4#aNCxCUPlKC}e>IH>EFn%p6%TPZR7OievZpLyVRmLFD?c~`h4QO*_71Ba{Fl#qiEZd2?I0!{ov+EK<OYWpn9-U7Hj!$Rra_u_>fZpQQLf;e&"
    "mw72Nsv2RM8{p4r_8}xBQWWO5dD^Xx4#X%ZA*>Ln$A0r<G805{V-a(jg70M1g>k>+g$R>*dk+_BN(#i590-Y8YTag1lXV`JqiFeUxe;TSZBh6?"
    "bRHU4d#*>@iwSWb1*p#a_X3NaofE-I9n>jQ52%Evd-zkGZ3p0!_+;C%C$!y}-q{e9YOaWZR$QD6!jD1?CFQ%RJ0yh=(Eyijthy6_)U|spl;Vsz"
    "l=5eSpyzg5E@lF#JV{g}vQ2NN7zy4+XABa=l@c?$LsEQT*bxMQ>M0v0gxhlx)se40mERcj!{+PrCI~-Ky2##N9^!hh2M!WJfVZ%kXXoR3VU8Kn"
    "7;7xlEY8C&OmgGlv{<mUwP%lfqP}>_o}~A-faBL6LLuO^7oXWv2Bm@|&B9tqbe!KCA&5fi$`127y;+SCUuPQ%`{^*SeDz-4iUCmoP?{GLzF<gQ"
    "E6>MUxo^6FHw>au%R{-TZn-bB0lmLNMQH$cC(rDIf0E9q2k)Rjg@Jn5M9<PYJ&ENm&&58(o0Nmn6l3u+b}mw8G(gLEK(PWDm5P;Q76Tv&FSCzx"
    "j5lPG31Mn4_aO;ob5p2xi&i(!)JPlK(;RT;mJ|@G`s}6T%t|qr2d;J_l(c=^&ddhKB{C?#oDXBrHpEuPDdX!@7E5p5H}x`=x_dl3XC0AYjdhaR"
    "5$F)~hqACfuW<)XNpts59u{ATTg6uZ>?fj823A2S<lQMMWX}=vN&w~jM$yYoPoX|}@!h@@h=Ia7IikbJI~AD;2{Do;jUaUPDEh$u-I8le<`k*l"
    "q2<tXk0e%!guJAc=ULr?*hs&Crzljdrm=(M2=_I@O`7@I&gwGMolDoy3E(2MEUq(FX!p$je*jOEVd9q7Xo>&z(AOVb3VCoQD$JA!KZaQWN<CQ@"
    "330A9PW+>H&!tPo#5rdN3Y9E^17iU*P}!dmQ=mmcr^&KVB&4*k#0PR$POzyR!`DYPKzhhG`zLaLiwxn7GPbuox-Z$g=mvm=-1bb1%8(1QVsrt8"
    "dQ6-daMru?&S;dXV9{w&jS|uaxJa0AL1*stluQx4Mfmcf!b*XurEWd15yHq6&`MDmrS~{ARtqhxmLX$a!LZJNH&Pj=vXMH%&Y&R#EEF<-(urfh"
    "hUlCQbip^g&6&V&7Fm!G0Ycm}5brQjjWBMiIDrO4;quRoafB&HY4q??$f_9-3x3G^SaOBl)&*E31Bj<kYmYT8cI?aYZ{UhzvJR}2-ueV(W(}o?"
    "g9(#hpg2s)E2wBc5JeMtsQV%Tj$>p%B@lU2G_No-jE_?WP{<3fz<L)#`5~Qw!;gxs-um<PE^!F961Tz75|pocrz9qD7=zSUqJ`Y<=gK_A{wA%9"
    "vh<k-Xe6zWUTPQ78WK!+fa}Z1c!h#O>U;`+I_@m^@}T3el2`onCpPxGqiUEq18o>qy^%@6RNa};!P8qA9g*^20MJ71(<J#8(Ml9p$owEvkg>yb"
    "JUsw3r59aBI$euh%4?S;FNRdmP_I+QsAZKhHy=0;0s9y_CeNi%;tKkGX(0wgw@eI-1ys;9W0T{gsg@5&@`$T6PP0$+U&$1}!x{-8|B#oN>jYjD"
    "0A2{u>Urc;Oc8Z<1(M2G#SF+8Scx?*tj(l`iLs^uK2qW;M+9c6J9kkCol!<xiQ*&TGhQPrFIOz2N~E*W3Pa$Tkqm{cmKt?z3N^!nNg2OMhFq}H"
    "D2>Kvs1{6SED_QvsCz?oVX{j=w6JPfsE;=u_K9R;;EPik__Bs|)NLMJDQ-_Sa**D~O&vbqFXdi36(i!?&7|GeJALq~Vb=6TLddPA4xbZ@l)xK>"
    "j3zEgLnWe^v_@wU8b>!0I}nuC`*ct!>;R4xHBc}B$I1ZyGVOd+rsv~p0PXvJDnjTapi-j}H)mzMQni|&4&&&tm^{cfCa?VDArAS3qJqM_!$csC"
    "_d<Z3B~cPipR`>f{BSS-qeJquUWq7Qu)%}^<8h7ifztnm^*DTig!tMW*pD0+u&<Qu)Nt(4f;6s@un=xKfhlcu2q?~6yjv@=?_^a`l^LQO<I`DK"
    "*;AI8mjSs*Af89fApDuVy5Zr9XGVNl<AQI;`zQ~En~e9=BZLDkxjYoZXJO8=M{mc)7U1fwai&0-Yt-md0^kX7Qw7%?0E)3va9NpXkt@il)Lb$c"
    "P@~l0xW+ZsPRi7lcg)#AZCaE`Dfu(c*SsGM%m7lCC>JC>dAAPPFB6U8hWD9&#hm3&^1y!eMm;AYUD=&|^}SBfHc7EqS0M`Xs~fd3u!pK$GrOHg"
    "B9u}yVsN6&gR)wcKdT<uy@~temtA#u`2%&SJsHwK4X7nu)T=w(lS^U97@Za>#-z9su_lDd74cHN!K^Vh1`;4S>Jb)zRmQr?nGg;Gv6KF0!g<Cp"
    ";u1(9Ww0GU)p}wVyR_y3ss@5n6~N1P-TsR3m_B`1*}tXpXUauzKfZCy%(1epk`i!4DKQR&+I<eI2N(uXY5*>lnQMk9vA2)`AOk2fjmrIoI7?WW"
    "_D3PMkLe?1%9cYp8&+sCKh!)PE<Cd-Oj=2KeQJVD7&9wn%o5JJvs0^5amhq96O?cVa=<Gk6kU#%I__$T=>k0jOV`OU>b^i%cvNE7SEAyZaUl?U"
    "eF<ADgzT5j#oU;R4&Vi4nRi^G=YI-ior{Aj`=2LGLNVwWuQ+6)jtal!uknhxLR3bZ*KAui=wrwsZ&*nQwavyXADt+mSjbWi;k?Ea9*~Q{hOK9l"
    "KB%=W@8m2z8r{xe6AX!Y-3fh4>DKt;p%8as{7;vuI0kQ@H+_%*ZZ2RI^ca3@uD4L3ze)qFJ^$`Ij|GTB^FjYgaT+7~2f>E)kWSg>r_PY0mv!}F"
    "F;!?1f0W8>syd@(0)Z_%&urR|p+eshAEKS)B~AxGKCs7Ar@0{zfOoIn<JYsl$YFGEtFqT$T^^WB9WaeDpd_S8ZnwP>X3?lnADpE2%>(C)63vTl"
    "S<r&XjXl(4&Dcdbrr4;bP>Cc)pDVJ|l$Yz+Ie4L2pw3{F)yHNsD^ahX7u}AALuesFw)wpxHMwSPS5*JFTTz*`qi%fQb+;m~N<BJmtj?gvbj!2b"
    "!ZB)kXzzt`%?pmFAKilw=^xZcAu2i|fKYp;>}9a+FGofvo074o%NY*K*n7cI9OSOxB61c`7^srq;r<3SE~kv1NeyY4yq<FmGS06`vv0Dnke#9I"
    "E9!coclQv}qxlKv=}*zn-2|iG!v}AN(lpOPNvyMDJv`qvwt$TooXcn_#B(}JNE8BU*!ua4W4X@TvyrXSWA~GFpcQg@(4HQE@**tzS1$9^Avcqf"
    "Y_^wS^eq=c-)FJ;isi0hFQgRXR`RS+T^K>s|E7|>!swmXu;73`m+rLZL570KQGjA*ce_ALs=x4X0l9S+M}K4ZJO0hs+<xP+{tXi{O{ErX>Mox)"
    "wj<M?-Uu+wxMWjspN8&9td<fqS!Q<ok@H_^;DA-qL#jW5;WC2^ylnsIGYI?m$_lmn9n~MT)(>%FCtiM;5!hY7I1hc!xvVmz{U<EHdn(Uw9NDL4"
    "#Vdf=fIU6Z3@&2I{3(NMD$vPxElMhQRHTNH9U4fy;o(s+t*!mh7pnZ-Sq)h+DV(vieAyC(zngKf+WSCWx;Rt-l#94t>PicJ5q(lZ1z7NI3izB7"
    "VGlq=a5p^dq#Q7YJM1QsI2OVrxH@s~?ClC+CMheMTEm;IvD2PGGP^%d4<Vkz9v2eHn+_F-51tq%a2DBMa*+WNk=A;Og_jb3a>H@{&_62X5!fmQ"
    "0|d!mSnqPk^=YWSl!c<@Z9)yMC|;;MQ6UGQ(#nN=1oF8K8~Q(voP7zo%ysl7ZXS>$6wP-w5mF4qh)*)`%52OScLZQZmduhM_Zv<Vm4QkCiL;La"
    "0eO)bSQ)Jxk*Kaw=>jGa(GbD!Qz(W(X-uGk<Oc7jezZ6eTI4DOKki_P2LugkCaBn9X6nGx!6uw%AaMmpfk2H2h`H%3SIUCJtD0jViGeXl8hV|;"
    "W6yZpWT%DGNd0-daWcd<(i5t6#pNQ>>)8hCQNDmEp?bX=i#l#OZ&(A)Tt0x!_u;&NtZAT>-9xG9DQtnF%sIB1{c!=tPRjiap-&i+E-sP(%G9?A"
    "nZM~0%U>9GebvE9U-fvn0Kq~abA7?zbG813VM0CZdQrk)ygx90Sd-d^Ks<B?`U5<M{R4&pp+?e*a$$s4NRypPPJQ1flC||wCiMf1$oFgjUHF6%"
    "h2`_ypvc}e!(x?;rYPDb3PFiz5j5i78HI_#zXG?`=of)B$$iQW{SjjsP<fGnc|Tf@me2xB+27<`If)Q}25at5QT=LN0sTDoph3A3nL?Js6>5M_"
    "Lc$$XNIX;ibFr4YkYy-@O4-=c+Wv67Q=RrvnHr?K1E{$L-+m6OD{du1oD$_ny))QjoezCbd}#OU#Y{YCF4JJ<a!Ag#<NeB;$+eD%9ufBSsr6vh"
    "Z}6!+Sl_x+^6NKyC_l}>;2A&u;}83dHYcvU^@<+8#&XubQ2Q=DkZ-ho`tV}Dz<lh~@6Jfj*(}ufsS!y$LEGX&b~MEkQnX#agAV~>M{z6QKBZ<#"
    "Ln{6F-u*B5Q#2>o;aAc2v%??8Po=BsrNF3o`~7y^$iOL(RNOuZ3FkS_Bl_O`H|upB``-Tey{>F$_}&>jSf}ga@6~BM4<01=y}p0T^L72@b;x-y"
    "pBlR5b;5gRX3Tzt-G~K_5j0ja!z^I8+OvDV3K<e>PkyhGD@b0ET+4p$Z@<^=Y9Ud={`vdrvR%FZ77)zJG`MUNPTu;|`KA(qmC|$tXzxB>LRi@D"
    "ivD;-`3GbCi+Sk($r$MmuE<A`+Tm=4l~2`f6;}3D1HFIa1jw*gqMb>u=x*-@M+8v1>hma##I9vJXfzt6Mq#_13Zc!}sjxombqWB1tX;(lv6h}u"
    "v4F&o=dQC@tIRpQ?GlY*@ase>9Di&_`>cG9csOwx*O-|1q7ZJ(eMQFs!q3j5$hgo%<|ShK6Yn>eJ~+Dj25W&m8y!{NtHZgDvJFc&WtluGs)JZ2"
    "7bu5G6LVc9fK;C^Tw+<MJkL=`#$tA>9(aM~ZVFD`8i$S&J7$j#NJW4OhBkw|9Sh)Z7fQ&tm*BbtoZWq2>Hr2L5Q~4WIX0(#Kb9yR_tP%-M2Li<"
    "0WR%&0cDXi`K(@Xr=B6^bYU9`^078v!`mERh&mhR={v4HU*p}rExo=os)?%8Tf5srWMp6J8UYUH3909WH4-GXmV9B7l6f{Iiqo~m#F7lGxAq<<"
    "Mw4;sO5Vz@E~B#DzQii(WuBGbl%#cvgb_ykV_b%G+G=vo=X3N)h=e_gN>VQ}Pmf&Uy_0AxC0ESTQnx!t=T*1cuGGRd)2{pb&gv_BTur40+neR5"
    "Kq>1I893XM6Pav*rOE}{>|+!912?kBg#mvB&p1bU>ETdjQu)p#bJ@ztCIiY3#zgW1WwhNP?@1oh>t~-6!FF9KyK?r3Jo@eO+RlgQI5}jlWBgKM"
    "zyL>YzpuehZ*!@pxa-S2WQ(+(%<8jDSDKs+A-g>}g!H>-g&5j>M}HrYICI<R*l*FKoL(un&4<BW^mD#Bx5wn=ifu_&a*#_l#<g3y|2wzL6iTd#"
    "=yxd`n*sZS{o28wNKCwR{;>KJhDxoap|ou|JCQGDF;ZCXpKbd916%Dch;{ws=q1o^sZW+)t>h2q_~$TZ3|g7fvOEm*b&dM*DomFjV=L49*JI6~"
    "q;DmBAFsdO_cWSIc4VJ?UO_RUoWAXF`k%im#xLnOb9Eq?9k8#Rysm{puSAGm-cBck>k*7C0S9h>7;!I5X5{Zr3Wy993Sq3%CsEF&N2=r7XFF5s"
    "VSOTX{@T&a#g_5>{rIgKlJ-2cZF@*8Wu8c`QjL^JAAoHgCYOM|j1DfbY@hEj*{X9+-<E3q^iRD`9eHgccAHgxmO#&|hO!YyfPFu>>V6jT8?)KL"
    "cd(R(|1j6lnbIRZ2I}4ctcYH>kSaoZa1Wmtav7I2?Fu5>+XO&Kz~RUha(K4u^xwb30vPJ@F8K3$KT4dk$@6ii<YnwrKz!WyLJU%w4lKs#P(VLc"
    "aOiZORS!wdZoZ^f)$w&Qos#_p1-rvD(xY9A$B#YUFn_5s1jC+}^Qq1jQ%TJRzEdT+hdv$YDHPlBmONd@a{5GlI+Rpj-0z{!QhAKP=hE&^Qh911"
    "=P-Ykl0Fxb7|U0YRh-nC&+l(6F%)3dBc|8T<r)Xmoh_Q6xKU=ou_G7$9A%taLFvK(fKeZCr{RnmvKPZ<^TiI&`Pj|}t7ao|Sn%Tbvv~G$=z#3r"
    "Ue0rknBMdm0WpKJVzW$4j*{Rb;<ujjT1G>Xqwy#gI6IJK@m!oxD%b2mzG5SOsZ1#@#cRe+-i~w(6i#i4A%hCeAf1cfGA?Rlnh;S(p<`MenK;(J"
    "gdY7+lb>-!I3}X%ixL*UTtd`*N?a&<EmsPpy;x&X8;h7b6c$8Sk23D(bcir#r{KlRP}l@xSg7)%`h>_>4X>3=W+g(H0i_~0<K}pNLeL1Vn7;Z_"
    "i+n*{ndF^DBPOKO;t<?1uR|jfd#zJc=BVY5bc(XUt~~I~)QYS<uIFxDcWWo(5eKr{HLS3(ki+(b6$CAyOHZ|@#_*E*qnN6#X^=D5ACLAdFB}uV"
    "1P=0NJl=D50<I5`#u==dgBpG^Qxwir)vt#W;sVYZmU!x2qSHx`{h$rE9A)^+(U(w<x8j&rij|gtcT&cQ&7%596s<i9nH<a1!7I5EFj8FtJ(Esh"
    "o!z4+hr78b$&3Jwz;H^M#nlIarjFHM?cyE=U}5!=LiiBJ*+1V7SXsI*=6=NaL_oMh3F*&_psdwEi{$tBgH$HeKtHU;RiVYv)7}TcoxyD@Z3eKZ"
    ";SFzXeQT_|;j-b{UzF&_{Hh%OCeQT%JL;rX7v#-2&sK8B5i5|ic=MC+5N+AZe;93<oc#(!K~kuCM_brU@<C3w<f#WSO$!f)GOf-^r0^06mNzV|"
    "qLHBZh%~a^LA#0@tFQxQY*W*-@@eB-+xDxnr+>=62Y1b)azO<9|3}znIT~s<lW@}UEdLHJ<$gu)!=_vc)8Ym#%)c8_>uswGvNdo+*^ZreVLsj9"
    "1<AA~btqH>B|ePq1QG6iKHKP4U%{6E2}r~NWku(dj?+Cps6#2vz3An`I`}j*6*5~7gsh$pi5ePQW7M(8mkryQl?RXSd~-J_>+nU@4xh+r1MB-O"
    "F4oSCan(SK3CWy4u&Yj@FK{ldh#epa=|MqK+$?PAe))ur{(yGm1VPp-j8r?*^*<`#PA>m4-}xI^Jy61L>1AW}emS36J_L5M;blCC?f!g)b!K&Z"
    "eI=xuNxk|QzRKJyTV2A{f7z((XWr}~l$}itpgvabyZi4nB2OA-11Ejyg{X55v4C6vboPn<Nw`@f5&c_XrP<2gj!+j3)M2vS#M4w0t$BW0&kUuc"
    "VaC-yfRXmFglaHumVg2<tYQC<K0B^7zcZ8DiQ1#jWw|+KAR4T=V5CM_E-z6daacN*i?+9O^g6p}pq0QGzP=kZuxTz4*9m#VOp=PKDtkW*3E~GE"
    "3^+yu`=)qRM9@6P>!oJq8LYH@#vC(fn0o{T??M7#F9kxtk4Zz(JLPE>#URATQQfeTRBD<}+|E>YDuW1yr<)8{#=O{x%(1XE>u|oiTV`he^<U>`"
    "z5jW%o?X|x3hby7xw=yn$G}YG^QK!$@#iN4lrx}C5`=n43qJ|5l6(5e=@xTsgQZ(8Y$J!(?dTw#CW;8~=mC~I0j@;<_YfCmS!=<V8CsLfj&~W?"
    "ged&hu#{|`$mzlqs=f<^e%DEEuI<x7V@#OG63NaE*c(`wm2pS&#3Pacerqw<y5c%-drJatOkWvzhXTR}9@od(wOzdQSLa&B^GtvnlvtVIis#Y&"
    "`Qcm5QT5hDbe<E77(p)_mJR^Dm=jB(zUZSu#oR1=Gp9)iF4m+=7(V}xDa}vNh9xh5+=oRdLi@T8%bv6aV3)-Bvpa^5>@RO;QdydN!9ywa&=!(-"
    "_eb(Dl6P(!iN}0RpC`Zc=W1babPWS7%w<MBJQlw-GqESYS?)lYv5y3dM76+xkGn?eBy61uiJSb9d{PrEuPm|H_kkFBm^=4QJvCI%<OO8Bp7q1}"
    "bz}@JjzpD80<o1XSDL33G|a7x9>0)DH7d@v#6n&PFO;y<3L{cItdoAi#y5%7WrKCf%yH^I^m$mP&eBmzd8PNuo|xi$BPzGRr8rDno=jXOfguGs"
    "?;8vog+7?OZq40#5LEvn%+k?0o`KQ|8*$$DZfk8lYMbWEgf54yc^GN%cHU=ito3}F9ze}V{5}oYr*`Gn&OT;sr+YzVvhg%81Sqq7+v_BRnq@x!"
    "YiBe9G1bZ{ZdtF)CUYgAmMdmK(AaWCea8$tC`wpvb5Iz^X%a<T&a<Ce??&7n5KHDA(Pwr09vDQBV7<ozkpNik9<Q4Ba;Uo`^vyX%7u`}x2x@`O"
    "CUmI)t%{=B&SygT_!26wgFX}9bg%xam6@uQ_;EEp{4*0V&upP2KK@tY0)d6{eW^PWi*W8BP&ZG6MWD>}0pZ0;5k=x<%55WQV@_bpspn&ir1*W1"
    "*z$D>O6Ccae3Mi3U$7fW{S)J8y@rE6R5!wt4Fj_^i0Q+0Nq4)ma4ql*hyyF^Cc>qnFMHfjBPsv*{Cy}ne20DqpfUlL4;pAvz%;K8=*I%&2LO;a"
    "OJ25e&3SaOd9PueGAmjyZqSYg)!7D@Dbx%ZcR77vH?7QL0m^IvJ;-!U`XToLtm$$REr@ZsdX&OAA+zWXi0qW9V!jSNek%>&NxcZDMh5FCbUix}"
    "^3Ms2rH^q5d`Xk1o4Fv!_riqo=`5j0GIjTis{0^ooRd+t_|-OHxb=k*5U68cKCm&HJcPo)Xp{Q=@nI**Hf*$k0ZA%$a-6d^cBs#&$*>gwM&%fH"
    "@jGaByn}_IT0p;xbc@>?5Q82ez@bMDdM8<)@2~^Oih;Vhy~s88e`n9v-JEMstzV%@zB_Y&W4M)B^RdEey@#xTN|df}S)l-5POMcIs>bS!!z!QW"
    "Ze1{rE;Q-WF*yRDoE(5*y$-EiWT+o%`KuBC7}1Mqp%6OWvX{-YQ(VD0))+R=a)6eb*_o>%{D5<>?FOMBB57u4kTCmRX6e@IXN%H&yEaB=a`2-l"
    "<lI>dS#F9hELdg4Gch__G`i+}TGIt}Y6BedLcytw{P%SBe=01N9&U1FsS)oPpswg(JweQ^P_;#Ug#z&Na-7n4Z88hdSe00|E<rBO{_0)*<ak{^"
    "Xj{CxDQqp4g-w(1YtXa9^^f6D67pOMdu*=fTX!f}!Fg?PdT**-dr3ep1JPBOC)%Tg^Z0?YbI4{k|3si|HtXFM`FMIz9-!?NmaU%E59^%J#ickl"
    "zSkG>Cxy9#p#>XI_lkyt)rj2TEc7%H%N-Gt-OQmY5S-CA-jDqPp*0e~%e;b=47mKbSct~Z`2+hpjh@jOYGl#Y-NT*x`paA?%oDUj-$+Zt-ULYb"
    "Vk7*_NJQ%p`YlK91-2zm{>hX#`Fc-MMd+-1H#qUAIA(jJ*?#co7iQ+a_b#B1TOqs#Uf<R~sH<5*J_6AVMJ3Q_3<ndUPyzi;00S~)Lf$085KCae"
    "c3oKD$eQAf=1;JPTrU5zf%u6j<;`12Ps~(U;3ULQf)A{d^YPS!0__%XxNgoz0?#H9+H-k`M$!xvl9<~i!!r_BAKveqjP;k<>Ba?<>(M#lrkf6)"
    ";AzkIe->Cbe6-lssVaoMmZMG*w#Jw5sZ+=<<mD{vS;?SLuq~_3VS8soR4Q8{29?lzs$h4b4xtMZi|rnkQ@q_l%kD-C*Tf%N?OqG@@jt-$X;-oC"
    "qeQ*Tq_X0TM0FP1^mdBL95g!P&Q6oe^&$p#n8G~u=;<Ir76256oR5-HY#$e)tW6E)>kmvMFsgKseJj~x+=WPL1O2kjg6aL)b@LWCmdeQwq1mtu"
    "0+2m(_9XJg(bHnVrrDl7@`+l@DSMJ0AQ}!d2FQV!hGTSgeGyOsaHoZJW9S&vZ^!TqFX@-_kkkBTHOd`b2Xm|+*ph~ISzW#Nxq8B<I^~)9#e^>y"
    "5~#}a@pgMmxgck00R-aZp<+`vd_ZwG6^V6S7#idg_<!k3)FXdi0$?A7+&41NVjm)h>~5v;3~A=%2c<PTdrm^Y0}Mx{dLJP6YE%Ww?Bj>rVkU|~"
    "Ofcm>B%$(b3I$`)>gJhUxQ|W41YpE+ih~^!Kb{_2X4Q<#1Kqh1=w=_cGqVwdz@UP0K8!)<4O?KQEF5Ck^O?#aUZzrak0+kS=+~^VPHHs*9fJN)"
    "S=Hw?M&0O}yNB|y_)6R=z5-xB5t%Qr3Y_YI;?3&L5%WrP8k;Yq&I+DFee&YFeJOzK4Q+;q4kPbWWTwT#c#brJ(AlHt1A%taQDjP?NI<Tzte0M?"
    "a-qUD1&D`?HFX&;NHS0f%IOOgd}-_;Igk?#D!wkIBAuz=9=*tuf7R@YB+r>FtY(e5AAPPB`%9Oi3=^*=ZD7+6^^m9^T?%<{CMw7PtP@v2-c&Ky"
    "9d)<i5j%eYEWR)w#aN;do6l6oSSYOz4vaOxKyiFVRlY6K3f-IvLAgKXO+*=;sb1lT_GQk!JaHHLLw0ih78$}DWf>ZIbYHT71a~^OAEbw8igY6v"
    "X2s|N3iX)2F`#{S=bh0gRl%aux)cSBYX@2=bL42tK%J@m$4jzMVnC2cplp!a{p{BB8X=5K0j(5OB6^QQW5G>MVPJ`Cv(6G{$T};g?8yAh&=3L^"
    "N=$+AStrHWuQD6HoB*F8X9B-jWI;j%2r)}Qyd&gA20f&!^8{AlT6FT<7E-lC<qk#<FL|n{P77IrGA$;xxk7L20xXgN#8W6&$NK)d!o2ct;EH0h"
    "4y+p8`UGX-&*em1jO<@7RF_l<U`U#0jc0oGCWx0#kpRaGTX-T|-qf8dpa&^AP8mQUFT4WlT?nONbOsJTik^Dw&)2)eA=paXh6@-;kaWkDs}WbE"
    "v(#9k1aS9rWu9W69SWf^bOJQaPJL76s65L5bXJV-gAlsDet9{*0F9C$M*p%Amdk?_!W!@$`%ZcuR>U)%Gb@Z#hCsN4sn5H2@buQ0bPvuX0JKp1"
    "1c))}ri*|U3VUXjwvf?|3Iv+ci$)!tuEnl~wUbNBndQ{)*q~i#BFvMx5@NHdL%=?Uj>%Uj>L+M{IP6OcF^qvDZ3+e6z~XTPlbTK73<Jf5LbN1&"
    "&v=Jjyb)Lh9@bb&^3Sk~sT^UaQ+V(~h}_L1r(%kzvr`9CRy)Ih44X3rm3GPk3}LKA2dVQ8)=QkYAK{3`0Fn_1s1KbOK$c?}M^<EN78113E_-Rp"
    "<+T~fP}r@gQOBlGGd!4-@tb7G1uKoxXnckWL}kVjA)SJ{H&j|By97iF8wLpV@lZjU&&I$Pr!w$mWtsV#uVqJ9irZ6}86=q@wg6dgMs%WSMDP^&"
    "b~9=B^-dqW>Nz!ik$7mTOcXaxFj4|<6f&B)Bn?$rVpP!1A~cR}Bz7Put={fH*g<h!s8E1oWdMJfcK&salY15h?faG_Lg*yEEj@5WfJ$)!c)@b{"
    "y{u;!@JB$lF?sPM4{^vR)a4WA9VP;Cyw}p}EQykE`lRhD+lPDkA03jP^-4rBNd?xUB~z`_%lSa*f5UnlzCc2J?GEfmjtk{lgZEG43TE}{V7xq0"
    "2+CG4-zT#wEI<jC*mttUA<7KVQ?;V7()}zmF9ULsKs=B7Dflycb;H9I&y4uA`Xon+cprtWK#h4%JwiC(lFNfaMi%BQd-Qf(Yyqy`8fOZWxkimX"
    "B><iPH`Sf<w4y*MxU5X~XGXqI4Uw|N%wg#<pr_VYekfC0-Z5tf>3JwC(eq~>Dm+j7CU;0(qFj*l<lQ=Czf3fW8{TLB6?2w9$pib<8}*!s`eS$Y"
    ")wc^p+a$$$SA~eQuWr;93n9=NOH!=?5}}lu5rY$D9u%~LdEe=U2*%$hzwE-j%O42$?#Yk_1mi8~qFxQwo?Hq;#^6#XF)6M@tO-QdL;)VHK45GN"
    ")JyZIM_2$>8A}sqLO6uhzA-N{7*`)2gOcNlmCT*E!dbuA4^TBzb_LXU(2M!FB0Q!~-&OW+>HL{;9a+$OW#(8}R!IpsqLdg1LhU|>)dLKJC^Y~V"
    "%gi-Hl-S>0y`l}p;JZ#ZpOg}d_;SiBqnX%nCrm=bmZJg@$~ZaRP;n4SyfMr#yqN*J0B{=WTO;ADJ3F;1)o1jUmh?%4ht>k#YQ@ip?oLb9EHPc6"
    "hhXVCIY!+sFhcf#cBPP-Lb?!$y}pFq2}1Tur{Y>b>&XjTju>B=^Bd^=PoXlh6ScCF{jW)rP)~WrD-PMgqrz|bYrJBv5S{Aqo9&DSeT=iryb?Kg"
    "n~hmMI#EC~Op_cUC1c=LXzhuFHPh9}HY}``0TIGkOPWg!BEgWD*PYO(l#Ey<4TZQ9<A1tL#W8sMylEu_aB~5xpvUlIf4YULb5$B(?fG}#yemK)"
    "nh*L{iqlxRn&oLVAvHA5-(qJ8P=+-WGDDD(IK_d5mVPiPRXfi?TCq|y(!%__&r6&RfP7$^q)u}~AOLs7Pqd!>MGm8TTb0e-Cti?T!&~0hbEYI*"
    "vMuGQfdqh9aqbwLr1s4N=ZhCymMIm~h8JE!od5>r`L%4+Q>e~jg2Ibs$4hQ4U8JdkvOt}|D65anoYKVldC@RvID{6a`tn}XnOrk>{HcH3@TUwJ"
    "0gDg3Zum1I2JRiqtj?gvbjwpXdc73!!VXy|*Sz3(`q4djkhXCzEIJ~P;tFLigKd8~GCJ9mOq5b7!(kcQ7dVQ8+!b7ziO8gf1_V>`tzG(N%dK)|"
    "J(C*JGI>4c7-XDZm1f^$VIez1*;mv!Lhl9~Mq%m+=jl(;(A`I(dr>gje}=csMkLnRu^ygptcN!QoH|h_mg9|F9=b5dC+cYBlzqy@v0Ufv*~r%E"
    "vHQuIxC%KvsG=dDya>zw-NJz#ax*E(W_uY%-*O@JeHNRqL>jtLsxrl`h|-m{iG>kF{ckGCD~#TG4GRu>thl&(*W9&4qH2ghq_+F@dr=jkg#P06"
    "^xhl(9tlC;A$G2xzhOeAsnnuP4cgPjcEmXOPG>m|dKlcNLF}2;Qi49k%x*t&{+|^P=P~tBX>jB?N+el1PP2hjw2<_?P&VAx{v5T|4{>5AUVfPo"
    "*j?!}Lxn>gH74f06fgg_ab%zR{jLCF1NPKNVgqq)_>@65wRlAWnaB#~5{SnvTn!^TG>~}1!=qwaTl=F&1wd2=xJ<Taol47>Em8Qp85hvlL5bYs"
    "5XH(1h4FWVKUo+QRc3YIQ6oZ_C0k=6g1g~qC*^=Kj7Wk`8kZGgX6DQJ2KLU^7BYe`Wio%WHFnxFNM`rv=^?~(*yBPXd3BPo)d$uYxvq0#L-G70"
    "|BPv8-&nWVTb+j%OfiqZRxubLNdCflmqV^kL-nOB6fJKPYH&sILgk4HIRKSbF61MS&y{s^cr$YLCFG=)L-~Ylq6ms+ot4hyQ$pgC47@TMGltL`"
    "m0gfo66AivX`(Vv2_SLyr2zY!8CV&u9FeH5QRxCE645B}2z`45N}^{`onpE8qx%zMw+X?IJDB1DLBpB}Ds~78wmLf4g!2p}uHYyTs1X4%H=X55"
    "S#XgEKLwH)7=wg&*9koKjK@u{UpS4_pT`>~Lu`8pp;}j5E+W02ZJ-|I3y2b`*IUPSbj$X?PBNDdVDo)AFCc5GoLSQ&n%pPNQq{E9ImN3OEx_1}"
    "xW6Iv2}9DwCGuaH`W7McH(g@+3*)X2a*7Yi7&y~j2xP7=_<OF_zc5Uwhus`X7>xG^#t-ZB`VfeR&Om>F$FP6EFd)?KMo}(|&<bg?Q^~2{T^2$}"
    "G^b4J2N;p>*)ZI-Fim)Rqsf<n-FMBfSS6z=infVDP$F6cjktGnivnn{)T+QIY7qp~hv(CA(HAnH@*)BAezYDfp#_+-zsb3B5+MM%F~^?xNoSKR"
    "hQY?bKEP&;E7Sm=goHb&ka(v2=VC2)A<Iw*m9nv?wf#YDtAWnRJ<X5h&8N9&SY2@|5#p36KkA*q9_xJQgW^NGUoU3jK?j@$Gnb%!(w8#$KLnWU"
    "8~"
)

_ENCODED = zlib.decompress(base64.b85decode(_TAPE_B85)).decode("ascii").split("\n")
assert len(_ENCODED) == K_ROUTES * K_TURNS


def _decode_action(encoded):
    """decode_action() from policy.cpp: 'n_units n_orders' then the triples."""
    token = [int(value) for value in encoded.split()]
    n_units, n_orders = token[0], token[1]
    cursor = 2
    units = []
    for _ in range(n_units):
        units.append((token[cursor], token[cursor + 1], token[cursor + 2]))
        cursor += 3
    orders = []
    for _ in range(n_orders):
        orders.append((token[cursor], token[cursor + 1], token[cursor + 2]))
        cursor += 3
    if cursor != len(token):
        raise ValueError("trailing encoded tape value")
    return units, orders


_TAPES = [
    [_decode_action(_ENCODED[route * K_TURNS + step]) for step in range(K_TURNS)]
    for route in range(K_ROUTES)
]

# kag::Action{}: n_units == 1, units[0] == {OP_PASS, 0, 1}, no orders.
_EMPTY_ACTION = ([(0, 0, 1)], [])


# --------------------------------------------------------------------------- #
# observation -> state
# (submission_bridge.cpp fill_state + main.py _pack_observation)
# --------------------------------------------------------------------------- #

def _get(container, key, default=None):
    if isinstance(container, dict):
        return container.get(key, default)
    getter = getattr(container, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(container, key, default)


def _counts(mapping, names):
    """_fill_counts: a dense int list indexed the way the C++ arrays are."""
    out = [0] * len(names)
    if not mapping:
        return out
    for index, name in enumerate(names):
        try:
            out[index] = int(_get(mapping, name, 0) or 0)
        except (TypeError, ValueError):
            out[index] = 0
    return out


def _tile_kind(tile):
    """_fill_tile."""
    if tile is None:
        return 0
    if isinstance(tile, str):
        return _KIND_ID.get(tile, 0)
    kind = _get(tile, "kind")
    if kind == "PLANT" or _get(tile, "crop"):
        return T_PLANT
    return _KIND_ID.get(kind, 0)


def _plant_tiles(farm):
    """plant_tiles(): count of T_PLANT over the whole 10x10 board."""
    total = 0
    for row in list(_get(farm, "tiles", []) or [])[:BOARD]:
        for tile in list(row or [])[:BOARD]:
            if _tile_kind(tile) == T_PLANT:
                total += 1
    return total


class _State(object):
    """The subset of kag::State the policy actually reads."""

    __slots__ = ("step", "seat", "shops", "n_shops", "inventory", "prices",
                 "money", "n_units", "n_quadrants", "hires_today", "shed",
                 "inv", "rival")

    def __init__(self, observation, seat):
        self.seat = seat
        self.step = int(_get(observation, "step", 0) or 0)

        market = _get(observation, "market", {}) or {}
        self.inventory = _counts(_get(market, "inventory", {}) or {}, _PRODUCTS)
        self.prices = _counts(_get(market, "prices", {}) or {}, _PRODUCTS)

        town = _get(observation, "town", {}) or {}
        shops = list(_get(town, "unlocked_shops", []) or [])
        # unlocked_shops may repeat a shop and is in unlock order -- never sort
        # or dedupe it; shops[0] is the FIRST shop the town unlocked.  An
        # unrecognised name maps to a sentinel instead of raising, so a shop we
        # do not know can never be mistaken for BAKERY (0).
        self.n_shops = min(len(shops), MAX_SHOP_INSTANCES)
        self.shops = [_SHOP_ID.get(str(shop), _UNKNOWN_SHOP)
                      for shop in shops[:MAX_SHOP_INSTANCES]]

        farms = list(_get(observation, "farms", []) or [])
        own = farms[seat] if seat < len(farms) else {}
        self.rival = farms[1 - seat] if (1 - seat) < len(farms) else {}

        self.money = float(_get(own, "money", 0) or 0)
        hands = list(_get(own, "hands", []) or [])
        self.n_units = max(1, min(1 + len(hands), MAX_UNITS))
        quadrants = list(_get(own, "unlocked_quadrants", []) or [])
        self.n_quadrants = max(0, min(len(quadrants), 4))
        self.hires_today = int(_get(own, "hires_today", 0) or 0)

        # ``private`` is our seat only; the rival's shed and carried inventory
        # stay all-zero, exactly as the C++ bridge leaves them.
        private = _get(observation, "private", {}) or {}
        self.shed = _counts(_get(private, "shed", {}) or {}, _ITEMS)
        self.inv = [_counts(carried or {}, _ITEMS)
                    for carried in list(_get(private, "inventories", []) or [])[:MAX_UNITS]]

    def owned_in_hands(self, item):
        """owned_in_hands(): positive carried units over the farm's real units."""
        total = 0
        for unit in range(min(self.n_units, MAX_UNITS)):
            if unit < len(self.inv):
                total += max(0, self.inv[unit][item])
        return total


# --------------------------------------------------------------------------- #
# six_day_budget_guard.hpp
# --------------------------------------------------------------------------- #

def _existing_sale(orders, item):
    total = 0
    for op, order_item, quantity in orders:
        if op == M_SELL and order_item == item and quantity > 0:
            total += quantity
    return total


def _requirements(state, tape, start, end):
    """calculate_six_day_requirements(): purchase budget + static reserve.

    The reserve is a per-item high-water mark of unmet demand: how much must
    already be on hand for the window's own FEED / FERTILIZE / PLACE ops, given
    that the only in-window acquisitions counted are BUY_PRODUCT wheat and
    fertilizer plus BUY_ANIMAL.  Harvests and pickups are deliberately not
    credited, so it over-estimates for anything produced on-farm.
    """
    budget = 0.0
    starting_items = [0] * N_ITEMS
    item_balance = [0] * N_ITEMS
    hires_by_day = [0] * 6
    quadrants = state.n_quadrants

    for step in range(start, end):
        units, orders = tape[step]
        for op, arg, count in units:
            quantity = max(1, count)
            if op == OP_FEED:
                item_balance[WHEAT] -= 1
                starting_items[WHEAT] = max(starting_items[WHEAT],
                                            -item_balance[WHEAT])
            elif op == OP_FERTILIZE:
                item_balance[FERTILIZER] -= 1
                starting_items[FERTILIZER] = max(starting_items[FERTILIZER],
                                                 -item_balance[FERTILIZER])
            elif op == OP_PLACE and arg < N_ITEMS:
                item_balance[arg] -= quantity
                starting_items[arg] = max(starting_items[arg], -item_balance[arg])
        for op, item, count in orders:
            quantity = max(1, count)
            if op == M_HIRE:
                hires_by_day[min(5, max(0, (step - start) // 24))] += 1
            elif op == M_BUY_LAND:
                extra = quadrants - 1
                if 0 <= extra < 3:
                    budget += LAND_PRICES[extra]
                    quadrants += 1
            elif op == M_BUY_SEED and item < N_CROPS:
                budget += CROP_SEED_COST[item] * quantity
            elif op == M_BUY_PRODUCT and item in (WHEAT, FERTILIZER):
                budget += state.prices[item] * quantity
                item_balance[item] += quantity
            elif op == M_BUY_ANIMAL and GOOSE <= item < N_ITEMS:
                budget += ANIMAL_COST[item - GOOSE] * quantity
                item_balance[item] += quantity

    for day in range(6):
        first_hire = state.hires_today if day == 0 else 0
        for index in range(hires_by_day[day]):
            budget += HIRE_MULT * _fib(first_hire + index)
    return budget, starting_items


def _add_budget_sale(orders, item, quantity):
    """add_budget_sale(): merge into an existing SELL, else append if a slot is free."""
    if quantity <= 0:
        return True
    for index in range(len(orders)):
        op, order_item, count = orders[index]
        if op == M_SELL and order_item == item:
            orders[index] = (op, order_item, count + quantity)
            return True
    if len(orders) >= max(0, min(16, MAX_ORDERS)):
        return False
    orders.append((M_SELL, item, quantity))
    return True


def _apply_budget_guard(state, forecast, units, orders):
    """apply_six_day_budget_guard(). Only ever ADDS sales; never removes one."""
    budget, starting_items = forecast

    available_cash = state.money
    for item in range(N_PRODUCTS):
        sold = min(max(0, state.shed[item]), _existing_sale(orders, item))
        available_cash += sold * state.prices[item]

    shortfall = budget - available_cash
    if shortfall <= 0.0:
        return units, orders

    orders = list(orders)
    candidates = []
    for item in range(N_PRODUCTS):
        price = state.prices[item]
        if price < 2:                       # settings.minimum_unit_price
            continue
        protected_shed = max(0, starting_items[item] - state.owned_in_hands(item))
        available = max(0, state.shed[item] - protected_shed
                        - _existing_sale(orders, item))
        if available > 0:
            candidates.append((item, available, price))
    # price DESCENDING, ties broken by item index ASCENDING
    candidates.sort(key=lambda candidate: (-candidate[2], candidate[0]))

    added = 0
    for item, available, price in candidates:
        if shortfall <= 0.0:
            break
        quantity = min(available, int(math.ceil(shortfall / price)))
        if not _add_budget_sale(orders, item, quantity):
            continue                        # the C++ uses `continue`, not `break`
        shortfall -= float(quantity * price)
        added += 1
    if added > 0:                           # settings.sales_first
        orders = ([order for order in orders if order[0] == M_SELL]
                  + [order for order in orders if order[0] != M_SELL])
    return units, orders


# --------------------------------------------------------------------------- #
# policy.cpp -- select_route + Context::act
# --------------------------------------------------------------------------- #

def _select_route(state):
    """Route 1 on either branch, else route 0.  Reads the RIVAL's board."""
    if state.n_shops >= 1:
        first = state.shops[0]
        if first == SHOP_BAKERY and float(state.inventory[FERTILIZER]) <= 10232.5:
            return 1
        if first == SHOP_PET_CAFE and float(_plant_tiles(state.rival)) <= 64.5:
            return 1
    return 0


# Per-seat episode state, reset the way submission_bridge.cpp's Session resets
# its Context: on a fresh seat, on step 0, or on any step that goes backwards
# (a new episode inside the same process).
_ROUTE = [0, 0]
_LAST_STEP = [-1, -1]

# Instrumentation.  ROUTE_TRACE records every turn-360 decision taken in this
# process: harmless during play, and it is how the router gets measured.
ROUTE_TRACE = []


def _act(state):
    seat = state.seat
    step = state.step
    if step < 0 or step >= K_TURNS:
        return _EMPTY_ACTION
    if step == 0:
        _ROUTE[seat] = 0
    if step == K_DECISION_STEP:
        route = _select_route(state)
        _ROUTE[seat] = route
        first = state.shops[0] if state.n_shops >= 1 else None
        ROUTE_TRACE.append({
            "seat": seat,
            "route": route,
            "n_shops": state.n_shops,
            "first_shop": _SHOPS[first] if first is not None and first < len(_SHOPS) else None,
            "fertilizer_inventory": state.inventory[FERTILIZER],
            "rival_plant_tiles": _plant_tiles(state.rival),
        })

    # Route selection happens BEFORE the tape lookup, so step 360 itself already
    # plays the freshly chosen route -- and the guard forecasts through it too.
    tape = _TAPES[_ROUTE[seat]]
    units, orders = tape[step]
    if step % K_SEGMENT_TURNS != 0:
        return units, orders

    end = min(K_TURNS, step + K_SEGMENT_TURNS)
    forecast = _requirements(state, tape, step, end)
    return _apply_budget_guard(state, forecast, units, orders)


# --------------------------------------------------------------------------- #
# action -> Kaggle dict
# (main.py _unit_order / _market_order / _unpack_action)
# --------------------------------------------------------------------------- #

def _unit_order(op, arg, quantity):
    name = _UNIT_OPS[op] if 0 <= op < len(_UNIT_OPS) else "PASS"
    if name in _ITEM_OPS:
        item = _ITEMS[arg] if 0 <= arg < N_ITEMS else _ITEMS[0]
        return [name, item] if quantity == 1 else [name, item, int(quantity)]
    return [name]                            # arg and quantity are discarded


def _market_order(op, item, quantity):
    name = _MARKET_OPS[op] if 0 <= op < len(_MARKET_OPS) else "PASS"
    if name == "PASS":
        return None                          # dropped entirely, not emitted
    if name in _BARE_MARKET_OPS:
        return [name]                        # one HIRE order == one hire
    return [name, _ITEMS[item] if 0 <= item < N_ITEMS else _ITEMS[0], int(quantity)]


def _unpack(units, orders):
    n_units = max(1, min(len(units), MAX_UNITS))
    farmer = _unit_order(*units[0])
    hands = [_unit_order(*units[index]) for index in range(1, n_units)]
    market = []
    for op, item, quantity in orders[:16]:
        order = _market_order(op, item, quantity)
        if order is not None:
            market.append(order)
    return {"farmer": farmer, "hands": hands, "market": market}


def _pass_action(observation):
    hands = []
    try:
        seat = 1 if int(_get(observation, "player", 0) or 0) == 1 else 0
        farms = list(_get(observation, "farms", []) or [])
        if seat < len(farms):
            hands = list(_get(farms[seat], "hands", []) or [])
    except Exception:
        hands = []
    return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}


def agent(obs, configuration=None):
    try:
        seat = 1 if int(_get(obs, "player", 0) or 0) == 1 else 0
        state = _State(obs, seat)
        step = state.step
        if step == 0 or step < _LAST_STEP[seat]:
            _ROUTE[seat] = 0
        units, orders = _act(state)
        _LAST_STEP[seat] = step
        return _unpack(units, orders)
    except Exception:
        return _pass_action(obs)


def _kaggriculture_shoprouter_b_entrypoint(obs, configuration=None):
    return agent(obs, configuration)


# FORCED-ROUTE VARIANT (family probe only, never ship)
def _select_route(state):
    return 1
