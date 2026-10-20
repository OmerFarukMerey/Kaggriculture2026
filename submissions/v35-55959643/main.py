"""Lev Neganov episode 91587143 player 1: distilled trajectory with the tested c17/c27 controller."""
import base64
import copy
import json
import zlib

_TRACE = json.loads(zlib.decompress(base64.b85decode(
    'c-rk<%Whm*a{L#rYav#VY{@&eR5MKsTNFsjg>i#uG%#ZrFvg3vcZUDn6d(1t85tRwc`hYtdRL;V?mh3585tS*%l{tz`)|Mh<L|#8{mU;$pU!V?j_wvm|MA;@{q4W+|8W2DAHV(npMU?K`_I1|{d94?zW-nP;m6N^{q_9g#n0!LM~kEPSDT~7vHA1OPwVxkqs7Vdf84CsAMXFW`DuNAd$c&6{Q2kg<<-Z%KYzNu`tbSv?fwt${%>*6i;MSv`TS|`{oDTha<p0B+&(mP`{Ak2dq3N@Z@>HAJDwVG_?C}X*S9}CJaqTTzUS$u^gU0_RG<Ch=Znh^zuy1z_VbqsArGE>Q*Zs{`TO;DkmwLSee=sK96bO2KR(`WXV!VopY|68d(Gh&59a#(c75$V|NVI|K#yO*<MP~t=a=q1_vuS)Tqc_gJ#N?Z!qnOq>>dY}y*{D#x!b4t10qkPef-VU=cfS&;}K4vKhC>_XNRLQe|xR-$3dSzyXSYOmK_Iu{?_Ny=PCmt&mU;EGA`jff@VMe77WK@D^kte{&u(Crhlq6&kpa9-ORe*+0EOBJauWzCRRqHvX|K)JbXwz4%s>3br7z!_g9yf>-V?6{%L)EdvSU3Zx7A1_epB47OpMS4Dx{ITQ1d5@Yb-Q!RREL{k(TaPEfr0-8-wWmjC$4A3ynqesXvw-mEXbxNdtp<<TR<9-#5j&hAqF)7A=!Pafa=w|>^5c9a=^=x}IYhmY@)XU(J^o!en|DOMT^&VSf;rG@@og4-DX+zeA}?>*TEgNF$WJ|3k?1E=<WY7y*tO@&w60WLIQH^8O^^7w*ja|SqUAoDB>N2wX2!ZWrbWPhuU5O^papz>|;&+^;qRd;ab9io`WlRw|wUY~D%Twh=R^=PpwUWSto!!N~A*W=f@D7#nYvwONXQ{A3OuGj(qmE|i{zc*~-?6HPNr0rHsuiw@^0sKCC5s&DAfjzS$1SSz-ov|;eSV+6&QF`94VJ`kX$jtOi56uX%_QC`cY+belHJk!a#YRp*x6ak~$3w<Eq-PhjJYI4pPQ#^t-2J26<zC~H9$~S~#(yrlXpSTOW%Zt4|7+m_1A|Gfi8APrFmb>`K_IQ-Bu`yzsW~=KM3(c{m;~MB-nLHa`0m@-1GmxdsON%Dp4lD5J>TBS%7o}1xebTPvm}MWDt-R`ukPoQ`-cZ(xaQ_N<R;zwKk3nx>Ymc{`d?;@g9hY)Y=qbai`~=MQtBHVU)w@J4(1D(3xpiz+YRxl?GeJpj<UZJ)zOX*VUG<EjkDSZYb)&T%k7o)_@TFnrjH!~>o};$3n1MISDeKJI<B~iqIIrC*3J5uDsagQKcp3=F~p-6nt|B*9f~V_xW4*yRKXISjiRfoOGcu8T0kpmEv&vZYhm9*c?m;-`5$>k;`S&Vf~w>%#6&!TVL}Y(7&Y*~6&;R<bXX`T*ip9&^pMgE4E?4u?#!}D7$f#Ecp-!jvd5=c2gKllr}ygF`@6q)J{-lSodp}vi-;Gx%zL3rm#Veo{^>GzfGA^Eb6B@e-Y!G>E^WyZ#|I`OV9O#w?j|`h5C8FaJ0G7Oa@@)Cp4{ulnfQQ#T{^A?0CD69dp9n#3V@tiCfl-zs6705g_o)plaZrAE3)N}-?)4JWONWo{WJ;z+I^C~G~=b{n{Er4Y?5l>vW_x={J8L|8QV~?@*^(A?wj_&uPmbJ36J|maFQ{0T(F7`?*(*lL`!J^V62$P(N&mOPo;p~b{OCUnNb@tDmF@nK-TRmZJ=v9Q!TFrtmo%Gez^EEUd-+Y<??IHA`KUVF?6{lQ=SlM`v$SON!we#32*|zk_3BV0MW`GffK7v>9ZvVXe2`|!D@lG5V^{205zNy2Kds9cYk+hlaCK}i|q`=C-?U8^eXJ((x_X;R2Rm+7FRbU#|4XH4~uAnm(3Ni4kq;_=xO_L?wyM=(ji)4CuC&gnY&5`oFJw%*BL3IBfgC*c_KUW*N#yq@z#0W{_(vX*oLoBN#ZR#Zp}n9?1@?XX%?hC1ed8ng3PSiq9BeOnghssnt5?ptKBrqI6oD23Tm~xrs|-O!tNq+Mj?~Mrx05~blY`>bMFdf(a9e;Skel)4w(7Cjo7`-jJ+F~j~5RMT7-7ob~0GnY2t-w3y0@yxQKv%=br}9e{ofeYA2P?k#v!c?QkgTsd_qr(MQaY5q!?+4ZR3xvmFzeY4tGJr(rAOh}~d&+!r1i`=Yo5!%Y02FE0P`MN$EiSRY~jNocJd5NTQTOUK~h7CmzZBICY-Wk&XLEsP;B10-uWXC4pd6VPZzi>|WDnvLMr4==(2M3(|#B=Y&<1G~a2nJim!c-Jx4JP$=M=GnN6@;Ru<xLeSL<<dxe1xq9J4_y2>XF?NxxMO!DKv1R#XhCScX!C1B2^4@Rjj~WB{)K!Kp{0mU+0ap}ZyR9!bN4t{l!nul)W5L-DiDhhW3mPC_8D;}-sJvjt!utPD{=qP%pDq+SOr)63>16v{)r&YOc`WQ+;XND#j%D_Z<>(B&eV5KxngH`rL4NWw}N29jtDu}1xbxi#wUYr)w@BIvO`t#cO(e$!vLoXoSM4RWs?sX8HXCb0ekIfG&*>C1P*aSoOIBqvv+e8Tpb+A{{vGix*bJ6UJWk;&9r`_pHJ_Yqs_ip8!Vzi>>8hPFhf!s3&@GX(ezoV@yUZ|Kt5cXH5Pg-c)->mjJFR;lCpNLlSTwsJQb)rwPxh#Lb&D_lO5G$m<eE~YrBf$pyiDEODA(O7!}oNuK`Z30(L0qQd<-gaHca&H90)?3hJBv^=>geW!b>daWc5papK66*>Hw!E5?O?r&HmPW*0g4oRQO`kuE!wLRX}c17j}AgP<Ted%M>QdBT;iIP?*wASW~Vt3P6*N8m?j0I~ahyFq*i#q0QVGt9DnNr=-MCTfFbyIBI!Fd$Bp7NbB1Tk4N9n3|f-QJk@Lz+l5}2B6*!t10RXk6DT`*OK4+MVzLAsG@2$Bx=0-zwO~L3~lNxP0-Ty&21HU8HSiKZOt|-mwyQ7Cu6<nk}zz^G<)<y9EK5jnlFhGMl(B{D<P7fA!<j_5;dK4D8aRgN;Tm%bnBG>f?g`=D1Iz+)q&y7;EPH?TgW#Z$k5P?$PSUhpLlA?^5IOVzc31<O+m`=f({&OWz6O#b~7G+tXx_hV75Lj?vPua5_VA}R)bgspHVL<Zc$a2r+g9eS`NK2&P9b8jofNKhcK4MSMyWDhN1Ot6AS=(jzR_%)=dz+=)<nPp#y4)9Ev9}Dkm=uk_D`;_~A{eEqOXvErLgQivuu$K!m9Nbb~qJ4?iS`z=Z6X7#w+;$_un%9!~o=>ysX^=$C*+|K^o>sg8hHO4vHDE4>o@TM%<Yijv&xJ(w@daoPXMGN%M`=n22QQ$+2HzC?~_Ggyrf`wOAkcD|9bYaCL}E=NN$9x;;E((}c8*$n{~n8xg_tu$21+_y3g_^eUGxBqdtd&9uDv5B$;DF9r=R4^nW4d*d;vOjbl1Y{F$h|^l7d-#&*cIC-zV;UNcJmA^LDJC8Wj}qaWskw2OI}yg8(Rs~NJ<1|k{>lXd>lJ`mC}mv=10AMlkfqFn$J>Pw#hbxFJrkuWa|$!SjeAA%zN3jIXrvV970iz7%_YfP>VZlbtmIAu?JQ*KgGj8IN@vcK_n3WCX<Vt)lZ6JDwlfYOE4zuci#X)+=GnXL;`#S7*4q(p5?tqz3l|R<<?Ac7hFaprQ%cJ6?rT92<4RUN^yCEO)|@)||L^wx-ixx&F?bOqF-Iw@zWjhEB$}2X7#~0XHiG5fMr2$IFp?PV=<xT*@Zyl_D&)4$X%@6~$dHv3tumM_(;x%4)$2$!&$pK=EtR64p=Llt@JuW*+aR=Rq{N3_^$^a;@N0|YvXEGC7Z{|S5L_+xZ9lLqyL_dLWlF{Zw5G_J&tXug;;#nF*<s5F@DW2CnB8bmsuA{@?QI!F6zd;s`BS>M_I}&$!8PxSA4aIW)jkaN#b)tnzA3J;tCzMP>D>?N06~M3SL8{(q;F-<Q{A`nW3~Bk?x<QM!1sdmqc{}WD{xa11}HPC#}`dD<0SEuWf))6lPlE2DQ5fgF6hOyh)YQ$H&PT;GMGyni6;e11qhT%D#Nyvjpv23V~b{?=Vf^>0oJUyICs7AL+LC@eW+8ADF7tXRHaWzKVj{&lC>0GU!iQIBp=a%ky8>X<Aa=f5cpKCFz>^R)tF)c4)BDK=Qu)!kTCtJ%3XqmEuH`IJw%oHg3u^|CVXOi%DG?y0%V&2KYUXFSy_8hcMJ%}Nz<nTpMoPyA(3FqFyin$rRp_`c7!_=V~d3`oipe3Ye64#j2Us?-#PC4+wX&uJs;INj(e_3xx@|)I|_-OG>O!WY~t{W5qQ&FK?8yWqYKc=^yn<bJ3u{VESk$ArV6E7(^hXNbh}w?Ia0R9R#w}o?Hr_8qc?Pa0R)R7znO>>6pnmTrYJU<Mkw;->I`x1s(#T-|7i2biO?*!e=KGvOF4*n(i|mcWSE;QTu)~f9D}9xPFdn|-2_%~O5nSb6kB?ZVy-y>9U3c}4ipXL`_cHKh!}eB{s3&bi@YWlW1m0TwFlv+i76$s(yaiK^)jh(NS*l{FM?EbijG(Ep;N1k$Wze(PDSOF6>hVyClotNZcZd-=UNdE+6!S>yHxkz!Kwg6e2{s0wg)2i2MK;l!>WBJ@NbKW!vj6he3ZDVXg{X-@6wg)YmjxJtGaUkCltSjzdEhd9`0mP={|Wz6^PtrP5t;xY%am16I}jIFXju1Ya&QmuXrrAQH-q+JP!p$buUXx24-1xF_PZZWJ-iu1len9?$?5O2{yQtfX6~BzJH#r3{XosW@0jIm(@ZquJh}sdksramTl?kCR|GzK>@wCljTg~uK{^P*#3d=zRu%9QBo~kIP$2I#~(}IjUSboq)201xVGuC;yJ-Zg#s{9ta<@Job4r!amv1k#hBXUBP(lAtcCHUT1$`hPGjm2kU0XpwJ>&bK7!*1U&-!>vSo~v?3{pdkjAJ$QS>;#Y+B_mAxBP-WL=clW9O@yQ_t`V;&DmPk2GPdgG}x%tjZWp){ry;iAj;Cdt|MH7fXpK3hK+X?gy-&`MNQ5?J(s1ZID&J4*;Hg)9jL=q>`5d=m`I_?!$7_Z>ekWb+YI|Bul9vT;jxzPiqFql)~$6<>rx`heWL!l6q1vcAr>$oSl?_&I+2zfm%+otuL?MKvI}-kA~p3EEPbf&M1i^HAG9pe<^Uh8MrCcbo;@H-P!u|3Ja=}sR#X+MDIa!TBj$Zg3%glenO$$heG02u;uYxM>9#Nb3U5ZCnc;UAd+ZB!TG|2q-1d=MKuNx?^*3?DuJ);cKcpIybyY9QiOwGZIW{&nJy^}IN$;m*i2FJVqJ#5n!qNqJ_@gu{Jeb!Zuz#u;CS7M|2@I?<<}N`2bY%5+n{BlO2@L8T@cx*T3xmduUd++h^HfMBuRp3s(~p=?g4R?5_uak0<&n+C4}u`sPg4(e_hy)M~zYu-t4|r=tX3`xsZ$yi)i3kOd$_Tx#vg>gb~$|F~}z+rM2K0HGzMck=8}A0_MtaV!N+6Fki-b#25+i$|PB#P>1le#EoRpYE53Am98h*22&gI^sZ9&49YwDC@0+;FH!qZJ|hz%AIfo7sXIr=N18Xu6bR%CZ>01rjiqa1^<3zK)vdGX-it5;9A$2;eOY&<45#^dWTTJJD9Dz3_isN?^NvNStc#t>z?U@S@yQRaH~v$pik|F*rd;XE^Y`n0U3f7#O%kl)u|B9EH&l>*Q_rONigPf(?7xL|)Rwn%f{Y}^t5x7n<4AeHXm*AHgon;@LKZa7$4w_m%U@I~0)+WTDq0ixgL<;R#Khl7bikx^VJ5@pB})<b(wAwNPU_-Z<cowTCeujyaPj9*4vs4l^w}EHIJyCT!Ml|Tu-h@I5d);cO_JzlWEBg_1Fad$r_Kcx*GLsCJM~H2qLvk(aCTLOiPUb<)7!{GAZcYtMp5Cl-Kh}Ah=Kq~LVbeNQOpQ=J`iHQ1>-WnJW3C^NUkDEy0N>hJw=2Q7NsEJ=(mu?k_&d{vR2j2O~$ku9Lj7Pri?-@14Vi`o4paB{Ob-ufurzx41+%ro^!Q%NOOcD<`vaRYFRziIgyf(#kC_J0`96FFgp~uC&NgcoQgcUxE1o}mxXj_Dv-j3GQ-C*IRxe!q$0UIEB+Vu`&1ZM0d(x^m82{&U+4i9Jpi>%?m{Zn@yT76jkP+#7}*4^UcSbxn^8(SC#Nrjuoa575U{8KnhC#ZR(1)5Ssf3U{6Z=LGo)ZeraHQoXUl0*9AvALiFGfZ*p<7ZPf;47I=0a_XI0DDUYPy7{1l?Wj0{O~72m?^%d3xH0QL%nEHKeT0vU`Kkj@U3%^`SGyhWjsB-1e{F(gv+M$mjHVd~3c6eURlZI%kN>tx2_ueqHol@!`p)QXJ5<G0xyA7{uTqS6?lzERv!@>?rNq;MC90(cr^XMP3_^uoqteFAGEBh8i8)&*k-cUz-N0k4E1#?+ZlYAH3MgG~F0z@e=|;M?iXEmaQUR;D(}me8b|Nzja6^k5u<h;PuJX-hc#>0!-U_M0Q|v(A9Yf`Fl2o;<Lum0Txtm&W3->qV^aAQ{ib-q;O_8TI5+pmbtpda`oT#g5VIR@RkgHh1JUC2C}o+U0mUEMF|0OOg`=MDr36%M>1{wGn{!5}1zofC*rW312XE7P5XQSShhz85@=pd8wNIb4MVSRwDrJY-fi72uegR-+cG%KQz3flSg+ssfwocm|W7}oy($35Hyoui#bydUP2ypd#n-1M#~0AiLorHj@d&k24X}ck(gA};Sdr`r?>lJZUQ1`9LcFI%FsFn!Ympc__hmkX+;)G5-iM}g2&CGcM;S?Gjp>k>dmxOW*`T~{=@KHTz>fV{;s<HOsc$961wY!^a7`iXg}>i0S}SZFE`9S(F^cn*K@HbsiJHmvp5V-(Q<9`lucHkWLeH<%}S|7tl36UUSM(q*0eqN7$M8LbcYMAHzodYV7IX>Oix9!z#;|?Mu~@LkAvy1Wx4*5P===G6pOm&rJ93dL6oKB)Ul9Du4oO!u~e$Q9#&@yt04L?B>@G_6580L$_}Jx5NI?8(*R7+DK}vQfE*g6`RC7vkOdGP{wKwl3QeNjKmf!T^0p3OD1Qz-;boFch*AS}H=of@{Ic@&;&;o;)mUq+g{-0-2mYko&prGH>No41*v0ZlCORSfDXF?4L+-54v3uj>r=FU`<hKafT)?q?wN>oqtFRtxo1F-F6qP$3p_Hvjk%c#=Qg(e*B3oLvjJ9$}(d|y1Hy?kA0xiAD;Y$H#$z-Snkc&#S7*t$7lkh1--~$7P)+4Gce|jtPWgL`{1OGk8idQN!7MZG>ls<mKfuO6Js4HppduFAM>VjPfuy7sf80EydH8%jo*Jb>2Ks|QW5FXPI>P8n;-j(dl5XTJ@BIkn{ecBk+K%jvZ<1RK%Gm%CS(z5x@&ETmq^N>|D->CB0d^j@a0?q7=Y9F$*!K{bCl1NYz@#RV`G9)NNNY9B=0yL9vXKG<?om$4Kq;=sC0pd-<v-15v>m=uHG^v=>6!RG)h~F*QWj^p`2J9o!zOod1wu!ZojM0phtlxgTa^Q^bQGsh#d}Adh^htQfiYs#|;J8tHkMk1-XZX-0Iwl1|{^A>$O*Qp-1-DeTlI|3Z;=Z7k<>a?yUMUNF4OZfUy(&m?iGuzI@w7HOL4hTc3o)<Mm7iZFxGYn?I!LHg$1Mm@E5x-ZDWr{tLRJNAE+aosm>^+e%cx5#r*?pZmn0<@@T%G=2MV&vCWqo}N#zle@GTv^{mlr*y&?`45PDIflPn7+Z%2uQQc?}WZZpdoWm;E-`tV^O1D-$#>#zq<QqQfTNe}R;bv#h|@*@X}t_?YvyYy~js_)XsdV#^3lw(NwpdtzRdT}IalxCGF6>ZG*$xoTd8m|>g;A&!EkD)A#Oe&#rc7!{vxCm(^I&VEh;;S5vrDYyV%MP3^MsCV3ALfULprz{|ri;>Vh{9Jy_x0FZc^c>QpipYGgPf(i3>Zm(-KGh&3B@r3)>c!bZ98&AU`_cDh`o7=ZbR!$E`!`alUnvlbj~`>uVIwOL&VHh84ecwaUu7QB`rjjax7*m(a=+^OQm<DOGzqK(yK;QDmAH2$>M-UDNRwX0a+*;8CQYv=686a0fh`wTr5sxOrTeG{p0Yj?9<|_(f?x3Iu$l2XB%kh9yx$9PKt~>mdiM^iBGI5IdSYpxUHe%4Kxg+pQOs2jl-j1PAYRuGlkeCB!X!#7b~#`GJ{eUI?(pwzRLl(o-5rRno+44VdIAu6P^wz9N-fkheAD^pBwcdICYh*Cpf@7&Zp@&TJQxPwUW4Iux2#96ALSX^$j%Ga9*14D#sOK0v#8l@=-py+|4Q+U0fs9h23hnF2%)Y2tKRTn;bX#DRxN+TxmBA<vA%v1S#6c*c;C~mB%8BI5(Dlu?=NQl_)8BbT~g$M$%a)3h#^7j@$^n21#`crb5V-atpia^2;_S4eCF=b%yQ-R1Wm}6NbveJ10d7+HoH4S?L9v3SiH0KAD&hRA_37Jr?Dci`hz>e6H8<YK%m+rOXTSSt;rJf|2?+l2WdOk-#f1BYeNC(7Q6(6?!tFpqZiT*^eQLScw(JxGPh&M({wG4;kr3X=x7Y8^yQ(c=aG)UL<Gbg62#wN0c<_rJYFyu2`A|^7A<+<ZNy@>?tY~I*dX{jP;1ED!O-ZU(}6|IGjME%VoxL0I*(<jwQ|tN_Pwp6Gq+N12SV#B0GroQ#TV+tsxNENp#@50zIN2zC<ym$ZT9_rF69WOcGW;Pg}VemJE~u)0s(*w7721sOrceV<B2FF%OQ^xgk^&@F!0LT39I7w<YEHB)SW0==58n7&ry-Ydrv&j7s&wDH|xI;smHfQo{-yosmqNGY_k>O5CRauQ~f(GXpcK!((-j3Izoz@=bKCH%T&X$#W&I4ato(ajrtz$)ycR=eluN`;DGYPKnqux$1zCoF@-`GH`qz0Vdtm67|c?wA&cvH>Jm<dIyZa>;9iGyCo?n8wpM@qiON9lvSJ6aH1uC!jgtheV!yPEkd0QnpdLC3DJB4-hfh8G-j!Up?|S6%K?&5VT3z_top%H=E)ibS8e7PPXwRT%s;2*gy!BV+zi^Ilx1O8O-x1P0SaG7yNHMMs+>-a1ZHY54e7=u+>o-`tZQe7mTY0hM7@#{Wp@}6y{#z6(IGd@&N||cW0~J-RB4Ky3Z#S;Gbn6o=$1zUhA1cU6u^xnvH@TKn9^hGcWEqe=?1o0W^iLOy9nm-(7FI(ZQwY8%*^MuEyT+@R4)%wjaY6{ez+BMiPelCkc1=7ZoiVZY}mkqVGTV4jV=`Sb;R&XAX+i4&F|evJZ-f!xY=1kY3p@YyPG3JZKaibSjCBF{I`i{(k4-SN>0L|JfKd&xrEFUO>yBmRYCFK!Bv=Gro5;d6JZHLHeGBnTEa5r6rmJ3CEsq4ZWgekq)?|4r31#loUWEL{p6y(brC4$P-WO?*1{2zm2@IhMa_T=icsk~S{>GkP0p>|7F4GW4@{^^lp8Xg;*!WI4ZoTZ5hj9oGXF+nd@1vaP%2iOOiGIuiaQskmSf~pA&{4=FG<BPCbMvGNSRpO9lD8YW5#xob+LpzWTMPMb+Bz>BJh&wZmY5yvRS-4!yM%sQf?rvcv2_LQAjE{V^BsY8C$>hSD8b?DpL871?b<pErn9{Ygx(qPAke%F`B%1*Vlep_@~Ft?7ze1xn7ApOxw4PJSd#79CJ^WrGy|orKTd+ujp44#jU%UG8%Ivr!U+!^ZL<EDX({A939(sTAGe)wvG_A1;$P-C8}7SCn<uMn{X~jm;t2#Q5og?vsxO|_SFoCq`AOiFp}a0>jWnWCBlw+)X<kS4x*;9br^YJ3160%%Mp%1J8SeT(0%tp(ejettDr3Fl!|q+>KM&UO_1iaRP$yzG|DrL1f?p&6iLD;GHqeO$^w$YHg~xDnCq62!~@q7DPz9lQj&}VhJcde{?s|{PZBX;Aw|G*hD!c74eTn_lu;$=Qt`2rkCV%MXeC(;YX!?y2|_u{Ej>FH^egu4k%4Zhl>N@)j=bQ3*b1oGqUkR%;#$qAWI?#d1jl^3u(WEsH31k;=~(*6z-dzSkP><hnUjyzmDJ<49%4XM!n30kOIyZUE6jnZLhtKba=t=bZhN8ixss#uDdj(|-=P-v%?Z~MX+>sstCP1L5?pGROwP??F=7Z0>Cl@aGfCog4J?c8eH~O{ZepcGLn7CqI@xXnxiOfi*_G-+@_MO2uDp@@cnfv4NxPn0sTjg^{=9X?><7jT2nrS+)-rgj#BQGA4w;N_>qauq$o_09<;g7l<%!JmYy>Km9)YeQ6@kO-ekvGw>gpGc4TXV~m8zn!Ywt`Ux^Vb=%{tu1cmEG_*RJ*'
)).decode("utf-8"))

_SELLABLE = ("STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "TOMATO", "CARROT", "WHEAT", "FERTILIZER")

_FRONT_RUN_HORIZON = 1
_FRONT_RUN_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_LAST_STEP = -1
_CLONE_CONFIDENCE = 0


def _public_signature(farm):
    """Compact public fingerprint for detecting a mirrored build."""
    counts = {item: 0 for item in (
        "COW", "SHEEP", "GOOSE", "WHEAT", "CARROT", "TOMATO",
        "STRAWBERRY", "MELON", "PASTURE", "COOP", "WEED",
    )}
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value in counts:
                    counts[value] += 1
                    break
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands", []) or [])]
    return (
        len(farm.get("hands", []) or []),
        tuple(sorted(farm.get("unlocked_quadrants", []) or [])),
        tuple(sorted(tuple(position) for position in positions)),
        tuple(counts[item] for item in sorted(counts)),
    )


def _signature_distance(left, right):
    distance = abs(left[0] - right[0])
    distance += 3 * abs(len(left[1]) - len(right[1]))
    distance += sum(abs(a - b) for a, b in zip(left[3], right[3]))
    if left[2] != right[2]:
        distance += 2
    return distance


def _update_clone_profile(obs, step):
    global _CLONE_CONFIDENCE
    if step not in (4, 24) and not (step >= 48 and step % 24 == 0):
        return
    farms = obs.get("farms", []) or []
    if len(farms) < 2:
        return
    player = int(obs.get("player", 0) or 0)
    distance = _signature_distance(
        _public_signature(farms[player]),
        _public_signature(farms[1 - player]),
    )
    if distance <= 1:
        _CLONE_CONFIDENCE = min(8, _CLONE_CONFIDENCE + 1)
    elif distance <= 4:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 1)
    else:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 3)


def _front_run(action, obs, step):
    """Sell one premium line immediately before a clone's expected glut."""
    if _CLONE_CONFIDENCE < 2 or _FRONT_RUN_HORIZON <= 0:
        return
    orders = list(action.get("market", []) or [])
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(0, int(order[2] or 0))
    planned = {}
    end = min(len(_TRACE), step + _FRONT_RUN_HORIZON + 1)
    for future_step in range(step + 1, end):
        distance = future_step - step
        for order in _TRACE[future_step].get("market", []) or []:
            if not (
                isinstance(order, list) and len(order) >= 3
                and order[0] == "SELL" and order[1] in _FRONT_RUN_ITEMS
            ):
                continue
            item = order[1]
            quantity = max(0, int(order[2] or 0))
            if item not in planned:
                planned[item] = [distance, quantity]
            else:
                planned[item][1] += quantity
    shed = (obs.get("private") or {}).get("shed") or {}
    prices = ((obs.get("market") or {}).get("prices") or {})
    choices = []
    for item, (distance, quantity) in planned.items():
        available = max(0, int(shed.get(item, 0) or 0) - already.get(item, 0))
        quantity = min(available, quantity)
        if quantity <= 0:
            continue
        price = float(prices.get(item, _BASE_PRICE[item]) or 0)
        priority = (
            price * quantity * _GLUT_WEIGHT[item]
            + (_FRONT_RUN_HORIZON + 1 - distance) * _BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        orders.append(["SELL", item, quantity])
        action["market"] = orders[:10]


def _terminal_liquidation(action, obs, step):
    """Replay-derived safety net: leave no sellable shed inventory at season end."""
    if step < 680:
        return
    shed = (obs.get("private") or {}).get("shed") or {}
    market = action.setdefault("market", [])
    already = {
        order[1]
        for order in market
        if isinstance(order, list) and len(order) >= 2 and order[0] == "SELL"
    }
    for item in _SELLABLE:
        qty = int(shed.get(item, 0) or 0)
        if qty > 0 and item not in already and len(market) < 10:
            market.append(["SELL", item, qty])


def _shed_access(size):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _move_toward(pos, target, tiles):
    x, y = pos
    tx, ty = target
    choices = []
    if tx < x:
        choices.append(("WEST", (x - 1, y)))
    if tx > x:
        choices.append(("EAST", (x + 1, y)))
    if ty < y:
        choices.append(("NORTH", (x, y - 1)))
    if ty > y:
        choices.append(("SOUTH", (x, y + 1)))
    size = len(tiles)
    for op, (nx, ny) in choices:
        if 0 <= nx < size and 0 <= ny < size and tiles[ny][nx] != "LOCKED":
            return [op]
    return ["PASS"]


def _terminal_action(obs):
    """Observation-driven final-eight-turn harvest/drop/sell controller."""
    player = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [])[player]
    private = obs.get("private") or {}
    tiles = farm.get("tiles") or []
    size = len(tiles)
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    inventories = list(private.get("inventories") or [])
    inventories.extend({} for _ in range(len(positions) - len(inventories)))
    sheds = set(_shed_access(size))

    available = {
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0
    }
    actions = []
    pending = {}
    for pos_raw, inventory in zip(positions, inventories):
        pos = tuple(pos_raw)
        inventory = inventory or {}
        load = sum(max(0, int(v or 0)) for v in inventory.values())
        x, y = pos
        tile = tiles[y][x] if 0 <= y < size and 0 <= x < size else None
        if load > 0 and pos in sheds:
            action = ["DROP"]
            for item, count in inventory.items():
                if item in _SELLABLE:
                    pending[item] = pending.get(item, 0) + max(0, int(count or 0))
        elif isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0:
            action = ["HARVEST"]
            available.discard(pos)
        elif load > 0:
            target = min(sheds, key=lambda q: abs(q[0] - x) + abs(q[1] - y))
            action = _move_toward(pos, target, tiles)
        elif available:
            target = min(available, key=lambda q: (abs(q[0] - x) + abs(q[1] - y), q[1], q[0]))
            available.discard(target)
            action = _move_toward(pos, target, tiles)
        elif isinstance(tile, dict) and tile.get("fertilizer_available", False):
            action = ["COLLECT_FERTILIZER"]
        else:
            action = ["PASS"]
        actions.append(action)

    shed = dict(private.get("shed") or {})
    for item, count in pending.items():
        shed[item] = int(shed.get(item, 0) or 0) + count
    prices = ((obs.get("market") or {}).get("prices") or {})
    sells = [
        (int(shed.get(item, 0) or 0) * int(prices.get(item, 1) or 1), item, int(shed.get(item, 0) or 0))
        for item in _SELLABLE
    ]
    sells = [row for row in sells if row[2] > 0]
    sells.sort(reverse=True)
    market = [["SELL", item, qty] for _, item, qty in sells[:10]]
    if int(obs.get("hour", 0) or 0) <= 1:
        already = int(farm.get("hires_today", 0) or 0)
        for _ in range(min(10 - len(market), max(0, 8 - already))):
            market.append(["HIRE"])
    return {"farmer": actions[0], "hands": actions[1:], "market": market[:10]}


def _base_agent(obs, config=None):
    global _LAST_STEP, _CLONE_CONFIDENCE
    step = min(int(obs.get("step", 0) or 0), len(_TRACE) - 1)
    if step == 0 or step <= _LAST_STEP:
        _CLONE_CONFIDENCE = 0
    _LAST_STEP = step
    _update_clone_profile(obs, step)
    if step >= 717:
        return _terminal_action(obs)
    action = copy.deepcopy(_TRACE[step])
    _front_run(action, obs, step)
    _terminal_liquidation(action, obs, step)
    return action


# ===========================================================================
# Market-controller overlay
# ===========================================================================
import math as _math

# Per-step remaining sell volume of this field plan, measured over c27 self-play.
_SUPPLY = json.loads(zlib.decompress(base64.b85decode(
    'c%1Fr%Wm5+5Cza*39{~j!?(Ii3pWj#)PQRsXp4SH(SNTlZOK$D%hrRG91k$}ECK|GWl5pP5&z!5eqB9m??2xC_S${8>%g|40o8~KRn)i|T_c-Ng)B~CGN496wl}hgs1QXm@KJ@zO8JSLEoMTcp!~L+F{jWC^e|LF)=(2sf$PIb3(SlNzsDBEF#JfoWe(t$Yj9w9c;Cbw<7UNFSXW_+8eK!jXnZ0v6}ZhU25LvUVmLTB{V)npQt&Tu2T?{8u6>1DeP;Bfh-txjrG(rgadmg#C&QQ5mb7*zObT%PjIEHq#)0xwmcrH0IS6;r%ds_7fjeO<R-XVDHtFe5b{U9c@TIh4Qa~f2^712`IfKEUA#@B*lD={N5Gf8RziqLrKOgSyKR;|X>+lpP>YsCQadB~Rad9Oo3_rH(mxt||haX&ATwGjSTv-akk00C3!|SKjX7dw65Q*tshG7_nVVGkyprl}RZvx~bgg>YpF-fdKOSG4qgU%8bqxwVs6t+gzh!`qtez1P$MN(W?6824OUyMG5Y$A?9(^>?+g>mRks6oAK>ZeGxbZYtsodn6F-$d?$<E};~EL)F^?O7_S=&9^w^}PO$2eRE-I>Ru`&4T`{s6B{cFwQ{YZl6U*zQ14uWyS3#%h2Z*@^*MPQP3v8n8;y4cWAPRbdmZHJgFv)oG)UwHJsJsBlnMRadB~RadBm-FjM*T{4I2j>|PvW80OtT4e<Ic^F9%mLxt<aObni{eUSnSOm>`25B5IDhw)1T#~HJ2gbkb)it^`?XCZfm;OhyiIuT((rx*gdOtM5Af}2MpCW=~4u!#b8dq^Fe(W!z<VQjEXR6G?ub;2p#H~XpMB5DU|K3=`9*UzC3<m5IO40GEoV6^e>(Kih?vsxDB>cI}F?O-s7>4zgO*m=mOMPEO7fFHFt)1`zxoKzFEYZV<Sf2W`*g3~vl6)Si2btbe1*(mA?61N3mCrB|}<jgtQPJ>6GFRRV=>G|o`Y7^F*FlVr6C;{`%5t~lbSY!)lcb=RE!hfF_mzI-r-D(o354i67ZQuEZwrOsCA(S1oU{8hVL>-fNRvtUO?m%zt9OxwICh{0%a-kZ?nHV;0J{oL}oHQfG!C2wLe($Yu`<RKME{uGWj?HT?+Td1C5YbH5F*r?^*4GKtKIO3v+vWF6XxHyrn;6*2-<p>3c(Rs!pD~m+;RUgj8S*-S*aeT2QB@B!|NaA0p<>w'
)).decode("utf-8"))

_I0 = 10000
_PRICE_FLOOR = 1
_MP = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT": (35, 450, "log", 0.20, "sqrt", 0.70),
    "TOMATO": (60, 200, "linear", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60),
    "EGG": (50, 332, "linear", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
_SHOP_DEMAND = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_CENTER_ITEMS = tuple(k for k in _MP if k != "FERTILIZER")

# Products the controller owns, mapped to a reservation price expressed as a
# fraction of base price. Everything else keeps the tape's schedule untouched.
_RESERVE = {}
# Sort SELL orders by gross value so the most valuable sale takes the earliest
# slot; market slots resolve index by index across both players.
_SORT_SELLS = True
# Ranking key for slot placement: "gross", "unit" or "impact".
_SORT_KEY = 'impact'
# True places promoted sells ahead of buys/hires; False keeps the tape's layout.
_SELLS_FIRST = True
# Only these products may be promoted into early slots. Empty means all.
_PROMOTE = ('MELON', 'STRAWBERRY', 'MILK', 'WOOL')
# Extra slot priority for a product whose remaining supply outruns the town's
# remaining appetite. Such a product is a race, not a hold: its price will only
# fall, so the units sold before the opponent's are the only ones worth much.
# Ranking purely by current price gets this backwards — a already-crashed product
# looks unimportant precisely when beating the opponent to the floor matters most.
_RACE_WEIGHT = 0.0
# Products that may be promoted only from this step onward. Selling wheat early
# lowers the price an opponent pays for feed, which can rescue a cash-starved
# rival; deferring wheat promotion keeps that pressure on during the early game
# when starvation actually bites.
_PROMOTE_AFTER = {}
# Products promoted only while the opponent's public money is at least this much.
# A rival near insolvency is the one most helped by our extra supply, so we hold
# that pressure on until they are clearly solvent.
_PROMOTE_IF_OPP_MONEY = {}
# Products whose SELL orders jump ahead of every other order in the turn, rather
# than merely being reordered among the slots the tape already used for sells.
# Slot 0 is priced against an inventory neither player has touched yet, so this
# is what beats an opponent that front-loads its own contested sells. Never list
# WHEAT or FERTILIZER here: those are the only products an opponent can
# BUY_PRODUCT, and their buys lift the price a later slot would sell into.
_LIFT = ()
# Step at which to pre-empt the base's own end-of-game liquidation. 0 disables.
_EARLY_TERMINAL = 0
# Force selling once the shed reaches this load, protecting end-of-day drops.
_SHED_PRESSURE = 80
# Reservation decays linearly to zero across this window, spreading liquidation.
_RAMP_START = 576
_RAMP_END = 716

_SUPPLY_DRIVER = {
    "MILK": ("animal", "COW"),
    "WOOL": ("animal", "SHEEP"),
    "EGG": ("animal", "GOOSE"),
    "FERTILIZER": ("animal", None),
    "STRAWBERRY": ("crop", "STRAWBERRY"),
    "MELON": ("crop", "MELON"),
    "WHEAT": ("crop", "WHEAT"),
    "CARROT": ("crop", "CARROT"),
    "TOMATO": ("crop", "TOMATO"),
}


def _mshape(func, x):
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return _math.sqrt(x)
    if func == "log10":
        return _math.log10(1.0 + x)
    return _math.log(1.0 + x)


def _mprice(item, inventory):
    """Exact port of the engine's market_price."""
    base, throughput, below_f, below_t, above_f, above_t = _MP[item]
    if inventory < _I0:
        amp = below_t * base / _mshape(below_f, throughput)
        value = base + amp * _mshape(below_f, _I0 - inventory)
    else:
        amp = above_t * base / _mshape(above_f, throughput)
        value = base - amp * _mshape(above_f, inventory - _I0)
    return max(_PRICE_FLOOR, int(round(value)))


def _remaining_drain(item, step, shops):
    """Units of `item` the town consumes between `step` and the season end.

    Shops fire on steps divisible by 4, the town center on steps divisible by 12
    with multipliers that step up on days 10 and 20. Still-locked shops are
    credited from the day they are expected to unlock (one new shop every three
    days), so late-game demand is not understated.
    """
    if item == "FERTILIZER":
        return 0.0  # neither the shops nor the town center consume fertilizer
    unlocked = set(shops or ())
    live = 0
    pending = []
    for name, products in _SHOP_DEMAND.items():
        if item not in products:
            continue
        weight = 2 if len(products) == 1 else 1
        if name in unlocked:
            live += weight
        else:
            pending.append(weight)
    n_locked = len(_SHOP_DEMAND) - len(unlocked)
    pending_total = sum(pending)
    is_center = item in _CENTER_ITEMS
    total = 0.0
    for s in range(step, 720):
        day = s // 24
        if s % 4 == 0:
            total += live
            if pending_total and n_locked > 0:
                expected = min(n_locked, max(0, day // 3 + 1 - len(unlocked)))
                total += pending_total * (expected / n_locked)
        if is_center and s % 12 == 0:
            total += 4 if day >= 20 else (2 if day >= 10 else 1)
    return total


def _count_driver(farm, kind, name):
    total = 0
    for row in farm.get("tiles") or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            if kind == "animal":
                animal = tile.get("animal")
                if animal and (name is None or animal == name):
                    total += 1
            elif tile.get("kind") == "PLANT" and tile.get("crop") == name:
                total += 1
    return total


def _opponent_scale(obs, item):
    """Opponent's expected remaining supply of `item`, relative to ours."""
    driver = _SUPPLY_DRIVER.get(item)
    if driver is None:
        return 1.0
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return 1.0
    me = int(obs.get("player", 0) or 0)
    kind, name = driver
    mine = _count_driver(farms[me], kind, name)
    theirs = _count_driver(farms[1 - me], kind, name)
    if mine <= 0:
        return 1.0 if theirs > 0 else 0.0
    return max(0.0, min(2.0, theirs / float(mine)))


def _reserve_price(item, step, obs, shops):
    """Reservation price for one unit of `item`.

    A fixed fraction of base price, decayed linearly to zero over the
    liquidation ramp, and scaled down when the town's remaining appetite cannot
    absorb the supply still to come: a structurally oversupplied product is a
    race to sell, not something to hold.
    """
    base = _MP[item][0]
    frac = _RESERVE[item]
    if step >= _RAMP_START:
        span = float(max(1, _RAMP_END - _RAMP_START))
        frac *= max(0.0, (_RAMP_END - step) / span)
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead > 0.0:
        frac *= min(1.0, drain / ahead)
    return base * frac


def _plan_sells(obs, step, slots, short_of_cash):
    """Choose SELL orders for the controlled products."""
    if slots <= 0:
        return []
    shed = (obs.get("private") or {}).get("shed") or {}
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    load = sum(max(0, int(v or 0)) for v in shed.values())
    forced = load >= _SHED_PRESSURE or short_of_cash > 0

    candidates = []
    for item in _RESERVE:
        held = int(shed.get(item, 0) or 0)
        if held <= 0:
            continue
        inv = int(inventory.get(item, _I0) or _I0)
        if forced:
            units = held
        else:
            reserve = _reserve_price(item, step, obs, shops)
            units = 0
            while units < held and _mprice(item, inv + units) >= reserve:
                units += 1
        if units > 0:
            candidates.append((_mprice(item, inv) * units, item, units))
    candidates.sort(reverse=True)
    return [["SELL", item, units] for _, item, units in candidates[:slots]]


def _cash_needed(orders, obs):
    """Coins this turn's buy orders require."""
    seeds = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
    animals = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
    prices = ((obs.get("market") or {}).get("prices") or {})
    total = 0
    for order in orders:
        if not isinstance(order, list) or not order:
            continue
        op = order[0]
        if op == "BUY_SEED" and len(order) >= 3:
            total += seeds.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_ANIMAL" and len(order) >= 3:
            total += animals.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_PRODUCT" and len(order) >= 3:
            total += int(prices.get(order[1], 50) or 50) * int(order[2] or 0)
        elif op == "BUY_LAND":
            total += 4000
    return total


def _race_factor(item, step, obs):
    """1.0 when the town can absorb everything still coming, higher when not."""
    if _RACE_WEIGHT <= 0.0:
        return 1.0
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead <= 0.0:
        return 1.0
    glut = max(0.0, 1.0 - drain / ahead)
    return 1.0 + _RACE_WEIGHT * glut


def _sell_priority(order, obs, step=0):
    """Rank a SELL order for slot placement; higher goes into an earlier slot.

    Market slots resolve index by index across both players, so an order in an
    earlier slot is priced before the opponent's matching order in a later slot.
    ``gross`` ranks by revenue at stake. ``impact`` ranks by how much revenue is
    actually lost by going second, which is the quantity times this order's own
    price impact — that promotes steep premium curves (wool, melon, milk) over
    large but nearly flat staple sales (wheat, egg).
    """
    if not (isinstance(order, list) and len(order) >= 3 and order[0] == "SELL"):
        return -1.0
    item = order[1]
    try:
        qty = int(order[2] or 0)
    except (TypeError, ValueError):
        return -1.0
    if qty <= 0 or item not in _MP:
        return -1.0
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    inv = int(inventory.get(item, _I0) or _I0)
    unit = _mprice(item, inv)
    held = int(((obs.get("private") or {}).get("shed") or {}).get(item, 0) or 0)
    qty = min(qty, held) if held > 0 else qty
    race = _race_factor(item, step, obs)
    if _SORT_KEY == "unit":
        return float(unit) * race
    if _SORT_KEY == "impact":
        return float(qty) * float(unit - _mprice(item, inv + qty)) * race
    return float(unit) * float(qty) * race


def agent(obs, config=None):
    """c27 with its SELL layer partially replaced by the market controller."""
    action = _base_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        # Liquidate one step before the base's own terminal dump. Both dumps hit
        # a market that only falls, so whoever sells first takes the un-crashed
        # price; an opponent sharing this route dumps at its tape's step and gets
        # what is left. Nothing downstream needs the goods or the shed space.
        if _EARLY_TERMINAL and step == _EARLY_TERMINAL:
            shed = (obs.get("private") or {}).get("shed") or {}
            rows = []
            for item in _MP:
                held = int(shed.get(item, 0) or 0)
                if held > 0:
                    rows.append((_sell_priority(["SELL", item, held], obs, step), item, held))
            if rows:
                rows.sort(reverse=True)
                action["market"] = [["SELL", i, q] for _p, i, q in rows[:10]]
                return action
        if step >= 717:
            return action  # proven terminal controller; leave untouched
        orders = list(action.get("market") or [])
        keep = [
            order for order in orders
            if not (
                isinstance(order, list) and len(order) >= 2
                and order[0] == "SELL" and order[1] in _RESERVE
            )
        ]
        player = int(obs.get("player", 0) or 0)
        money = float(((obs.get("farms") or [{}])[player]).get("money", 0) or 0)
        short = max(0.0, _cash_needed(keep, obs) - money)
        sells = _plan_sells(obs, step, 10 - len(keep), short)
        if not _SORT_SELLS:
            action["market"] = (sells + keep)[:10]
            return action

        def is_sell(o):
            return isinstance(o, list) and o and o[0] == "SELL"

        opp_money = None
        if _PROMOTE_IF_OPP_MONEY:
            farms = obs.get("farms") or []
            if len(farms) > 1:
                opp_money = float(farms[1 - player].get("money", 0) or 0)

        def promotable(o):
            if not is_sell(o):
                return False
            item = o[1]
            if item in _PROMOTE_IF_OPP_MONEY:
                if opp_money is None:
                    return False
                return opp_money >= _PROMOTE_IF_OPP_MONEY[item]
            if item in _PROMOTE_AFTER:
                return step >= _PROMOTE_AFTER[item]
            return not _PROMOTE or item in _PROMOTE

        # Only promotable sells compete for the earliest slots. WHEAT and
        # FERTILIZER are the only products an opponent can BUY_PRODUCT, so
        # promoting those ahead of their buys would lower the price they pay for
        # feed; those sells are deliberately left in their tape position, where
        # the opponent's buys have already drained inventory and lifted the price.
        # A lifted sell jumps ahead of *every* other order, so it is priced
        # before the opponent's matching sell in any later slot. Only worth it
        # for products the opponent dumps: for WHEAT and FERTILIZER — the only
        # two an opponent can BUY_PRODUCT — a later slot is strictly better,
        # because their buys drain inventory and lift the price we sell into.
        if _LIFT:
            lifted = [o for o in keep if is_sell(o) and o[1] in _LIFT]
            if lifted:
                lifted.sort(key=lambda o: -_sell_priority(o, obs, step))
                held = [o for o in keep if not (is_sell(o) and o[1] in _LIFT)]
                keep = lifted + held

        merged = [o for o in sells if promotable(o)] + [o for o in keep if promotable(o)]
        merged.sort(key=lambda o: -_sell_priority(o, obs, step))
        rest = [o for o in sells if not promotable(o)] + [o for o in keep if not promotable(o)]
        if _SELLS_FIRST:
            action["market"] = (merged + rest)[:10]
        else:
            # Keep the tape's slot layout: sorted sells refill the slots that
            # already held promotable sells; every other order stays put.
            out = []
            queue = list(merged)
            for order in keep:
                out.append(queue.pop(0) if (promotable(order) and queue) else order)
            out.extend(queue)
            action["market"] = out[:10]
        return action
    except Exception:
        return action


_SBT_SOURCE = zlib.decompress(base64.b85decode(b'c-ri}=aS+`69D*so&pB50$Q^O&)~gBcsDT!fdmNTkikRTL);VIlU$XA5#2qr?u)p%i`ySNNUF-p%1U2Z)nC7Ut<qalonDZ<ur<*lBMTI53S<6I5c7FWB1;}<$%K73QH-oGEK5@+MIu-9OcA7mX~!r_ld_~u3N0(((+ms#Ir9WfGl5qm0koFBef|3N3&V+mq?o3pOb2}Tr<oug?!Q;Ez~6r#S!Vj>3(;w%GC5OB`}B<!NJ>WFmv0n36F5<#Wf{@oeVc~-@FhhfUrgY?KW3=3j@tT5&PkrC7HLRsExq9>X{THMT1D>E^YUsDXDn*LW*JHO?ZUgAjk;MrKp~hC@++;~Y_c3GRI3{4CAg*658kz%Huj_(CysM%8Lgfzp%d4QSjDcnmsk<IEqAV^BFWRn*LR&meNQ%3>><2Z>n17_qJ*7KRM?j|_EEkO;R5yXX+wk;7T#^H)~@SZqn+(sgWF;X!yCKae!Y={J!&5EW#m+Cknc~jYCT0+XZFCU=~*wLQFLUh43BknqD<S{#C)e%Pqw%-z(i{8?WEH_PfkL%vm~RUJMFR~Tw`)dtv%GnTThOX@nWi+-SrAYB6Ary+u=*5Ol~@zW4CQp$BV9;XceNFWo*PR$4B*m9f{s_Bd4T7F5YyG<kO^sN3v^fS8daDOs<3jQ`}Q&A(Q@~XYL8&@EizHNMULBhe-=E3;M0SbG=tOS1bqI8Lc(0N{ozcFk-8=9i7dLSd=aG#K^qi@l8BV4KD}hDQnrAr#=O9Z`KWZj`q5-*}QF!Tq?e8WtoW+gL<plq|f^nYV}g><6+Pq;#`F&siy={Kg1dtPO*cP$rVzQ)qI}p)#zZbUrA=iYlS}9RU{)V*-gN{7RfM*w`ix!ox{^*Qtclzt=6Wv9h@tU@^r8}`fPICJC%Y*GqDIC=5e%_2%KzHM~>RIyWY`0n8FBJO#6bkSZn*T`%|gY#3+AqI7OT0Rx4LMt&tAd$jv1;8bWt{Zk4h6Qr-i<q2<ALhjO{WbYG_wF&gc(qG8nHU)h(bP2Leq#mo(IPR4fU_}D)Sld*AZe<=-@+%V}FbdmB{Fw^`wi`P11d#^o@NQGolSoqNFz;&ckmqgsz$t~)6YrlN<t`k@;7VQs%2d9E3?Yn@xUoAC@;}AX`2Y1dDd2VmIDIuGV*FC#|$2{sw(|%*AcK!HRB*kO=9I?B`kxh$=kkc?DO!{nVciwe}*Q~9xTgF=BSVP=(`)x%qo9ow<vmcu$vq1|#-0txDpm|Dpaka2QHeBw^oQ^Z+6-@++jk@HPin7Y=l4G}A$z=SpJ)4@Zj%_Q}ZXZ!$dydfUo-1H)<|koauRK`~tSbd)`~h`fBbu4XZ0MTOY_YsHla^sibnXM>`fBy=qPY#)Sgy*$l22?jEn@}sls$pyF>@`3t=IO|f*d4vAhtVr-!@Ww=b(!tu++IQXF{oll;@`L31FrsnpP)=qujs7Dm5=MJ8_X~EsgTkA~|t$Nfaw^drHRZwyfx5v;K0tlWyCB!UfyY(@tZ{U26TTg0?2=x*;?t=xl`S$tF>cwj#$}W$oqn@gX-mO{hd9xd<<Zj$v#wC7H=JR%<HhVz2AiCCfep%Oc*r$Q)h6)}Boi=(4zqc1LB$5g#~v-9j|CT4&p%;nZR8*w#V8K_okQURo8+*SK(rSiL+}E48z9rCf@pugs=Yk}^(j*{^10a?z~JL~ksA7102%oYT(m{MsY-eV_Btstii)71Npvcwwf7I_|Z|<+k?i2ryvSIZJR6bmF(h*O5uv-kV={ahoMzH+Oo~%Mc0Lht6xj9%)6VgTbWZWW=z2EY=n|UoPQO6BhF&8???XxtWNXS6j*-n|T%$mX$7tMShYDY#iki%C-ecylfdXQrO#$Rj<TZdbDsF#|y`KAvMlT1L-7<4$XylZrneNEa%b$?}c&8F0ndKmi|mAPnO+<AWkNej*RF#sVqNlHZ7ggIF)c`vVkxqhIxy(msFU{oJEgvAn5il2*Cji-AGF1ypH+>O*nkzK3?w&r+ztdbd|=LYvCH3p7>Kv@(mMyHool>``D=*s-8p5-ZhbQj*(Piw<7FngPWGUf%2In^UagHgXDvggcEVH)rq-0?gc#722!_kctePY*Xaq*bou%;sbsl)lCPkh7B?!#w&A9^la~}uuodXzIG5{EsB0KaBud59q|)u>fhuB~u{K+qY^`m)Zr;%rug7^lt_g3t=dSf9h55V^+{VMBZErw(CTDXt$rk**@yX-%AL|ECg_6Uw;o7xi$xP+KoHvtL22FHBV|q|VkUcSov^*`&70kD$UCY@wDEh8yisuk-o$;+V5hAw7iE3hZsKt;K<M3tFjD5im?f!|7FYj#5bk$o*&lefzjHq<`&bsBWNggfk{)s@g1E)|G(sj$IWf_SVKAgakiNU~@SY|Mq3h@hXqs?r>X&UDjOIhX>e?n9$X=zgm2w9J}!(I21d`5AzQs200tHiY??cM(ClpRju(^{UIBV?G4wAVE2@a>RbW+enC=&J0>UsqRutJVpkL1B7z7x<w^L3iGRJ9*eQD_dJ^DqX_#Ntn~al&6tcTejv|qPbplWQy2GNUcc@{Tp+_<r}rU`z@D0(nFt8C`*Wx!k3pTWp|k+jG4rSg5PW#x;^=vyD_QNtvROM8eUg*VOFO6^-i;ccPrOrFvA^3=~8Bh_Sg17H77SBY0QnP{XxbjQh{D$bY$Y^ewN=>YmzS(Lp(qaoh|9u&>qDKSJK0m8O}UI%X?qBVU5*d1->3gMp|lgU!~jCXq4L1*nSf(`-p=lKFBBP`+W^JXDeH*Wf?3p?b*Pb!P1_wFWFkHuKo1MQ88D<lbh?h+@yFJ9a>@YwC+<*teIC?N8evXvrKlm?0dOJh6rUN7gR29SBhCx8rf59)3AxzjjN4Ij(|6g1-2)LWFO+QNx$ie4C-0S%9bTY(KwQ}(>;G>&o7D-sp_lucbB>+yi&3%P@dC0V*#c`0_rba+Ts(%GQ$ztYTj0bfzYn`T75Yo4?@L3X6mNbrFp^bjAyWhlWYrkDZSZlU391;PF<<fX<K0S&S^Q&E%(<EdsvzfVzEpNH!{J9A#)E9Hy&Cx^2@nd_S%z$0YV>zUh>c#ohyoeHYoZV3v}i{<J_v8Z$;RQSg*3}&Q2~jrw(b?*e@;BsXa@uxW8cKqIB*$l+tsncwn+QJexxBp!p)y)yib#bt6^xrb$K71zDVt_F~xWNO+g!^mZJJFX+B`8mGwq%nyuhB@l4Ni#v19pTHB6y~s8CPWQqmw3_&2t>(<TYHM%-{`KmTS~Q{^nzGg6O)A}qFr`Mqxl6VC*Ph~S1f2B{msq(=S8{pCZ=8%}<8Jl}N;u2cr5IYvbmsZ#p_DF}^OQ9$2J6!_)>-@NVcvV5qs{U<Sv|T~|HYFIIL*KjYYo<cY-i%cD?V4PcdVx5LegVR?_+NCxWlhi@0G3Z8*a37uzRp#H&kphl@YF-QEqo=1~Y0P%C9fS<G2uYL=WLy#lPa&{IXDEk@P7WZ3O2jb96=cBUHtg4Uw%yJ<{Q9Q$AgY&l8JDEQ^(nF2}}x2u5;^VxqI?TSnHkzmc#u+TEpCWmAc<zl8UWGcOj!UECx#M^1LUe+=N3=`~nzDT6(+>;?VRRbtyvNk7p`U0ROmLKcg?YIHQSk{-#m2-EFJz2dPq!qd=7nAa=IS;bdt*AD&cvX0?OAk_w{?${!1ju>@x#T-$-AzBVTM>w|)Uw}^>Q`bax5+Sas6P?@OgKbW#E}G0%Rjm~>7p_mI*G<`%VA_*oY!ny-Ejw4lN~pXoY`zMy_(2|wW7dq*b*_wsxV#80i@0xF%;tP?A=#<fqC;l2weQQwE=iF>V^Ay9ZM8{^_jsC3tIJb7W)fGTusBHb$qrAgXW4UjIwUjIOD<NgTf_TEB!?iES;%SSPgg#)Ul59F^<XaI;9U@7x?9+%H<Uuz!)kWxPg^6|d{~OLd}F@vqnuP^i?60EHaz96%k!8GQmDo5oRu=@u@~vqXJsxmu4c=bP=9sVkbQZ*^WY_5)I&&1zShf8?7Tk3*#Q-2%M&hh;kGf%ovN|x`6ka>%kjp}vYhVoWofPU$+OkmUeT$P?O6A&N&{)z3kTiIF=!)(^G3WkVy6mMN~wu*(^***R-sZoxt&!A-rLU%qCLgIjshUUVdq0U=R2x1#xiiYfOZ^IBNIzI==5z6(VtK@M=yJBMWcz-EV#^*qSUm_%7KK`345ZxR<}MrWOBIUoOGPe)$wkRGW)$fpP1sCJX+c%kNwp$m$qI!U>UFOL6Ir==QYV=E#<{TqZf<rJI>_jz!F)z!)G1Xl7Xw0DsH`s%GC%YvbXshR*%(ew~CcmPH6>vVywz4$+Fsay2w_nwK>(j#Mn9}Bgwk^Jlqa)g-mdCI=B5*!nGfT+3My{C8%nj&7Vd)e}O35m4Uj5L@a#X8I}F{WVY|g@afQ$lhxEInP>u84;-n8JW03XHKKH}Tg{=yzMb-srM_deChL}|L*b7pZ#kl5j<rTS8&A~Tfosj%u7*y?CXz>^z?Yx!eeX5BPVA%2ni-QRZZkVw`q|T-#IQ@Tk+EDRR5t2v=hXh(;Rvt|Hs{GU{qsdWu*45b$FONF+8donp;kEXOdvvI*k;+WWi9o?b|r2--X8FX60zQV9Cr)l?xB>CgQ=>knn}`qS16Uu2bDpqNcNAF-s)s$GjVsJYi63Iv=}38>q96$h^ENc+&>d5nfx(6ZaI{^W9D<Dvz1s=b(q(kj8e9F2Ot_zi<1)YRD|NftB%i^-T-H8*+Syrw)O0u%CI}gw+}>UIjfazm-;cvcf^{|IHVA7ev>~iyj5z6#AFsU6S3Zv@=gRsq`gBr;IpheT{(eT8X2E!H?XT^IZ~>x5SsAr_sO%PbS6-|5Xa5^;Z-^H{hOveUrB@x{mrm4i;WL_6gZFSsh4Z7ttqJ&$OVz{a!{WxFS|sEbhpAS%kCm1iV_jp%n}Xo#?cBMc|0Buh&<PkhUIRww%$e1cxkf7WW>@z&q2mBW$=X4OvfsPEuQx|d4xH0vwk}lX?9e{bso-M!uv*^;?Jmuuw8LK-<}56>BOjaKo9Y7*E_rT7;#XY5VK-sX}-|u6EK@oCOPc0eT;K=c6oN|VuAsyj2uX&GIp$%NWJZ3Px)FRH)U1@Bqv7d*xK4Z(nurQ#`A&rvUkX^f>IyNMid(B)~TE;U~b0`#r^tduIv^8+H;cKyM@EUcxsghYmWER<z#(Y>6^E!z>@Zkvc19LG(eL9&}hi5_GP6&cGnqJX|Ik{Zb^kfu-1s3&cGIo8;aEME0O)sMsir7bXk@1gO!R6Nqdu12a=R(7SWBX+%SvQsoEXvJw6oM=ZVH>)Gwoqim^2CRILd=?l~Qr%6t&GrjO;KMe?2og4|EKS0xTfjy7s}d6B8LERkG?O{_DmbKzKtCwCck)mdEC%4ytiTD(;3*ivobW?HzeOAV{1WVs@j(yH5@3LA&VjqQ5{H4{0M(b2*ppTY_mO_qhJPcoC-7F%1E=|MN$K-iQr%M`mE%sN>%3M<aD?z#u!t{k^dD?zgp>)KIseA^bT+l2QdQtMT!Y;CsV5zEk(Cb-l--9Y=**o^Im@#LXND3e~qp5+>APoY6A3YWc2S&jOl<0Ks-OllR$P|CSh49*8)#k;Jy28qQ1wF3{g=}(jq85@<d_Oj0zDJ~r0RW-JWPyAGjo0N!z*%~B9aeCdKx`w55T4lrAPGq$|HkeI*!#b|kKr}AxCri3tHM4;Yww<M<xK(Jg3Bq1-d5&|=<`NXOny6K_r3<=FT}5v$*O<=jHH;Y-Q-!cdN5|b|s3v7*Qz4Qpq7Acp_Lj-mMF!rktClU1=1zKL9WA`J1z1VkYF*L=w?~br!+k9tw$!KIu78x_XOV7-a*fjFPT}m?pcoaaRn+=EF?M<rS+(ql%s|{+I!q74aFfAzg;A-0vh(G`_)@A{Bb<}*<jcKH+2ZHToBF0qBp2$bOi#@t^=MHenRc*t_9RP*X!KH_c&0;}-^HKOEbd8GL!IPo@9cQ@9Hn+CmuopL&TDD4C3<D#D#j8EUn}7!RC4W(+Id&TcTp#DW8njeWqEMauE(K@D!#K6QwHA2ULIKwjDzv6amq?`_Ll7;zL;LE=lu0@bV)T&#a%2MYqNDMbV<31nnL!>bypz2X3(j{<99LEb0ckO!~xS=azaZS=KS6i7Y;3*9*=!d8q1@w-4`D2vYDjY70DOPn^F0^JlayFxe$~GB`H?NLIX80ZP_xTxEqsJ%!b6qQSY(h*iwZ7$|(LwIA!%jXdJ{dKEGv5^*fz%IUCL%y#yoI6XW`}-d1K7C4NkFlWoACEwXssT194k&O0S4GRTdG6W-nR&Vv@*wq_mbIUUXw?QGoHBqY4fEE;np5!_eLj@FL1%}>M2Sn=<JeAJhsiv!M?DlP;*lB`xnWYFr{5uB}?EM46WSHF|pxS9Q;8jZ9pl_eXTGVA@gSN12x^u-aKBD>VC-slqOC^{2%oeZt64rF5$cKWumj~(wWxnik&$aKs#_S{j?WwPX_0OR09`N;Nj=>>u1Ny;h_6|mlgs+=j;u0_wLx?Lk=rc=e4Mt2%@1kI;HYBU=vHPN48(aQ3YTE;4yYqd9}>rGs2#>x|>*u>&!pD*{lnQ^_l&gKs8dVE>l#XQYmUCxzb2&X32gq=EVTb`8%zgpL7xVj29Bqo6-F<+0F2tJWapYSQF&Q<BS_hBxZB#g~XTOG$|+2~|TwubrEktr<>bHuXF5M}oy9LVPv;uVDa^~FqRE@s_*4ihfiey}34TXf|uG|`N+)Y{YLjn&;P<<hR6I<aG;nwvuQV=m-5*}E<u6E2HP+?L=@BR+ZP1Ouye!(|CxoW5~))}HS9aR_N=EOlw63Zy^i@18;xewne1S_tOwx8=FFdkTzV)q>y{(Gpo~3WF}|c7{{iRF%mW<|C&V4UQV~h%Z=*xk+MBa%Z#MVdD@yVQiwma-Z;P(8DFhHp;s%x|>xSpDR}Aj(gjkRMx9x*J~S3+J(cizmn4^MxXM?V(Y3|xmB@8UA?ma-EFa>l5Jg&D|-*2(wm~dCe0Jk(HxZh(Smz_NCi)7XVVTO*ki7>H7DZ<slJKSGGR9|lg5Ku1Gssruu<rIs*p=BLrlnFcdpS{_lVZrYhMntBwQnQm@0Z}i^4VUJ|^kdIZ{h7gB(XTyRAqTxo~u7dafT=WMI7ZtI=hop_T{ea%PFU&1jdXxtr%Lk_r#!lRWDYBGIY}?DbyZ?0qj9-}J_0s(E6j=q7>_p-#!~61k}&QshMFSQh?Xsg-Q47sVx3?q)ohi{R?Ixo)nOKf7@p1ZTCZ<PCr@6g%w-{K@RUU`Jt|aY}tJ<{9LI4ga9oZZDU|kUtp{snD)on)+(Jc59cF%0qO{1U)LfXrZoI!B%M=y>qs`aLMv~C(O8WKX?%ih}G*a9t4%KOb=AI;W>zug-5X(aJy4XRgj9SBxPTFd>}AhBa74}(x#+|lmLOosN2LQ;p!}3vgPGGZys{uj3AcWdf<vU3VxKST^1gDrZB5T+KIwSjIZMqx5xX=N#}ZsB`d|wF+T5|B675d%QI^@fbE9nF&UgNgT*DzxZ9WZD4&~z+em&q<DHdcaVj(ABDWR&Jrrq1!xL7W71#YLU5wf;?Q>9Jy@77GT|+ibH@&F`t+h~fIvdtf#iKwCd%@Bmjx+nP`Dlrp6E*dktgchr1J>XBoc=~E7ApiqoU=>iu$QU^gi6}cWy4w3C*WrFN?V&@i#>Tz+`eie9ZwdBfIsA}T8T?}@2{5<A;j4Vy0VqawmHu^7lBDD6WjvpP-vWXl^yGC()Cq^o0~ghx9G*QSo4TRrb2$Ubf(&uVoaDPPo-JX9<fJ+h=c2HT#FOxMm^kcE!ah=P>k0FALiV;M{EXfwddJEKH;mnP`_{MRabE-mhVoY%L+N~I1-!0t{w+GpKmF90n4NLz@}mKibQd{TH9upSaX5U&a_vkZdc{7^@33616DjF)+zU%No6BLYtdpoqHTUXv%`2!u?E@o5<}6eHP~>te1#c(UMY?KqB=QYcwrr4sAk<9tc?nBR*rI&xrztMvacwLl$uY~;=NU4t{#H&Jmk(DsA9;r5}f5}+*6Uy&AvZBXq4iO5FbHT2*vsbopLf=TJtA*mR`Fmw$*kN#ab0xfwN`W$kD$~+H)OlGp@(aSu~zWyQ%RiNxBo8U~Cx9Tb<_0X_{fN`tX>vw0e_5*io<7hv9V0eW-@FgGwQq5IC!^vWdjxj9aA8=oZEN+c+0fi-qwv77v(P1;_H5cQ*U0u{iOR!-DyU3lz3f%_Ct|bBjxb-7h-ixH+CS3-Z!JT~gF?yi}TVW++?Ek#a~Wu4`)y9gGI3yR>7m^J$!lTXAPoL@_i=ci7U|JBq|c!F4oFCJx<Nx1RUmqj~p$*trB#P>-eLE?C5?zGY|T6&%qT7i32HePPHaO6F>DVZ~}(GUwl;qikO~Db-fFp31pMLFVFP7j2vE{T9iY5Jw#EjwX{GTOsDD_3YbBe<NJ#mLp3i3!Uxw#Icg|U{6eZ{zkSmXB&LbHL`isW^<Of^hYC+68c;uhfb8<7{{`x)e^THH__&%Iq%fzODi(nT9)UeGdZ{@L}Iu-3=h|pOgIKI)w7Jf><+2#L`pffsLrKCvinQ{#3ZAF)4CTrRERsr7m<|RoLgrdDGN^9EfNU!PTPHkL&hb0FSm?D+WxJS9Ugi%pvT8GIn(o|s`GADl#Zvf#6;q~<tbb~5PNriG#k(2O_33Y1?ZMA-uQ?^&`M!x_okDQ*AbtYr=xJlp6Y@KE4!Qs!PscpGFx*K^Mqu({Fa@ru9LXhEA8;Ay;od@eDrKbcGX}rJ&{%`avyYZ2pMyY@g^6|;)Ua;f*dN5W|m78J=S;)?Plw(-M~${oRLtbIo!qqp#bTgFDJW><d^rj)S(L}(LG!x!qGE<%oBTWNwu<`LE5%nh7WsdxKUBAagJhYV<ufF`AbxLDDJyO+UBe57cQ}h%bpdBuCPXG*isAZn$D!n1G6PKy;>%P@`>)25{S4vwyG>5pnj>v3of6pN0m})pfTPZ!*z7NUec-TSWNF`R4FrDIy2%t8MKeYq`gya?i;&q-&a!i9!ofos<sDX>&jLj!%obXwa9qIy|skcWDFG#uCuQR?9^NiFFoERpZC}tLyuBvb@<41V9B=jbysK4rBl&u%C^PYmcYz8i)5}`+7?Qe{79Bn6R~=eB^;sjv~yipYgQZS@GdRm;3{by^B&AHnMqTi<w-?k$gw9vw0(3YADh|^O|*sexl5ov-O^>uO$A*=q3CNTfOLD?OwnCQW$nvWitq-@QX)HJCd*@-4irPtVa3L|Bz(|mx0Q%go}WDl7whR$_!_m$vGkCxXOLhsfCLg|B`<D9OvgE<o7MJghm`k)#?oFxfC=_R){=J++XsiC@u7*#Vr0S5twsyeMZja()!nlw0qk!6pn4{$^EjA_x}u}{0k|c~@LF<GgVU-J!E#wMj*hy>C2%ekR<)e1C+w^4k`sxpcFnU=CmK63P}sQYn5W&dq}>HcXj(cwmm=@$xw>dc`rXG;-E+)D51e(>2@_I25boo%LO;@2TzWKD&Rtc9TSlC_V9<lfxHO}C(X=O@x8cq4ez6|glX<hd+VO@<!CiEiE2bUozB?B4hxnjfI-o;J+S*q^*}lsb&-+qD=8E&Ca6%72!))q>A+e6*{!EKho7Xu~7>Kiq89{(sS~?2HWNcc=6m1>*z-sB+OFmK&5OO6cN2}v7YsF|*txqD^!mv@{H|pMs9Wz2ciB1Z|$>!+pQ3@9bo@a?&%0Al`<7F;Nl@22^9tksrLq<sOp`BPuZWz2CX1DEffGlEa#=Kf6OS)%1G;(Xo-Q-28n(=1KX&<_rFGB@%W$ucJb30(GB<%iP$9p6cL9`WPIR`Ushv;CVG1#>_HaX&PE)M2&&vj(RC3cVDAspRf4R@O?1P}FMttPwTD2a`VL%)v>##C2a0LpRHq=Q^%=w8->Nz17(CNF`*$#M)Jr2>_-*U#r!-+e8kt+cOl@Qy6)NMXtcgcz84cbURw-GDmY^V?#wQ{ltoWntFOZRl766WskVQ^gNqo<osfzJ!dLyJ5)Y9M{y`q2o%nd=A@gMGgZe`shm6m<G*e)-x;?90^QsG`w)@O|Q`D`BuHyq&<za?1R+6#rW*`GrcX3(7Aa(jA84cS4<8Mje@s4s*r#ht4un7DovOZvi70vdfZ(-m**AAzL#?OE*?Lmxz;d~ub9)@7~o2OgbI{L#cGi*r1?&c^h*JWD|<6JdE*=P7xa4LNSu9=7qhTJx1Xz?#J~ZWN*SNEf%fr)6FYg190=E!HInGWn3=r3womcGy5Sb%=V0Df==+kV@t74ugGIz??w5Qcp)>L?S7D(r$h&wdiEYV-&BNe0Qz)qn*_78@dwvyD_LDD`FGSOg%(S*G)Y~l)53||Ou<y6*g{iA59{ZhIqc(M=kMVSQY2S^wq5rULwNan>P_xO+c|zLGwjQF|Os#UK-Z(7}Lm6v)+0KThiL6)+1+m05D&{0Ud>StH$fl86)3*F1ZNr>BmKKTRHLoOsM;hDn!IX&acfLlsO<98BOnKaw3Wu{GRXUVQU5P%QW!1HH3n5!+E1A14^LSK^=CT9ilnQ&ph}=mPXvc0_AW~Qa5H1tC1lt)ts@C|^;JV@>ipSFQ3yZ`SSeY}?&I_5%B!x41@j|-et3Kb)q}iRzF^I0)zP&RNo=W3k*^33-Hd{@!VdYSp?jUZPA|mvPRum9$<XQ81<BC^m_AX9f4B2W}568keD^;<1LbL~%YBo|RZfM*(-dTsm#dV+MGn;_Nd`)hG*~T%<HdppbZ&{vE^eG{qPmNJ}5J~OM1?Mtro&|k$hbLGyVvRMGiAP#zfQ28>86+|sm=g!jnNUx;RXkrD(+kzNw)sX&HeOFUR<UW*>zrajVbfi=Y!Qoflj@fe77AOjW3P(zb8^v(ts}83;tU*7>eya4;?X7FT^){GwjA|^ZN5Rx%zNEy9B7qpF0kT9)umFIk})MV9WCo2W-rSYHA}6KGa754TU%mutqojpSynO)tm;pQg%-YRBocWbXzqB1O_GIqMp*dDiCKs)Uh&h27H5SjAIxk@$^C%eGx(fw5(U(iBx<-v&5Ft7jGu3P^?ieP%bnF?e2Rq!iFh=)>Uemm?Q)>fVr5A;3n||&QYYdYQr%bu!X1uA7C|;@GncvHAztCajv?I)B-c1fueXI=d?6NQzRsX`<w8dgjO~<3cR%h;W44o`VlysRAe^nT^N%kM$G2N4-&a+cqoJ=3$CoceJ6Ely(p6Xuh<t5#TB&|I*J=&FzL~z(a#g&p{U}u{@ZUa;SK+_8LIM8M!E31w4u54*trp(VniO*>?MFV>>XfRbQLgnB4wG-;^$yYM)`=qCDvj_u7!NbPE_HIXwuZ!G*mu|%k#Kw=(y4ZiXtYXNA>--R>$}P0cfWT1Zo)k7dw=i{aNmJ|#%}lJ3sI<cJ48QMDik{}puFGw??HLK89?a|H&EVh9ssJEYIlfsC)WUgP%ys?fRrOLcs*ar=IR=%?k``yQ1skHi0YJOW`xWvcv4X%8kv(4=lHJGS$_TcH6w5$Ia5q}Gt->m7qlcw46m5xf@Gp-g`O$krHM3gj3fyXO_`=D!%|vRC<HPSR9=zclo*BPzMI@yNBG;s@Fu;WQyVOU_ceMKbGZimQNZzb?qxNf3w&SnXYXGyO#_gk+tR>fa9o4i&*ieWo{o$54@5{3b`T#p`)><cLB1*sOUt1BkDm?``2OSP_s3wcJ^Tziz<%#O!~dAMi5C<TBQw0Lko=5BV23vo#mp4PYg3&_JfNaVzkGnhtm%VBrmrN=a3l-ypGkrU|6MaY_4N~2Tas02KyNspHWdKF@u3w!P;UsJ>r3<z(sTKKXl;L*Tu@#<Yc`c=a;<$41({J8frm@}<4I2Vi<Tfg0lT_?I^Il9<oR_;^3)5l9X~Z-5)F9L$R#Yz|F+wcBNSC+X+#zzg{BN$RGt-PYnmc9DoIHsnA=PLUjfh`?sIc!Yjb~sBz(;JBZM0TA;<rG;r$zE{rkP2<1UyFi6mfMw#Gs%Jy+gL60=y|dFcKL(3+geT7w_%pC(jq1b#YRn}PN7nw+<`yxtxIlSehe>Yc#z$6m4u;!n_v1Wl*<^vO5V6i(yFh&mwe&l_^!*9`>VGVPP+r^y_<ee@Va#W;k=xZ?K@cWS62MJhBgV+EcjL`j$f=0=36{AQ9BTD(zX!3tB7HGR-`cT`|gT`U1h`QA((pTh(=NPC57ALB8TFQmQG9&MnBDF(EqLCkanb-e+&3bHxC<H_VN{PZM(&bG3{6g7E11$L{$j{)Qq<N;BC3qZOxh;GOGW&ey%9^gOM?(z>Es!>{g)e-~i{o4Amun#1nKq)+@^qIBc7#<0|ee%g=!gP2v`wpV-FCdb8#QhmW^a)X>|1}KnLk#B<P|bv-@(3`4K)~Nj@3{^bx;D+SCcv2{QKC6U<xDIC9vF_JDF(1DdoWFDATl(tk{Sp9A)DyE2rMVCmJ3!@9>x+7;UhYLW8m6<;=KSmxj$tlL8530vL*{idc$02D2|lYwDO|!j7+L`bU;DCJ_k**K-E(RXwaY5Q|kuBO7H*d2*4U_p!W4mLrRyt$B^2HUhSRs47C^#ysywP{Q7E{ZV3F)+hIR{LglBw)24WTugQ$-zRH?ZX<vXY(j>`o7dxH@%kY>E%~Lmyg~;iLR2=$(18AQt!h?q)A?B(kidt*v9gx6ZLT-JrHwfJEiS~=V^h345Uc8M5eRX_(7@Gh5)w+J_kRTr&fxo{zANqd2T!z=!PYvmJ4)zP2zv~TYRx|d1`|=Iga?nFLJcasK%WdRK2=HbNZd~vYmD`7#^#&fzea+q;gTA8js&+mF1E~V+-MzooSYB#8Xi)qTvjwW-tG1Y@i$i}4o84dO>?<)d8VWk{?0RE`*PeRA$4lKcUkbP0H%oQ*PTow&$9Xyog!%?s$%tX?$SujR<dmgf*8n1{A)tf3TQR`nMv=XLe6EpkMS&<jpc~LJ>X=9KSB>~7Gij87BF74(g6MQHU||U9^yM-d-dle`(ouVrCLOTziHy@^jOuh~FFjl)<a31r=yP8H2L$sTrw5cLTDQggMv5ZPG6-@<^X;~x54t_{{jG<=NWO1-TgzL+=UBRyzYq087yI{}e?Hsm2I$9~Gk@OYSpM-HbN{@XT7{OtT9YinG8>fv{vPP_JFDBGp=W{uILsDEk4(;KfHF@j-+|&Hw=@uLlMF1g#+90YG5nV1wPTH>0zQ#4aNfZTjOJI<z)@2m^ttu>w{oh_99k;f7R$5(=1i*WJJtQ(#J-Z;sP|sXf)3)}SzXUB)VK!i@}d_sWq!}qJn6I1IOR9u{vxWNaoptA1~sbS`=sv(>QjRLGWJfQ^)J8TK8^A2F%&?DAZIgplvHMp^o@6xBs&KP!#Acs|9lNRejwUc6k6;1FJS()w;$g;+r74NJeZmjwltv#J5r)x`1od0NC^<=O$*QE8$$ax6Qm&cu01N?StF_5_H$hgNU7`rb@tzXsRF+Cb8VO|LH0VHK=vJmzVYAo&86;rT_5@aJ!?Arrf(f@b&6VNI59}Cm(KCuc5dTcLuc2sv$kF_jX8AUJ>5?cH0MEkUbj*oG#eP#4Q&GtDW<`JY^J|D7+-0CfAEK&Klr^Cvwp4OnMyAE&Ii3Siy*$_DSp6wQ~T>jjiyUI)EZCqg->N#+G<)3rJxGqVS0^ZQ5uHHs0MIJN?Tf1{-h*9{1fW3_vfzvY2*l_x)=SWhphKd;2s&?eG91Ci~;UDZKrc9BpI})?^0*R5cu<@`wyw2*EG>xuQT)`=DA_2_c46``Wp2-KYXM23S_|3MPn)A>Apj(pZT3zuEfyu!Jk0e!0~}@M?R_^pp@SGNl)#r@w($hw*$j{%SqC_3g`hQW2D`^+5YX3ihQ;M9UZ?g28J}Gu7Uy2JTiq}4-Cyxgvv8oTI}Ji0ex+-20AkvR1p+hm;-(Z2?50jiQK&zjP5O2^q}RNk^Tl>5;TCy@1AmlU<}iFfQuP^KiN^s5(*@=(lBXd@I|+`KtMxp3$c0h|EA?PfkXQo=bcWzbNVf@D*pf~0%(Z4VmW-!D-TTrBLY($ME%AU(J;K5K{#KS4}|>lF4omZ4JrLK+rk@Pe||_1>sC+8A->M&gNOb;^!ePDzc{q|x;}!R+w-e|e~GYlJl@4yT5jimz=FRdO)=H#K}+{aork1-1FrP!W`Eydbzg>8(7M^Zg&x|fyun0#j3v1#MVdC>wFK%$&$R9#3G`<SJ|Esinh!kx$`yFU?1BAnP%}hDujnDa#Sb`1T6zRFc#rG{n&|`nPp0%67I-fIoR+`?kQ<43AOrXyPXZ}&{E`DQc(t0#bO^(K-_I|<4#^EYZwCAI%flPdA8)Gr=KDjeU(Jir+jo5Vg=F4^=Yw3r-VYJ`UCiv#f&KTmA3746`hMD<-;L|ku=)@vW7>D<3hU3m0r6_GK4>59>(5uzpzSm4%jxd{6M<)#(g8AS=<p40r63Z$1tBFJ>qsi?c#XP#d=e$-X5R4TF^(3MKD_J~uWBi%MxW|k?)w?I!A=IBg^_3($O%OrzJ3xFz4JGqXk+f1pK%L=-tJm9^h})qzvK6TQL)s@eZ6@)HxKo6_pZL*Ssf^WH`C3ldcMTI!?!n%`hJ6~(dBY?ZsFZL1i7Gf@<2}K=gcAoE#15Qn8$wf+b{NJw4htpX)n}<?+pZdGZ|8{&rJV4YKI#&u%RBp#|-2Cejh;hZC-ZG9|_pM+IV_F00h%PEciZe@Oc>U<wXy{o07g!G%dm(w;BG>vb%c2-)=+bE&gWq#K;W#SFoNIK)e6he*judV;A%ptC)bDkU(hhKOX6JpA<(bOA{#ra|C|C*)(Vg)mB8JIg;U_Z>j}PTY&{GvPl3@=#r5^xCLAdEu{&>iza0iRxdzIP4I>*&|{9mc<9>~qTOvYs>6SGSCtLROSV4eclk3%(&-JKt}Al_DKTELzp^+Q&6Ye6eeELBu6NiGUa@9vOQ}@|V{7Xrm#Lf!ebz5F{Pv^SPjAv;E|Ku;Gep~Z3dL=Uv(GJru9X(=V9p(4hSnF3^fgnc`@(@8ds!}ItU2J4m2&ckhsy10PN;QeqWM~N<xi`AW=x-}c}EQK$a8C>H1#5Fwtkee>0I7Yo(p|orme$Oco&{UGSgi&*sbT=gFfL3(G~M*z>nP9z-6@Tdi>RGx5rgG=~K_ai%rGeQ9Yf+DWnGCSe9-?((@&%>{n6&krpJyEi4&(v+3uiLFW;lc5IDRDOcQB9Pa&&n@L4?sU3(&HcBRf^A(LpTj-#dEh>51KRtEBvt*~V^fk%r+%pbho=It5$#qkfWZKDQW2d^mFb}nk%%&<;@J0JjX+_S1xQi7V@u8e)l2rQIBB?MgcnPV9aC_x^UXlZQs<SJs+MO**uGemN#%n&eE2}|}+6DYgry?&4L4xn~3hRR?v6t3pyT48si}+B?qjRc)w+p__qH7CHH~U>r4k)h0acQ1x6#9rYthGAQPXt09AKpFG3jU!rl?Wr_c*3=abFH-;5K@)+h%W4>qoE=T6d%Z=Rw`kQ<}Q(IuIk8-6L^ql$L!(pZhUFrRuA3Ep{00Bo!EVy$w>~RPqX~4c^Zz`K-YO}Vm`HhXnQTTrDx<!j-9nev*F!__)z5FoApzT)|BE##quJ*bqEDVcULUSWjW3AwbqR|X%5Y=YR=BdSMsdl=f<`la^p(JM@LJuaXxJ0s(U3$;!~bE(cL!R#<}>!<4^lb+2ziGbu8Cn*|V6grw&FLPZER7XwF6O<$)=w9R!i~&IN@lHGgV;@zlgjKX&!0X3I20ZN_;T>6?$yUUQWjv;u{MI*oWlOYu4oYiWPBd#-q6ld!XU%y^@mzl8hTg`Cg}jOjR1VV1D^Fq@9gN|$^BN9ADLcU<63F2>=tMh*|o^ToX4z$VANP&wvv!%;8Vo_qQe=fZp4vH?e%@l2H|jX4o6l?Y&UFPD+h=Sy_8P@0W$JW$BDTD@4ja26)R;5hHhvpp%0iJT@jzj9@#?V;Jh&Ze<e&b*xG3GP@zB{Yi&UcZkC1V>FZH`+<KoJk>VOz56M%U(5(&g-qM(!~>;?WlzD{jQW*p4>JPU5^rcu@`ZdPeSz~6r1ycIpf(?X~a5IC(%}=mOH71{wh)IBwQT|%lL=WqCfAH5@V;YP*Ex++`Dyc`}x3NUpz>BB;fR*Q8DhFAuZV~X0Mzp(&{c&p|%rkJ4w3ZX{M8D^SMr@++sAo`&ETr$qj4e+~B`2`bGqiui|)1FQBV69@&grwHAm$JpMP6&kc*y<c$Q=+wN~6_{0he?ZM-|RTSLox<DT<?BjoJWdsm>^tn}lfj+R5&ZCV3cil<NJ^SW+=@xi&d#R&Cw3<B3{cZ>&B+StFUXh1r)qP&~CuoA-UPBL9q6pe+&ApyaF#Jf1TU8&TRS04p&+9aPh1#wB57Fp=x&6Pu>^Y1fP=bTGe@VlaXVCisjA0RP5ZPQURnI<`J)NrLbfVr1Gj&F|57;P;Mk%eU*5+PE`K;c2ZJus*>zN|aZs>gR3iGud^4?{bYSn@Nh6A4$_Rz~j?;jz<W?H#a?TNxK3Oir1&UJ`PDz8JlmmfZOsfOd7Vk!4qkPm{VTD4rOP1I7YN=~2CZ|WM~PY_T&ldE@ftw)8bo*i53MS@y11%wbdqH8T_{aW`593n}e)R`h{H+dS}vK`FAaWG;4LAYQdfyea7O5Zj#>AmLPfCj+DA_1_ubn{z*9|fHrz1=rc4tP!n;8+1~OUrq!fj_H{sE{J8d68!zJXBfQ1fp0$g%7~BYUSFwRxhU~4=tuPbm(BLcCTTX9!v{KkmXysqAX|-IYCymH~Qut$-+U_v_2eQSeBt>1%Q)TL5bYsK=>fT84BzcW=tu155em{$eA|EQ~<uDo&}eo<A=98TAT`L4g*U7vqkc2I7wKW3CRz^!Y(tK1HsUD(^m~&xQH-|^%aIBUm2~8_Uj#DB?q0!KlHbM0GJT84nqdy6gUBv2I)aBxdg$UMr-vT|EYzN5j`LBk-`9PK~=u#1=VdLUuv~GPsDMaJ;2u5lHC}BBVlpUb4(C_2^s+pI=R5Iaw3S0fq%>cTv+xS)c<%5?`Xx^e`reak2ljFPlkn0koV!gPzwKWfU$FXMIvvcx^JLsRfKm`OuMB35Hon}swe_1z<fa1bDJgL*FR(c?b!;lt^z{%Z>BcjC<8d)-ve$YVFd%+VI)mUfu+8KXkWhZ^^VbswpbXH%)!Lo?!2Yt9>D{M4Q^#y@U0+<AOz$UKxOj&3epq2lubLpwM!ERF!*L*5D^3vu=eX<nyHcm`rbwcv8}8}AX9R-hRHM8^nd*y|0lrl7TKdSiPW-9x5)sQtRSpqh?*AikQyv{#>jAh-IC@3s-#wkZNwFdG<=?e-VzLx6ev+pcA(&a81q?h?*8U})f1%hfj6}If=HCpk=G(Dfrt15>H}Vd!vkDEPmO^ztaorkh=V?Ll7Av6k_TBYnxbjy4fJHd0?t4Sz~M7hE0zOP0D&Cb1f$@pGeF`aCW@ZZlJp!*#}6u`yF6$wfzAT-2MC%dRk~9~=j;W^L3z;Vrh(V>9gsy8Fanq~U?};?=tL?HRPS9wJ!tew7l1zdfm3c}^Bj0SXdJ1)(gdKoGy>lFC8f{I1T8HPKutaIGp&QpW;cDeq*<t^r%)&)pqDj?(xgP=-5ss*H~{#80zlz1EChDYn0LnBBwQOwG0e1-C-6ptsNr=@L%mK|mr$c}Ua6e;R8TPg25<wz7)lc~xm6_)VoN0aqNB$Hg`x`w4VOluwf4})09xrwrEBZEa(m>~RA`AbwX0?Rpvizr#SN*Y@fd)yAYrB%GTU>9h^HA1vD<Fx5*V|a5i%WM##$481}YZ@&J++3N|gM<u^L^qR1B)+05oj^bdqLL_4~1PtW0%C3vDM70MraUGy_kw4AxSjzXO1fqA&X7p_z>X1E~OT(%m6ksBAaWdDGM8OPY~1y8wooD@Hj3rT_@Lu5fpP%IcVD>K!b1wUmcKk3h}bhGI-AH~9k^127Is1EsHlg9iQ&eUda!p~4)6!ecTdnZ5zqQ;ZA^F_f8Hs#P5lKwfI4daA0W*DR*IAOWQ0n~o4*&7-!&kosU*!7AJoA|&e@q{01M$!$;ys3N!tuG!>bE(_?8Yqz^CXoNy=gqFc?0pSa&k%ZUT9L(uROTyj6YXj|o)faYP*+s}!a3tfDpmwY^fH#?HK|1+^f!mv$=JN)zz?XYch{(1|JzYDzdhmuL8}Mk$dsp4?SwHgfE@&`(*H6NH?z%slX^GcQ!<@&Fkx#tlM^N)<q`!Hfdk^Ox-(NlCXYBT9aC`MJQhT(xz0w@pd!3BD1X7O7Rettn+TRk$z@LRLw3?(_Ao3x*y8qA;1UnyFnVg@t1d-Lpd@W2PeuLkTz2hSu!UA*us+0B+!M?doF4O)c*ZTPW{Cc0cCb7tU6Xm9_o^>L*y><W#`o&t}5*RUl!DvO~x?fA^{`b8c1WN21XeSBkVkxRXwM}VYhl%<92Y5qH;l|zk{sV52fcU{sTd3`O+*N1P1j2vAE(Zsb^*306u38N6=VJ*Uqdif0Zgt!bCux0L8Yt(-o-o^h8ffuJLBEc~9sLhTJSO;;NTBbKc=UYEAB70LtR~!yF{VNE-7hc_Pazs~SQBzv--oYCP!b7uIJAX^&J+0m5~#H2Qg=1a6Rh$CHkv$qUT9xrl><t0N-H}Wcr6pye{weh##%;wud)pRo92ve{$XPoDCsRDGcaBP9)$1B03FN|n(R*-VtRR;_IDsSl~ouK#8%SH%hFsxRn(j;sB$sApuyt?4k7$o5~zOIN}ngRb9yZsF!T&GmN#FLhMk|@$>V4Q(A)ZPEfWHLAfDc7fNp*USXo+!2ZwfO791Kq-9S-*>aeyz*1UhPE&yi*d<6u$5&Mg=7$Wu>G=C6p;2xVymWLCe8!tE~UXVTz^0r#0=U%o3?tb*_RwAVL2i@;gCoHq2AKOvSni@lGHV<a@_Vf_6J=AA1=Hu4#`zrTa$G<3$-f0DBCRiDII~8*8=zw&>^ynTljsg*bBiyI>I)XMaSL_D(H~aGUJ@VTQrrusB4o^IYr)>fn=6x^8x)1I!5|B^?1-RCFG0^SZO{vSoZM|a8EoozxMXzqVb%*iMeHrA}qaAOipvQPZ3^FqqPb)3;8L1?jY$p9Y*}I|+Z46gTBh>q23a|6fj;q~C@u6@<qv~CH^!?O(<HrUv#13HQy_K225YF-Ooah6$S3I01<T22n4~*Uwo!#lHou>nH$2`BAyiYq+2C#!Q$!?v=5Rc&{c6*7vsA8@EUDs*_5`<PwDQWxfZzgz5_Dy5Z+Y&ui^smnT{y%l@7iRGocnS&Vq?>p5{gb0N@PqM~@4fA(XMJzY;YuL7u*#al2<LDI6*E%lmwbS|JMIEYdLJn0XOcC{8`V_3^YvYIkLCb6?n8b5@)x6gw#4_Ch>&OGeJdV{uc5H^8Gk=`^kZ7-Ze&4RN&~Y2RTQu{Ah4Dno|Mi<&^LN<^&bT;&!dof!y8RM7!T~OJ3c=z`j5_vK7eub->dk2@;|Iy(h$}A!y}5ZPeexk!O=fo<VF`87;DPE=m9m!r@g>@w1GZ5sR*Z{RfOx1VKt;C-*;7O@U`6Vk^`vDwA&7D9sax>;ei9Z_**a%qzR*2t*dFh3gXq}YJJFeYX#-Jo(6of$<41y0iSBGc`l#jz~A)H6MX*=dun9`0P&lpe}tOAj&PzL&1(!znJDN<XsM}Z%JY+iC(H=|RioFDOl3iu>RyS?-r8UCf`iWlAZI2LypVteS0ydK1(DGjGS3{NmY&k-PR=x0fZ@8HJe2_uJ+Tj7!yMDA6QvQr5JCL7)n-8=!S}Zm|7&=0ub44J+J>4qk>npov>*duZ>DDejv6}|i_746&e)S<5Mv*$`~@%#gnc_k4gGP5;9tAwdYO_=+dE!2tzf8kgB6!f;0<7oA6n_?!#TJg?9no1u{$7OMD<|s*GlanMS9mb6prs7Ck!jb;Dq%V{i(NpF_YRFIkg^-t3OzhC$xOkv!LlsPrGT;mJ~vm6EFvBxDRA0yw3s7ZyxYtTj{}4^2@<0EuHtN9=IP8_?Ks^j1}R3RSx-R`>rBV^Tmy0L%Dm`_i=TE*7`+l|J{Oftv>R#)_e|AW13s5)gnV<^OE0!{-$v)v|@Zci~>pnYLU-QaB9x%P41rbUc!2(zkO0mYyCG4R05jbfIh3w4d*FKI_yUXeNU)p^L_=b@4Upck$)2=+%&u{xqn01e>#Ty<*lB**S|&enM0NQAvpttRcoZ3oVyMF(T&mJyf{l>#`@b2PWy8iA7`LG3=4~JweI(FRUHY(J3jbT9qe7s-c`YBK;G5C>PW&fR1c^>zH74k^Kq;RvLV6KG(}Ul3j;KA8*dF__*<S84h-zqR6X4Fg+v46Cq463GOZt*IX!ZXnETC;Skwv_9!bPcE>_a&7Vde>ko$H>MRRI(xO)Ed`>kXHCS$+fDpT~#D}?I)ADpND7+L)8UW9jX!pkX580!m)-s>-<PY@rc;@v-u@CB_R_AA^pXu~UyK0DF>i%?8kl8=`uI6pa7|61a27&BEb)l$`eGU{!~{^Pi}4U&H{@VoN%=h%K-b@~4(4j}Y-e`4?%=E4%HUj;YN^&;jZ{L`!NmDy9epwIB)A8MPXHy@CG7GdZ<AaDS|!<%WzEMVqJ>j-%3<;oG`R&X@->SMeMJN~Ps{C}U%^%n$z_qUh~J|~2Z{>Blzjcz2lQv>oiv<y5l;$9<hR|^jZE#@}FE+oGOuKm*)`=lHta$op`K+Ae{2VfSxLPl?Ui)?EDu0}>nyOR7<(~<f?dE*F%t=Z2DDmYS^X)ODMV%WdbgN?~VE327IVCHSD)dfLA$HPJan209V^f%B*FR3xMS_(UDr~T2Kk?+O#`ffi9_ts&Vk)Rif0~PxyN4RalKQ2U281BARso|<`jXq6>NgrP;=eX^{YefQDwFC%w?iU2jRCuu0gzN-?g~jJAtkUNgcJ0uDGu^3#XQ_bYR7|&6a?a{A6>lX^us^JTcr($9h2ukFTf6V&zu&&|;qEIFdguMm?qpG<!)G@Ge4;t&{frg?ik*W<=iuFeZ>An}jkVvu8&$tVAbLCQVa#xY5cD_w{(GG84_#d?g%JDbMe1J--Z=74f*!}O{PxY`zLX8T_XEOrJRJE)dS!FFaz+dDW52gK4-4_ET8rJv+CI=(SJ3bqw3ZO+=e=*GaKGrkffvm<4ZvWu|A`k4+r5nQDHbm<wWg25OZ=K(cpe@z{M`{IAWrZsh_?F$9b-+`>J=m+DJhJmKqOjIw_0V6R-CA-(oc@+KTl46etOFBQG{-1qkeZT>e1F>s@^h7dexBD*PwC@#T@tJLMBS(#BZiFRO#@i4D5ws07%|vqiHj}0t`%A*ZaGrpw+qPg^F`Vf|X5=GE9}f*RdJkX)76dDQ=OM<gGpnXjMs20rEN~U_eOod-bSRrvg+IET1z#)M|BL=?FbnzM1NR?)<<knyg4P33P)NU_gu(f<S3oZja&<8So<g&FD72FJO6G1_*ff-M3c{@86~`9%3Nu41xTo2PTc$?O(+7?_>K<_mA$VJcH3!hvZ!h2?6~y9xyY0_;~3Sg#2+#ZM<K^t{>0szT6{Zh-u$Un_Dm|>QA?Q8smA+PcHGeoq{v&(|vZB??Vrrn+14p$3vK&A|JWkLG&nfes_7&Z|>%MxuHT!;nSK5`0;|v)8Ts;Wd5(Oee?Y5Yu|49r`PM=9#78&`6m~cXj>OrIpsYhKt8|B<aBvnXL1ugt>0$=wFH~diGN9PK=SM65bkn77>1s=^UA+Sraq4GLKu!)R@L!73t*@+|LmOl3%?`!h%SvO9QyrPzh>&^o;0m($imKu;P{lQjT~X*20{P->)lX>^n*y;*W>*q7oS#@zK;Djw#1CLW<0mX;>L5=pCO|&$A?=?f58bagwlO>SkU-^R*$^R=cF`{Q>)Pb^ajKCw-*{O<oIifJ+eFZseagX{9DKvK0ZOg?DJ<Bd~$W&XGm*h(!V6gW5egA`6r-n?KR1`A2l#q!P~np1|I;wRnFd)?IxD+XfCbLj~$BpxsdzG2E8s9aJK=Hp+xs@mF2z`<;uc~tE1JWYo3i(=6kP`Hk9q^rMX&}yrFtmD}@qC?SzB@Agq&*+<@KAhDfl|iDjnRy+1IP1y0bd>KY886;9u;+kqi1Ezt&e@1k%Gp(Qk0_gZT$i}8AI9yAZkT&vEyqx;POGIjr|RU5B#H|{=fr<R;@8Y{##H<B@A2n?|PB3E#$X9g%8jL8C>7xV)eFP^M+DUtCU)MFVnZ}Yp>;K33`M$m(Koe_-W+X=tphTD-2LmjquW&+Go(dypeVT`wz>CQ-1rj6X8XOTWq-@qz6+F00aRKBpr`+XhOTrUjzA?S_+B%kJ7Fh=We)Au(c4#9j>#2TcJqOQN!T{***G{Sci`aZ8^^cfw$@@hXr^p@86HMWkAuHMaqx)H#oZ!kUm30hiwpv&XNkr!+56LkIzsn<sDApZw?NKjq<0x@1t{vL848@@1#;jGwSyB{}Nxirk)`5zy5>MW)T#KCw55DJ2ROzr#a2K?KMBzmsZEEtY{kjgt~cg3W!$9sJr`Q!i!aA*$j7>@Go)p^!(wm;tAB1~&#!J1#L&(rZC7JE3`khq_CAnN1(6%E`sQ4kTgmW4r#OQ3t#kae|Y4m~xazkZMD{boA7<zKB3=<vEKAH$qm;w`8B173drMO%1sv;+bg5*FZ1Z-?4oNtMLF)bh9c$skxeC5X@jY4^gxS-}Ld3eS9q%xtaRYJV;8K0`_?k5!;%Q-IRdj4Ql^37U9#ofL$8KY3<MtdKV^T??~;78Sq2zrIqh5WQ5j3y*<demATf(qGn610q{$cT)NlFWCKcseUWlZlyXUT&wH!_-`NYr#&!_`|$>cC))#|`-^|^_hCRUczf@E{qrz7KB>G8NV~NPG`U~2`M5Omer>0I_2=a!-Sy8dLOuO&E<$}p0WL7|bVz=G7b^2$*#G}R)c=oMh^jGxR{!!$pugQV-EZrEj}}z!nY1v})O?nAe_S*6$oPJCtM^S1Kfl!bCC&B}_18biqDv7)5!&X<<8q~2W%S28s_&*(|Ni|q8u@uqnPz-$=HbQO{4P`U^S{?Fu)>VIU+ZbO#Z%k&dwXK>ykqosG1&`C{hL4M@EG{z4?1Y$e)-MHeE;(M%l|*UtMc7tbeh5X^-b`POWywcz&^jcdmi@C!A4D=nw-C?rFw?d|95j&&!aF5L-+m)Mk*G%R>yQd14XFl7+9!4C-v{2{1rQK8&Y7n38Xe@;x_TibMhPwGbi$PRI_1&0)*BQ0~GG#!LmzJ5U40-QGGkBkmn!1e}zuBs>C-b?;@Lud<3xW^YT2T8P7aWC<qI<+Ow!U7O$>7!4~$I9{1{aT%X17TiFc2xW4p!#qC)e=770$$|3U{(}AUnF)tgWT8@&v8LE<noP}Or2a(@b_|+B|_?HRfH7eM(64xIUv|bRkeimC=)Vcn+*0n^pPeu&d#WT3y)DlJlrh~S;v`F1wQmEhxQ}eaO+NHj#UfT+6w+Tka;lZd{L0Fq+8hO<rJ7Mh<tB_ybK8ER}cv?@)roOtMx}A-$nA1)ahU^2fXkLX7cif<8jd{ez!zlsT6`Nh5#W20AW-hg18AoQE!8e{Zg|Fv&8{ph1kfNZbZP%>7<Jd=i0-zvnm&uTQRMXD|ErA={X|g>78JQ&d0wQxTN40ge+&BgweHQ9^iwt<oCrDqF=NF!$q4)H=i|D%g^cuY;nZ;>+j*F7GO((8qE04r!HljoT+ZEoT^0gR}1h7%&nl-TFm5#1-Fd5%zdbz9JO=3J{5TmDmj8ne>jeV5Ph2JjVc2WMj4_SE^1=qx1hq(~^+>lt1fd5zDgiGS*xtQ9{R?r2FOE1L!Cgk(YKDb-SYq&eRK6M3-MO(23Tt&700c%Q?`v')).decode("utf-8")
_SBT_NS = {"__name__": "_score_bank_tuned_branch"}
exec(compile(_SBT_SOURCE, "<score_bank_tuned_branch>", "exec"), _SBT_NS)
_SBT_AGENT = _SBT_NS["agent"]
_SBT_TRIGGER = 408
_SBT_CEILING = 250
_sbt_host_agent = agent


def agent(obs, config=None):
    action = _sbt_host_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        farms = obs.get("farms") or []
        seat = int(obs.get("player", 0) or 0)
        if step < _SBT_TRIGGER or len(farms) < 2:
            return action
        lead = float(farms[seat].get("money", 0) or 0) - float(farms[1-seat].get("money", 0) or 0)
        if lead > _SBT_CEILING:
            return action
        return _SBT_AGENT(obs, config)
    except Exception:
        return action


# Weed recovery is deliberately limited to workers whose remaining field tape
# for the day is entirely PASS. Hired hands reset at day end, so their position
# after the cleanup cannot desynchronise tomorrow's route.
_weed_host_agent = agent


def _weed_trace_op(step, actor):
    if step < 0 or step >= len(_TRACE):
        return ["PASS"]
    row = _TRACE[step]
    if actor == 0:
        return row.get("farmer") or ["PASS"]
    hands = row.get("hands") or []
    return hands[actor - 1] if actor - 1 < len(hands) else ["PASS"]


def _weed_tail_is_free(step, actor):
    end = min(len(_TRACE), ((step // 24) + 1) * 24)
    for future in range(step, end):
        op = _weed_trace_op(future, actor)
        if not isinstance(op, list) or not op or op[0] != "PASS":
            return False
    return True


def _weed_step(position, target):
    x, y = position
    tx, ty = target
    if tx < x:
        return ["WEST"]
    if tx > x:
        return ["EAST"]
    if ty < y:
        return ["NORTH"]
    if ty > y:
        return ["SOUTH"]
    return ["DIG"]


def _weed_use_idle_tail(obs, action):
    step = int(obs.get("step", 0) or 0)
    if step >= 717:
        return action
    seat = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [{}])[seat]
    tiles = farm.get("tiles") or []
    weeds = [
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and tile.get("kind") == "WEED"
    ]
    if not weeds:
        return action

    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    inventories = list((obs.get("private") or {}).get("inventories") or [])
    inventories.extend({} for _ in range(len(positions) - len(inventories)))
    ops = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    ops.extend([["PASS"]] * (len(positions) - len(ops)))
    turns_left = ((step // 24) + 1) * 24 - step
    claimed = set()

    for actor, (raw_position, inventory) in enumerate(zip(positions, inventories)):
        current = ops[actor] if isinstance(ops[actor], list) and ops[actor] else ["PASS"]
        if current[0] != "PASS" or not _weed_tail_is_free(step, actor):
            continue
        if sum(max(0, int(v or 0)) for v in (inventory or {}).values()) > 0:
            continue
        position = tuple(raw_position)
        choices = [target for target in weeds if target not in claimed]
        if not choices:
            break
        target = min(choices, key=lambda p: (abs(position[0]-p[0]) + abs(position[1]-p[1]), p[1], p[0]))
        distance = abs(position[0]-target[0]) + abs(position[1]-target[1])
        if distance + 1 > turns_left:
            continue
        claimed.add(target)
        ops[actor] = _weed_step(position, target)

    action["farmer"] = ops[0]
    action["hands"] = ops[1:]
    return action


def agent(obs, config=None):
    action = _weed_host_agent(obs, config)
    try:
        return _weed_use_idle_tail(obs, action)
    except Exception:
        return action


# Minimum last productive-use step seen for each tile across eight independent
# weed-free C89 route simulations. A weed is worth clearing only while the
# underlying route still has a later planting/build event for that square.
_WEED_LAST_PLANNED_USE = {
    (0,0):599,(1,0):618,(2,0):621,(3,0):514,(4,0):587,(5,0):574,(6,0):642,(7,0):564,(8,0):569,(9,0):571,
    (0,1):594,(1,1):589,(2,1):643,(3,1):593,(4,1):586,(5,1):560,(6,1):620,(7,1):563,(8,1):568,(9,1):575,
    (0,2):573,(1,2):568,(2,2):563,(3,2):560,(4,2):14,(5,2):181,(6,2):566,(7,2):571,(8,2):637,(9,2):574,
    (0,3):612,(1,3):613,(2,3):608,(3,3):20,(4,3):9,(5,3):176,(6,3):198,(7,3):519,(8,3):610,(9,3):615,
    (0,4):618,(1,4):632,(2,4):129,(3,4):5,(4,4):4,(5,4):165,(6,4):165,(7,4):204,(8,4):594,(9,4):599,
    (0,5):617,(1,5):588,(2,5):583,(3,5):586,(4,5):581,
    (0,6):610,(1,6):613,(2,6):608,(3,6):591,(4,6):630,
    (0,7):636,(1,7):635,(2,7):634,(3,7):632,(4,7):635,
    (0,8):254,(1,8):257,(2,8):639,(3,8):637,(4,8):640,
    (0,9):263,(1,9):260,(2,9):257,(3,9):260,(4,9):259,
}

# C90 retained the underlying C89 entry point here. Calling it directly bypasses
# C90's broader cleanup wrapper, letting this stricter policy replace it.
_weed_guarded_host_agent = _weed_host_agent


def _weed_use_guarded(obs, action):
    step = int(obs.get("step", 0) or 0)
    if step >= 717:
        return action
    seat = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [{}])[seat]
    tiles = farm.get("tiles") or []
    weeds = [
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if (isinstance(tile, dict) and tile.get("kind") == "WEED"
            and _WEED_LAST_PLANNED_USE.get((x, y), -1) > step)
    ]
    if not weeds:
        return action

    # Preserve C90's worker eligibility: either the permanent farmer or a hired
    # hand may dig when the remainder of that worker's day is genuinely idle.
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    inventories = list((obs.get("private") or {}).get("inventories") or [])
    inventories.extend({} for _ in range(len(positions) - len(inventories)))
    ops = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    ops.extend([["PASS"]] * (len(positions) - len(ops)))
    turns_left = ((step // 24) + 1) * 24 - step
    claimed = set()

    for actor in range(len(positions)):
        current = ops[actor] if isinstance(ops[actor], list) and ops[actor] else ["PASS"]
        if current[0] != "PASS" or not _weed_tail_is_free(step, actor):
            continue
        inventory = inventories[actor]
        if sum(max(0, int(v or 0)) for v in (inventory or {}).values()) > 0:
            continue
        position = tuple(positions[actor])
        choices = [target for target in weeds if target not in claimed]
        if not choices:
            break
        target = min(choices, key=lambda p: (abs(position[0]-p[0]) + abs(position[1]-p[1]), p[1], p[0]))
        distance = abs(position[0]-target[0]) + abs(position[1]-target[1])
        if distance + 1 > turns_left:
            continue
        claimed.add(target)
        ops[actor] = _weed_step(position, target)

    action["farmer"] = ops[0]
    action["hands"] = ops[1:]
    return action


def agent(obs, config=None):
    action = _weed_guarded_host_agent(obs, config)
    try:
        return _weed_use_guarded(obs, action)
    except Exception:
        return action


# C91 only spends genuinely idle labor on ordinary cleanup. C92 preserves that
# rule, but treats a weed underneath the route's *current* productive operation
# as a route failure: DIG now, delay this actor's tape by one turn, and consume
# the next PASS to rejoin the original schedule. This retains every intervening
# action and never moves a different worker off route.
_weed_repair_host_agent = agent
_WEED_BLOCKED_OPS = {"BUILD_PASTURE", "BUILD_COOP", "PLANT", "PLACE"}
_weed_repair_pending = {}
_weed_repair_last_step = -1
_weed_repair_day = -1


def _weed_tile_at(tiles, position):
    try:
        x, y = int(position[0]), int(position[1])
        tile = tiles[y][x]
        return isinstance(tile, dict) and tile.get("kind") == "WEED"
    except (IndexError, TypeError, ValueError):
        return False


def _weed_repair_productive_route(obs, action):
    global _weed_repair_pending, _weed_repair_last_step, _weed_repair_day
    step = int(obs.get("step", 0) or 0)
    day = int(obs.get("day", step // 24) or 0)
    if step == 0 or step <= _weed_repair_last_step or day != _weed_repair_day:
        _weed_repair_pending = {}
    _weed_repair_last_step = step
    _weed_repair_day = day
    if step >= 717:
        return action

    seat = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [{}])[seat]
    tiles = farm.get("tiles") or []
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    ops = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    original_len = len(ops)
    ops.extend([["PASS"]] * max(0, len(positions) - len(ops)))

    for actor, position in enumerate(positions):
        scheduled = ops[actor] if isinstance(ops[actor], list) and ops[actor] else ["PASS"]
        pending = _weed_repair_pending.get(actor)
        if pending:
            ops[actor] = pending.pop(0)
            if scheduled[0] != "PASS":
                pending.append(scheduled)
            if pending:
                _weed_repair_pending[actor] = pending
            else:
                _weed_repair_pending.pop(actor, None)
            continue

        if scheduled[0] in _WEED_BLOCKED_OPS and _weed_tile_at(tiles, position):
            ops[actor] = ["DIG"]
            _weed_repair_pending[actor] = [scheduled]

    # Preserve any trace actions for not-yet-present hands exactly as C91 did.
    keep = max(original_len, len(positions))
    action["farmer"] = ops[0]
    action["hands"] = ops[1:keep]
    return action


def agent(obs, config=None):
    action = _weed_repair_host_agent(obs, config)
    try:
        return _weed_repair_productive_route(obs, action)
    except Exception:
        return action


# kaggle-environments loads a submitted .py file by selecting the last newly
# bound callable in the module namespace, not necessarily the function named
# ``agent``.  The helper immediately above used to be selected by the file
# runner and interpreted ``config`` as an action, resulting in 720 PASS turns.
# Give the real entrypoint a fresh, final binding so callable and file-path
# execution select the same policy.
def kaggle_submission_agent(obs, config=None):
    return agent(obs, config)


# Live-counter experiment: opening feed protection plus debt-tracked one-turn
# sale splitting. The field and weed-repair policy remain C92.
_c94_host_agent = agent
_C94_OPENING = "feed5"
_C94_SPLIT_ITEMS = ('FERTILIZER',)
_C94_SPLIT_CAPS = {'FERTILIZER': 10}
_C94_SPLIT_START = 120
_C94_SPLIT_STOP = 715
_C94_SPLIT_HORIZON = 1
_C94_CLONE_THRESHOLD = 0
_C94_DEBT = {0: {}, 1: {}}
_C94_LAST = {0: -1, 1: -1}


def _c94_reset(obs, step):
    seat = 1 if int(obs.get("player", 0) or 0) == 1 else 0
    if step == 0 or step <= _C94_LAST[seat]:
        _C94_DEBT[seat] = {}
    _C94_LAST[seat] = step
    return seat


def _c94_opening(action, step):
    market = [list(order) for order in (action.get("market") or [])]
    if step == 0 and _C94_OPENING in {"feed5", "feed6"}:
        wanted = 5 if _C94_OPENING == "feed5" else 6
        rest = [
            order for order in market
            if not (len(order) >= 3 and order[0] == "BUY_PRODUCT" and order[1] == "WHEAT")
        ]
        action["market"] = [["BUY_PRODUCT", "WHEAT", wanted], *rest][:10]
    elif step == 0 and _C94_OPENING in {"bridge14", "bridge19"}:
        wanted = 14 if _C94_OPENING == "bridge14" else 19
        # Buy feed first and defer the cow. Sheep, seed and labor orders stay in
        # their C92 order so the field tape remains aligned.
        rest = [
            order for order in market
            if not (
                (len(order) >= 3 and order[0] == "BUY_PRODUCT" and order[1] == "WHEAT")
                or (len(order) >= 3 and order[0] == "BUY_ANIMAL" and order[1] == "COW")
            )
        ]
        action["market"] = [["BUY_PRODUCT", "WHEAT", wanted], *rest][:10]
    elif step == 1 and _C94_OPENING in {"bridge14", "bridge19"}:
        surplus = 9 if _C94_OPENING == "bridge14" else 14
        action["market"] = [["SELL", "WHEAT", surplus], ["BUY_ANIMAL", "COW", 1], *market][:10]
    return action


def _c94_repay(action, debt):
    if not debt:
        return action
    out = []
    for raw in action.get("market") or []:
        order = list(raw)
        if len(order) >= 3 and order[0] == "SELL" and debt.get(order[1], 0) > 0:
            item = order[1]
            quantity = max(0, int(order[2] or 0))
            reduction = min(quantity, debt[item])
            quantity -= reduction
            debt[item] -= reduction
            if quantity <= 0:
                continue
            order[2] = quantity
        out.append(order)
    action["market"] = out
    return action


def _c94_split(action, obs, step, debt_schedule):
    future_step = step + _C94_SPLIT_HORIZON
    if (
        not _C94_SPLIT_ITEMS
        or step < _C94_SPLIT_START
        or step >= _C94_SPLIT_STOP
        or future_step >= len(_TRACE)
        or (_C94_CLONE_THRESHOLD > 0 and _CLONE_CONFIDENCE < _C94_CLONE_THRESHOLD)
    ):
        return action
    future = {}
    for order in _TRACE[future_step].get("market") or []:
        if len(order) >= 3 and order[0] == "SELL" and order[1] in _C94_SPLIT_ITEMS:
            future[order[1]] = future.get(order[1], 0) + max(0, int(order[2] or 0))
    if not future:
        return action
    market = list(action.get("market") or [])
    if len(market) >= 10:
        return action
    committed = {}
    for order in market:
        if len(order) >= 3 and order[0] == "SELL":
            committed[order[1]] = committed.get(order[1], 0) + max(0, int(order[2] or 0))
    shed = (obs.get("private") or {}).get("shed") or {}
    for item in _C94_SPLIT_ITEMS:
        if len(market) >= 10:
            break
        planned = future.get(item, 0)
        cap = int(_C94_SPLIT_CAPS.get(item, planned) or planned)
        available = max(0, int(shed.get(item, 0) or 0) - committed.get(item, 0))
        quantity = min(planned, cap, available)
        if quantity <= 0:
            continue
        market.append(["SELL", item, quantity])
        due = debt_schedule.setdefault(future_step, {})
        due[item] = due.get(item, 0) + quantity
    action["market"] = market
    return action


def agent(obs, config=None):
    action = _c94_host_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        seat = _c94_reset(obs, step)
        debt_schedule = _C94_DEBT[seat]
        due = debt_schedule.pop(step, {})
        action = _c94_repay(action, due)
        if due:
            carry = debt_schedule.setdefault(step + 1, {})
            for item, quantity in due.items():
                if quantity > 0:
                    carry[item] = carry.get(item, 0) + quantity
        action = _c94_opening(action, step)
        return _c94_split(action, obs, step, debt_schedule)
    except Exception:
        return action


def c94_submission_agent(obs, config=None):
    return agent(obs, config)


# ---------------------------------------------------------------------------
# v24 layer on the C94 base.
#
# 1. Clone escalation: the base front-runs a detected mirror by one turn.  A
#    C94 copy does the same, which ties the exchange.  At high clone
#    confidence we extend our horizon to two turns, landing one step before
#    the copy's own front-run.
# 2. Boatlee-family layer: detect opponents replaying the public Boatlee V16
#    route (signature tracks from self-play) and sell our stock of a premium
#    line just before their scheduled batches, their adaptive 713 wool dump,
#    and their staged 713-718 terminal liquidation.
# ---------------------------------------------------------------------------
_V24_CLONE_ESCALATE_AT = 4   # confidence (max 8) needed for horizon 2
_V24_BOAT_TRACKS = json.loads(zlib.decompress(base64.b85decode(
    "c-rmV?T+j?k{;k&S?upMz=)to%C}-H48tG5!p4lTwqY2C@7+_UN~||XNhyj!r7|ahGmY-*nm+X$DkUlyAOH6s|IdH;*T4Mxzy9SP|Ls5gyZ`%-|NF21`d|O^zy6QE{e%0bfB47$^_Tzl*Z=rmzy68-_D}!)um9s;{^!5^^)Fxl{O|lf{lnjW{TmwjzkmMQZ~7nq`oI42KmYuWfBS*<etmuO|M{2y{NMi5&Nu(_|NEzZK%+lmoc{dv`)?-r$9J%O|B`pL$)8{Toouo&c;Q`bqwzNS1LG@g-zvV!M%UPA`E|rbMmG1BHdooi)<!KhdMz7o*ksMd);7M_#+TUS0-Lnh#MDObZ6j^taW-zT@%?Rn!{*m)-p<BPvB`xtcbQFEY;u3w)MA@P+T{Ig1UC8D&e)2*`M%A+qRn4uqmRwNHnrHMP226_lmm=(JWlz}LjU(5ly?=%NB9mxvDrU=gdgG9&!PN12<7dC{v-SdKf;gjBm4+I!jJGH{0Kk7PsDWB$gP>3@8}yBHNBZn-qtrLQgbuk+udK}{eAc#bZ_Y6<&$?aUoi3!WRZV-*ZHD_kHN=p>ytbBl7){JpDf8TAKyj3*}~_*=RUqGedJ7m{sa5~Kfn+01N?ggzIH71AX3hixxW<;E8YDY^Na(&_u&bY^UJ&P*f!kzbe^p7M&CK<xjgqyJb@_Fjd(PMC*yhiL>|8x&qLi3+Xk9$!V_KMJensLU!0;V{pp=}47}XP<9&DpXPa&$FEsJki0AIf6KkHk70+An__n;sns={@Gkka--iLQ%-tD5D`$!tGhF3;ApT;YGy)92hMmwL$6UaW3cjeK@Xy+4nvc`L#J16UCCyfjTK7mKNv+j*}(SqlI$AfuO6HknIauu&_^}G>}b(f}h;}JwVX=Et=nLJtIoOj_(Mt9C4TTpItYat_^yNVaCzjI#6Yg;{M%JaHc>eG4gt#!#-M}u{~Mdx2l*K}VAAKgdy!n)TEbG~<!GrU?#=hJoB_+~nRw7GZH@siK>#ybBlIt<_PQ*~~Dj&=O+8l8WJj-I3o7wX(qI=)utU{cLH>Ese!Y|$mtG*!`4hTc+_|N5>v9<Q4|I#XRful(pbb>XA4*3nz*+`H@iN7t>3X1d!&H9L)b^RVXAc-JIvKA$He1Dl<^KZz0D$(#JfJQ^9=?B$u{rn>v_!f9TSo9ae}knX~}!?S(1<uRn`@P{{=rxM6QzQgo|-rdMz=MQhA8aP_;@Xzb5cydFYx8N0FKpNR5;t4!o@%V<kbnum3_INxvae4&L@AD>|2tg2<@NbBlmaF_WxVaC9H_ov9mhXa_uEZscOAm379DY{ES{Fy_<WgPEf{4rS`3gFB<azLvAm^%*&MD&&WgX@0i+<kA^&R;Onj>ezp0{)P<xc7KVSZz=`t4lu$AuZGbf!xEb}s(o;>y)np1$FluXD+oi#A+zxr@48IWZGm0djL%iefih<Zc1W7v(V6{IDPt0t_9n?~O>TVD0a7TQGvB$Y2;>3gaU%%u<Ak&~}&rOf)P)Wj4PkEH6uf#1w0o9D!lwC)`OIVFWOzVY0xS*`??;?B^jhOy;*`31r?(Ha(ExF%?ZlGXLiasb##xO8R8eg)+WCmVZ(TM`Y{_WdVu`=H+&QpEIL1J0#P$#(r78=g$kpFZX}9JlL*TGkpi?m-%I>3Rym4j0Up!JQ;1sXxX@0$U-4=SI8WE&QRuhWWVoL2Wj&-8b6oD^oq1(NxNOJu^SrJp}{KN`1&|s1szXL%(){@mfu&ZufINym#s<>V&x~}oCS^`+~Xn6O0S9&2sRM}=@93J;pj0gSl|TC569!CJsgk5i5+fkv*}mVXko*nQCnN<!s#vMX`Dbbh++Sqqd_;orL(vqhDTMX%b!aOx&@BbaQQUq0vxa2PgL+^K8tfYNcoKu2rHZ5R_-TZ$EL$4owlHD-rBadaJx9XS+eW9Dg)$W55~<G;uyBdt2jBAN7;#+t#DrBW;hXk8ZHjS@gN+#LpVPgC(Dh~07s3u$sCshMR{nZ8IBuq;gxXGh)eIha{irH?%-$cei2Lq=%3Hz4O1rXU=s~njcmS>O{&yMOaq-D-7uU^oiwp=w@n}w6m2=K`NB4wi|eb%AHSk49J4*;K1ru-__$+8TJUgv%G=xGbvCuX<a`j?ozD;|8ox3vY8q|O+%ss>LCdjMSLK-pi1=Mdi?%ebXbdSuU1=zNuRH!MjetgwB#Jb5HEphG{wyu&T-a6G{3P0RmgY3gFGmCgjbD?NIhcTm(Mq?Z@6pTBa@HtAtkPdkQzsuoXj0Mm8PTqL)4HB(r_<R!v=8k=GornIbh3oXku{7j5u7|oBX4Wl`}!?Kq56S~p+iO9rTY3^MWP`&%9X#4XZ+~myNY;CgkPs+tBga3{7;$29YwSzitu$5F?`)wzD9@Bq9RQ<K=Yqkl(S$Hq#n9MBHy^9cc(?XCd%=~39=9fg2aXBCvT?n9fgY6o24jjh<FjrS|pD}2iAy-G{`GN`6ap#{WLP{6#1g!yh}8-hy-$eXbI_X|5Y~?<-O-c#i^x(+?}u{@{7oWi2Bzk=zdwfps51oB)S@u^xUHZpaV-(OclNeG-*%{Bf34%_xno===^Pg4uf(_uzV`<Tl8)MN`|1kFUw875R^9vw0s5o66IEyv<FIUpfm#H!4dVjGFAlT2BzDa)bQt1-U2#*Q*e(!9zgln3#)*{3N#<;3V0Y4pg%|f!uN)}KO#u!H~=EoCfaG3WJF5Umd^o+ACS^_0YMXqdPt$0Bo9dQGf4?Hp~p%70Ert(JeoB3kc3Q0?#K)5bE0`$QaUG{$A!F}>LNEfmiG#*uvP(%d6k%lC@;f`u)8awdK1LGrp>`L_hhB2>12LOoZzT<+8ju8XBKa;NV8lEi@&>&HL>J0s|fP#vz+d7xHf?1o~&8t08Q|gxXKb^mbif|+Gb&g!?lSlTiFOA-|?YGs}+v5i#x?~W-MuCB^wrIM#?s80+zs0vH5CEW-Ni&%M4}stoy8mK9)bmVq+FpEDXqCQ>2{M)N~OZWQo~lE9cem2FvMwamXTTmbYQ~ij}rm*wS!gK29skjbTlY39`i^9Z);RnvSuIZt!7)g|`w07DJXKJ!Ww$%jmNe7nUrq|4H}q^Hm)pCW4x;)?~(F2%H{d#myePy{!0T7B{lOF;;p$OFpcltoivY|2)>6V~5A2`W5WwaAvLGHI0a|-Gg?U_~FxCTLHwaufK%LFEhr9CUBGfx`#K=@h<Ln$ueA~j*Lb<c-A+D5YM|(KZ|w3MZwA%S)LX5W(A!CSg>e~#ba1x!zzMO4i57~M{gn|pJi4!{LT{2?Sk!DtWOtCu`D(qHmp>!1X#H?l$Sgn+tpfm74xTAIJhIOu>x!taTZFnUaers!b9+&y95_3(!b1E(T2r3<KDs17sKDzEO&_2d=ZKzi#3ZO;9IbqW~G~6gbc&fM5j7oJK1=WMU5;<mMo`PZjCip7oi)lTF&x}$iaRnRQ+*9vv?$n%vckgp42SA#&Sn5LN>SvPqM-z7H_cl)~gj;Slq^HzGaBnVM=Vd2)XSdY+Wsy%vj+7E5YUoS@V5a(=k@O6YKRuh`-X`@4tODv9ay-qN4+3TTL7>hA1y7!+gUciioY*UQ-tIEN{%J%mqa9!ZNC4SdI50GSQv#_GPrZuw5kc<}z1B-d<ehc4b&WIaU^6-)$y~(6<p&_+C)v;lSA~iN8fEDNfjQuOyqGGIOrNRZoy5D_MYqHk4s@80Vq)uOy35y*ooD2R@xqHvHZ=Tgg(Ds94AZ`Wn)KE>Jg?)$!Bk$XurkHFGsF8rN(i{r81rT%{kOOx{YC(@-yv9Swck$b5&4Pd};eE^EFT<45+cvNwo8meP46!zx&X>F&w9Pl5NdVGmmy`u)i(cY|T=cHxog>+wRE^uu!6SOH@_G$;22e;HUVbl!rA?squ&O|%b&S0F8stO7<L$0mWdhA}h`r6ulDEEK`tcxZTZ&Cb6U=HcfKYblMnC@?pMx@O})5GDYV;V`y`Ii1;9q&4OpBrS=mcZbOuOr8c4Ggy9bxvG0@?iqm{6mow1Yrq5+Bvw(Z3t`?2MmmsBRf9n+W@l*r_8Krc43nXo;3^^YB#dCgkrUz)T!A^m$3ZwU47}Z60*l))9tB&87@UV;n~SZEiVlu+_a^h*3Kjvz$6)RaU~(xeS;Erpr6}+XuML}@37ZeXUO(RWOQoL#k*`c@PH&MI*noSrc;gt_e%fQvd-1hsTX~Ol|HW`Q&3Dr<@v#W?OjRY<MYONfGcy`#np<e3vwlX?7-*;a(ypdH7U8R+Y2i!IME8CVYcv7c*p0Hd5j3|(;|-b{bU6RJRVMdKTWv7WMvE{Sr^pe+28NgHDGAP-`eg}ZvLW*qZ7NM<0ixV#Ll!_52VRa7)L?cT5el5Y?8ETwE?)6U+6}{*9y!}gbf_3}jCt&ei7_na%FWe^ksjMZV^_=@!x&&rAIA_J<kE8c91jaNFih^r-N_~}BP<Ps1sfPctBE3`vw-~$z!?jRb>&4b%vb4H`Ly~xj8Csv9}K%_AgrjO!Ty`Cv0`4satgKA$MXWk)`MXy>ELHz(*c;f685{t?}LR37WJiwSLv-_@6@(&c}?TDN_jl)`}$8mdyw-zP`;&e<KtP*r%;mxN~)M@k?a^DCW(1J`A>jNQDJ+3)nejhLHt@eU_P<IfDi_c>82)MO|tP-tGt{Vf~j@prgYvU+9cJy7hiQXtW7`1aAu7fzfALaQ{L;cj)~?7@v3Ro33Wd|hFR>5zoUspCR#JqZ5mfiY`H&V+G*?BW^#HcPtf;0(MP=wqIF!~%+Cj<IM3fUGNm<BfFf3c(wIGybX|KLCeq;zoJ(7qSepn;WUx+xCf{q4HB*u17oa5`nq<o)UDsZR$-yE$G&wL4B!~R`=)LQNZO%B4WbGo+HYxXEaN8u`TjPjn9vvjS^7cuwBDwul>S}|>p@$@Jht4_Yb)sU_A13#Z)YY)CkAyA63sTgi9JijK1)kk1xq{>dk#Y`SgoyPF%?j;SDcF<TBa+uGBiMG8R2>y0%G#0wBqSCjGQaSu&(aXmq#G30q}lSq^S38;^;_H_y;Hx%uPJPQCd<=$clg)txcEr-a@Ee`WcyJ*xmXrWWU>}66G)7j;5biSQnot&nIXSz8kfXY$kK8$)t@f9H7S`i?1CG}*W+eB3#-G+H7r-T;I-(+!+!qP55sKNA`3P^xBS7dpkQPN^VM`~Yzys2XRj47wtzVudPi7<<h-k4Q}@kd2bKUfHhJy$_2ui1DAEC&^cWY0jPeOu6*{O#9SKWjumJZ1gvkbsh93F@EPT&SJq?Rc(j1`TQeb>{j;W1@{hlxQPFR9znKcYs_GNh*_<;U}@%R6!6P6$=Ue;i&VLTq@I$`tj-i$ETy)iKgPZxD0`TDd;>VxsJ2snkpYnW)59}f#Aun5WV#qe%~rO~k8VCf%N{!>2<3ovR|bXz-F4p`5?&WB9@6yEp4rem;qbVrikoyXTVd)E!~_k*zsOaSJ0VeTHVcWSV>P}4@4;;VO9eB}EI|6Gx7czae@`|(5dZK6YwBUog>TAc_z=_GB8q%s5${4my5>E$VwuUJt(04LZ$d)Q3cvVOvwp_AqH<m8$apzertT;ay7X<>1d_Zne?S-cf^cv-s*3qLENVuf864`zuO%Wq`s1$coGh?DU03SiB0-z>Ia$?~%wVbNgLPe~;Avv`e_-$Wx+$KoLDyRtk4bdqLC#qyBPLL*u6Jd2^uGUS5PiZ$tfg*BIC$Vw}$)T7F053_E;v8qagRG4n&XA{(<Q8;r4qof`Nispnq<2kk#DA6eQ2sIBvVOi>wi*lP$RE@lzs|nHh1hYV4nz0RPGD8)|UU>OMxH2;;#|G?C0a4t83c4zOhDbfOQV}>48-<EcVm|#2%RPaLy1x1$Dn}3pqofCw9-(q=3V!Dh6c(cNp=OOLMsj(5jN+hFV=&4OLQNVq-vsqe9TLB?izfd&faW~{hR1y`RG&N;<u`u#qCKK7G8b)8lNl;h^~qSbTr@_MB5Cois0hncqw?WPF_U1jDb&-bpZr(@RH||>v4th+YF^A$G_4Z-%9QFsVG>wIg$<NjL%GMOsr5Pbwc|~_sC?DURn8@L<aD}5IVVi{Rg}l8sjcoh3`X$*l$fAcWk*f34JyA%#R?U47tVA9HMOpk!_25@&b!fb_lYJGZto)uTCg<**JBcxtujN145$9&ABXks9y`3-nZ9CaeJ0i>oHvW(W1?=jDGerRyi5EsQIClr%2$}en#n`kL#!YzO`+8!m@E{y$AopPwJC=@3llvwHLsJNohzNDS({R2n)KN80B@4Hz`1*!7!R>JOrlL`F|juJH4_<|JVx1r?>BK}^4gRii2^1Jx7*z#QWuFU5^IvLNZ96ek97VP@%4>)=W?DzI$f|H>6Rd#UW5gWR>>8l^EI$Yn)NXbc4WjlVyq|kW;b%ek89{BIUq&24;&|n*@egUr2I})^v%4A<aSB-ivo5m-q)Ql{rT>@7Ag<Jef_td6al=E$saCJe$b$>(=_*+4i01Hs`uY-d%Rtfw3>cLJ@uP-!&FRG<!U~2`FV=U#0@(^{&`z8Gtq{Lw2A7`%!Mf_lY4BM(B$XSCOK?!5Y#M8t34NgD@Ek{;rEE7DkS~+OOJIf?WAjV1KcZiNVG~KB&EkBT^l)@koXwMLnh}QiIEf^lT?IOycNl>kz|A9HL1Ai{pPnwzTxeWyh9QvE0VxHujnC}(}1=}#k1*m-oQZ;8Ig+Cgk1Grz{DjaadqMO`;Y`W6OvA84?1mWg7<kG$vlqa&yg5@ZIObWiWDGZ``hW*lr;B{NN37oAt#bN%nXW}^b>#HBTcQOsgvYdNEqh}STs_QREXm7&eby>-mvQ@5s;$p;#XXFTcq+Pu6C}EH?H0zi6#@0tdTIS4CmWmGuEGk_D&Mv$qnVUDP1HFspv=|xD;1OKPSBfN$thC<-+6deePD&#UGhT?jVV~CSeXVlAJb|q|`_fJh$l}i6#l02Y7u$%enUXv*h%ZX-5iOBoF5<9(wjkmGF|A{W?gyw<Jw!9%dH_Z{J?evn~o03li^>LK{iugQVMq`}7ldMM|5|=b!75wyKeCk@VN<`@NVS`o8|fb3%UiL4}r?$g-RC*NmFRq7F_&=G~+}BNX?e;#vndoR5q*McPgJ)1j9Yl;3KQzMy7H6K$AiZGs0`nSOh%`|o_KdE*tBn|em>lZuopr%PbANeq*RkC489=kubX_BXVM1bU9iW;E%TC|ZiJ#dbaBnDwxMS`<x0zk98;h`foYo^DKQBGIDyq!faf$3&qJg?<rfk!TU7j}@Yy6aB_DlC7&wa*)PM#3mw-BKKG{*Wd3>h(xC?)}q{$G_8qvN2J=OJ{F0JGoKd~iI@rEtwrS#ie?bemMCtDWL4zNME;TJ`@cR{B5D)GLd2V*U?uv#oF*MW&lBEfNE(}UTsp1p?oy*@!jOxxNc3U!_a`NfQo#~tobNN;LnL~{T+)qwvEyhV%Jp?w6s$y);67?5l1h{wiQ<-s=T#AHioA&kD;_+CjUS14V~yZ$d`zSoy%>w63Wd!Ot=tk#R-&$pj&*!;hJfrUh%Nx(_?wfUsp|X36$nRvW3{|J$nSw}7vMYZ6t{Orzd<(NC>puZfxVYe`L*tUSP_fKA-7fusAR4AU;cX0ug6rCicPxot3*$Ckd2rh>AVS3)jUu|8!FN&GFN#jUO!H%q{<MjRXOnI;2oHTsMtnTRNREMAm6IWEdfhYmB-_G1J!<@FG5}ANLBfAWur>EKOU;$nkpPtr9-NK4fM@a^O}l4MQti-RLwRjsZ?n#FdHGDL=dDkR!#2U%dk5b_^VZ->s_%TEJAjisfx^0cw#oMwZ|(0O9U@?)+)wK5gV1;P?1(SSWjz}H&aoist2S*UG0WNi>9i{OywZA4^{YdPI|s_g50cIt8&0UZL3IE?|p~b2B~)6{QFcG%#9F?IjrJFmFnkepvp5(_EiK8E50K&V^paJ<&UA}i%{uM<f#!guc17kST~;RMY(69(n*xGp@M@t=2walo_78$JN=Z7-!Vuy%J#g9-+Pf(JN{ujE$Df;tI2=2Ajw*MFdHzKhV7$b4tLy;#B0GpB<1rV>>-y6C)k)2`$e=CLPL>kh{QxB^=WcEUFwVNb|;v`JHZ1i?=S>9t7GO2Z$60Qp$G9iT*Q@#DpA4=v_j<DL?H|j#Y)6lROF4!*blFBjZ%G;juOc+5pAwfX!{&-{t?dK8Dfjb>+x}BA~F+A5U7ZHg66)+frx9-bb5`%TvTLc=Fkg4Qi3#yrnWl+yB?A3io&*t;VtDSc-tu|!(+XooH-V%pdX5Io&`ZbcU=^UtLTv^*@*a<D1k^|YQ~JA=t2}5MPaOnw?({&{JtnPismB!>ZFL4cY+*eiEwpIAete$v=-5xh>nP&E5c!BqNGK+?lR{qIS?i2MplaEHW92*m&mP&xKTuFPgv;nacqr9r<B=%W(^7zh%_iJAioE4hd`{uMdv|b8-$IIS3zM1#Kl3`BhYjWNOnQf4#+oxR2X>^bi06FvvV%ChO|5jZWz%UhkNGS-#e+o#!v5c61#sq_P14)oViLM_E?X{RSo-~*~6rh8Vi*)u2rnxy#CDS>qG@8FsM-;x+Agf@MnTrc|rcupVtJ%8z=!30V)`Ms^Ul#Z48}eKsi9g4OHu6*%_gV$=CsQVp23kf;IAa7}m0zH(4nuQvL>@7(QQ7qeP=-BUC6*-T>vHMsy1$EvUxJ@AplF_qT;@rU-*989F9KU5dzHBD;kmOH+Ur@AWX;!o-mClINEin_Q2HtID^ehi3~+1JCh`oSk%UlLwOk<%r4Z&R13_+L&gTT`9Wr6T^wkK@&CJBjjL=Y@jKBo}$eL3F3YXkI6Hp>5+-`zz%^z=A)*@v$fx-(n(X$v5CUuVLUyW2s$!8-t)!Ah_ity?V7wc`BA3d&=RREtJ5Y7xp>_H$wLhen&gp*8`o*FH*sYu-Zu!gumt;vVDxz^5*E8iGepd`NWLP`qgSZ%)_nNm)J39QQqXTw3_J5ol5Nt|Mp}tHyB7-shEr#6v{7|A^~cGc;)@4;&ui^>7gE@W0*1Bu82h<>&7?4r<kym{iYd6PbNl$Vq*w(2^E(&onp0YC@hK<IHQwfF^J!ejEl9jZqHU62Yem*fN=2my8T1t?I^f}zmT+3HZU&#ny2<9Asdbf%NV411Zv<)kvt&oY9(Y9oX@b^~428dYq}DByzmVkCNCa)l)=B4|OJ0>3oo;C(x}3KlMcAG(ypRO!h-bDt>LwMzh*+igWlUTn#VwNDfP{s-_(;v9oDvgtpGlilikFbW8i^_rn~=h=3vbpW>^+g2cqQH6lvYX8vsWpPS}sT)hT<g16)8@8T)iP`CCx@8(xe%(-$aj3C1^}G>qoN*>G!?&CxSVh7WoZPF=~|8L|DGuxe<pvKQj^byemY!A;Mft-+2q43X$s(g$)r#j<!Uz(Hi~khJqES&LTsQR3Hx*>B_58ID7v#1MvY64$Jn%r>+xptQTHOw?eL(_#FpHKWNr@ey>uvd*1omt~K6ubjK*%6N7tq68T3NeqlA{*C&EhBpZ=zl<gK{dOb9?@h}9fF5B%8<s;W#5pT5g6Ft0_pgl;yILxMKI+ZhFDXJUa1sD=oh;qQMyfef`(PSeMeK5E$!p&h8x!j(+Qxt7PMRa9a3+wr9QH1$>ouahTlq+^_D%_eVXOE#MX;EAim9f<0c{;&Rg!!>3N?H_;h<?LA(pC=f+ezF&6px9*5m8y0b~xX>TO=S#Sf3BcrD=(~h#p*tqT*gRxkeG0iHeVW)D6?}yDdRTDL{Sl@2tH}5!c<`Pl}2baAB<lTrDEVMS3JURLPcn)$QE|H0^@0uV)7Ryh9eCd=bruJfZT)xffj0VWMfHWS1a~>X1j8JhRg;>?b`Aub9Q-*812nG%2k;RC`$efgfI<UXOd^$?XMePulVLCeKV&K*h!rz=MU>0`a;4CF1#bu+zh~9)|XGJ05}qrtFz5JW};R>+%qErgM-Gu<A)oo<r|=^Hjx#Y&=POc+E2(@n8$;1D<5)Nh3V5$wQ70fo>PSYj#SJ0{dq==zP}*-Z<VfD|PRolI=>}P|cc>$CbMGP+{6#ou*ezIb$eu^&?eNzbfdVW|N)^hSTT>>Re@zYVJY>jq)2Ps!;hA-vm{>bj&|*UnfjO@<W12FcX{yPP(#zbnWh{DV$xXXPCk<)6{4x_FD6~$}X>)>IXP`E@DO#Yykos!^<|wH<HMZ6xT?iLzSVOBxiR}VfS2yj!$@XODh(xNC7iCAexlRTUSYZa+4cWl=@VK?nBYECL&u=^-;1Rg-0Z+NVG}%4Zu!qZ&o%U9Oa5BQ~5y@q5diA8u2YrY7?=Eh_xtHDN|C3L{AQ|6GbbLtj!fEvOrM8TC{W3wLOzkJQfe5BO&sjMQ%-$pfW8S6SX~((o|*S^opnwVFTs_w}R=|oxz`6BQp^n6FFV`xg%=3eJ3|alqwN^j<U!v5g0oW9gFidh@=t~?c)cF#84D>MII6e7!Eieid>T@9*kXDiWsUgaGdp}qWdN5^)WXdyLTzYEmow&O<T>wc5%<0#CsQ$-z~&#o5TAw(`wT_(bdEOqIr0?c{F`(ZZlDJ^XN5UVqV>*%0t__bkvmgO<~{U&Y5swSZ5&mwecs7ruYm~&?e0J5ZzF}sH^dZW=~E{rr=FXan}^I$w3bdulowxn4*a(trejOTv`HCT}GRXuDzs7wlKYbwMi-yJvPZR)@jzMZUMG|b;~*jRn$XF^Eeaf_HJ18Njme&)?|9^O^^tiUu@7c={Jrr$RxJ+z1k$&<e+0yfJ_lfQ?N4SO%Gms#r6SBcqty9c6!X@3{3*pQf*>5e8Tf5GB@#|;;v&RhKMX}#4jDRtP3!7_t+Hmv+H!;L=eGbc<f><i7FF6H1XVaFHb{F^$<C1S!ZRM9^T7)O|+QYG1KE~k5iNBV6kL}X{t=FGCdgG%CXH9N1MVMn&Mqew~PICGU+FovUH{+$D+0~IWBQMx+XCy5jI-Wg=#>>cFglGD5(PKK{p7GI)|sgTB3?)0!=+AY?qOL+MEcDu@<hvOuMMih6+Pa*lQ+MlT8COpvl->)YOKWY*4g@irXj$vo`0)C~iVc#Y)YcCaEG55z0~oqBCfc2d1`I`b1VHOcxbM{D@FGbkam^w+Sy+CW4-U0zFwGymg={KsweVlW#H!S7#nwCej6<44<c*Qx$c7O?qsSr<z=4N|0?ul_@UQ<gTgh^Hkna<n+y)U{8xJn-V;Z9hl;A)BFsQXc9r$WI<w0O3TM=kJR?er8@F=l9Xov_^P51Nm#0Tl+^abB{n2^{nrE~lpYE!1FThAZj!qJr6y7uA;K(66cIeTa*^v}5w(4kOhknRNARY#gjw|ZyNXCpyURQ6RMp%}kZqcDoz1O8tfvy<E5=Sb#hpcH@p>(GMDfNVzaiS6G#TDbG+ih9^IiYpU;py&|N3A4%h&g9hsfypA+q%ojo%QT5+6JM@JEbWfw6b6;jn`@v<W<?-oz%5|AxKouCvj28|j{KSJ()Xy2sn-8XLjE>_ZzF+1y*&TxAnm8@1TzwQRg$TTN_dYa3r|<4bIEflXR$VrrxJwvo2+I2*Uv`2IG(Ve@M?Z)fAD*yKW+yUZpnHo3oTYOzftZSsCL0-JnnXKcmZeBb6@(dI9-(Z^<Bn_6ts!BoB*#3=_D>3E#-orV7IK`8Gkl#lQogkrOQ{s=$9v7bZvdl1Uo3;jp<5q^Xp;YaupeuN+4NB9wbgrA7%u8~_aJKxbaE^2x+pS-PaP^9K&zPG!-$ou<5w{UtpAM18bxA6rdA3+xR$9J7CTKE`z{I)*1qc2(b2*!BP$9JV~w(vRdxsUHkpK1cp5A+}42lxSgfFI!BBk;9jp$Cz2uFU<dc)sfP_?|rDfbV^HvNrbk-FR#p?tMB>)_9}uob+6tdncYil<7u18pD(EJbogN-;C#>Zi#IJO*i3*E^!{slZ!7-(Ut!6PCN!)ZshSkJc6@LH<A~ccx=RT_vDE+&)tgWEqHue-ek?Y*Toq=ybtfgyD{%}(atBV;g!+Or}65xv+v21k<rd)@<g}beor2ajCMYOCu=-<r>7rAJ85J%@CiK9opo=-ixxZwJRZ!Ou79a@I@)=o)$>L?)?J$3jYkmeq>-WcXYvFlG`qJ6Nl=w7DDM=j&aH|s;5{K6cqOlG^_(fs>t3l(=f$_yC2JiG*7+8le>GjxeI<N!AKeS<UOUYB-cio*YAKyh*Jb0I=>*c|-c^^U`@XTxzl#pTw|te(U!`Lm|9fK{P6WA97p~RGB|5%V=LYLyi!R#f<bJwjnx-m{h5N3$oYnc!oz_hsovALLSAKMzy719i>*%d@?%j3%qwCg1Gu`c?nw>_zd06vlylav-pU;z#fz3|dpTvmn<V}8K9*qob_VP?}Q{DY|;WV$vO?4v!WOw1+;n_ah@)*)|_`@5`Qwd}t-(mVf?`~wV^M|)l4IC|a_~-RjJh>syTkwi7AdPGj@dTc)czi=%I{3;idpsVTI6Z>r_j!{}gdhk__&3B&%T<0G+}wx58)sO4%Xh&|SK^Y!rH4334nM17t&5{|a;Yw##>VCMd<C65@;rD-kaJZ@=alh?vW{~0ML+N5`i}es&5<)<&)d2Da;NnAFu$=_{dO+-<HC$oI#Z>7I~V_Paph_(Pv3CO*STcPMH?=<+(q54oS2EOu)G&E7R7G3$lU^#FUn!Cc@>5Qp%7r`fPHU7Vg+k|pWA{FJVge>_)-`jfng3NRD`y}1Yn|J5h}C!MPYea5+tTr!{i7I^Ge}P(g-7fISrEq=FBcduVFtAsbMm|ElVKtX0qvl43DX3GLrc}S4b`6C05cWn=X{`1+x5;QaB=GXDAC$GBGc=3;diJt=S=&zBTsC@;!fED1N#ByXC=l&6?>uNWaW4OI6775o0uv#plUrLq^NS)j}2unY%*f;B$sD*CYFVw>n6h$I<w?G^SUiB}>}vf{oqKunrAY@y6H3`6}pma$?RMakBirQhojPalC9*iV!P58Rsl;1mPYJaaMX&oItRNAV`NeHw;IQalry7aDF%#7a!nwG*0YrbDK@SqDBiF9*x@CS{F`lF;C+JqCpJ%{~Qgv0WO`z6)`-jLS6n`V$dycw1&&4Q5WEN^?ss)C-YgH(?QB_oIqIF1Xtcq(!NcHPdaTu+q|`{TDV6zyjimAyD9_ZV-Lp77vdPU%Bwgzmq*!&o2_tO<7PM!ei|+g#ql5<yF)lX8Yjz*(*Q?}xXB!s14VggrWuYKap9G4(uhm%ymJ1XSMK0v?tT$W1L&X6<PB3M?_d)RTa9eKl1-}ANlXKsAl)#WPMtKdakot%6%=hbuKB_?oQvzL$REF=EgZ8w<vvNLZTPrjNLui4eahS0;&nE)zvO%n+MUl3DjL5sEovHV(A+a<(m~6yS6Ahk2Z;DxNQ<^Ku4oJ?MO|qqeXl$IERBFhkR*yUcQtLUY5puN>0H=V+WaKibe85c%`Zm;1&v>mmN}S!h|x;7r0>zo(sI@)L#)zYPg5r!LugXb_!-fzd(*m}Yp2uMKC}<*Lo=eiesr>g%8@mUFA<zPNF#4++xz-0MWOnEi=jhB-lh8bT}7fHIm(s4j%WPn;=77?O@v>kWvh%shx|{O#vMhpCW`QN6fu0=S-wVx)1o3xH$d~BT9mV36QmxxLn7a}qj#r8ye7)=#tE_z2!h0g=qGQc^BskX*qfy&Zisjh%~~XnMF-Z1i!{h9MENDU5dAbV>=gN;;=D^VwTJ|AerO5laQ{^|73IC>Ma8M5gWR34Ci08OgNXXqDCmA!y`ZTA<s`Zql=R%A1E2#-RLm^82sCL>4kNlf(D(aG3+Vi9fewRmOR#(@@mut60!oIUyf4d5z7Ui*2()|!`x50=n6w8<ZJ;y)<iQd3xiVG+<p!qPo7C{<Q{DnPe^YReKpsH(*bA$G#0oSY>I!%m6revy0mAo&ygwpH={Nu)*CyI&m}Eps)t1izi64;CcL6~YiF!z(n<NiN^D{{aHlfE!{s4&^Nj#b~_mG54N$$uC>~o@dTT(hFoyUc|p6VhuI+phetgu!Aj(L@shbS+@im<yYqIwg=y{65<H1}kss_A5YOPt`Sc-kCDb7vNBut>993yZ(IkTtR7G^+^m?X#Tja=12t=ANus=KxLcmbl6iW0tsqEZSyahr_jrEL+(KBH!_$N2?W%wTnB&a%L=PWhEOHW=6_3YXX+QQL*`IO=c{C*vkxM_^kV^g+7))#$sa@S1b(3U{j==*3@(n9%PBxXDjE`@dnH3esRbmYnHcR`HGdcS=iEWV?ItR%Z*`8kO{KIA{|gW$C{3@jBfB@gN3&e1{On>Bt2$vE6eD!6&IE)um4H+^7B<4A|`^GuhwM7VhEfbWW~)MyuGaWWEMBF!ZB8QK1)8VqpbP)EdM;#onwc`r1}-?=Wu4N;5ChivE74qoA}|=U0VUft*^g?%P%v=iY9QA{<?=Z(D5$rcgZqbrjCq8J$TkPh7ixYQa_7z!bQQ#8d;td_htp116Z(Vjm2YFWWy?gQVtIDL`QETB%ftgIQ-5M&h3KjS*%YNPO&UDAU3R2u>@GTHk6k<9^2Jgc@^`gSva^OuCW4a7jYI!v|g=X$-+bMpt}SYEYiQsS<!~YI^*8K(HFzt*DQC4)qD|(C5ttSA>doEoMxq)UW5$8)I_H`VLRD)l0}UyN|r3AS#FIrR~Mlhuv*UYjL5-$C{+D%MYDJ$i_BOPoSxJyzs7P$FG4oB2v4%YBNlJ4_|~fxTUgx2YQANN*<ng-xd^%KB5YkPn#@??04u@f30d=fS<^9Ayc6s7Lx{i9pYIPZP)%%Xd%fuB0NGX(M~orLOUf|cu!tgJYqr;v1wG3fvnq1|k-V^sDj8Pey@*V7r@Va`EiY^r$-KGDRgt$Bm$_XTR#1+W1=x3+$s+V^#1y_4lzBLCc1z-KkxGgaHr*@9CaBDut8mp5WXVbvAfXLqm>tG>=>03nB2@3rkja5hXOs=UH_leFR3$1FGJ(E^bf62=jb(NG^f@xuDMQU%O^n7h+erU?AsJWcM<|oGlI1ki3uH$_-!?MeA>-3e>buLDug3V1y{qgEB9NtYJ~A^WK51U`DBXR^yPxcO*w@hSk6pQ$3+uKEj#OWd7rLa|l{3Z)7wdUBxgGecxN?c}mP>S}!@=*MT`s)*XbE8zE&@1q2fVY3p=l^BzhkjX1b^e9(a|+K{!W*NA3LmNGUi&q+z;xS{r)(YfJ=tE*xcoGI%AQ`n756zWT)QTC2KBunoF!)`GMuChPAm(1U5~`DeW)e5?GE{#jP%Mc`Fy`$URjZ1+jXaq1)R_xahD;hVFZ-1k`gbf^A05e@k%r<%Avw(Z?|GK7WNPZo7Dt>tKA~kPCZSY_(5xaDKZthVM?U2rfS6a<A`_OI^v(m3FT~fp2(e*ZfS^-%WA!uatfgLB2Ak-=sXc0rzT=#WA$~^v0sc;%m{i@*C?ui{Ww_chfMzu?X!<RmIjtw67F1Ga6}{TWF-Sdq&gvmzK`TRx=!na8=Qp@D*gDJG_TAnSgBU4q4m)nOl?bhRh8*f&bkjllztVZdru!H$@&GHYvPhH%Y(8O8u||Fxi0li?)*%umAz=v;hkMivzF4392m5p92b<v+TR@oi1MS9@^`|nH@QsOmtWnbBKBDdWo$or^3zEdXb*WLSxs<+qxKBP9M7voYm5D;~eh_CN9j}$*spGAfqb{bOjR^LmP=ATeEQe4!0TWipQ!d8eG20w94nv=Useyy}Df39|K)QeGGQie2Mk)+Ld#oy*_^zsG=V1I+*7@KkP~S(B-al{qE|!T%mGBeI4Q@dMDRAHDmmdE|0kPNMt<B`}!|GdpPqgOunTV<Kywnr%aQ9Nvh~+k-``u`iMC_`450iP2oGX*lXftJ^WglUp|__;17n0>82)M&8G2H^E;d{GeLH{ttp*1i8e_!!Npg73TxBPd7D}5#V^x*-juhvtizu<7QAYjb+X*gk6{*Q<L?=+MkZP_)r}WdO>DU_{B!m&nV6g&vlH}vPxP6tgWw$3_ww^WDE^+PZD&errT}HB1jR0UCh5BNI!vTP8aQdTHnBDln8;wA1WmrzBx|N3jW0lxJ2c6bNxH7R4wHjLdT4TBB1i)H`O$mV2^*Jv0q1@aZIg0m1-DJ|y;X~t&(T4`D{r3^E0Wt^rLM+yKf{Dik_7J1IiI}FMU48x<Q|f`S`hY;uqk*!ikg%|)iX4;vs)!skisBR&eV$#rJkYvpxr73dy;!Z^12BG+pdx-kAhrSTT+0$!-7QS7hd&Q8bX?M%fXs7TV8nn_N1;3iaVrt>Y(^FSMATNczVYkijQ<JSHV0^wjbn^i)GP7CTrm`fh4F2PVwX=Wvc_78B*D%artV6EG_$i{>0F&*~g?|7u-O;9yjw@SRG!jVY!qAuSGW=_Vd4f80NJW`K|%_-w%cb1tU9{ujW-_qh~)lS*?Jv1<dKtJHjI5;$01!x^EskumrHN*=oP9FJE^=kq+3T2eUBbj!)2h&_TiJNLVt11-Ks|Og3ON^t>Nn;d>hDX;_4k<p5Qc0t2~oOl>^u_k6*3!V=8CtYO%MFU!-w2lOwDzyD92uml<KvIb)f<MA-p37ePqW`wcsc8O7Vx~SL4*QZTVAB>kpz_}7$!$iaUcvvujMaYFO#&IJojfVXOOaH*~!P;q9fZ@5K8`a5jz<LIDK4ki*w!R-W9fQrI`;GkWJifl!yKb1jAB;_40x-V|bN7I~Q_IAK`lnbbykXbGhrq7@&=u*1_jiT0pFdRJCOR59!bKLY)j7|TPSM6_Dnk&#k8^ERHJ@_%$`$ofaDrX5haIJ@i@#l|ljZe5<eC+r;D~f^;l`|KVR4oG8ex}Nyc&3TW4jFtKP;hQg<Td8W{DZgZ=~!6c#9DTmhkc(V9j#htYo5+<wrlFqQR;u{~tP4yr#-8qY)}%ak}+QRUSe*Nvot%dB|v?k*auF#ZX-tauI5!n)JWIN=q_SrBXF@s`BB(th;Tjs?s18=9~H11T|?Cj?uv|sfQV%Iit^bG_3_nG|D|f&4W-_jyln1Z0Zq;swviUHS{?jVHPONGqyoZW~k!a3opM2S7t`#;D9|UAc}iXL6^eM5UR(<DFTOLqfikF%O~E9ZX7^GU03}Ol|zVwQPP7-k5IWd1;29$3M*0iP_srAQ?|T5M{!WAF&O0sp(c%*Z-RQKW{6+uMU(&S{rDaM!{fdeDo-Aa@*6*V(FxHPsf)I#$qW^$0%a^*E_xtJk+pbNRD@-!QTg<xm^d)mRO)HePJ(PBDpkps*sYRuIWHzFnwE)vrAqanFbgdIzF`C9)==&-YHEFseeHNtFDhSkbCq<7%{QGcQqCDueih~MYHBOI4uesA03{|UR_RgGY=g?LQn5k>-ElJ=K~1eI<uEmB+D`F3cAsc6;r2elECpLra6Kl0(J3>8$Z(=ht~O)6yT?xMcBZdbTAzuv2}j7{beO37Yf6Jj8t)Q+Ow?l{i1HPtux9em=@3guOH*hy31$lg?lEB@Yi-IQ&%#6xP0j11$Kgt+Y1XDxnI=66J;0k}u5j*NC&mM;4wGn8T1>1>e$7P2CXZ3};QLKnnY=dTN1}iU!|itWh}1>mio}}aD-t$#-6Ng9MSR^Mwv&+$lSt<a*7MpD#M6tgpwTM1f^@zJ7D=-{#=%yMSV)Wo<=*T@PWW*R{UisZ2={^GBr&`2*q)T%iHe4qSCQN<>3&hbj>Y@B6DIh+8<r}M(|!HNo)iPT6UrYhQ-08+uoE>KpbpMi=BfeUZ;!lPl(eF@TR*p(c*9hTPUUL$a`};p%ES%3LH>DTG&9kLiL{C8xyywqDU*9_n$YCu(<V7=auC=oOskC-f6GNgmZ1T=BvmHq&tH11lW8YixEtVRu|uL&5+Nx)Cg}pn*@VQ$NFFjd_ehMS_?V=kwBoHuevKp>B(F)uP473yMZRCg9+134(%1iNNCNk~qLE}y1==DN52xQj0|!ZDL@N3da@BwVlb4Xh)rIHpLlS6DNIIoG=+vbN-sy4d@*q+;O=9@9MGATjQh>1SZ@Xht(%eHLohysgoJjI8Cn##tPYimGG_{hZPLgXOVXQA;)kr~7VT#9FSI>BW!>*r1K#IDRUvc4Wk;<F6+POa7xO$HynoLNtM#9uGoNI#}S${IxJ4uA6HxxF<KDUrOB%>pV;8I*A{ham|B()dkmJ5%+_qp!$qZUcLM#4O3Bspy^NvV+}cy`l45={~~6Y%<mmecL?XUXX+(~cCnNFL5!JT&f;D(NM6{B@9eZ%LZe_{%O5-oCw_U0swY79`#$g*KAR2T8XJ`ROO{ij+1Z&_CBB@trG$TYbM5^F!a)zj#j2?>?x|G6Gq46aSh~(^%BO;m5q2_-BOTepFm*1Bc^~@uo<-iGMouvV!tkUD6lSY-yqm6RnN$AS=^v!*&0ib2V=iWpY#F$bC|gcI9*#%r=SPaP<i3`*%JsDr$d2i%6jHm~2Lqj)|hB2>Wc;gN<2F9H>RnMD)AYN{h&wi0XmHv?dZQs!vNHh<QvD3Q_16krs&-VG3Cx`Z?8aTqD`K>Le_Ggk~Z(5qT83$D+CT{;l_UJ~F%*H{gXRcP341BHj_H-l>m8qT<ZwMMW}Zf_Q6DeT1SJM6@M}n<7~ic{7oJB>MiZ&y|SUL~|kHO;NBCeP2$K4xs0u?lUBg%{nffR(E%)Q8Z!5#aJZzF#7w7$@5gOj2VagO!p9po->zpcVBEfT8MIuT^0o^5hb{fnu(+mrAMN;CE|HiM4KXSBEqT%k746SBHmadxEmi6sYWlxBB?@QGej%5M3a@M>!M>FpPV5ey9%NUKsW>EBxtId|8WJvvENuRZx8Z&pxXub&O3kppEn*pGR#J9bZGB&SbnVqAQr}Ae#pI90xVhU0GPjC^zAWarDCI=`c<OGJjh1ek96*YscIgmq74;k6`89%6|W#CRZ?Y%)~X!*bMPKaLsV>|Dk^WnTA*)L<(8nOsmkLKy@6^!*cYL`a-^z!!Lm^$-6aoIaZMEttI{D=z)t#Rs(DRCprSSvHL7MCl~k&<7MzU`R3Zq}8mlH(ybzyPVaOR(qU&C<GAu%doT-Y;RCsDOueHf5f=dK1dDbe%Y!Mrk+fb2KIap6?l`mA&X%$tfdQwW%Rc~0lXsVjbR1Wg{P=!zDqz5f0$j`d9DnIqowu*EW-*>oekjleRgs}<(x)B00hgICDQf*xgRC)NxzKWo6#dox3j4Jh@{4vyg5i05ElMQNKLwP{4Za~?Ka?eDilPGCJ1qb!aFElgcyz^(-Z(R91%=Wyx-+Pf(JO5!kE$G3xs|kR&Ajw*MFdHzKhHa!`4tLy;#B0GpB;_+A>?N0rC)k)Y_lsyPgoYy75Q&LM>J#Pj<-XW<cY=|;6Fk834nv^BI%d!C=7TsMdJxaUMO=xf5+%$+D@49c6v7ZutVFCuMefLqeepWiDAiZ#D3Kf!(dHV3w$BkyySXF&c$2?_BCqGjnTg0uG(n&u>QS2eA_pR_Mbqgu5_3_JotZ-~1c?dKAe!3l4D5PDvMUPPB8In=pWtn$s0@$wigNZ?sDged%DEN<0o`>`D6XPMqGTiDW1<8if$14DhN25mY!rpDBHkA9BJ%s9)F_&Z9IW#-z7vF$^B$mRtdrnMqcsujiRg$Zx*{BACQ4eAYcF%ok^@nKu4JWXZWF;8b&1@Xh#N(;_JoCgAIH{+bXu7WXx5-mfk=bm0`hwxcL>BfTy!23wn5kcc@-3PKwKP@JpxVFfMgdm?SOnE2oHm{LAML&H9O~GYxt*zKHM{+HxBpA@xOOcg^i!y>qK_{c=&ItDminNK<u#|k*k{aLBoehXEhcoX<VyVswSJkzX7TYYL$l;NvzxanW+4VDp{d;10{eWKn0_ZRUC<;jnUH#C<myxfogp&J0nyvA3K+bVluFYM>nDvCia=EloUCC15gZ~uc%R?QL_;$lql{;c_<X!LP-m%@$&n96=BBj?=(f2XvxqvDe8Je1{2vW6j_=A^m?zS;ua=`q?a5dGB&v$6IbPLNl(xg7zv&O7&$%Z-X;$w0m>1R)tzrz|Nc(X3_~nMw|`<dvN>p?#(RVmL9!>9^5-eqY>*)Ew}1ReM*@HQCf1WX1ge>jni>z+$aR{64o(y%4@2tFM9`M;@t!X>hMWydY1ibn$&WJq#+FD`E}k}F%*E?ANFIuC&?Jvc+_+AYy@@MR@xDQ@g(cWW1f$PWk+IlCnjvJiMe-Gi9=$?s+?pSMoVrM~OA7i;ieYD-NwQ6v+DK*S*}q;KFq}Gkqm78?)E_8&iZ34YJ+HstT}WXg3>emiWb7yRHIu?fl3&ZRD#qcmPVVE|l42DA%<o*Ri%w~|#iyJ-*La(!&8KnDatji#k!YLb*ZPq)lTuOYK?co5iZ*z7r6nBOt2@Hy`EIhgXKGy~Ba-ZP_8URk{w&#%un}HSL7Jd{Btzxz9;tQ9<S!(-H4;IuvUSq==aR=g`}w{$qU(7JQiSap!wX5kws>Z{qi#|WjEGf^U&h2WQrsfR4M<qYi;vVy$~iGnH=DFsrFaP`tdXc9u?Z;*yYOaB!sZjXlULGBPHB}iJ$se%%;kdQVKPpFWRc>u$JHC6R?=)lB2Ahh{Y~^7Rf6thvwk$2kbd8Le<GOEX_4O$6*EV9O@#H!of~mT^fMD-<GVt{8zM}`^qsfxsSvpyQP>b+<Y-GY8?DjrZYWrR>NGM0Nd@w7k*>Tdg|qi>GY}sD;nZwjeCj$u#~R|bv@GPRlizWW^n+%d==Ule{?0ppj;*))s@-CM$1vR!!+W<P`A1oPVKwa6M}ll5Ba&>??iTZUJ#@D5Fb%D)-R&UlcYkUS@kU=i(Nla0dV~aw#cYbEQ+X4XqPqKCfN6n+C<pz@n?r0AO*SIYhlBef+#qI=%YC{#MbSo7L|CS^(4OBGMHs}_DN08>b2V%%+?pt7kfA7PQCt<3@zmqFI>AtcIkG59S`?3nenUXgRue(qP!x}e!V%G2=iMAjI`0+<h!Pg*LxO2qVlSd6SfZ%7*G;ZbL}sGmBOi6wwETWc5LOCMr2IQ{uT#Xu_n#LPec-}cAGlgXkdO38bf}yyd7UO<2AXz3*xWONe%>PsP`-%fL!O{L=L0LGLq*d@-7Y~Y)gg~GdFG<(>!iow6|;EUS~EL_PNlVnY7gr_@WboV>v4}fxyNAbNjo0j<e7_{9JcZV@L;vIK+G;cop?SX?DVj$hoMK^j)&loDSKuMj~r@-cGyGEp3Xs1z^W%Tc@Dkf&65renR$}-@S0~n;=w-D2RzBplSX)AlZPB10^Kf#*X)!c4VL_!r|^#BJ+oZ*9xB-`*A3OsDS2G3dk+<+-qopk#kezuQdd7x#r>+Fr<+ZBKp2jtBdB$iQ7Y<E1+DTMDymfZ9p6M%ymb(rF4rwGAQH@jncz@x(&Y`L3wT#e;p|F1!xWC0rbbh-*&;eu-{p00{QxJ>Mbv155~u)&@v?35jV7`*#Wj=YXk}<O$=OX*z{#U0%36^$>2~{dS+au&Geec@Dv3|-bN2(VhYEEcil#LY*@~(UlMN|6B2h)6P10`+c4~XMvJv4}SInHskD>@=P*InPZ;4Wyh)qPSMXAc1l1e0cf`FYUT8U(BzDSV_f+E(UovW_xsg&ZekQg0_k_RnvYoY`NYT=lu?U|IOV{P>tL{y2e5p#lD!F24-;7_iRnTU^xoGt;~5w+dEe~+7tMX3_u=O~N(5`?i6(XmipgGee-(MEo-NDM`BSL7jwfZ>eup~y9f;=%BxrHG+814mn5D!O0JULTYEy-RY79LiERZ8Z_w*FASC?`=?iw<Nc1Chzl5s}1->7ZwKy>fs&d(ImFH4Mhct`casmSGTP4(84YqMWuaI*hifl1c)ocIup^a%|dB3#b=m;Hev3E=<fPOjg3Dvh;nK&1#e=CyQZK`4*F?$-DA+k6irNNtsqU{(h?Z)GTLNx?Im5lg=q$?O;VZYu}Qkt>Ex)!S*N@O*bCO}>l{>64>8T-Or%@AVF4)V3@lqydF@R-*WLsPv3bvorb)kcgh3`TF~x0@Xp@8PO#w1SEKR}6ly^ON?G@VxG~uOqc=YKplQT34TuZfy;S36op~&3ChYG!pnHa*dv=PK~(7rCf1m0sK)laQcmx&;Z$?(|4fD%<EerV#k?OvXSn(B#i*uKun^x$Q~z(kA59Wy<?_Bb_}4i-*!n5N3)D$|2Gt{mG;akMGCp()<gbh`jxCzCebKhlx2QQH9>m$)8XlNgl<8*S=BHLYSh?s*rKR8jSyn}tW6%2Qx1QN=TXrXCcw&d5J)PKd@>3s+&LT~ug8g&`>HI}@uhrvaMLWb7_#YC}ynC|X0sZIpw-oAYB7H=(9_VY^IHMJ6JYrwBx6&?FB`ZPE0JtW20TDv<pVp@it9iP~-xUaU+6{R0L1vqX67KvRI6tVbr_WD-6!0qn4ebRj6i=P4&vMLpy$JvPZxO|CK}NV%fQ6qjpq*VOiTDsL%r`eshBr^WV72_DA|O!2sBeg;W2iJ*M4Ah9N;<zu!-YJ29E7pgl=%6}fdsw_kjmh2uSwLNi(4M|@AH9;w*heFE$Yn7Ip<ZeKziIhf&Fx3)81kbKq?D|+lZ675QQDMP(ylE|K7QOziBGRMp@=iNdwKo%_oF-jwb1M<+5rz1Qv6E17XAxSwUW*-3ys^k{i1x=$hPM+<*NOi5|NVd6YlD3"
)).decode("utf-8"))
_V24_BOAT_ACTIONS = json.loads(zlib.decompress(base64.b85decode(
    (
        "c-rk<O>Z1mlKd-%&OV4uijww5OFd&^XvvVMY0MggVPI!4z+(2`-P>aS`%0qNUELL#5s@#eNzppFEp}JE@0S@F8TrfqKKaLQzyIs+"
        "zd!l6?|ymm^Tqr3Pj0^d?#VxY`>+4_?@#~q>3{z9+wcGR_y76yf4@BW@$%jJ(>K_sA3pr;*NZooKV4is`S^raZ#N(Ra{~VI{>SzD"
        "=Z_!GwtsuSUcdhIm(7psi|dacp3VO9)B5V|o4vpM{O;}R53jEGe|GbK-+#B?yUSO9`SA08dv-nj<;iCK{`$7{yH9r`GX3?g&HJO1"
        "yzs77hp&9|_TBZ5x6hw^L@&L20)6RS+nv|^@Zs|6^{*fQ|N6tH2_$bg__o=jtBY6b-6+x_y!-m6DLZ)8$G^R~-YtmuoqyU}QtXun"
        "-#%C)7uV}|$*W#n2m^TgrEuJ~{o1x*`i3uGWaBp5$@saG{#2I(de!8ya4(sQ0KH-N*mStOxkqn$|MtV(%)rr-raYaG$@)d3RiE)`"
        "d(%;BnDO1=i3X`*#?|2(pK*EE>Qldc1RSl~ZVf$mvTA4lIP_pN4V?>#3{A&E+CFT3vBdIG$7-q7bNk7DE;jX~%S&3Xuijo=tzTXL"
        "`lt1~>&vUlf4^-wxC09YPWjqJjUtcP-qe26VGE?D)3GabWP3y`FqQR_X7r5u_QP*Ke6&A2Jfq*QuRgoclZ|-i7e`(>@RiSR3a;zU"
        "^wQ40)U85(uKsA^Pr-+TgK=_GIPPYh8^6pZ*L%I?@UFt$QCpl{e_@-or+`tEuA{9Lw9qKRNeTwB-r$)BRaiPxU$xv2G!5kzO{M`f"
        "$eIN>%h5DQ4JPh>`E&;(Sbo-S0MR3y0fbKv#&7Uq`}T<8yL$iDK19V&W`B8q{qAD(!}{I3zkU3_)3F=<@Y8}<d-pAW?-zd8-M_^S"
        "CKKD#JJAn502rFg1M`+cjYY?6G+Ism?97_zxY3{ko*Nd8T>=PtY4G5TW6)gl?N!@wvZ@9iJZWhXgK0LwV-w4;wvat^h#_~_4d|Ro"
        "Ajq+1A40MXH}|)P9ra-?c25T&ksr}>p20V}<`{MjvnZBz%*T2$hdIWa;}G!pyb&(m{k44m!tu^8wK4F>wd>%+VGy|vWX#YIy?J-n"
        "kiIwWeYz}sWZPPONG3mt@DfBYsfMyUOr#u7*_j&Z+*t?;Vh(sSD#w27qw$BfNVYf2^IIok1fYq@jwW<-)<awz^-bsI&B`}`#?d2e"
        "2x%U$h8#%7VwZXKkjx<H^&i<NN~xr&b)?-Z343&zsYn;IF(=vu5p!{r*>L)W?4ilczq?9rKlN<Q*$WzByb$v`W|YOnPDs3}0XuP^"
        ")rPB`48Z8Pt7zDLKCC0&2pEUQpR5N24V_k@A=T-@uYB0H&z{S7RI7)$a*}_aVoIGDS?vaQ!(;^XBVbkU^dKx?L0qeWE{3CVqc)Be"
        "7d_?#ZR)c_>^9fJLXV4<kMzLT@813_te)JyoOtwa-(GF65O}+sZoTi1H|6Umnx%^{BixW26j&|7=h!{lJgQ8qokIe<2kw@v`I6Kl"
        "oID@Eq=zPtnTwM6iZIpBUFzyxk7A)^uPVyHG^iyb0Nd?$JfZthO)K_sxYZc6b^DOha82t`Krb43nx6+RO*(f|B=h?)5Nm}j8=$(v"
        "$K&97xCxG1-Pv*r8HB0LnW?qBy$wy`aO9$%p=+tWFlRRu8JYt-tJPwq3-j<+!>5=}s2g(Ja(^(MUa}My%9hx^6;GnG=oX>CWBeVx"
        "KAzJKrw{E5{_0?7tS!q25-Gvbhs!2)H(Vo6O{jpVt$<Dwhiw$n&v^*yd5g!nk5Y+F<wILJTu^{uW3Z9c#Mjsq(D<ghQ<jGW&?^q7"
        "kpxA}9S}%29Bf7Wf}M-<`tr}SFP2{~afbsJ3IC>n$N{$+Y>RQ*)tMD}+#vtd)P_XN;CRH;eJaS*L0rN&jo_fug$NnkaYe9FYUOji"
        "u079nm3gi!(>;)V#EBsShjCoMA%6GXHM5%l&v9DaG-*OuKC11=i^;*Ej|ptZWgSc<QjwWDp^-VXkf=WinjLT$kF%mgrxF;rBDYoM"
        "9U*IaW)XIWv?kYfG(vV}wo0Oho<xjMR9;IbJv2BE_J+!{g<cf2>nCppGnC;P+QK98GsV2#%^Hy;a9@s33E|L}79jMgvvY@{4z`{^"
        "en_SS>jbsh4VAha2hK$}MVPYH$qk>G8HdhAc}{eS5O@Uv{>Gh&C>E`H5p&D`{HDslf{K9)IZ^lJI{kEc^_S0s6vp>Xo<fJ}c~jW0"
        "#Z6kpb{}_>h_9u%Ok&_h_I4tsmu=3ABplhFD7Y9)5qNN$(Oq3`;c3Of#^@!#-rJaIRX&&Ed}~)snff(b`}ut{3ZU2cVxogY2Cdhv"
        "W2W_FTNIbsa2O7*C&BN6VYs@!LYnL%1%0(J64-<ZaZ6hG9o^r(4%)E!itgKaWO%TH#uxE?!kV>RC}cqw@tnI^lA1$-F_<lF5EnXd"
        "|J<G5TjDKR*5K3LONh7GpW7Pkq6HI(^2Qv>&n=$ao1(49Yr+xZUJJjJku%Seh}VuMy_CClgfZ%*mmb!jdEV)P!V}o_KoQdcMgYkd"
        "TT_`rK}`MiLXWZpnyxG=bRKRpyDKOEl-#Hxs%;s|MEynna;CZx8_PYtLxv$L@-XRv=}*tfvhWbEF%mt#IZQ5Pg_%$&V_IoNpFk4h"
        "uKN41S7Oiy^%7d(VUi?dR@S2!hJl0j80=6`s3@<JwQyhrR)3;)o^S*~p8<~mo5sTts+Y}(`Ux{fu*Z>s1~I46cFkssB9*`nw_nbk"
        "o2<CIJioxV3{z0oTHfECId+~HYAG%0MMg_fnb@%0Pe`mY=$IBipR5`b1%wr~B&u=1@p2KH0PBt;=Mf4fA{QknCEqmg%>qE_Aja_A"
        "-fgW6CJMW$Y@)r{J<qnv%cE|UJdl3)Z8(m^f-wfNXUz+j0X6Cp=F|S4Z<h{V5B2*)jC-Ux7`(p}HdUdel6G;+Qr0h8R)Un=-j>eJ"
        "N(8p)vbH$qyAv%3drCbWUfqTvROM$BJLhU`x35yQZ^{Jwx0IRd#1bshC2Nv<?u(eynO%QRSgwxmE`!86DH9PA%Wy7T7vOB1-%hVn"
        "AC+rDRB_8}OtsY1<M8B_q<@I_5D*7nzk}V(!PKSbNeg0$Y96jgV;V(sMS63xR7|K~vUv6Zmxq;}#FB(0vGmczNwWCST5#7s-oS80"
        "4vEVvNeb$Eh{4ES-TELu7)&yCl5$b1dL{;04cgu`@G9+4K`os;WSduw@}yXPQF_M?ji7>Ny4#Cz)mo(V1PmuuLJQYvhbkZD63F`p"
        "K}f~YA5mh!N@RYrh=&^jgf5;bI8t`3iwrA;o!FZ);#07Yc3s_kIG!^pEZhgv&bk7}afhy>D96*UAF*IOw1Sj%n7sre+ks3qM=a1Y"
        "_KxpW_Qw+w)p&8E3UB8bMAU^tgOo7M+S8*dbbXB!cb{2PD((LP05f>nVaQpvb|~AVH_t)c0iM?xn5^3$A8c_W3L0$WF|ms{ZF<!2"
        "FUh|LqZgzS$O2{B0Ov(u;+kw`ssVMP+NIPsIU|S-DEf`7CI&<JIUU&=zlit54iRtJZrCftgvop@*>#@tg&Q$3p_59%lSQ=t@?943"
        "gA2m!L&X&lIzVFwxhUp3=at!qF69&eb|stq0|P6$$5fKxo{9TXWJVB&J6a5>MX29-1L~=mo|*#~StE+OFpu1;@py+Jl&%$Z7Y^q;"
        "7q}xv;ss#>)*EZ02GQnr;RRGiWC+wq+eDOOZu9ES_R{LMe2fNUWVQe3yF9+tW605aXnHQ2P}-^}?9!q}=zP3qUPebrhI@)Grx?;="
        "w2F?%vQz49e1+NoPsv6kikbDuP>{SAT#?6EqC^~?^m=%K=Aqi|?1mOyLhK(B9{LDOWXOBaSUU3d>V`XUBVF>nO+bK+in|ysZS=k2"
        "TZ4+B;JcwrJSe18vW1l=J+VZnviPdAo|zv)oDa$pDCo+tXiG{WI*PyxGPZyZzEpi=l6YLs(`{8Xy^k>UJ@fk?c6!0SbPUK6Jak=8"
        "AFgMrYsPf?s1OEeP<%<F_PymQvo}FAk0*P(VH&Z1;08uGJ(}hNC^3k-K}eh(uI%YelUjUTd}Sj^a||)NX|amJ7e;p4p4JHu#&Z;g"
        "b+vWFk+go*^Ej#)D%xm@r<)5P@ictB54cWY7)i=PUofz4iP_t(GbZ`2Jx27R&JNw}MAK`*aiTTl(#?fEv->Ddseqd#tVpJMlxIaW"
        "^Mn%temUKaq6(PqphqsS2!bW14fNJuXePR^B8;;cVg<p1pG9&q(tQO(wEj$wy7M@*!P#jj9!^>EV~x(``FIGwLnlEV%nq4{`>B?A"
        "3^?HBV`l850*)u9YS;k1Ukhfd^nOwr@qo-<6eiFq{EaH8<Jbm^dxuEI;uwKbZvwierKAHCOkNV`@bhYE$iC=4s`Mw>bSP(n4-b1~"
        "FPcT=0#lPOpN8#;)=Wf#V2t>{YHL(^rLt}^lwt>~98xo9tncO`@GihVk1_65vN9E5fsm68-4QL=JlM_TInf#11lnU=KtqXAt72c+"
        "GZbFs`mwleUHgNLBI9@r5ViFxxY5w;gx6@<PA8ZD9C2O05K?hiU$br)7KrlvsR2#kk%|h$TA5r6(QGJFYfCF-vAGVx6ehU0Tbz0J"
        "L+k<*O7;s($qrZP$`uks2nLGLbzl}~zsO8`i8y)$;9!q3aB>DY1BVqvr*rw0GYP8IXZGFw5&WS*RA^??2dKko_D8AGP4L@i5}fhu"
        "rfgdYfQo<UrdRb)Js6id;ZjL8z~;e`EcE)Ylm$R~ST3D8NXYQCv@JOVIp$2$k!#L4F_ia`Sa^_zb9$Ay^-=|KbGAqBB?nFb$!4Y@"
        "Ls!2nPwl|!7CwiB)o6`;$TA|-k)p))JXql^a^z^a#6zG>Skk~@oJ4Cn*}jBIR2O=aGqLgZFBJ&$&e<-IjRg#J{R*j8RZERx%&7$v"
        "rBY=o+BiZ*4^1S4D36XaYIN}waxGLBBMhlT!w;`ki-5!UkL{E#RB#C&7o4Jl!A0>D^kf=^TxPia;36~fZ+zAimcD~|H?<W?gf#O*"
        "Mv{yo^3U*WHW@m?e9D5Ml7#AZsx9)eQb=!Tx+uhjIetK-Rqaxu)xo45&TXVh6hxWS<Ky>6sZvT_#N`%yU7a{ZT!!>)k5P!Et6s|t"
        "0eu<gSv?BXk2%tLL_D*jz>AfF)vdo!Ax|X^;+PJDs^G|-!p-_2)S`eAe<BxnV~}7*>FOMy61;-OiXg4hH<r*MUV<%En_)&mX4f*}"
        "VlMb_>?OWo#2$uc4Abl6=(@DB<uo0aKT2pn<Tx`3ro#gYTPg@9D&952R_jAaoS+o)MV|_~gL=CHMjRvmRF#HQKODYanAZGC3%adg"
        "S!COAIcmb4TY5-y^U2#X&OquCq{wKe*^E&X2)R~M*S-%-5!m(lS$+s;6*oO;n?ov1ZA3D(L!cb#1Jk2Ti_vJBx?_V(lC7M&G&cJa"
        "H7&r4M5Yw|(K1x36{Nboe7u@08Eb0s+^mk$D;NUJ=uh>!B|$RCI7@W1?j<MnNKux856iKukP%ZTrjoMUhnQ2Ro!%wvqf=$Yk8_m?"
        "RYS@E97Z>i?gwJxrNT*3u9OOC&@z_Glv4^zED-4kUlV0qccxZlsg~sg9TgVxA1xzgWR?+1S5ZfG>B>vgk#gmj3jyv{G3RLeh?omK"
        "x(14^l58MWfdpaNB%H43yLUmctRRnDFJ_DpSEu-qsTPaKXt{B1FcU_@^io221Ix8U4+L{OCq+ll1T-oFe7VVQhQZ|t33PPClLzNu"
        "bTpL<Dj@`g@cxYv9bO`8jT2IGO(~F4s42s$DXXQMo1mlRHI{>^-;r{<022uSIvFZT^QHPsA_aVq2)svi`GY0!Elq1l#dt>&_t+_$"
        "Wx9olcm=+PAUouOM$@xG#M^8=qT`TnAdppK?aMuQ7)5=8q9iF#hu+E1P|SaJ1Wu17MT;l*_2r*6#EHtcw9$V8c?T^y&&o~A6<{!&"
        "upKZ}C1OY)S<dJSVR+FUB%(;86Fx4rOj$^zBJElRTu0<T1P48xh8hziQ^FO*{v>h^lOQfsXpZ9ZT3S_fRIAg6wWrA`D4e*tC^f}1"
        "x95una4-=%Z7d6kvn-uCPa$rbB&blATR~Kku9&u77a6Z!?)mMIABdUae=uHSu%JA+Yc&d>mvz<>8wd5_)g@zDZ7fBR(-23dj|cY$"
        "n4-|HPzO;pQtVk210KPR6&)vpqi8QhHdn+9@DC1Fc5XO$Qm7%Ing^82&QjU(GT;bl6m$BX*FiYRbr&`yqDvMu#x-lDAZWf|F5fN2"
        "s_K!AXY?J2n(edno-RPhdypx8J#uGf=l78x*jt#5Vy4e-MzqbAB?c7Bxe-^C@ItgxMnqhg__JLwn&H0=ygEu+u>hCcVW058bBKlW"
        "7wBNP=;@&DnU(skkS|;igP2;XZh3g|tgqg_!P)^EmG#R_+8UWrH#nD3M$5H2wCx{gD6<k}RkluHnq@sTh@T)(mI&8~et77uR0+Fh"
        "oiQX#O6-tBg#S1R_JhHNt0}i#?-m3qnVk!M8CsRHJP{)$<tL;j-RhPW%*>1AVh?Eg5}b87d0r{>WRL4r6jNF4JRWWUQRMhrtfL_o"
        "l`FNvp0PD8B38roJqx0Pn$m+p1l%nbf3?$`6ftK|S{OnWlfF`AE0;;vTY3CKFXs)T4BR-@LDdg9|DhnGt2uCR(N}2c!EcD^nf4$u"
        "hX)tAn9&Ps4&*jNkPVZD{J0z<_5SU0M5Jy-K<hE;)DY7q^tBMayQvZcxUrF|=owKUAIi3m<n2mbiR5Ew1Eus=kM0tjd>OKA@nn<J"
        "ne>-3e$mh<3FrIY5jFpCXlCBa2!34+!QngaBqj<A1zPr_D36{#yiC=PIJ13P*EFc{b(Er`E2~JkY8ysvryy-J;kOyp^6He*Z%c&V"
        "<}#*)u}TY<GU@TWPbmUDy8Swo*;xOB7`IncBmBi@dfG#)nW_~o&~o<(vOZj9m71PjCOCcENQKY=%?;kJwOp7Zk1CFdH&W+V?dIes"
        "TM8%f%o1=&a0Odxif}(M8hmPYj*+Wnu?<HVET#LSOo(U^f>TiP{(ksydG-3&kEY@Ehm@jfq#);=!g@q)XB<v2y}Ed{zB3?8Vx7o0"
        "gnio1nV!u)^C^HUclUmB+~tNuL?_`vhI~qeM4VZDM8OX@QOqzZwt>Guu}1AstY=S=jDJCtLjqD$a7GdVaB~=gb9%Rdc=!^cdfSba"
        "T8Q&pD51amZvIovDF_x*T3tIrT=Kh0stSG_UQV<uce4v~+XYGA)a0`25`Y|Ee)@2#IdfYQ8BHo-+FE9p<Hx+T8NvWj!{g5M$`l~&"
        "0V~ClqOg@d4b^HcYG<CFLG<@z^;l`SEwtIwMfC@4%&Lj~N`XNsuPg%+yUX+D;(ZnHuv1p8$WSE}cm=v?Rp@SzYl>49%bYR>L)WFe"
        "pot74kP1e#kX{}2E>yWn6+r9RoNz?bpgb=Gm}d+(i*68L!YVAI7M2_q+;lSa)jU#a)$xg&fir`--dX`>VG?rrd97Xb!tuP`r>vB3"
        "m#NIt$$4|qvbOaF3`e-Mf@@jjWaYR;zNwZ3TgfEDKSiPH7R#4|R?va<B0Hoiu$Nl8?~tDiun40oT`aky!w{7{i<z51d68YIx$`}|"
        "W}K@hQjv73y+fuGAN0X(K-3mh#~&7)k;=TLYr0gaL$8xEu!?<$9yaR;MM>q7B7fjq<>kSXXQSXr@Z57nka?}@8ZE(VGAf%Ai#Pwb"
        "W_$*jmPRpDm7l}1ndq2(tz}g?!o$9M%yO)FMy&gt!9Mt_bMnIdRB>hVQgUe=$AM&inCOGT(ot1f8IMKb!OQ77W89qjUbl1MBOcN^"
        "W9<k&3_LIuUW`D5&(l6|I}Kml9zzy8Z=(xBHjsz|ZRCPIEFmdR-vi62xU&hAq@pmzWG1f`8vu*z@d1HI!VWVrd)C^$Xf2IMPcro}"
        "MEGRzIN+<XoMVmkS6#zsdbK4CPwP_gZKD3cS)U0>umlHNMRqnYx6-cQ6tPxvvQqgpOVSoj>y$d8lFoAOF`W$lDnG{33OjR&wXtO("
        "28`5Tpl+;^Q*h|)LkUv|1%sIURAr)Yx(jvaagwVligd^Ojgsp8vNR!$-YNgMThjod6pjiLkR-){G~y@1ZpqP}r>K(B1hX%Wp{|7Y"
        "$%mf_RWg4wMtBR^1qInoPbyP*AUTgI`L~Klui)AKMOE`rW6~|vt5ekZbg-T^(~am(?KLuVW6qu-=6J+JUglWowsfxRxd_@7iNR|{"
        "t|=8W!9I?jVi(a6c`mCk??#%5n^#BH54UGj#Y$FTqlmrf6|X54ol<!eRX=S)#Pl9oHAVcN4bA1O^BsjHo%%zzNasdOp3~2?Qe+F7"
        "zC?dc0bSRf<pET^MWs50QEHqNB524%$D5O6i3vu$kt5Z>2F4%L9ifz<C{+S+Xu!IMujH36m76!$?a<s|0ScUCO3v*V$Nk@kdR7&;"
        "Ud6^Ce(jP!g;c^l_u}P^TO~=wSL@X50KPx;f(zv?n2ZOKe`7HMb`lht$&3BS4ONvj;~Ik{^)b9~0dlpQRg^Z(3_haF{iX89NuqRy"
        "D}S72X|`_dEkh#?4H_hM=F^%F3+>KO6>zx=d7NPx?qo3Crze8m-Clj|dk3(NSL~&!oXc6F`784%PY26vF2|5GgzH!l<Bs;r%qN2n"
        "X|y{rVD5$GNHSRU+A<E$(J+ZmOewpKsBLBu9i_VH0v@&yrI9k|ER_U8T~kB<jZkepXAkRn3g(`pDz+SoODJcQg=o}b?x&d6lF%jA"
        "Z8py=^KPKhYAMl`)QzPr%cr&yXBM}UQlwEW3#0m4qo+rJv$Ks<s59-HxlIQ~o=xV|{U&${VF6~U@13Mos-@t?s<I6Cuv_)$m5i%$"
        "sU}|XB0WVa$Q;`-IT&n^NAp6_<!oY)LCN51tKv5&hc%rC!C}W4^lBa(hi6!sAE|Pr0;3HceS{Avi<L5o-3sakWT<-Bf3OE!?2UCd"
        "Tp$N89%71>)bcC}Tx)ZW@o7=??;N9lPZ9d}?D5yN_zLvq7<-M8-di>396Fm^RXOLq-McECJ^_G1eN@3#U8YVoDY+--b?`xG*s;u9"
        "5*`<s-)k`oljZ(fq>*%9yI3xwsY!Cx6#59tYgm%{lH%coyaE8W4kL{BrJFaF0b5F#IvG?VBP0^XP23Rnt3m!9>MGN>B3)LL<Lg{f"
        "Rftb4;c95}ImI)2k~HDQVEnSQG7DT{hvJ&NcwU97!5!-wTrab($xc!P#8fG6xv~qszeovZ4$2%DiIpwoXZlK6fh0CYf&fNfNyv@`"
        "y8c7D2;3G-<BNpSL#v{?5h%jk%dvhI%MVUNk%-vUa>4olo)tRi#UiJJEX4eM1!13DckqBHSUv4>UZSQfsGw{ZdJB79y}ZaI6?7og"
        "PqViyByG5gr48XAJ;RBoj}^LW$u>O;uRA@p^wd>G>&Yz@WBQbnW`KGc-jU~#ISyL6SZs&1;K^75R;^^LS2UutZ&V3egiUp=K%%MC"
        "Uhh;+y>wwj0gcO{yCpW1ERrgK_RvooELc+9OG3p^FGoc#(r5zLISgtX2`s>qS8-f|36k!5M+bFtjE&$b;<%!60xI8=>PSmo=35^7"
        "plR%_odc!DCp6}rxq7OAu|)MTDP1iESNJ<Am!AZmh6)iOR{_ZgKzj2gzlU<^Y{RpBp}9Dw+=Nh0IM;nn^w*S<gf9n662=r8RI>n9"
        "@O83vN%zbKW5_Zsu7SFh2u(2);oL=E;v;4%gC=2-sG~g)*oama$=g)7?jAsLwiG%cr<>-@?gD}^QS0m(Ptye2Szk#8X992yww2pi"
        "QMq&+;SLTzq2@ZvsxJqHB+VUyGKeJ|7Sm^^1Z{dzW^Q0_0Y8S47-3Q;-Gox+&2Ci6uv*z&Y+V-kxSm3?rGi2nD{TW11%9<)0#9ah"
        "Q$Sey4Wl~dzV1S^t+F{?*Pi;9>*I)dlO-n!RStRYdJ4Xpc{|{*qXt5wJWzoajs_A@Aha#T=F$+ija_t61}5x6%>2$~n3Ap_fPX)`"
        "xhwJdJRi%V6>~M#Iv_&YN$Er_<$OsjJ!e`>wq$;Z$<oYU_SFk(U#XbDlu@_K22*QQ@`{i_i_fsPW_E)fdI4-hYBg%MjPK<&P%pl<"
        "sijTxyOcQ%&nT48qp}pZ>1v@5B7YRy+KhZM1i|a_pSdAduOv>TMoGJ*ajg+on88a?2x6mag9aKV*;8(<knYhltZYMf+18b1!YIzW"
        "sm)agJ~28=xEFLSOTjQ7EbJvn4=|E?b`lLQKvM)k=#JY)gc4{jyr^)mCrK4rs)dT_6{DW;V_UjP-F7(Ug>fYUy?mGmJ!*s?5$qtr"
        "Rp*{6`(6Ho!eYfoohGIeebbC~K<tD`?2w{xJ10<&b7&E^yLiy~%}7Tme^-FKaEkipjt_L~%<mT*Z0M2apJqRyA&_&GH-D$t@<QyL"
        "+0Y1g!1*H*+u$HkK<XP@sPi7*wUoKCYTsJ=dwOmOQZG{<E9$@2h36ledGr6pil4L"
    )
)).decode("utf-8"))
_V24_C94_TRACK = json.loads(zlib.decompress(base64.b85decode(
    "c-rmV+m7V8kp|#b8Ti@@kP#F~?W-7b<@JSO!?W-K3uCeGzLQ;*%s)sSNHM5X<|NQwbk`Q9>uV_`G8l(H{O|An=a;|#<xhYA$M630C-eKCe)q4x{q>hW{^j;3`|F?n`<H+G`JaFO<!`q?|H1wKr(b{lhaLI9pMU*J|M<(l{`Suwf8(z|(AKZpH~;(3fBNfxZG7|3|M&Z!(CBK6(~tlA^_vO)_zt$OU;M5%{_)Gbla22Ty7SJq+3_~}14d`szEpIU&7Nbk_g^(Ot7J28X)}e5b#1oAW?#!jD>h!Tk+zLaw$UjzKEcK<HdeLS_qJJSqj5HBvC;KyZpG%7Y)->Qcg7QJJlMuyGpE_O#l{-fZLDo-u}vDbwd=-jV9TzX1slKFbvwzHt<AS>?iFqBM4SEC6l_zAZCbTmE>1bXXzSyY?<{n`1tGtykUzqA5VFqt`6K)Y$9@j^w;<%V7rKw|Bm4+I!jJGH{0Kk7kMJY>2tN_iO(V5tcD|!;T-5YpK7L!@ph(Tdd~f%B;rI99i_pBGFC`&d%;%MS7P81czVm!R!$;twxApNAeNn?_?>@dK%Y1w%`DP8D0iXH!&h%NM3UnXf2lxSgfFIy*5%}7%&`Km9D|3G<9#*=$H|8k^e6Pb}DCg&Q<&kc<_vt)d;*EZC+UN4jJMkEzOc&zWF+3j6qbKs{&3F##mPj|ybP*oQ66eu8KKbTkS?O=ziATUojXd6mXW?wqjO6(y9x3t6HF>PfGne8y4IW*VH)->(b#wX;@5B4>F3h`JwDSqq@XToE(|Fmhx8?E3Xy-F|4B2P=t~@(3+W7<?FY)X<z5OuSX-9?wpTM)Sv+jj>L4#+2M}v9O`I}lJqn#JJdQOR#bs>B=o`q<q9T|#$CXerN&a3byr6*^WEy(W_t4^(oPvAWv9C#+L?dlm-o|C;&pUw+!t&7?^J6Pvhbnex3P0tno(S39;tb6S+=X*yv{i~&PK3$iLZ>D2Nn|oIs-SgSrSm)kFhv8c~OXtqgk&OSnu?{DKoT>BY>i85LovSm0b)iKU^mKeZT~tj|Wyr#PS6#~L{OAtrrjJflm(D9cx=x+{=(KhAt##(zb?&3<)&(`)<)WIMM!I-dvy=DZX#K*;o6qO*$iU_^d6<awwmdsBwAss3$xSua<N3q9EH~AR43J%gcZGNRtji-v)1eP<G*2Xu`SgV83%#3>#m*nzN;PoM;Nid5Tk-gUJg33S!hm*Un}{dyT*0FY@?zzdows;2IB|Le&u#N2nFwJaG~wP5H{I{@%i!id96mVx{jYo@oI4E{B`)sbAURw~7e?#&Il6HFJ6}O(YTgG=334tf?J;GjQI=88zUb$*TwjqtFFAZ9?0GqtyFV!tla3UtU(UrpT$qt+k5s8&&P6|5RJa<;(^p*cc`jaZ*%g;P-DSI7DKXQ-)$#XzL1R(uip!b{!Dt|CUW8#mC<GWfU|)OEP{7*vb89dQZ;`<;Iu%AWFwDV(iqLi#1B~x5z9Z>KfZ<B8bXg*lD{I5J28Ma1@FZ!3S%8@pm{GeGGuZb_YM9Ke%Oc1$9*Yi^*XuGorm~Zg%&o}i9xLgSO()8zkj?iGm6|NJ$;c?mJd{i%nS;-n(lzr{*Uan6(lbAkrP@!gaLwvuL09JPp!rU5_lStOzu8_{W>;kPzHsf6h5IgD$jlisvm!G+vd7-4k~WW{+2_*8j-%0Q&@LBj+=bd5s9%P9t$5?><6IGRJUB7uia5Uiy<B|#^>K7xs$?NndNR&v;4FlD9K>1etKt}fO%{T5h%>`*b|2?8a17^%gK=R8N2779hnw4Ma*G-?Y<M)PYiqr5a*25u#}Ex7SpTPJ&;@YuC@zcP*&@{CjwJ?N0%w<S=``vD9PI~B=A$?xgOp#mR3D**%bzE4+a|*&oi;CRPTN*oxIG*`EXnlUl^*i32jk+2ID)0}B94#cQFh{HEu53M8BT<sh6_V+GzvFY;oN8(-yfU`INOMu)Nv_Ll!j)i;iwVkUkS&JxOf6?e%6(9<8Y*o<1wGP>qRj4pk^QX<1=}|l*udDSi%+~o3CW!B6SkeKqp8y^oLU?RczF4!&FeTrMTt`+i)(fD<XgNiZ)+od&+at9=74@jv#3PQ<eGcZQ(qdSYJ{)2<^^i@CA)tnHD6?uF%XgXxu?du~$>%nR|%%ok$D1G%9EWDMejrD9tpn-El{0Rwjm~>{q0jvuSflb4O`W=E5%0<|omnqckIFDYG)8(QDEY2NMu6T4^AC??q`TYm^{X>CUH#laC=ZE@(6;X0rKSyEd)sy>>XA?L&JfntN-SyE^Ulqmwz5Yp!8<iQr@<%{pD%*4Hm7^2HCF4IRqzF2&ccDq;yqQLglLJmW_ft%=AyS42x9{JOm_m2v2h`#yQOoG9EI=42xLI*JIsZaPI`8|@E^vNYWQ&3{T!%7TrMdT91V>43F<MQ;v^Xi1dfjT2-cSO^klqVK$!Em6fD#b&WL1rgsxL5fmPk?x{dig;gCag8WTgFHi&Hqn{ryOH6lXsQyqtm3>&G_{Bra(?VRq_Zcgxa+2@y!W^WOB3QfQpd809!2ghav-w(*T~C$S-qgC0Hq{4k|7)?bIvM2zUmTXGmB0FO%jyCh-M2Ee_Y}g(DBEDl?$^CP-+R5wpWj$cNI`n1Tlc@5@?3wJcf6dgI1X9E1>zuf3gJ>M}Qn;_RaEK87qQP1Jl(-Du2DaT0qAi3PytF0^|Ucj=iu7h_yg-Rad}jkO$B#LHOoLO#>~YbnJoXt2C)aw9zn0mE?eAfJ8ea_f<g9M6x|3-%a9+lT16wRgkEWMAs%wsw7jhfqhOiPgy#T3wb@&WzFbV-sM?~Z6~w5O3Xv#*I*IUzm`$G3F2PU>R_5{vV75WGWC+4;HY?l2*vBLNV3w1MO(1AiN%d9KFng7bGOEFY3LU$bzg+_wJ66NAnZ(5vaCLf%|MndSSfST$~X+yW+T*IEkBTD>R4vLO&E1pB#(G^Sq5S<=DJtQ!iFBN7DoTD>lk(bH2V+uW)>^6(zBrKE`Tk^ut}b2eQ$AN^ttyYjIe50WMu*98Ge6B7E6|s?Gmu;ImmJ_b6}Nm_SFh?tQ0t#VOy!o^7<?W7A9C*$x11MeBDO|!IRKQ7N*2wq?#aWOZ{q1`tL0~;UO9LH1cS49Lo=3l|3aBE1f2qk*qL;WsBZ~4k#zE=JQzY!#ZhWa`o8Z0V%H(yv7kRwrkLCA^bCP0k5v|D?fdiHi-Fv*H!U-U7uxVu{^<KnRbGA<_HyOsa&B#Lka<6zTGfY>_nw47#Ap(seu`aE{XDcD1t0N3y0;C?2g%svN|X(KKdDoB#I@<%NBjTyOb~l<pD(nDph_)nMP~|uA@ew2v8}<t_DR48!vYlg|DDkpwgU^AXA-K{YrUFlv_bz5w(FBlrQR<hHbizpt6B*p+I5cCZezvm>C$(IF6zM#VaTyI|FZ{o^|^Xj7)R)bU2m~H7g6kQ`219L)k`@jhZL}sCg4*TTsncs`hZp*5s@j2x=k<gM{XeB1oxGMp-qK-$Z4jnzQC0Q8q8@d{Ee^hQdRHZPdJUrRb7ZDz>0VqUKFh^MiubQ1cSX6)4+|YQ0i+8jf-w)S0N)4+}n|{_FdzMqPv_O<)<Nd%c+F0NGk=Moc;6my}@^VHrvDu<U<9nU@o~r(z*Y70nqhEVD~7wNzvGBC;~WYeTk@tTs&M)MaKV5cSG3vndO!*+SYf4~cSWvI#a^Sw!^JWZ7!b$${h(<iKJQ+bhT>$hE=29a*D@Q)NL#=8HMB9{M_YutvzId<9u3WTB7+DWlP{Sw$8hI%A>oIFoUjApS}+hDa32E@K|z22YTgP8orWVH=&UR**@(uPJlI3|Cjk_#+z}?tZ?E4!^0dE<64{`^er+_69M?Tsps146;&psp95mvRq?!;<Z_eX^2^#;$nK@SQcxss9=$tfkSY1{R*s9wVbi6j2hdKtf<4{f@PLi4yK`5Xk>O(7C{$KmMns_L<hgg`m>E)>i4p;?n7Djn}eEk9Ay_quk#1846t}Gi}YEkzfD+TrBZtfy`?V9;w2V8iN$IxD!S7Ki0YumKsUWq|95Q`udq_h_Bkx4#<CEtU+fKN?$^w~DNHJd7+Y7`%d(p+3oM35WgJ~s%7+^VSU4M-;ce>*mIW4%xd~5U1(*<JB`e*umn@gXR9IeV+=iw!N8OIOTB@wj&Pv~Zc^0iSLp+leHCge)8q1o0D-pzp)PARY+_IwIq`bKScdf>c&!TN7GG;vzUyHVu$yoMD^rzFPo91PT&RVa;t!dNhG&?EMtfZCw61Rp;>(S^zi$`UPxs0^gGVv8;4DV@QWRG#tHIcUmO{*2FE6Qj|Mk_Ki=&b#*K(^)~bA2*~mXN&OJF!i6d@*SsM@XG8Ct<t-b7Nt%GAzA=;|k0JEDXFCCoDi*Kl7V+Pg@xJth#kqfIBe^ykJ4g<-moF=~(u=46wHudA(TCg#)DL;(Foy?EOjSYT;8&mxVrW*npaf#)IQszTcImhZ@<xF0HgOR~+c_DlS@b*(Fzm{+IELH`sRl#9ZHbl~-K0$922`aF>f^GtbQB;d;#{-G@5Y3rA6+%gW<+g2UOtu35!3$)6ux49)q^b3In|T`n&V*4JG81lM*3{yQ~OyhjP*GIi<?$Xy$Fh4IRlFl`h~Zw+2nH8}+n7x7ardiPC5>GV`HV)?LX(lYtNWTD9-%ka-sGi3RYY0@#Jp*g%_Vwv$_AiSz>3dc>nWTKUOZ_V`GKvJ!dqWc<he$<o}xditf$wr9;efw}Yq>=UQ-OFBF9^SJ0luUlb6d+-&G<~0Zs)cOa_vwS0Db$%5nh=^r6ZdRSh;>Y<<6vg`deC`kqQXRKA*fE1g>-W4qR4WJYLK_t42>_7iPgeSDkg?1qp~&M*N@{NuvTU2zW3(CV<8<R$#0VkkW%VInkCI@y#|#?8x0gmlB^`zHPZ2vZ0aIe`EK1Hg@R;&WE4o4?MUu0iQoVz>oe%!9UGz4-oh;5Ez<EWgMFl|O<hUC8`2h}8Awj`#+z1m_H`tJ-T)<uC5b9YUB$kT;d_`AH%YT3#o}@)TqRKrr9qk-Nmic}pHHG~QuB@H&LH_7Qdhgg4bnTcOXTk-;eB0_TZ3*~>|(lCZkRa2=GLQpe7eo6*ruf@Aj@bUy{OHvr%`&S06yOqHE3?BBV=m8cRKC%P6$V7_%`!*jxDBXdl}t)MH&_T1(D{?evpi%5foRYjptcy_@Wjq$Y%8=Eu}1<NsDQoayt!U0*f?rGVRfb&#TZ<Z#SIToY7L}w=-$;Q5wO^I6^8{mUigRq&*@a?(0!<nC9*e{0P|#S>~aaRaIwo8NAV~1}#7cDw|;PB-;0iq=)8V^iPD-EH4*YCv^laXrw_S=qloXHa&%Qdkrvm&{%d5i1NIJ<+8+_PIF2$2eSn+Hhd<HL}3R{eY9B6jErkdFpB%UE{Z>BUXL~}(R>H(_$&MNu@6UO7Lw>wAbdk+&z8lbG9zWQC!;fEepB{NZ4__yIXCK$<SGA#ofLP0xBtM4q$LhjElzs&#kX-e<waLDYp6ET_?-NrgZT^-9EPyIYOV75kctackU1g~43m3g<g2Qj`BKGB)LJH=gE~}#h#o=q&h=5YXyqB?OU+A^RY|AHQ1&<qKP0w5`E^vvJ@Q&PVi}4wQ30x)J){?~tdz)5Rugsm#z*E!56M)M0_5^dV@Qv!Mn5SQBpfcWLDCCU-M(?^BssY8G7=Xg9Oi<#V@8$a50f5g;`cz*yhNHIK$Ve#7KuzonmS2Fl6aF8VIq8L#AVdd-frI*R7i9unIhkEh7NogDXNj2CW#wKGbAmhAhA(v{CNAu^$7hQ$;yVQ87V;azkvp;8OiF9a68;VGBWJqW$}C{D$fnXIq061L^`Ahq{;M<CKxc~<>a4G6rCFga10~4FA^Ol`6W^|{x|~3LUdG>gyWgUkZ|%_IF)p}b?hLLUm@WQ`C_E$illeyg81X`&VI#Q-e;0Zz3=uPdy(+pV3b?=;j<QqE=yR{MUf7QS27YE#4TCIFGQx|g;8!Dg|k>O6KB#X{E{eMPp@o2Wg}opl$BMy7G|z!R2|Nk5Y>Y!%iL)R6(E-_D@`{0DA$U*{TsSoRFMDjuDEa+3hQ`NQdo{kd%#;FLQ}o<ZTqN>nu-gzhQf5PUKEM+r)knbnLElCgPMbEwHa$rQ|py_6nM}VD)u}lnoPX3u(#?a-(zA3et9_B&rH6U>|mf8Ox1KdZ0j@8iiyD#WjjL;0l*3qH9jSNm|~B~Lio!sje*Hb4iXI`X5(ch-)ds)G~8#(rdv@l17^{L^~p-tNn|xmbEj$EG&wLC=zVG-&TbU06XEHUH-}9)*NVYJPcUJq*4us($sz5SGw5W|H3JFT<LNyjZYSe(m_(8k3X;3WX0ggU)R2xpA#NmIk89SF(gc@Xl9d(8PVFk0jAV|HtR&6Q7z4MoNHVgH+^Idsv15>T{Up;(VznD@BnfZ4`8<-@Bwa5EcwBl*y}eN_UAIDcobHK@39p25n;i(bzB6GbYEnR9pSX=t%2ecQt+pnVC~8HS!@XTf6Rns?c9EkZxR!sUf-u>J#UOug7}ZR6#bl+)f{7PR5l!<xX+qL1ucxa8PYuaHSTiHh66ulC!s&#6lN1EWbT&%L{`sdO`)ZqH7fBXLVV@L{#FGk%>PQYo8g7vYNq(O+3zE?yxg`>>kenoC&%8(Xy6+0V9g;Ih>h91rLEbMFBpgz1)=AmB>5+L<NwP{L44ac2us~46Imt<)z8J+&t|6XDVrU9!WtO^!u~h_-bPu0BH;m*DlL&sTk-Qv#<Y91CDudL$@unV<g<|fkLqC!nWXlFg;>E{<Ah}kO?If8Nl7Y!A9?nqnhq#DR?5|uMiIX|sPqIJ?vL~T|W;7e5ED46h!gYV$>YN}M6%sFz(h;EtQiKe9)*?~9&gFiRgKYEcK+(gIR7v7}l5JQ$K%<LeZ(0<Q6lJ}qofH{3w^|UzHqqnhK)y%BQp9i`fcsZ3NB_)HWR*p(N91IZxmyysby0*_guNmbhoC(od~{<|Oea_2nTVx``aee=yFI*6J3{%UT7cTMt^0RXgtb>L_-*FdTHf=@eJ^Hm6~(>_F~B|(WUK3%{8EoTYy{_4rjV4SzB(rAH-)7c$ElatB-b6-kC1oP>I)`X9h%@%k(vT2E=>T&_Gm2o$zV-zFUcdxA1<?86lJ~m(s6K*d47ad%cV%HQ%xyyYh_f<-@pH$h-Ee9h6oG7oZSA>P6Vk!^vGv$S|XewfQe%yMWzrf9{P5O#P@57cu$nIt!onTqUiCsGxq?Gj;L%#hi$<!(WAxFzG%)wv?ltFGk1xwLwJ*jH$+pL=#h!^5Shczx&Vcgaj9WojfmAmZk))22tNrki0r<|E{axH<a#1Zk;vKuCeZ{x+>Xevirk`z$BJmFk?(w8QB;XSCbDLS<g(jTlT;44T_jl;d8<mIu4e-mpQLS)mm~*CzltP+GQoo+tnN?6)EUW25(9}ANwJkQVIH#@DMGsm2i?_@BmjwONoJX}dem;6A}K(IqAU8LW+dJuJ#r3fNunQ(8p%VpZ$_d!DNXZmFF~4MpWq;_cP=Szi7pr8E1+|&(_#OCt4<n*lA5_{dGX-!7Vj2*IU~Y%ZPQviKVRg*VT5nT6c<gjmaOAQ#gsMkTRiueip_mCD@M&^pt4cN#Dyu`SL#@yh^O%?rn%h6_nNSi-=fJCrWC%^FhL4Z>@;zODJA3Kl7rwVSjA*3w^g<>;KI<yk7TawmuZHh(^UPH4uF+SM#Y4)tVsqa(tZn%gGZPgo?z>ku#aD9ijYwj<O#OEsq5b33R4Q1t(mkwPd?i%9yDc@xn9m?z^YelV(sO*yp}1bnX=@ZD0_Wk#Wk9&Om$H)iAfB-rU+ZzvOOWg38H~{Hdfg*8D$eg=eso%Et#yIi7G=CwI-6S?_4prdxD%sUknx9F@-7<>zG)Y!lnr;<FnbXizeG>a#(WRWn!p%jVrw|(d581tD3x;i3$@z?3`tTwUo`6jU7H@vTLTflVsu6n}K9x{umb|-Xl>XY1SecNs1Mu2wgHqken8YDo93>q9(~3b&_o-g)WjgM7mz+@38ZGU19mc?fi!6o>$3xA(C79(Y;KITlo3~NxW3W%QEms#RRLclG=9(5-k<+BFVur1hdr_)8P6^Mup^8`rUa*f<sb(v*TXUW3e8)NLkebp21};{8Hsj8mN#`m=<S}u+3saJEX_zLW{&eT1+VoFhL>0seTI7<Roq*Jz8muCXpni^(+@@S-qtEkY0miS4g}<B1u|*)lP><p{InmUSy%^yWJLXqsVEBLLuUH5iN<R6uCx`&k`wgL=mR<WC2X<{Fc&P>O`(e6wVO&B@vcNVK!hcn%YFcWPyp$^JLf%@ruYwk=wdPTy>42j>yT!cPVl*Q;CXJPphJ-Q54if6C4(zh#Ey%IUAIx)rn?knzpfnuL3y$8Hk1<XqGpf!KD2ikgfU{kqQWN9Z05=nxefJ74601{r6J|ijAO23xtIv$3S)w6dFNJ5oA|DQvtG&&t>j`bsZ4ZMZu~-rUjIq?>nIUT&(&E>42OJ<L`oK59CZE$U{HP7Ygb%J4GX>@9o86vE&8%^F463>eR3v_so30E2-RGMxQHY-D;_#mWr3!2`&!k_45DaDsuYfMpa&b6V_^6ZDqTvtj9z-%GN`AGf5OHT`FIqqLztPOgI42$!1+D7b>rdRWPw^K$T7B^-v>`nY12%PSfPqO)SR=Fq9M#jMq}W_e_t;LKrqPWwoxEiJ<r0+5uv0G?_9{@t|p{GX-g~6{g0|lb_29Fn7%4_e`Abg2ASsW(r{P*d1{xCN|XMG)<Gt;<H6Vf+!2A(8Oxbh)3-5kx+WXWbP+oP8RO6JOqf)SI9xEV%ki;Y`spTY2qal%LMI+{oblf9oNZpnzHIVD@{%&GjoHf^;upVsvS(eOr{B1{cf8Ws$FYMbqR2J<ouv1ZPh)P?52sJVPWmP7aFgVnh6^dFGiXj6pmZjutCG*^Yeh?iNEn4h0S7SER!#17>@lI5Ugslr<(i`6FkcsO|dhVd4~Gdv`)41Q9dn^xc(90+a3{WBnu=XpAd_rhTW5I`!x9%jQ}2VUV2DxD{h+WaL?=5cOB7o?2nfM8;d!8&7!C;s!8eNr6CrJvw5!|$};-0#HuI@Nv-VFR}SWdSJtwK*Pid+BHJ%YV>kSY$SsMilE_;%QC4-B%|>PjP%zwVST40J3XRu@l||{G_khT$+;wr3XmK8Dgn~(|`oc3-?p!BL!$o#ol;#48wW99(C?0O*l7X<yxQw-!YS8XYxAXAs0tF~ZSp&@yWOqTW_Z*D?McF1hD}%>d&Z^&XegtTiAio5{vQ`gM2YPQg)&e;R!sG}qyQnebw^$H=hoU>L(4+|ROCSpY^b8aru=i*I-w6sbzoi$H%GL-9^E~9eU<OiZQ82+5dqG*k&eRFAP}~~jMDbmaSp?D1$95Np<S;J0<*=9CEYlJ_oC_WX?G%4%g6299>4LH=WJZ7{2{Hh(yC6P#g-kyvw1bQ`$QwmatN_JzkW~TMD$w;}c&*NbuI|^3;SIv=&3_&k!@G=VEryqkCEA_2(JW$R5z81}*^iGQ5*B1C#c~YqxM;hJPP2$sM0kLKC9Ej`wl12gL@pCizlb1)SBmV4$gYW8qbN@@IxgZu6jnqY8n!2q*}q1vO5`;~UIv6h(T6X{4t1HxFN&r%(IdHyyo$&bB9;}oRz@jM6m~>hC8Eks;0+?G6IpoHMc7K^qDS#&Ra5=ISt8Cs5f|^58j)WT<sqV&b&TE<`790RpopZ%!|0Pm5kZbYCd%r-UDmFsx=y1T<cd7KDF2ui?-=W%J<w#EK+#rqKjZp@Ymy+6P3aedcNoT81;r{5RkjJ^`oYw;0)zo@w++ey!FwQA*`>V}grS9c(2U)yGEjPMRn@e|paZhS&|lsInH7*-yFzs!uFJaNnjzabOBNeH1n^L+hh@lT&*QZ`>C`R_)|rb&dr{UHqQ|azT$?A<)vZ=}!jk8)0+62c{Z7VTRy|dv-!WDdMUL^rCQnrv?o2W;)a8jQp19(fn>^-99($I@Re3HKzH4QA`R&$Sd2H?|oHe7vcUM>O%218PucsZz6;)g$u6a2OI0agQM5bP7qgB+e^0L-;f_YW}3UDW=aTuwxT`DhCRHztMPN*VXRV-EU@W%>=TKS@6l_0>{h~n-`br8jSD7%C*RVZphO(n`5Ly=7U3KB&U#WLG)4`tg>tcJoUWH#bpf}*=@L`5CSw4t(pgQ#MfU>ty3H~C7Fo7+sLFqvZ}Q<$hQxx$os?`@i5lj*TrR5Mv=;=+_orBydA+<WHOI|`?npowI$aey93)h7Rp>%=h7nC>Q)Q6vjz7X;^oX5ZBI-i=1r<W@|nhe8BX7-Y)6eL7|$d3;&kdk#`Vjoj>4nA(;Sv2usMZ!)r*^;|UUurd(mpv~J}f=Am*BFu^=FKYyioYaRIuW9}+4>0LnCtG2%a^mg`8FrecNy|j?kPuD2*JQe$dpah+Zkpx2_eLffYNFSS1ajN5HY{v^%{6=R4U#=K3V0b*O)W0Aw9`b*YA7y3mQ#^}<RSLtWX<O$s%;+<yw=`|i-6^{lvagJog6$g2b!kCYxXi}$FG=3Hmy@P<?k*{Q-BO~l3n<+hE#i|&~}}I);?r0U2M^0Ae5fcE;dbVd*CoBnkE^4Elp9zksSQ3nx?2?vMVO6{Yrye41A>OOw;pBn0$%7(Y)*$mYM9n$vxw_XNnYAQ)H66Vlo9ox`?K!vXp4w<YYCPS;|bBp^DN%ZEM&uao2U~HCc%KM@aqOHpSX8afhCJ$4wI?Ax<(B7@$%&!Yx;AYCH4@q-F9DC&yG-TbLa5bxWH_O%rRG0>q2ZWMIBXX);wN^Q7w(WsNRD7;IWH89Co!%S3JKJ+Jn8n&qf!D@|C2oaKm_-Op32$*Y@ek+QpHGLV(JX=+=;dZ%cbmrQoaWaXvWdFN8wdatrLw8fOAR#RbOFwqE;8*SoE6F<*%x!7MTGY_x3L$SYXOv8}a-yqrEU0HT?!!Zbcsod2`{$)`fAeczzi;CAQ-%J^mXDS_xlX*Eg4%_TGxpBls+743BHc@SRV4o-T9NaJlIp7al>NB*<4zL7qkS{VAMV%-MFJ(mW3Mwu1HBs53#2+(7X~OOw8m6|L$TZMopv4B(9Hmm0T9a*C4LY5jNR-VT4b<#xm{L<Q(lrG|lRIkKdGXq|Xa%#PiNQ31DavA3FWX?+-IL(9&6U*&lm%!F#!$X*A<?-c*&!s-xk`SCL^5~#IH@h1X^j?%WiWXv2GbH0C0lufutRG5EICC{IvGp@Qds7tW0^Hp(W{EQmdL?^m5L!=r6|3a+^(oCLS}SDEQhRRhrdxCR;6{Vy`BiSN#(BzhE!lg9jiiKR21M&%POj_DRO%vFLzL`a&voO(IhvzZzGzXBl`LO0c+fzF8"
)).decode("utf-8"))
_V24_BOAT_THRESHOLD = 4.0   # true copies measure <=3.3; nearest non-copies >=7.3
# The public meta's opening is fully converged: rival routes are identical to
# ours until ~step 240, so family detection only counts from there and only
# acts once the builds have demonstrably separated.
_V24_WARMUP_STEP = 240
_V24_MIN_STEP = 360
_V24_MIN_RATIO = 0.9
_V24_MAX_ACTORS = 13
_V24_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_V24_ANIMALS = ("COW", "SHEEP", "GOOSE")
_V24_KINDS = ("PASTURE", "COOP")
_V24_QUADRANTS = ("NW", "NE", "SW", "SE")
_V24_PREMIUM = ("MELON", "STRAWBERRY", "MILK", "WOOL", "FERTILIZER")
_V24_STATE = {"last_step": -1, "hits": 0, "total": 0, "yarn": None}
_V24_C94_STATE = {"last_step": -1, "hits": 0, "total": 0}

# Boatlee's scheduled sells per step, with its RC2 relay shift applied
# (a locked copy sells hour-17 fertilizer batches three steps early).
_V24_BOAT_SELLS = []
for _v24_entry in _V24_BOAT_ACTIONS:
    _v24_bucket = {}
    for _v24_order in (_v24_entry.get("market") or []):
        if (
            isinstance(_v24_order, list) and len(_v24_order) >= 3
            and _v24_order[0] == "SELL"
        ):
            try:
                _v24_bucket[_v24_order[1]] = (
                    _v24_bucket.get(_v24_order[1], 0) + max(0, int(_v24_order[2]))
                )
            except (TypeError, ValueError):
                pass
    _V24_BOAT_SELLS.append(_v24_bucket)
for _v24_s in range(len(_V24_BOAT_SELLS)):
    if _v24_s % 24 == 17 and 281 <= _v24_s <= 665:
        _v24_q = _V24_BOAT_SELLS[_v24_s].pop("FERTILIZER", 0)
        if _v24_q and _v24_s >= 3:
            _V24_BOAT_SELLS[_v24_s - 3]["FERTILIZER"] = (
                _V24_BOAT_SELLS[_v24_s - 3].get("FERTILIZER", 0) + _v24_q
            )


def _v24_position(value):
    try:
        return (int(value[0]), int(value[1]))
    except (IndexError, TypeError, ValueError):
        return (-1, -1)


def _v24_signature(farm):
    hands = list(farm.get("hands", []) or [])
    unlocks = set(farm.get("unlocked_quadrants", []) or [])
    positions = [_v24_position(farm.get("farmer", (-1, -1)))]
    positions.extend(_v24_position(item) for item in hands)
    positions = (positions + [(-1, -1)] * _V24_MAX_ACTORS)[:_V24_MAX_ACTORS]
    counts = {key: 0 for key in (*_V24_CROPS, *_V24_ANIMALS, *_V24_KINDS, "WEED")}
    yields = {key: 0 for key in (*_V24_CROPS, *_V24_ANIMALS)}
    for row in (farm.get("tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            crop = str(tile.get("crop", "")).upper()
            animal = str(tile.get("animal", "")).upper()
            kind = str(tile.get("kind", "")).upper()
            if crop in counts:
                counts[crop] += 1
                yields[crop] += max(0, int(tile.get("yield_units", 0) or 0))
            if animal in counts:
                counts[animal] += 1
                yields[animal] += max(0, int(tile.get("yield_units", 0) or 0))
            if kind in _V24_KINDS:
                counts[kind] += 1
            if kind == "WEED":
                counts["WEED"] += 1
    return {
        "workers": len(hands),
        "unlocks": sum(1 << i for i, name in enumerate(_V24_QUADRANTS) if name in unlocks),
        "positions": [coordinate for point in positions for coordinate in point],
        "counts": [counts[key] for key in (*_V24_CROPS, *_V24_ANIMALS, *_V24_KINDS, "WEED")],
        "yields": [yields[key] for key in (*_V24_CROPS, *_V24_ANIMALS)],
    }


def _v24_distance(left, right):
    total = 12.0 * abs(int(left["workers"]) - int(right["workers"]))
    total += 7.0 * (int(left["unlocks"]) ^ int(right["unlocks"])).bit_count()
    for actor in range(_V24_MAX_ACTORS):
        offset = 2 * actor
        left_point = left["positions"][offset:offset + 2]
        right_point = right["positions"][offset:offset + 2]
        if left_point == [-1, -1] and right_point == [-1, -1]:
            continue
        weight = 0.8 if actor == 0 else 0.25
        total += weight * sum(abs(a - b) for a, b in zip(left_point, right_point))
    counts_left = left["counts"]
    counts_right = right["counts"]
    for index, (a, b) in enumerate(zip(counts_left, counts_right)):
        total += (0.25 if index == len(counts_left) - 1 else 3.0) * abs(a - b)
    total += 0.15 * sum(abs(a - b) for a, b in zip(left["yields"], right["yields"]))
    return total


def _v24_boat_track(obs, step):
    state = _V24_STATE
    if state.get("yarn") is None and step >= 168:
        shops = tuple((obs.get("town") or {}).get("unlocked_shops") or ())
        state["yarn"] = (
            "YARN_STORE" in shops
            and not any(shop in ("SMOOTHIE_SHOP", "PIZZA_SHOP") for shop in shops)
        )
    yarn = bool(state.get("yarn"))
    track = _V24_BOAT_TRACKS["yarn_on" if yarn else "yarn_off"] or _V24_BOAT_TRACKS["yarn_off"]
    return track[step] if track and step < len(track) else None


def _v24_boat_detected(obs, step):
    state = _V24_STATE
    if step == 0 or step < state.get("last_step", -1):
        state.update({"last_step": step, "hits": 0, "total": 0, "yarn": None})
    state["last_step"] = step
    farms = obs.get("farms", []) or []
    if len(farms) < 2:
        return False
    expected = _v24_boat_track(obs, step)
    if expected is None:
        return False
    player = int(obs.get("player", 0) or 0)
    distance = _v24_distance(_v24_signature(farms[1 - player]), expected)
    if step >= _V24_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V24_BOAT_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V24_MIN_STEP
        and distance <= _V24_BOAT_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V24_MIN_RATIO
    )


def _v24_c94_copy_detected(obs, step):
    """Exact-family check: is the opponent replaying our own C94 route?"""
    state = _V24_C94_STATE
    if step == 0 or step < state.get("last_step", -1):
        state.update({"last_step": step, "hits": 0, "total": 0})
    state["last_step"] = step
    farms = obs.get("farms", []) or []
    if len(farms) < 2 or step >= len(_V24_C94_TRACK):
        return False
    player = int(obs.get("player", 0) or 0)
    distance = _v24_distance(
        _v24_signature(farms[1 - player]), _V24_C94_TRACK[step]
    )
    if step >= _V24_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V24_BOAT_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V24_MIN_STEP
        and distance <= _V24_BOAT_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V24_MIN_RATIO
    )


def _v24_boat_frontrun(action, obs, step):
    """Sell our stock of a premium line just before a Boatlee copy's batch."""
    orders = list(action.get("market", []) or [])
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(0, int(order[2] or 0))
    shed = (obs.get("private") or {}).get("shed") or {}
    upcoming = {}
    for future in range(step + 1, min(step + 3, len(_V24_BOAT_SELLS))):
        for item, quantity in _V24_BOAT_SELLS[future].items():
            if item in _V24_PREMIUM:
                upcoming[item] = upcoming.get(item, 0) + quantity
    if step in (711, 712):
        # Their wool controller dumps everything at 713 and staged terminal
        # batches follow: flush our premium stock ahead of it.
        for item in _V24_PREMIUM:
            upcoming[item] = max(upcoming.get(item, 0), 999)
    for item, quantity in sorted(
        upcoming.items(),
        key=lambda pair: -_GLUT_WEIGHT.get(pair[0], 1.0) * _BASE_PRICE.get(pair[0], 100),
    ):
        if len(orders) >= 10:
            break
        if quantity < 3 and quantity < 999:
            continue
        available = max(0, int(shed.get(item, 0) or 0) - already.get(item, 0))
        take = min(available, max(quantity, 4))
        if take <= 0:
            continue
        orders.append(["SELL", item, take])
    action["market"] = orders[:10]


_v24_host_agent = agent


def agent(obs, config=None):
    global _C94_SPLIT_HORIZON
    try:
        step = int(obs.get("step", 0) or 0)
    except (TypeError, ValueError):
        step = 0
    try:
        # The base's operative front-run is the debt-accounted fertilizer
        # split at horizon 1.  A C94 copy runs the same split, tying the
        # exchange; against a track-confirmed copy of our exact route we
        # deepen the horizon to 2 and land one step before the copy's own
        # split.  Near-mirrors that are NOT our route (Kaito, Boatlee) keep
        # horizon 1 — advancing two turns against them measurably loses.
        _C94_SPLIT_HORIZON = (
            2 if (
                _CLONE_CONFIDENCE >= _V24_CLONE_ESCALATE_AT
                and _v24_c94_copy_detected(obs, step)
            ) else 1
        )
    except Exception:
        _C94_SPLIT_HORIZON = 1
    action = _v24_host_agent(obs, config)
    try:
        if _v24_boat_detected(obs, step):
            _v24_boat_frontrun(action, obs, step)
    except Exception:
        pass
    return action
