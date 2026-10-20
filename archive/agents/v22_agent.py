"""v22 for Kaggriculture: Boatlee V16-RC2 production core plus a
copy-detection/front-running layer and step-717 terminal liquidation.

A high-output production core with a guarded, debt-accounted,
three-turn FERTILIZER market relay for near-mirror farms.
"""
import base64
import copy
import json
import math
import zlib


_LEGACY_ACTIONS = json.loads(zlib.decompress(base64.b85decode(
    (
    'c-rk<O>Y}nlKd|^^I(#)Z0}8NbEbt+TZSwzG20Lt4a_VSSj--J_qN#ozOqEJij|R(k@;Rxvd1@CCad1}%Z!YS{Plm&{{8nq{_*!e'
    '&i>`svrm_wKcC$%&i>=~|N7g1Km6h0<3E1?<3IoYKM$XOJ^T6UcJuJR^uteI{`%YH$E#m1ug?}|?{Btei>3MV=bty5PiKqs{eOJk'
    'Y(6~vdHeI`^6qT$dh+LAHrF>FM}Piwd-LJT`@8WE?*DIb)QhY4fBEuh^!`JCem&c6KHohy^zdQV=h4p&?HhOBd&jO3$8Y&~b9?vm'
    '<3oo}_C33w()a9|sXqIsFIU$eetY=m-'
    'IuQuLLNN%rr!GN%lDhZAkiV(ee>%q96kTxKR(_aX4ZMnpT>)Vz2^9fM{|97x4HG6|Nb%<pr<e3aoP7^|I*QOcVA-TGTCJ4aYNG!Q'
    ')^!^JPs^-eM0SX4^Q(4M4m|d_|G?Ab^{K^Bb-'
    '2goQH*Hhodroqt^N3&@_LCQ_GG+%ls(=(lCG0xK!qG|64E|PaUW|Zdh;AKh>URhqudWVBK$84f}^|E;}v)Wi&dkfu|3N$00i>ybi'
    '*Z_WtJjdh`D7w?A!e@2;+|{_U}u_C877{)KA`HG@20f6JvB3f>wvG#H&^v-'
    'f+q=LA(YfBnGt@sl4vc|kupJ`+E0uD`l&qn+~Pkzo(e_-'
    'GgRDgWtUg~TV1Z~j|9Yf(GOj6ZZdG_b?V`{Y?O=|{`$FkFh2hJy1Swq0qVf0y7k#y>a16dv+>`=IkMfx*Y4RB7PU-cK!pk=ImswH'
    '@F>6NUjcEs)0-Oq(;nVFQ_GSvX3~5EY(r7$N&xb%ek}@c@-'
    '?i+`5iR<F9FJMS39Tu%P{`R?{|`_tz3_OEA)b@4KseCU2D_PQRQ=b~)AGWYK3Xr@|wBDrD<092N*RQ=wtjkCuZ9+76ZYI^-P-'
    '4np?qZe_H4j9-'
    'oJ3?R*5!M;|l8S{iERWLjhK9NLcPBH`Gd(mT#M%oJOt9&)wFid_KouJ~0o_`zz8??i^N=>XpvmJUXW}$m`s42J<u121KIst_+id*'
    'jqKoD@(qC8a<?X)~E-'
    ')~d<eDgh4ha(nJQM`dDo*m$#g>}0JK(kD{2Y^@yWEG?NgW@)jXiK1{m#emnrsK+o*!;yWkPh1+=fHtS&~9wl|Fy}SNHzpe)DJy*W'
    '7%E+@yQ|=WTSQx~DX~{#O~}paF6~HbU%z#qMcrDYY9M&ut+f2lE8x0wIU_c0+t>dxWsQqwKFlb+qF{*kc1k<E-'
    '|<+6u#cdAO3EKD2G3>0^7qIu0sw0;D_PinEwNiz}|8Xf4+w>t=mS6}aTY4`~Y17~;{1X5cwNg>@cOP>gl(nwMo9j2)6w*aghp2>n'
    'SPhv)*L<nO;k_<=z{4A<y2@WAuz4uG_fPEc&4ZU*QPq!SGNwleO_kV)7c_Az)Ngb(^~d-'
    'Ew+2gJS_Jjt7z>)lBWPVn{K{d>50KAgq2okbhatBD)B>KTOIKQVJ~=r$?$LJ!Y5EH?eg#Az8GYhba7QIOzed)^F4Hc2c{<*KwXqk'
    '=1db9=-'
    'PcnN)Z+%rqMX_OSR6hN~oq9BhyUgMRh#Zlx4&YJAfcRHi8HSV*3Au2h<(}Le5Kg|mCp!cdiU6+>XAQ4D!^UaUBY)WAMIiurr!yfs'
    'S)ipi*=?E+^-J-=%3zpaMWq}Tr9Q&r`XArN&n=`haI+Kj|uR>EJubr-hQv{ycS9%lG<eh-^9J~*%=#6S002-'
    'B9vtSAM#&g2tQCP?ToQv>A=3dlsSQ25?&O0=W9r#rCNSqjlcwyM6zs4TaGN+vTRG^eet^|Q_?Sm(?!@^1W(uFCtN4o|+_F!;-'
    'xcc+tONBSagg<2Cqp!CFp~1cYZx^qTN`#n!yo=ca({A?Zyu`C{1bc8~db&*u?5gyPDRYO);1R@t<q9HWhic_IR4d))m0X$OzP4l3'
    'l2YruZhU?p23EKDSN9##b5-{#<47tgWY`6=Ce$nrP>3Th7!3$nShYpL{T<Uv$Y+{)aR^?IG3o@`nnZfAX5-'
    'W>>J&W~ZarrdGWmH5Wfhplt~Z=}S1^l?wRN<l71|uI|AEOmyv>Zg>pRDbhs7sC8}cw2ETJ^<LbQd$b2eN=z_s&F1M1;sl0wNz<+C'
    '4Mtm7~o%6h7vPGIyAC!_~cb9zHB0zzzyiOf`Z7$VeQ9^>GgVi-@Y+Kc-'
    '<&jW}I^|k&_X!QSbb^VvGqkv;3%U9M9c+(n3X)^Iwjs?U`eC8iS*1iCsOZGaZkYr3%ffXQ`$2ohsJC^{p(cW~GHm$REBtovDo3R7'
    'Qr9c*moWS@5uW(8x%a)wxbqF-iK@qHbHZHxK5NbmX3%ame8loIvX@m{~h;mfYVF?vH42{JYzS%M^IV4=PO}#w41DI}PJ$BeAYzUB'
    '35iLP851rEExpy2aLBrlk3ftHS1jwZmgR@O=EpaEutFul2(R>&`n)yTha;D(2pMgD3-'
    'apa0nJGDJ5$NB{_u9E*470q5QM4|c=)yp0?CfI9HV9o9WyeC~Z#p<g;LOt<BpbU0Ar<zeF2sFD1WS8k(0HFx-'
    'kK+1kD{$>hY$`z*7`4U=xR8Y?V9!8`~-H#C~WMCwT-OC@X*|pV>eaq4q{<qm)pEUkibMm^)1poQsma=g~j~xo+jvkfV$i601MMe)'
    'd2*n3dXEj0Cr1&)<gYyQoLX$yc%fs2Nq9wG5|9eb(YT0WF#uu%&<>@aE;7o-'
    '%WLxP8nBXGRZ_a5^oklycrhGE*AwlK2Dy~CQeP+nJE{Z_2P3Q-n!ffg)9l=-'
    '5pAfNXU{Iv26NnR0Y&Jh?#<rNs{pYA%5va4<TftILAr<oUC&2wh*S0VL@<U9=3uHG~g~p%YHm#7w-'
    'CgcY^gzLWz@af`MWezBp2it2H`$xuxThF2?`&v<Ud@Rt{<bnD%+hLB9gHOoJwpih+#_QM<Qj@g#N$%8~>t0juO|Qf7f3ju!$RWcy'
    'TKnWDW=h&HFYk<h2?x5$)kgfo`81ax*kB`W*NEx|ZA9ciFPLgguOI}OR}3BHL0WC*@dXhci=JZ~VG@@pxF+cZLHs3{pRE!(o0Nvd'
    'IPCx8wZCV+0Ra-Rr}HUmYXJHDi(btyE8GIl4h65V;%9n@hR9J%o?fSykY^RaknIfI9-'
    'TRXS8WsCM2SXV_w)sO@%P4Obws7)fRFvZMF95?cb@J5Bx%w{*<M<Uh{Z+F|U;n(}zJDV6lIrik<s*O;HYUOqV<G-'
    '{C_e7|GC)tA6S(Eq=il0gg-r^7inQ2VLT?y<j3QH#fEN<P?V!Cxci!$VNL<FWjZ0jWB!)oVL?%uiGo?z8IW3wvx&?gw07A@#k-'
    '<Weu*)1t`NKD-aaXuve$em;R+woDka{p(kJI`<L72!%krRNTZ9R`=f(kmk%$&MA+H78FKPzbiq<?f@21hF{H9N<y%KI~y-'
    '?Iv6zXsR84cf1j`5E9&R)qG?xzpm_Zre#p!071g8B&ZUP9}yAvYGNeVyxjipC-'
    't%=GzB_h_Uj256cD~7%tC#LFz+H$wANpDTl!!jiHEF;Owl;9?l3tE_)pw3?<*!mb_M4AW#vk1MQE&B%28jUm9-'
    '(fmCTvPBdCUQMQ8Ka3URLqg_1Nj@!knhU*`HbbL-nl+I><INJF$V;wt;^O>Y?zxm043GHroOys~2&66JE?Z;{W;2t<{(CH&O|=RA'
    'fpZiTCh?z7(rmW}_I7;-+!3)#n*8+`B8_<6h3lhrquTJp^4@>@r?Bb_$irf{TwI(?wIO-'
    'T5(fj0t0^o|y{M%~nk8x5;01sNnQB_^a*f#zY#3A}D*U1m%sm36RTk&)0=NAhr+-'
    'Vt(T7(cXzIEcB{JgR72lZt7|T%82@H4|$Et?>E+SEc<<!zs;E&(T?23$o@Cedq!qlz*B8P*7J>*CMs5nJvu&qq#(ViiQ(X!+hEE)'
    '*i8*VCRx-EP<_-0@g*w>{JoF)AMRy6q9$Hk8cuMj(w{23v!#ZMEnl^6Y#Jbvg!SpWuM|b?&E>66Qltq0CS-'
    'r%NB%(WUAJ4)oZbhW<0Jo2W#D4(6^Z6zKt`cYwSy|rJVfV(#{xXm`B0LMK+?J7$jwbuq;l+iav$xncW$&^F?GKg6vDJ&8XaqhvWN'
    '^1`uD=m0UB99AfTmbSmQv7CYaPOsS;*Q1FT#{(eB-#L3F`#4s0&(y+;^6Fit~Pq=5nH_6@+R82HD5&LBdaN^kmz-4?Jo1-'
    'b2KSUSy)QVC*0wXy48v#VLa#L4#C=qd3-WfJL$oZ<(MiObDD1zCP{VEMtTc+;ms?E&hi@y6l__DU-%~DrCsqkv!7~i^-'
    'bn5VE)48V_eYS`2S%Vi%LxGOhJePwi%OV5MDa-H$!L~V^>QvSi4_f9O9ff!y-'
    'M6JQ!G=*y?wm|%4`^%!i=kyR*#&^Zyp*1bEtwuNZd`Xpa@R9q0-'
    '2W>@JJ5>4NYeI$0F@jp&SM|?*P2WfILj+jf4QHY!^5L8v$4(L8MAo36(30Mc64P80*5J#<Z_$I#4uXUE)=0)w}Qj97JMx`64xi^T'
    'N>Ep6F;Os2Q6B6ezN(oz!Tg{&y~kcN0#Q3T?F%*-A-'
    'GxN(rC6m=@~b68n~SL``ugh2Tg5Ge5iTP3uLteb3OAx)04UEC7QRbY<I<*SaPq|0*~COs~kG|bI66*<jIn2$ZpnyZ@%$M)f~LJxQ'
    'C{!gfp4uADps482qH6k}Xb;$WQTv1;<5fV<Y#{}p9B?OMOGFLqA$$C?%AXE=9C&VfB6jv=6$CKI8-XJpw$Gq<dFb`;YQ7Er-'
    '4KJzOyv8bKS#Ui5lF(d{s!t2C4(c4B_#t+1DyTv$Q9nwuro|N4c_3t@)gS;zqgRfW<2C7SG)8c!sL)6$duWGdYdj>5x>hWPBE4d='
    'aafa}tzsIY&zT8O!unZ-fk<3B&SYl7V@;udEnl6T#DxU~0B=0F;JVUT0+c1yjU*yeGmbd~2yIf%BVFt%DkW=o3s@{7Lp{gXKteo#'
    'o1R`|OlXU2e?c;Xi7#%IYS3=1D3~QlJ1mw=+s~d%MGR}0v=`4N7!ROaDRdH{e#t58aSt_6qEk96%}rFoACb4!Qd9}=QwaR!NP<t0'
    'uy;;!!MB%*Jq5jHMz>nj!{w}lPN}rnYSo?}Q_QGU1fT-'
    'vWxIJk(PSVfB#`^IV!*ymAPw-1(A@2zOx;CCK$mPnOR2459N_)B#vElhk%Zk-Ezm8c98lM}fv6)z8HI%@(by9_GDb&WCydB4>sys'
    'Ol3<EmJqoZ@28-'
    'G8KG4Ujy_ZNND!+zu5(=seia!Y68BP_sG++l~AcQUTKmwA{aAq1aVrL|lxjIyu44E}gdCm=n=B;Be@+~{~>Ji(O9HA2|B)u<LV`N'
    '&HZ#S`_E21~7#Z+R>*EUx~@rq-'
    '}G7Myy^9&KpHU=UO3SEPLzbBbvWhpf8zK1OMML#EYZk2CVyxtHoDyrF#P~E~4+iv<0CK|=7vN&;fdWXI0bJE>}a9X5qtUGx?phL2'
    'xcP_S2p>-'
    '5<K_f&|%(^Va3A1YYI8Q)vpn0*Mt_u5(S}@D}&E=!Fr1j@@_wzh|V0g#1)8}AeG57>boGMr~lM+Ao1X2Qt$=F{PWktN~1)rXuCZ)'
    '1cj3-'
    'ZJuq|rIf{URTYC9H3)!b8R<Ylr=g)79SPf#cql0BLM3k0NSy7OqCNi~&@)dv<0I38cb@lipE8pIcC9cw5`Ae;w?>)h0`Kx)Ez>5P'
    'Oc4p_r{D+=4JL`Epgof0djwcV8JaqTF?T*`-VDwV?S1#SR<6qYrm^CwkvPr&aezpSll_cxJ-GD}3>7t|}|pU{)d&Ejy9N^%kGIm&'
    '}8&`e6WVMd++z(CTRS*f|tsRU2Ul4ivqfT_fOF&phbmzYCywlBp?F$<n2-_A~eS-'
    'L`!iJneFvh0xyyB`%L(YGjGC}pKMn5yEmFvW=a95yK+a$*Flu%*?Yucc*&J|Y?9e301}whP3DLKXp)3(QrD!(mDxtpJ~t#q#g;ND'
    '5Cqq6f*rt^MAQ9cikPBaBuqV~gg;kqou=(FgK5#B2!ka`L&2717ShJxNYvayHSzwcE@VV2F`6cpC-'
    'A6^qLWX*g9KRcZcpvxa8X1pKAiyab`nB6kd!&(cUK_j_h~1avyA*Ggk*Qn({E3G6OSZEIQ+qygg2Y3E8eEGL}OObu3A(1K7xYRa1'
    'eXcPOB;oh;ls+?|Te8uOKLHp;VJb`SA&PqKq<w&IEi172OAHC;gq^2~Ax13*`D8HpkF%1r#y)J6C%n=XGSKnZs5({uwDl}WZWTHa'
    '2c6H{<KJ-W)(4BeWG!BeSr9yVZTA|;ZRmDZmhKz&C8JAfttSyNi4k!EO`sO1@8Qm)6zQB-'
    '6bDuPWtE<Ed$)}FDDAYEjl_n~Dg4Dc8nlQjWw|E@W1W?>T$Luap^Ugb=`iRHWD!&B&G{ig22!gdi47c4JFNK=1>?(`F!VqqRO1}O'
    '{6^pkein;igvv)~C=4=dxOr}IGr08u$twN2jVo3sqB9g(5qTW4nunZ#B20B5PqXKp`)IZ9J9Vt1yF_Gvn`MH(KIo?XnOE}dLzh7H'
    'zlBq|vUFD?Cpg+@=aJrobP4i^eAn2Qv$csG?uws+sQTTOcg^~7RW3awJh2$}yw@a>E$S3zhD}nS9_e3)i_Dp#>QJtGze{#(L3+iq'
    '2fzsffCfYtCFrPyzQ|IA+sjco4rLzZv!6(1zQG0j_`5>Z5k@F5l)-'
    'TTMv)vDK6OX<iC=VgneA*ufz^!U9=fU81sDNA>e2j5_N9@3^+SE?s<51lRR&SWE3e!rhb*R`!u$>&9>qYD9gNEoOoA@_lT3@GfPK'
    '>d}3pi0JPttw@GL|<<tE3F=DUA9hWT5f4AIUE-pkkDu(;H`>Fr2iZz7)5*5~+jyLAAn3r9A1NAsb0Ynni4ivQXStQ#v$!dr#|Pu7'
    'nFS1P)8H-'
    'gV&3;GyMKSCt?s<wvW!CqC=e@{aLJG6z!Vru_8f>iWZP4|dYs7oVgiCbf|cARUMH0|#X}U0=T6>};vDu9tOTKnM17q2)PFEM?<)>'
    '|V)E9&!)Ez<2-*lUa(G>yt7xft9<AtQ4LYjsBNIPn8Pr%S2cqaOtBW0b)h8gf>(n@dlobhxHzXf&k>R-v-'
    '2DGI;?(*N(i*SFzy>*M(ok4?FVYDu{~>&dMXeYwIv)An!4f=F65k=as*fpfXjC3`z}gPj-vznRO`|7661%oeB#M*>-'
    'v@?~{~jvrY9hAdb8xJ5VbjmloSvpIeY`x%v*scTF_8b^oN(6ynjydE=N-'
    'oH*g*OPxxM5&57bsMJLcra(|*1;rxDSwVfL&NtJGQtQ&#eo{)x;bSF8!<z4cPDN=Kag$k5yOQ9Rwv7Y^%nwNh6<A0fTDLT5<^}5#'
    '=1O&*26-'
    '+yWmC##N>oT~tFEjeqS?|do;Q$dNTt|hP!CDcj?L8gAz6n(14zZL%K8K2mtTPS>_fH+64eBGS}<LQEX$K%8I_y<>9C7*-'
    'x7E`Eo&yHHyt^L%M$qrUyg!?yXgAnwihCE8C55GQxR9NVgBVa9_vxbRU!f3A{f*13TARnit`DS&BMx8{({VEN^5f6r8SsxEkQd@Q'
    'MlaGy8b7~e4EKZe_eIZ;nObE^4u|9{-'
    'kA|n2|^R(#i3+#+6tUN+J<ZMn4~xZ>F%6TDUW!1<q583Jte@H&Pq{ea*yaPglK)4td@>S1n@3p-%X`5uHGhX`><dkd-'
    'R&*{c+S;+9M$Nn&oq#$^{o201vq!f<}TP3==5833_~VWI)WcD50qD+tiSR+4{DmVYMHrLMJyB_F@Q>enl37=*Bb@rGe>dcG(*Tk<'
    '}$>!K!NMI}`%5sZSLh7v=Q*#zoPehu0w6PBP{K03wPqBb7CS4tjYLbiPiQh!q7{y6w97EV{smqk5%L{18t(hF8DVy}Q7kYmLcZJ('
    ';dlqXpM@s+rXX0);6sCWw5^Z^T?0E~5%Fq}M6qoS24ze<si*wOnI)hiPKU;=PUB4IWSE8507PQ~Qq1wxob?bvxra-'
    '^6t@AOMW*p1P_f{~?CSJXN3fV~v8H>d8U>uUuMVh15-'
    '_~miOl|4+KWVpT;<guxOo)0gsixu@~>Tj<EGBF#>BLImqQFCXEQI9|~8kzi8PnblidQZQtsTZ9%VFVMHqFkzIE=9g}B2R=ZhUnUt'
    'G_R;8bQ-A93hr^tk#G(cTA{7BN_$+pTlpLntuFAR!UgGD^ch93t&kC-oiXX?0x<WON=}HlZF(r<N@`BAzOq`!kcscMBrKwh#L^-'
    'nLsiTbXkq=KPyR{{Rg|+z)iU2t^fAL^#NN3k(^Tu&NeiK(A*)BL)9H#+2Vx#M-%`Om0YI7Igaw%}W8?YVeL_)R!q;l-'
    'N{GZxJhWnoca*Ma1ZybB%Xe$4S%GG})G$Si%d7K}6jed%&Hx{Wd9o>Z)DB`|m{0Q5OHZ~1$Wx!YnO%uu3!<Ej9TdRyBGW{A&YNB='
    'G$^%~VZ%KMR%r6pORmE+D(Lqt*vHK3;*ApG=bl)f!n9hKD-!kQQHioTwCGw>V<q;5$eR*d>0a=sBt)?kDow>)r9_G5-'
    '%?lF*$N^pIwdNuu^1sJed$k}k)!9qGFFTf@$3N6RWeVI=vQR)s7fjQp*zND;jAUGN?bppSw2}&AlbQ-'
    'N3%#uRi?5jR;)l4Zwi~QTo_K+0CC+LMS)y#5b8S{Vy1NM=c?VQXI|@eCMgqgVL|4oGXjyXkJ^K=#uH`}u>wE)5%-'
    '}IJCHE7K*S=@X(k&yhuzRsPH;bwLdGiA6_V5v^eT!)$~6T85=!fag$GYSY0Z{)Ru~%$%E}`y^;3vZi6r?ls+yNWXN(|6BXJ0{HWH'
    '|z{c>je_;oc#N>;;1X4Q0Q-FzQrK!z>=GW5zIL$ALlIp&upibGj3lz-YqCPyX7NG0DGlja#@bF`r~l*d!ZvuP?il0_xeOn%||IyC'
    '=_g$V_E=0->jqS>Ev)SFCKYgAq^v{(X082$#l;r@YoALGn1cn!+d06Lvm$fufel}!{_)|FLQ2wZk&Xw7z!+*j-tRrO$<3nf-'
    '7d@@B5NGVt)Y6PiT&y7h#O0`ndtoWj`YFxaCNiy;rxp;ZdRiaC>wI7P2D595=lsGK+O{&TTuKuy%l-mQj6fz-'
    '~g~cQohASfcK`xe2wk>A9M&^+pxM7R~UK1)21YoQmg4NQHCOnlC!cuEH!&}>U2=;JQ>O58HO5`OuZ3H57bWAPEA3KD;Bxo5$cnpG'
    'QoZjW{1~&FNJt^hG^x0hnlvY?k35>#Pkn;2$fICfzPUragkn)<=30arM#3mt_$@wlK=o5R?Bt=5@C@Lkf+SH7e<$Qy5Wh`C%xJyU'
    '4?4$skX#z!5WTIQeCn*=GUM`s4ueltY^fr)$(jxQ~_!eaW?ZOU->L}^7ZmI5#4owm`Ox(2;b!TO9I)=3Ut*NS^ZD(A-DRF_6>P-'
    'Z(wr1n-VnJkMA~%VIJ9-'
    'f@BuqIb@#t%z0uKr$zI7H!o7#8qBF?F0QGlX;y|spI_9&n#ZpnF1Br8Q1=xuDXXEKJvGH6VV(Nm3ys=&OfR)O*O09K#Z79vxV!B{'
    '`^=CK;xOvo$L*<d&9MZ&Xp%TW&^E+IH&d(;S=)TBsQ7Ll^O#%}m|XO~z?bs~*yg%tod<oq?w8ZsgwFEg9S!$rzXi>wb=Xc2||(9s'
    'iAX`~621z<jwEMT6kqEOsl&6Kk#`HkZ{EPd*yP)}TqF{xZ_PF~d;oh(45XEN~Bl_K0FgbVfbbLJDo%a^IpDssR<ibjG;O*!h67R4'
    'N}z7wc$ymG!J_klLE%4D*Y6RTX+97ru4Q_1lv`HZ$f!1RPdjB=e=QrfprDpC=-'
    '*rqDk)Qa>r+<+9A&{9Wv8RRs{7(O{H3B1uXA2LIiYZxavw3Q=cp+yoyCI!U(sybvFyj8b>;*5eC!dihJURB4bOl`dky~+ISfhYj0'
    'd=p>$DbJ)SqWq%~LL;Wv60?P0Q}?w|b^`i}xeD>bY^3oY-Ubyw)wIBfO;f2#$i>E3L*ik}#@wlS$Gu)=fyTo^E1w6v?NnNI+xUo<'
    'q$q)yk&2_~=<55p5t2jvX%OC7!J^((WO!EVG(_2@lsD?14fREoNNtVUo@kWyOa<>z(0Wz#15!;B0%`mtmrm8<#;cGlRr+Ug<d~{n'
    'Fc^%TQ49UTWgq#9kqbqCLw}rFaOmU_6bazBbYL1d=2WGC73?_pD;gvnM>BTd{Kb8((VV3hq9iDT@v(=MPMoLu07eqHh2+EZ+Z3k0'
    '5IC&6#Q3*DHxkW)POe)fm3Cs4>4aTlrt<Amv#5im^r5X+>kC!-v2XbU*vq)NZys88|NntQ0?7'
    )
)).decode("utf-8"))
_REBALANCE_ACTIONS = _LEGACY_ACTIONS
_PRICE_FLOOR = 1
_DEMAND_ALPHA = 0.25
_MARKET_PARAMS = {
    "WHEAT": (25, 10000, 400, "sqrt", 0.8, "log", 0.2),
    "CARROT": (35, 10000, 450, "log", 0.2, "sqrt", 0.7),
    "TOMATO": (60, 10000, 200, "linear", 0.4, "sqrt", 0.6),
    "STRAWBERRY": (120, 10000, 100, "sqrt", 0.7, "linear", 1.6),
    "MELON": (250, 10000, 300, "log", 0.2, "sq", 3.6),
    "EGG": (50, 10000, 332, "linear", 0.4, "log", 0.2),
    "MILK": (160, 10000, 122, "sqrt", 0.6, "linear", 1.6),
    "WOOL": (200, 10000, 105, "log", 0.2, "sq", 3.2),
    "FERTILIZER": (100, 10000, 200, "linear", 0.4, "linear", 0.4),
}
_SHOP_PRODUCTS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_WEED_STATE = {0: {}, 1: {}}
_WEED_REPLAY_STEPS = 8


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _regime(configuration):
    interval = int(_get(configuration, "townCenterSellInterval", 12) or 12)
    return "rebalance" if interval >= 24 else "legacy"


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if seat < len(farms) else {}


def _align_hands(action, obs):
    action = _copy_action(action)
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    if len(hands) < expected:
        hands.extend([["PASS"] for _ in range(expected - len(hands))])
    action["hands"] = [list(order or ["PASS"]) for order in hands[:expected]]
    return action


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _trace_actor_action(actions, step, actor):
    trace = actions[min(max(int(step), 0), len(actions) - 1)] or {}
    if actor == "farmer":
        return list(trace.get("farmer") or ["PASS"])
    hands = trace.get("hands", []) or []
    return list(hands[actor] if actor < len(hands) else ["PASS"])


def _weed_repair_action(obs, action, actions, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    game = _WEED_STATE[seat]
    if step == 0 or step < game.get("last_step", -1):
        game = {"last_step": step, "active": {}}
        _WEED_STATE[seat] = game
    game["last_step"] = step
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    active = game["active"]

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else int(actor) + 1
        if index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - transaction["start"]
        if age == 1:
            unit_actions[index] = list(transaction["intended"])
        elif 2 <= age <= 1 + _WEED_REPLAY_STEPS:
            unit_actions[index] = _trace_actor_action(actions, step - 1, actor)
        else:
            active.pop(actor, None)

    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        actor = "farmer" if index == 0 else index - 1
        if actor in active or not isinstance(intended, list) or not intended:
            continue
        if intended[0] not in ("BUILD_PASTURE", "PLANT"):
            continue
        tile = _tile_at(farm, position)
        if not isinstance(tile, dict) or tile.get("kind") != "WEED":
            continue
        active[actor] = {"start": step, "intended": list(intended)}
        unit_actions[index] = ["DIG"]

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _shape(name, value):
    value = max(0.0, float(value))
    if name == "linear":
        return value
    if name == "sq":
        return value * value
    if name == "sqrt":
        return math.sqrt(value)
    if name == "log":
        return math.log1p(value)
    if name == "log10":
        return math.log10(1.0 + value)
    raise ValueError(name)


def _market_price(item, inventory):
    base, equilibrium, scale, below_func, below_target, above_func, above_target = (
        _MARKET_PARAMS[item]
    )
    if inventory < equilibrium:
        amplitude = below_target * base / _shape(below_func, scale)
        price = base + amplitude * _shape(below_func, equilibrium - inventory)
    else:
        amplitude = above_target * base / _shape(above_func, scale)
        price = base - amplitude * _shape(above_func, inventory - equilibrium)
    return max(_PRICE_FLOOR, int(round(price)))


def _is_sell(order):
    return (
        isinstance(order, (list, tuple))
        and len(order) >= 3
        and order[0] == "SELL"
        and order[1] in _MARKET_PARAMS
    )


def _impact_score(obs, order):
    if not _is_sell(order):
        return float("-inf")
    item = str(order[1])
    try:
        quantity = max(0, int(order[2]))
    except (TypeError, ValueError):
        return 0.0
    market = _get(obs, "market", {}) or {}
    inventory = _get(market, "inventory", {}) or {}
    prices = _get(market, "prices", {}) or {}
    current_inventory = int(_get(inventory, item, 10000) or 0)
    current_quote = float(
        _get(prices, item, _market_price(item, current_inventory)) or 0
    )
    later_quote = float(_market_price(item, current_inventory + quantity))
    return float(quantity) * max(0.0, current_quote - later_quote)


def _demand_per_day(obs, configuration, item):
    town = _get(obs, "town", {}) or {}
    shops = list(_get(town, "unlocked_shops", []) or [])
    turns_per_day = int(_get(configuration, "turnsPerDay", 24) or 24)
    shop_interval = max(
        1, int(_get(configuration, "townShopSellInterval", 4) or 4)
    )
    demand = 0.0
    for shop in shops:
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            demand += (turns_per_day / shop_interval) * (
                2 if len(products) == 1 else 1
            )
    regime = _regime(configuration)
    if item != "FERTILIZER":
        center_default = 24 if regime == "rebalance" else 12
        center_interval = max(
            1,
            int(
                _get(configuration, "townCenterSellInterval", center_default)
                or center_default
            ),
        )
        day = int(_get(obs, "day", int(_get(obs, "step", 0) or 0) // 24) or 0)
        multiplier = (
            1
            if regime == "rebalance"
            else (4 if day >= 20 else 2 if day >= 10 else 1)
        )
        demand += (turns_per_day / center_interval) * multiplier
    return demand


def _order_score(obs, configuration, order):
    score = _impact_score(obs, order)
    if _regime(configuration) != "rebalance" or score <= 0 or not _is_sell(order):
        return score
    item = str(order[1])
    quantity = max(0, int(order[2]))
    market = _get(obs, "market", {}) or {}
    inventory = _get(market, "inventory", {}) or {}
    current_inventory = int(_get(inventory, item, 10000) or 0)
    demand = max(0.25, _demand_per_day(obs, configuration, item))
    excess = max(0.0, current_inventory + quantity - 10000)
    urgency = min(1.0, (excess / demand) / 10.0)
    return score * (1.0 + _DEMAND_ALPHA * urgency)


def _rank_sell_slots(obs, action, configuration):
    action = _copy_action(action)
    market = list(action.get("market") or [])
    rows = [
        (_order_score(obs, configuration, order), -index, list(order))
        for index, order in enumerate(market)
        if _is_sell(order)
    ]
    if len(rows) < 2:
        return action
    rows.sort(reverse=True)
    ranked = iter(row[2] for row in rows)
    action["market"] = [next(ranked) if _is_sell(order) else order for order in market]
    return action



# Boatlee V16-R5B: weed-replay-safe livestock-mix controller.
_V16_NAME = 'Boatlee V16-RC2-MarketRelay'
_V16_SWITCH_STEP = 161
_V16_PURCHASE_STEPS = frozenset([192])
_V16_ACTOR_WINDOWS = [(4, 193, 212)]
_V16_ROUTE_STATE = {0: {"last_step": -1, "yarn": None}, 1: {"last_step": -1, "yarn": None}}


def _v16_yarn_route(obs, step):
    seat = _seat(obs)
    state = _V16_ROUTE_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "yarn": None}
        _V16_ROUTE_STATE[seat] = state
    state["last_step"] = step
    if step < _V16_SWITCH_STEP:
        return False
    if state.get("yarn") is None:
        town = _get(obs, "town", {}) or {}
        shops = tuple(_get(town, "unlocked_shops", []) or [])
        blocked = {"SMOOTHIE_SHOP", "PIZZA_SHOP"}
        state["yarn"] = (
            "YARN_STORE" in shops
            and not any(shop in blocked for shop in shops)
        )
    return bool(state["yarn"])


def _v16_swap_cow(order):
    order = list(order or ["PASS"])
    if len(order) >= 2 and order[1] == "COW":
        order[1] = "SHEEP"
    return order


def _v16_convert_livestock(action, obs, step):
    action = _copy_action(action)
    if not _v16_yarn_route(obs, step):
        return action
    if step in _V16_PURCHASE_STEPS:
        action["market"] = [_v16_swap_cow(order) for order in (action.get("market") or [])]
    hands = [list(order or ["PASS"]) for order in (action.get("hands") or [])]
    for actor, start, end in _V16_ACTOR_WINDOWS:
        if int(start) <= step <= int(end) and int(actor) < len(hands):
            hands[int(actor)] = _v16_swap_cow(hands[int(actor)])
    action["hands"] = hands
    return action



# Boatlee V16-R6: inventory- and price-aware WOOL release for YARN_STORE.
_V16_WOOL_GATES = ((480, 170), (600, 120), (672, 80), (719, 1))
_V16_WOOL_PRESSURE = 78
_V16_WOOL_BATCH = 16
_V16_WOOL_GAP = 6
_V16_WOOL_STATE = {0: {"last_step": -1, "last_sale": -1000}, 1: {"last_step": -1, "last_sale": -1000}}


def _v16_wool_gate(step):
    for end_step, gate in _V16_WOOL_GATES:
        if step < int(end_step):
            return int(gate)
    return 1


def _v16_wool_controller(action, obs, step):
    action = _copy_action(action)
    if not _v16_yarn_route(obs, step):
        return action
    seat = _seat(obs)
    state = _V16_WOOL_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "last_sale": -1000}
        _V16_WOOL_STATE[seat] = state
    state["last_step"] = step
    market_orders = [list(order) for order in (action.get("market") or [])]
    if any(len(order) >= 2 and order[0] == "SELL" and order[1] == "WOOL" for order in market_orders):
        return action
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    wool = max(0, int(_get(shed, "WOOL", 0) or 0))
    if wool <= 0 or len(market_orders) >= 10:
        return action
    total = sum(max(0, int(value or 0)) for value in shed.values())
    market = _get(obs, "market", {}) or {}
    prices = _get(market, "prices", {}) or {}
    price = max(0, int(_get(prices, "WOOL", 0) or 0))
    terminal = step >= 713
    pressure = total >= _V16_WOOL_PRESSURE
    price_ok = price >= _v16_wool_gate(step)
    gap_ok = step - int(state.get("last_sale", -1000)) >= _V16_WOOL_GAP
    if not terminal and not pressure and (not price_ok or not gap_ok):
        return action
    quantity = wool if terminal else min(wool, _V16_WOOL_BATCH)
    if pressure:
        quantity = min(wool, max(quantity, total - (_V16_WOOL_PRESSURE - 12)))
    market_orders.append(["SELL", "WOOL", max(1, int(quantity))])
    action["market"] = market_orders[:10]
    state["last_sale"] = step
    return action


def _v16_agent_impl(obs, configuration=None):
    try:
        actions = (
            _REBALANCE_ACTIONS
            if _regime(configuration) == "rebalance"
            else _LEGACY_ACTIONS
        )
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(actions) - 1)
        action = _weed_repair_action(
            obs, _copy_action(actions[step]), actions, step
        )
        action = _v16_convert_livestock(action, obs, step)
        action = _v16_wool_controller(action, obs, step)
        return _align_hands(_rank_sell_slots(obs, action, configuration), obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }


# Current official Kaggriculture defaults used by the audited two-argument route.
_V16_OFFICIAL_CONFIGURATION = {
    'turnsPerDay': 24,
    'townShopSellInterval': 4,
    'townCenterSellInterval': 24,
}

# Boatlee V16-RC2: guarded, debt-accounted inter-turn FERTILIZER relay.
_RC2_ROUTE_CHECKPOINTS = (216, 240, 264)
_RC2_ROUTE_DISTANCE_MAX = 8
_RC2_RELAY_LEAD = 3
_RC2_RELAY_FIRST = 278
_RC2_RELAY_LAST = 662
_RC2_ROUTE_STATE = {
    0: {"last_step": -1, "checks": {}, "locked": False, "due_step": -1, "due": 0},
    1: {"last_step": -1, "checks": {}, "locked": False, "due_step": -1, "due": 0},
}


def _rc2_public_signature(farm):
    counts = {
        key: 0 for key in (
            "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
            "COW", "SHEEP", "GOOSE", "PASTURE", "COOP", "WEED",
        )
    }
    for row in (_get(farm, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            for field in ("crop", "animal", "kind"):
                value = str(tile.get(field, "")).upper()
                if value in counts:
                    counts[value] += 1
                    break
    return (
        len(_get(farm, "hands", []) or []),
        len(_get(farm, "unlocked_quadrants", []) or []),
        tuple(counts[key] for key in sorted(counts)),
    )


def _rc2_route_distance(obs):
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return 10**9
    left = _rc2_public_signature(farms[0])
    right = _rc2_public_signature(farms[1])
    return (
        abs(left[0] - right[0])
        + 3 * abs(left[1] - right[1])
        + sum(abs(a - b) for a, b in zip(left[2], right[2]))
    )


def _rc2_state(obs, step):
    seat = _seat(obs)
    state = _RC2_ROUTE_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {
            "last_step": step,
            "checks": {},
            "locked": False,
            "due_step": -1,
            "due": 0,
        }
        _RC2_ROUTE_STATE[seat] = state
    state["last_step"] = step
    if step in _RC2_ROUTE_CHECKPOINTS and step not in state["checks"]:
        state["checks"][step] = _rc2_route_distance(obs) <= _RC2_ROUTE_DISTANCE_MAX
        if all(checkpoint in state["checks"] for checkpoint in _RC2_ROUTE_CHECKPOINTS):
            state["locked"] = all(state["checks"].values())
    return state


def _rc2_future_fertilizer_quantity(step):
    future_step = step + _RC2_RELAY_LEAD
    if not (
        _RC2_RELAY_FIRST <= step <= _RC2_RELAY_LAST
        and 281 <= future_step <= 665
        and future_step % 24 == 17
        and future_step < len(_REBALANCE_ACTIONS)
    ):
        return 0
    return sum(
        max(0, int(order[2]))
        for order in (_REBALANCE_ACTIONS[future_step].get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "FERTILIZER"
    )


def _rc2_repay(action, state, step):
    due_step = int(state.get("due_step", -1))
    if due_step != step:
        if due_step >= 0 and due_step < step:
            state["due_step"], state["due"] = -1, 0
        return action
    remaining_due = max(0, int(state.get("due", 0)))
    market = []
    for raw in (action.get("market") or []):
        order = list(raw)
        if (
            remaining_due > 0
            and len(order) >= 3
            and order[0] == "SELL"
            and order[1] == "FERTILIZER"
        ):
            requested = max(0, int(order[2]))
            reduction = min(requested, remaining_due)
            requested -= reduction
            remaining_due -= reduction
            if requested <= 0:
                continue
            order[2] = requested
        market.append(order)
    action["market"] = market
    state["due_step"], state["due"] = -1, 0
    return action


def _rc2_market_relay(obs, action, step, configuration):
    action = _copy_action(action)
    state = _rc2_state(obs, step)
    action = _rc2_repay(action, state, step)
    if not state.get("locked") or state.get("due", 0):
        return action
    target = _rc2_future_fertilizer_quantity(step)
    if target <= 0:
        return action
    market = [list(order) for order in (action.get("market") or [])]
    if len(market) >= 10:
        return action
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    available = max(0, int(_get(shed, "FERTILIZER", 0) or 0))
    for order in market:
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "FERTILIZER":
            available = max(0, available - max(0, int(order[2])))
    quantity = min(target, available)
    if quantity <= 0:
        return action
    market.append(["SELL", "FERTILIZER", quantity])
    action["market"] = market[:10]
    state["due_step"] = step + _RC2_RELAY_LEAD
    state["due"] = quantity
    return _rank_sell_slots(obs, action, configuration)


def agent(obs):
    try:
        configuration = _V16_OFFICIAL_CONFIGURATION
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_REBALANCE_ACTIONS) - 1)
        action = _v16_agent_impl(obs, configuration)
        action = _rc2_market_relay(obs, action, step, configuration)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }


# ---------------------------------------------------------------------------
# v22 layer: Boatlee-copy detection and systematic front-running, plus a
# step-717 terminal liquidation.  The base production engine above is the
# public Boatlee V16-RC2 artifact; this layer targets the copies of it (and
# its near-mirrors) that populate the ladder.
# ---------------------------------------------------------------------------
_V22_TRACKS = json.loads(zlib.decompress(base64.b85decode(
    "c-rmV?T+j?k{;k&S?upMz=)to%C}-H48tG5!p4lTwqY2C@7+_UN~||XNhyj!r7|ahGmY-*nm+X$DkUlyAOH6s|IdH;*T4Mxzy9SP|Ls5gyZ`%-|NF21`d|O^zy6QE{e%0bfB47$^_Tzl*Z=rmzy68-_D}!)um9s;{^!5^^)Fxl{O|lf{lnjW{TmwjzkmMQZ~7nq`oI42KmYuWfBS*<etmuO|M{2y{NMi5&Nu(_|NEzZK%+lmoc{dv`)?-r$9J%O|B`pL$)8{Toouo&c;Q`bqwzNS1LG@g-zvV!M%UPA`E|rbMmG1BHdooi)<!KhdMz7o*ksMd);7M_#+TUS0-Lnh#MDObZ6j^taW-zT@%?Rn!{*m)-p<BPvB`xtcbQFEY;u3w)MA@P+T{Ig1UC8D&e)2*`M%A+qRn4uqmRwNHnrHMP226_lmm=(JWlz}LjU(5ly?=%NB9mxvDrU=gdgG9&!PN12<7dC{v-SdKf;gjBm4+I!jJGH{0Kk7PsDWB$gP>3@8}yBHNBZn-qtrLQgbuk+udK}{eAc#bZ_Y6<&$?aUoi3!WRZV-*ZHD_kHN=p>ytbBl7){JpDf8TAKyj3*}~_*=RUqGedJ7m{sa5~Kfn+01N?ggzIH71AX3hixxW<;E8YDY^Na(&_u&bY^UJ&P*f!kzbe^p7M&CK<xjgqyJb@_Fjd(PMC*yhiL>|8x&qLi3+Xk9$!V_KMJensLU!0;V{pp=}47}XP<9&DpXPa&$FEsJki0AIf6KkHk70+An__n;sns={@Gkka--iLQ%-tD5D`$!tGhF3;ApT;YGy)92hMmwL$6UaW3cjeK@Xy+4nvc`L#J16UCCyfjTK7mKNv+j*}(SqlI$AfuO6HknIauu&_^}G>}b(f}h;}JwVX=Et=nLJtIoOj_(Mt9C4TTpItYat_^yNVaCzjI#6Yg;{M%JaHc>eG4gt#!#-M}u{~Mdx2l*K}VAAKgdy!n)TEbG~<!GrU?#=hJoB_+~nRw7GZH@siK>#ybBlIt<_PQ*~~Dj&=O+8l8WJj-I3o7wX(qI=)utU{cLH>Ese!Y|$mtG*!`4hTc+_|N5>v9<Q4|I#XRful(pbb>XA4*3nz*+`H@iN7t>3X1d!&H9L)b^RVXAc-JIvKA$He1Dl<^KZz0D$(#JfJQ^9=?B$u{rn>v_!f9TSo9ae}knX~}!?S(1<uRn`@P{{=rxM6QzQgo|-rdMz=MQhA8aP_;@Xzb5cydFYx8N0FKpNR5;t4!o@%V<kbnum3_INxvae4&L@AD>|2tg2<@NbBlmaF_WxVaC9H_ov9mhXa_uEZscOAm379DY{ES{Fy_<WgPEf{4rS`3gFB<azLvAm^%*&MD&&WgX@0i+<kA^&R;Onj>ezp0{)P<xc7KVSZz=`t4lu$AuZGbf!xEb}s(o;>y)np1$FluXD+oi#A+zxr@48IWZGm0djL%iefih<Zc1W7v(V6{IDPt0t_9n?~O>TVD0a7TQGvB$Y2;>3gaU%%u<Ak&~}&rOf)P)Wj4PkEH6uf#1w0o9D!lwC)`OIVFWOzVY0xS*`??;?B^jhOy;*`31r?(Ha(ExF%?ZlGXLiasb##xO8R8eg)+WCmVZ(TM`Y{_WdVu`=H+&QpEIL1J0#P$#(r78=g$kpFZX}9JlL*TGkpi?m-%I>3Rym4j0Up!JQ;1sXxX@0$U-4=SI8WE&QRuhWWVoL2Wj&-8b6oD^oq1(NxNOJu^SrJp}{KN`1&|s1szXL%(){@mfu&ZufINym#s<>V&x~}oCS^`+~Xn6O0S9&2sRM}=@93J;pj0gSl|TC569!CJsgk5i5+fkv*}mVXko*nQCnN<!s#vMX`Dbbh++Sqqd_;orL(vqhDTMX%b!aOx&@BbaQQUq0vxa2PgL+^K8tfYNcoKu2rHZ5R_-TZ$EL$4owlHD-rBadaJx9XS+eW9Dg)$W55~<G;uyBdt2jBAN7;#+t#DrBW;hXk8ZHjS@gN+#LpVPgC(Dh~07s3u$sCshMR{nZ8IBuq;gxXGh)eIha{irH?%-$cei2Lq=%3Hz4O1rXU=s~njcmS>O{&yMOaq-D-7uU^oiwp=w@n}w6m2=K`NB4wi|eb%AHSk49J4*;K1ru-__$+8TJUgv%G=xGbvCuX<a`j?ozD;|8ox3vY8q|O+%ss>LCdjMSLK-pi1=Mdi?%ebXbdSuU1=zNuRH!MjetgwB#Jb5HEphG{wyu&T-a6G{3P0RmgY3gFGmCgjbD?NIhcTm(Mq?Z@6pTBa@HtAtkPdkQzsuoXj0Mm8PTqL)4HB(r_<R!v=8k=GornIbh3oXku{7j5u7|oBX4Wl`}!?Kq56S~p+iO9rTY3^MWP`&%9X#4XZ+~myNY;CgkPs+tBga3{7;$29YwSzitu$5F?`)wzD9@Bq9RQ<K=Yqkl(S$Hq#n9MBHy^9cc(?XCd%=~39=9fg2aXBCvT?n9fgY6o24jjh<FjrS|pD}2iAy-G{`GN`6ap#{WLP{6#1g!yh}8-hy-$eXbI_X|5Y~?<-O-c#i^x(+?}u{@{7oWi2Bzk=zdwfps51oB)S@u^xUHZpaV-(OclNeG-*%{Bf34%_xno===^Pg4uf(_uzV`<Tl8)MN`|1kFUw875R^9vw0s5o66IEyv<FIUpfm#H!4dVjGFAlT2BzDa)bQt1-U2#*Q*e(!9zgln3#)*{3N#<;3V0Y4pg%|f!uN)}KO#u!H~=EoCfaG3WJF5Umd^o+ACS^_0YMXqdPt$0Bo9dQGf4?Hp~p%70Ert(JeoB3kc3Q0?#K)5bE0`$QaUG{$A!F}>LNEfmiG#*uvP(%d6k%lC@;f`u)8awdK1LGrp>`L_hhB2>12LOoZzT<+8ju8XBKa;NV8lEi@&>&HL>J0s|fP#vz+d7xHf?1o~&8t08Q|gxXKb^mbif|+Gb&g!?lSlTiFOA-|?YGs}+v5i#x?~W-MuCB^wrIM#?s80+zs0vH5CEW-Ni&%M4}stoy8mK9)bmVq+FpEDXqCQ>2{M)N~OZWQo~lE9cem2FvMwamXTTmbYQ~ij}rm*wS!gK29skjbTlY39`i^9Z);RnvSuIZt!7)g|`w07DJXKJ!Ww$%jmNe7nUrq|4H}q^Hm)pCW4x;)?~(F2%H{d#myePy{!0T7B{lOF;;p$OFpcltoivY|2)>6V~5A2`W5WwaAvLGHI0a|-Gg?U_~FxCTLHwaufK%LFEhr9CUBGfx`#K=@h<Ln$ueA~j*Lb<c-A+D5YM|(KZ|w3MZwA%S)LX5W(A!CSg>e~#ba1x!zzMO4i57~M{gn|pJi4!{LT{2?Sk!DtWOtCu`D(qHmp>!1X#H?l$Sgn+tpfm74xTAIJhIOu>x!taTZFnUaers!b9+&y95_3(!b1E(T2r3<KDs17sKDzEO&_2d=ZKzi#3ZO;9IbqW~G~6gbc&fM5j7oJK1=WMU5;<mMo`PZjCip7oi)lTF&x}$iaRnRQ+*9vv?$n%vckgp42SA#&Sn5LN>SvPqM-z7H_cl)~gj;Slq^HzGaBnVM=Vd2)XSdY+Wsy%vj+7E5YUoS@V5a(=k@O6YKRuh`-X`@4tODv9ay-qN4+3TTL7>hA1y7!+gUciioY*UQ-tIEN{%J%mqa9!ZNC4SdI50GSQv#_GPrZuw5kc<}z1B-d<ehc4b&WIaU^6-)$y~(6<p&_+C)v;lSA~iN8fEDNfjQuOyqGGIOrNRZoy5D_MYqHk4s@80Vq)uOy35y*ooD2R@xqHvHZ=Tgg(Ds94AZ`Wn)KE>Jg?)$!Bk$XurkHFGsF8rN(i{r81rT%{kOOx{YC(@-yv9Swck$b5&4Pd};eE^EFT<45+cvNwo8meP46!zx&X>F&w9Pl5NdVGmmy`u)i(cY|T=cHxog>+wRE^uu!6SOH@_G$;22e;HUVbl!rA?squ&O|%b&S0F8stO7<L$0mWdhA}h`r6ulDEEK`tcxZTZ&Cb6U=HcfKYblMnC@?pMx@O})5GDYV;V`y`Ii1;9q&4OpBrS=mcZbOuOr8c4Ggy9bxvG0@?iqm{6mow1Yrq5+Bvw(Z3t`?2MmmsBRf9n+W@l*r_8Krc43nXo;3^^YB#dCgkrUz)T!A^m$3ZwU47}Z60*l))9tB&87@UV;n~SZEiVlu+_a^h*3Kjvz$6)RaU~(xeS;Erpr6}+XuML}@37ZeXUO(RWOQoL#k*`c@PH&MI*noSrc;gt_e%fQvd-1hsTX~Ol|HW`Q&3Dr<@v#W?OjRY<MYONfGcy`#np<e3vwlX?7-*;a(ypdH7U8R+Y2i!IME8CVYcv7c*p0Hd5j3|(;|-b{bU6RJRVMdKTWv7WMvE{Sr^pe+28NgHDGAP-`eg}ZvLW*qZ7NM<0ixV#Ll!_52VRa7)L?cT5el5Y?8ETwE?)6U+6}{*9y!}gbf_3}jCt&ei7_na%FWe^ksjMZV^_=@!x&&rAIA_J<kE8c91jaNFih^r-N_~}BP<Ps1sfPctBE3`vw-~$z!?jRb>&4b%vb4H`Ly~xj8Csv9}K%_AgrjO!Ty`Cv0`4satgKA$MXWk)`MXy>ELHz(*c;f685{t?}LR37WJiwSLv-_@6@(&c}?TDN_jl)`}$8mdyw-zP`;&e<KtP*r%;mxN~)M@k?a^DCW(1J`A>jNQDJ+3)nejhLHt@eU_P<IfDi_c>82)MO|tP-tGt{Vf~j@prgYvU+9cJy7hiQXtW7`1aAu7fzfALaQ{L;cj)~?7@v3Ro33Wd|hFR>5zoUspCR#JqZ5mfiY`H&V+G*?BW^#HcPtf;0(MP=wqIF!~%+Cj<IM3fUGNm<BfFf3c(wIGybX|KLCeq;zoJ(7qSepn;WUx+xCf{q4HB*u17oa5`nq<o)UDsZR$-yE$G&wL4B!~R`=)LQNZO%B4WbGo+HYxXEaN8u`TjPjn9vvjS^7cuwBDwul>S}|>p@$@Jht4_Yb)sU_A13#Z)YY)CkAyA63sTgi9JijK1)kk1xq{>dk#Y`SgoyPF%?j;SDcF<TBa+uGBiMG8R2>y0%G#0wBqSCjGQaSu&(aXmq#G30q}lSq^S38;^;_H_y;Hx%uPJPQCd<=$clg)txcEr-a@Ee`WcyJ*xmXrWWU>}66G)7j;5biSQnot&nIXSz8kfXY$kK8$)t@f9H7S`i?1CG}*W+eB3#-G+H7r-T;I-(+!+!qP55sKNA`3P^xBS7dpkQPN^VM`~Yzys2XRj47wtzVudPi7<<h-k4Q}@kd2bKUfHhJy$_2ui1DAEC&^cWY0jPeOu6*{O#9SKWjumJZ1gvkbsh93F@EPT&SJq?Rc(j1`TQeb>{j;W1@{hlxQPFR9znKcYs_GNh*_<;U}@%R6!6P6$=Ue;i&VLTq@I$`tj-i$ETy)iKgPZxD0`TDd;>VxsJ2snkpYnW)59}f#Aun5WV#qe%~rO~k8VCf%N{!>2<3ovR|bXz-F4p`5?&WB9@6yEp4rem;qbVrikoyXTVd)E!~_k*zsOaSJ0VeTHVcWSV>P}4@4;;VO9eB}EI|6Gx7czae@`|(5dZK6YwBUog>TAc_z=_GB8q%s5${4my5>E$VwuUJt(04LZ$d)Q3cvVOvwp_AqH<m8$apzertT;ay7X<>1d_Zne?S-cf^cv-s*3qLENVuf864`zuO%Wq`s1$coGh?DU03SiB0-z>Ia$?~%wVbNgLPe~;Avv`e_-$Wx+$KoLDyRtk4bdqLC#qyBPLL*u6Jd2^uGUS5PiZ$tfg*BIC$Vw}$)T7F053_E;v8qagRG4n&XA{(<Q8;r4qof`Nispnq<2kk#DA6eQ2sIBvVOi>wi*lP$RE@lzs|nHh1hYV4nz0RPGD8)|UU>OMxH2;;#|G?C0a4t83c4zOhDbfOQV}>48-<EcVm|#2%RPaLy1x1$Dn}3pqofCw9-(q=3V!Dh6c(cNp=OOLMsj(5jN+hFV=&4OLQNVq-vsqe9TLB?izfd&faW~{hR1y`RG&N;<u`u#qCKK7G8b)8lNl;h^~qSbTr@_MB5Cois0hncqw?WPF_U1jDb&-bpZr(@RH||>v4th+YF^A$G_4Z-%9QFsVG>wIg$<NjL%GMOsr5Pbwc|~_sC?DURn8@L<aD}5IVVi{Rg}l8sjcoh3`X$*l$fAcWk*f34JyA%#R?U47tVA9HMOpk!_25@&b!fb_lYJGZto)uTCg<**JBcxtujN145$9&ABXks9y`3-nZ9CaeJ0i>oHvW(W1?=jDGerRyi5EsQIClr%2$}en#n`kL#!YzO`+8!m@E{y$AopPwJC=@3llvwHLsJNohzNDS({R2n)KN80B@4Hz`1*!7!R>JOrlL`F|juJH4_<|JVx1r?>BK}^4gRii2^1Jx7*z#QWuFU5^IvLNZ96ek97VP@%4>)=W?DzI$f|H>6Rd#UW5gWR>>8l^EI$Yn)NXbc4WjlVyq|kW;b%ek89{BIUq&24;&|n*@egUr2I})^v%4A<aSB-ivo5m-q)Ql{rT>@7Ag<Jef_td6al=E$saCJe$b$>(=_*+4i01Hs`uY-d%Rtfw3>cLJ@uP-!&FRG<!U~2`FV=U#0@(^{&`z8Gtq{Lw2A7`%!Mf_lY4BM(B$XSCOK?!5Y#M8t34NgD@Ek{;rEE7DkS~+OOJIf?WAjV1KcZiNVG~KB&EkBT^l)@koXwMLnh}QiIEf^lT?IOycNl>kz|A9HL1Ai{pPnwzTxeWyh9QvE0VxHujnC}(}1=}#k1*m-oQZ;8Ig+Cgk1Grz{DjaadqMO`;Y`W6OvA84?1mWg7<kG$vlqa&yg5@ZIObWiWDGZ``hW*lr;B{NN37oAt#bN%nXW}^b>#HBTcQOsgvYdNEqh}STs_QREXm7&eby>-mvQ@5s;$p;#XXFTcq+Pu6C}EH?H0zi6#@0tdTIS4CmWmGuEGk_D&Mv$qnVUDP1HFspv=|xD;1OKPSBfN$thC<-+6deePD&#UGhT?jVV~CSeXVlAJb|q|`_fJh$l}i6#l02Y7u$%enUXv*h%ZX-5iOBoF5<9(wjkmGF|A{W?gyw<Jw!9%dH_Z{J?evn~o03li^>LK{iugQVMq`}7ldMM|5|=b!75wyKeCk@VN<`@NVS`o8|fb3%UiL4}r?$g-RC*NmFRq7F_&=G~+}BNX?e;#vndoR5q*McPgJ)1j9Yl;3KQzMy7H6K$AiZGs0`nSOh%`|o_KdE*tBn|em>lZuopr%PbANeq*RkC489=kubX_BXVM1bU9iW;E%TC|ZiJ#dbaBnDwxMS`<x0zk98;h`foYo^DKQBGIDyq!faf$3&qJg?<rfk!TU7j}@Yy6aB_DlC7&wa*)PM#3mw-BKKG{*Wd3>h(xC?)}q{$G_8qvN2J=OJ{F0JGoKd~iI@rEtwrS#ie?bemMCtDWL4zNME;TJ`@cR{B5D)GLd2V*U?uv#oF*MW&lBEfNE(}UTsp1p?oy*@!jOxxNc3U!_a`NfQo#~tobNN;LnL~{T+)qwvEyhV%Jp?w6s$y);67?5l1h{wiQ<-s=T#AHioA&kD;_+CjUS14V~yZ$d`zSoy%>w63Wd!Ot=tk#R-&$pj&*!;hJfrUh%Nx(_?wfUsp|X36$nRvW3{|J$nSw}7vMYZ6t{Orzd<(NC>puZfxVYe`L*tUSP_fKA-7fusAR4AU;cX0ug6rCicPxot3*$Ckd2rh>AVS3)jUu|8!FN&GFN#jUO!H%q{<MjRXOnI;2oHTsMtnTRNREMAm6IWEdfhYmB-_G1J!<@FG5}ANLBfAWur>EKOU;$nkpPtr9-NK4fM@a^O}l4MQti-RLwRjsZ?n#FdHGDL=dDkR!#2U%dk5b_^VZ->s_%TEJAjisfx^0cw#oMwZ|(0O9U@?)+)wK5gV1;P?1(SSWjz}H&aoist2S*UG0WNi>9i{OywZA4^{YdPI|s_g50cIt8&0UZL3IE?|p~b2B~)6{QFcG%#9F?IjrJFmFnkepvp5(_EiK8E50K&V^paJ<&UA}i%{uM<f#!guc17kST~;RMY(69(n*xGp@M@t=2walo_78$JN=Z7-!Vuy%J#g9-+Pf(JN{ujE$Df;tI2=2Ajw*MFdHzKhV7$b4tLy;#B0GpB<1rV>>-y6C)k)2`$e=CLPL>kh{QxB^=WcEUFwVNb|;v`JHZ1i?=S>9t7GO2Z$60Qp$G9iT*Q@#DpA4=v_j<DL?H|j#Y)6lROF4!*blFBjZ%G;juOc+5pAwfX!{&-{t?dK8Dfjb>+x}BA~F+A5U7ZHg66)+frx9-bb5`%TvTLc=Fkg4Qi3#yrnWl+yB?A3io&*t;VtDSc-tu|!(+XooH-V%pdX5Io&`ZbcU=^UtLTv^*@*a<D1k^|YQ~JA=t2}5MPaOnw?({&{JtnPismB!>ZFL4cY+*eiEwpIAete$v=-5xh>nP&E5c!BqNGK+?lR{qIS?i2MplaEHW92*m&mP&xKTuFPgv;nacqr9r<B=%W(^7zh%_iJAioE4hd`{uMdv|b8-$IIS3zM1#Kl3`BhYjWNOnQf4#+oxR2X>^bi06FvvV%ChO|5jZWz%UhkNGS-#e+o#!v5c61#sq_P14)oViLM_E?X{RSo-~*~6rh8Vi*)u2rnxy#CDS>qG@8FsM-;x+Agf@MnTrc|rcupVtJ%8z=!30V)`Ms^Ul#Z48}eKsi9g4OHu6*%_gV$=CsQVp23kf;IAa7}m0zH(4nuQvL>@7(QQ7qeP=-BUC6*-T>vHMsy1$EvUxJ@AplF_qT;@rU-*989F9KU5dzHBD;kmOH+Ur@AWX;!o-mClINEin_Q2HtID^ehi3~+1JCh`oSk%UlLwOk<%r4Z&R13_+L&gTT`9Wr6T^wkK@&CJBjjL=Y@jKBo}$eL3F3YXkI6Hp>5+-`zz%^z=A)*@v$fx-(n(X$v5CUuVLUyW2s$!8-t)!Ah_ity?V7wc`BA3d&=RREtJ5Y7xp>_H$wLhen&gp*8`o*FH*sYu-Zu!gumt;vVDxz^5*E8iGepd`NWLP`qgSZ%)_nNm)J39QQqXTw3_J5ol5Nt|Mp}tHyB7-shEr#6v{7|A^~cGc;)@4;&ui^>7gE@W0*1Bu82h<>&7?4r<kym{iYd6PbNl$Vq*w(2^E(&onp0YC@hK<IHQwfF^J!ejEl9jZqHU62Yem*fN=2my8T1t?I^f}zmT+3HZU&#ny2<9Asdbf%NV411Zv<)kvt&oY9(Y9oX@b^~428dYq}DByzmVkCNCa)l)=B4|OJ0>3oo;C(x}3KlMcAG(ypRO!h-bDt>LwMzh*+igWlUTn#VwNDfP{s-_(;v9oDvgtpGlilikFbW8i^_rn~=h=3vbpW>^+g2cqQH6lvYX8vsWpPS}sT)hT<g16)8@8T)iP`CCx@8(xe%(-$aj3C1^}G>qoN*>G!?&CxSVh7WoZPF=~|8L|DGuxe<pvKQj^byemY!A;Mft-+2q43X$s(g$)r#j<!Uz(Hi~khJqES&LTsQR3Hx*>B_58ID7v#1MvY64$Jn%r>+xptQTHOw?eL(_#FpHKWNr@ey>uvd*1omt~K6ubjK*%6N7tq68T3NeqlA{*C&EhBpZ=zl<gK{dOb9?@h}9fF5B%8<s;W#5pT5g6Ft0_pgl;yILxMKI+ZhFDXJUa1sD=oh;qQMyfef`(PSeMeK5E$!p&h8x!j(+Qxt7PMRa9a3+wr9QH1$>ouahTlq+^_D%_eVXOE#MX;EAim9f<0c{;&Rg!!>3N?H_;h<?LA(pC=f+ezF&6px9*5m8y0b~xX>TO=S#Sf3BcrD=(~h#p*tqT*gRxkeG0iHeVW)D6?}yDdRTDL{Sl@2tH}5!c<`Pl}2baAB<lTrDEVMS3JURLPcn)$QE|H0^@0uV)7Ryh9eCd=bruJfZT)xffj0VWMfHWS1a~>X1j8JhRg;>?b`Aub9Q-*812nG%2k;RC`$efgfI<UXOd^$?XMePulVLCeKV&K*h!rz=MU>0`a;4CF1#bu+zh~9)|XGJ05}qrtFz5JW};R>+%qErgM-Gu<A)oo<r|=^Hjx#Y&=POc+E2(@n8$;1D<5)Nh3V5$wQ70fo>PSYj#SJ0{dq==zP}*-Z<VfD|PRolI=>}P|cc>$CbMGP+{6#ou*ezIb$eu^&?eNzbfdVW|N)^hSTT>>Re@zYVJY>jq)2Ps!;hA-vm{>bj&|*UnfjO@<W12FcX{yPP(#zbnWh{DV$xXXPCk<)6{4x_FD6~$}X>)>IXP`E@DO#Yykos!^<|wH<HMZ6xT?iLzSVOBxiR}VfS2yj!$@XODh(xNC7iCAexlRTUSYZa+4cWl=@VK?nBYECL&u=^-;1Rg-0Z+NVG}%4Zu!qZ&o%U9Oa5BQ~5y@q5diA8u2YrY7?=Eh_xtHDN|C3L{AQ|6GbbLtj!fEvOrM8TC{W3wLOzkJQfe5BO&sjMQ%-$pfW8S6SX~((o|*S^opnwVFTs_w}R=|oxz`6BQp^n6FFV`xg%=3eJ3|alqwN^j<U!v5g0oW9gFidh@=t~?c)cF#84D>MII6e7!Eieid>T@9*kXDiWsUgaGdp}qWdN5^)WXdyLTzYEmow&O<T>wc5%<0#CsQ$-z~&#o5TAw(`wT_(bdEOqIr0?c{F`(ZZlDJ^XN5UVqV>*%0t__bkvmgO<~{U&Y5swSZ5&mwecs7ruYm~&?e0J5ZzF}sH^dZW=~E{rr=FXan}^I$w3bdulowxn4*a(trejOTv`HCT}GRXuDzs7wlKYbwMi-yJvPZR)@jzMZUMG|b;~*jRn$XF^Eeaf_HJ18Njme&)?|9^O^^tiUu@7c={Jrr$RxJ+z1k$&<e+0yfJ_lfQ?N4SO%Gms#r6SBcqty9c6!X@3{3*pQf*>5e8Tf5GB@#|;;v&RhKMX}#4jDRtP3!7_t+Hmv+H!;L=eGbc<f><i7FF6H1XVaFHb{F^$<C1S!ZRM9^T7)O|+QYG1KE~k5iNBV6kL}X{t=FGCdgG%CXH9N1MVMn&Mqew~PICGU+FovUH{+$D+0~IWBQMx+XCy5jI-Wg=#>>cFglGD5(PKK{p7GI)|sgTB3?)0!=+AY?qOL+MEcDu@<hvOuMMih6+Pa*lQ+MlT8COpvl->)YOKWY*4g@irXj$vo`0)C~iVc#Y)YcCaEG55z0~oqBCfc2d1`I`b1VHOcxbM{D@FGbkam^w+Sy+CW4-U0zFwGymg={KsweVlW#H!S7#nwCej6<44<c*Qx$c7O?qsSr<z=4N|0?ul_@UQ<gTgh^Hkna<n+y)U{8xJn-V;Z9hl;A)BFsQXc9r$WI<w0O3TM=kJR?er8@F=l9Xov_^P51Nm#0Tl+^abB{n2^{nrE~lpYE!1FThAZj!qJr6y7uA;K(66cIeTa*^v}5w(4kOhknRNARY#gjw|ZyNXCpyURQ6RMp%}kZqcDoz1O8tfvy<E5=Sb#hpcH@p>(GMDfNVzaiS6G#TDbG+ih9^IiYpU;py&|N3A4%h&g9hsfypA+q%ojo%QT5+6JM@JEbWfw6b6;jn`@v<W<?-oz%5|AxKouCvj28|j{KSJ()Xy2sn-8XLjE>_ZzF+1y*&TxAnm8@1TzwQRg$TTN_dYa3r|<4bIEflXR$VrrxJwvo2+I2*Uv`2IG(Ve@M?Z)fAD*yKW+yUZpnHo3oTYOzftZSsCL0-JnnXKcmZeBb6@(dI9-(Z^<Bn_6ts!BoB*#3=_D>3E#-orV7IK`8Gkl#lQogkrOQ{s=$9v7bZvdl1Uo3;jp<5q^Xp;YaupeuN+4NB9wbgrA7%u8~_aJKxbaE^2x+pS-PaP^9K&zPG!-$ou<5w{UtpAM18bxA6rdA3+xR$9J7CTKE`z{I)*1qc2(b2*!BP$9JV~w(vRdxsUHkpK1cp5A+}42lxSgfFI!BBk;9jp$Cz2uFU<dc)sfP_?|rDfbV^HvNrbk-FR#p?tMB>)_9}uob+6tdncYil<7u18pD(EJbogN-;C#>Zi#IJO*i3*E^!{slZ!7-(Ut!6PCN!)ZshSkJc6@LH<A~ccx=RT_vDE+&)tgWEqHue-ek?Y*Toq=ybtfgyD{%}(atBV;g!+Or}65xv+v21k<rd)@<g}beor2ajCMYOCu=-<r>7rAJ85J%@CiK9opo=-ixxZwJRZ!Ou79a@I@)=o)$>L?)?J$3jYkmeq>-WcXYvFlG`qJ6Nl=w7DDM=j&aH|s;5{K6cqOlG^_(fs>t3l(=f$_yC2JiG*7+8le>GjxeI<N!AKeS<UOUYB-cio*YAKyh*Jb0I=>*c|-c^^U`@XTxzl#pTw|te(U!`Lm|9fK{P6WA97p~RGB|5%V=LYLyi!R#f<bJwjnx-m{h5N3$oYnc!oz_hsovALLSAKMzy719i>*%d@?%j3%qwCg1Gu`c?nw>_zd06vlylav-pU;z#fz3|dpTvmn<V}8K9*qob_VP?}Q{DY|;WV$vO?4v!WOw1+;n_ah@)*)|_`@5`Qwd}t-(mVf?`~wV^M|)l4IC|a_~-RjJh>syTkwi7AdPGj@dTc)czi=%I{3;idpsVTI6Z>r_j!{}gdhk__&3B&%T<0G+}wx58)sO4%Xh&|SK^Y!rH4334nM17t&5{|a;Yw##>VCMd<C65@;rD-kaJZ@=alh?vW{~0ML+N5`i}es&5<)<&)d2Da;NnAFu$=_{dO+-<HC$oI#Z>7I~V_Paph_(Pv3CO*STcPMH?=<+(q54oS2EOu)G&E7R7G3$lU^#FUn!Cc@>5Qp%7r`fPHU7Vg+k|pWA{FJVge>_)-`jfng3NRD`y}1Yn|J5h}C!MPYea5+tTr!{i7I^Ge}P(g-7fISrEq=FBcduVFtAsbMm|ElVKtX0qvl43DX3GLrc}S4b`6C05cWn=X{`1+x5;QaB=GXDAC$GBGc=3;diJt=S=&zBTsC@;!fED1N#ByXC=l&6?>uNWaW4OI6775o0uv#plUrLq^NS)j}2unY%*f;B$sD*CYFVw>n6h$I<w?G^SUiB}>}vf{oqKunrAY@y6H3`6}pma$?RMakBirQhojPalC9*iV!P58Rsl;1mPYJaaMX&oItRNAV`NeHw;IQalry7aDF%#7a!nwG*0YrbDK@SqDBiF9*x@CS{F`lF;C+JqCpJ%{~Qgv0WO`z6)`-jLS6n`V$dycw1&&4Q5WEN^?ss)C-YgH(?QB_oIqIF1Xtcq(!NcHPdaTu+q|`{TDV6zyjimAyD9_ZV-Lp77vdPU%Bwgzmq*!&o2_tO<7PM!ei|+g#ql5<yF)lX8Yjz*(*Q?}xXB!s14VggrWuYKap9G4(uhm%ymJ1XSMK0v?tT$W1L&X6<PB3M?_d)RTa9eKl1-}ANlXKsAl)#WPMtKdakot%6%=hbuKB_?oQvzL$REF=EgZ8w<vvNLZTPrjNLui4eahS0;&nE)zvO%n+MUl3DjL5sEovHV(A+a<(m~6yS6Ahk2Z;DxNQ<^Ku4oJ?MO|qqeXl$IERBFhkR*yUcQtLUY5puN>0H=V+WaKibe85c%`Zm;1&v>mmN}S!h|x;7r0>zo(sI@)L#)zYPg5r!LugXb_!-fzd(*m}Yp2uMKC}<*Lo=eiesr>g%8@mUFA<zPNF#4++xz-0MWOnEi=jhB-lh8bT}7fHIm(s4j%WPn;=77?O@v>kWvh%shx|{O#vMhpCW`QN6fu0=S-wVx)1o3xH$d~BT9mV36QmxxLn7a}qj#r8ye7)=#tE_z2!h0g=qGQc^BskX*qfy&Zisjh%~~XnMF-Z1i!{h9MENDU5dAbV>=gN;;=D^VwTJ|AerO5laQ{^|73IC>Ma8M5gWR34Ci08OgNXXqDCmA!y`ZTA<s`Zql=R%A1E2#-RLm^82sCL>4kNlf(D(aG3+Vi9fewRmOR#(@@mut60!oIUyf4d5z7Ui*2()|!`x50=n6w8<ZJ;y)<iQd3xiVG+<p!qPo7C{<Q{DnPe^YReKpsH(*bA$G#0oSY>I!%m6revy0mAo&ygwpH={Nu)*CyI&m}Eps)t1izi64;CcL6~YiF!z(n<NiN^D{{aHlfE!{s4&^Nj#b~_mG54N$$uC>~o@dTT(hFoyUc|p6VhuI+phetgu!Aj(L@shbS+@im<yYqIwg=y{65<H1}kss_A5YOPt`Sc-kCDb7vNBut>993yZ(IkTtR7G^+^m?X#Tja=12t=ANus=KxLcmbl6iW0tsqEZSyahr_jrEL+(KBH!_$N2?W%wTnB&a%L=PWhEOHW=6_3YXX+QQL*`IO=c{C*vkxM_^kV^g+7))#$sa@S1b(3U{j==*3@(n9%PBxXDjE`@dnH3esRbmYnHcR`HGdcS=iEWV?ItR%Z*`8kO{KIA{|gW$C{3@jBfB@gN3&e1{On>Bt2$vE6eD!6&IE)um4H+^7B<4A|`^GuhwM7VhEfbWW~)MyuGaWWEMBF!ZB8QK1)8VqpbP)EdM;#onwc`r1}-?=Wu4N;5ChivE74qoA}|=U0VUft*^g?%P%v=iY9QA{<?=Z(D5$rcgZqbrjCq8J$TkPh7ixYQa_7z!bQQ#8d;td_htp116Z(Vjm2YFWWy?gQVtIDL`QETB%ftgIQ-5M&h3KjS*%YNPO&UDAU3R2u>@GTHk6k<9^2Jgc@^`gSva^OuCW4a7jYI!v|g=X$-+bMpt}SYEYiQsS<!~YI^*8K(HFzt*DQC4)qD|(C5ttSA>doEoMxq)UW5$8)I_H`VLRD)l0}UyN|r3AS#FIrR~Mlhuv*UYjL5-$C{+D%MYDJ$i_BOPoSxJyzs7P$FG4oB2v4%YBNlJ4_|~fxTUgx2YQANN*<ng-xd^%KB5YkPn#@??04u@f30d=fS<^9Ayc6s7Lx{i9pYIPZP)%%Xd%fuB0NGX(M~orLOUf|cu!tgJYqr;v1wG3fvnq1|k-V^sDj8Pey@*V7r@Va`EiY^r$-KGDRgt$Bm$_XTR#1+W1=x3+$s+V^#1y_4lzBLCc1z-KkxGgaHr*@9CaBDut8mp5WXVbvAfXLqm>tG>=>03nB2@3rkja5hXOs=UH_leFR3$1FGJ(E^bf62=jb(NG^f@xuDMQU%O^n7h+erU?AsJWcM<|oGlI1ki3uH$_-!?MeA>-3e>buLDug3V1y{qgEB9NtYJ~A^WK51U`DBXR^yPxcO*w@hSk6pQ$3+uKEj#OWd7rLa|l{3Z)7wdUBxgGecxN?c}mP>S}!@=*MT`s)*XbE8zE&@1q2fVY3p=l^BzhkjX1b^e9(a|+K{!W*NA3LmNGUi&q+z;xS{r)(YfJ=tE*xcoGI%AQ`n756zWT)QTC2KBunoF!)`GMuChPAm(1U5~`DeW)e5?GE{#jP%Mc`Fy`$URjZ1+jXaq1)R_xahD;hVFZ-1k`gbf^A05e@k%r<%Avw(Z?|GK7WNPZo7Dt>tKA~kPCZSY_(5xaDKZthVM?U2rfS6a<A`_OI^v(m3FT~fp2(e*ZfS^-%WA!uatfgLB2Ak-=sXc0rzT=#WA$~^v0sc;%m{i@*C?ui{Ww_chfMzu?X!<RmIjtw67F1Ga6}{TWF-Sdq&gvmzK`TRx=!na8=Qp@D*gDJG_TAnSgBU4q4m)nOl?bhRh8*f&bkjllztVZdru!H$@&GHYvPhH%Y(8O8u||Fxi0li?)*%umAz=v;hkMivzF4392m5p92b<v+TR@oi1MS9@^`|nH@QsOmtWnbBKBDdWo$or^3zEdXb*WLSxs<+qxKBP9M7voYm5D;~eh_CN9j}$*spGAfqb{bOjR^LmP=ATeEQe4!0TWipQ!d8eG20w94nv=Useyy}Df39|K)QeGGQie2Mk)+Ld#oy*_^zsG=V1I+*7@KkP~S(B-al{qE|!T%mGBeI4Q@dMDRAHDmmdE|0kPNMt<B`}!|GdpPqgOunTV<Kywnr%aQ9Nvh~+k-``u`iMC_`450iP2oGX*lXftJ^WglUp|__;17n0>82)M&8G2H^E;d{GeLH{ttp*1i8e_!!Npg73TxBPd7D}5#V^x*-juhvtizu<7QAYjb+X*gk6{*Q<L?=+MkZP_)r}WdO>DU_{B!m&nV6g&vlH}vPxP6tgWw$3_ww^WDE^+PZD&errT}HB1jR0UCh5BNI!vTP8aQdTHnBDln8;wA1WmrzBx|N3jW0lxJ2c6bNxH7R4wHjLdT4TBB1i)H`O$mV2^*Jv0q1@aZIg0m1-DJ|y;X~t&(T4`D{r3^E0Wt^rLM+yKf{Dik_7J1IiI}FMU48x<Q|f`S`hY;uqk*!ikg%|)iX4;vs)!skisBR&eV$#rJkYvpxr73dy;!Z^12BG+pdx-kAhrSTT+0$!-7QS7hd&Q8bX?M%fXs7TV8nn_N1;3iaVrt>Y(^FSMATNczVYkijQ<JSHV0^wjbn^i)GP7CTrm`fh4F2PVwX=Wvc_78B*D%artV6EG_$i{>0F&*~g?|7u-O;9yjw@SRG!jVY!qAuSGW=_Vd4f80NJW`K|%_-w%cb1tU9{ujW-_qh~)lS*?Jv1<dKtJHjI5;$01!x^EskumrHN*=oP9FJE^=kq+3T2eUBbj!)2h&_TiJNLVt11-Ks|Og3ON^t>Nn;d>hDX;_4k<p5Qc0t2~oOl>^u_k6*3!V=8CtYO%MFU!-w2lOwDzyD92uml<KvIb)f<MA-p37ePqW`wcsc8O7Vx~SL4*QZTVAB>kpz_}7$!$iaUcvvujMaYFO#&IJojfVXOOaH*~!P;q9fZ@5K8`a5jz<LIDK4ki*w!R-W9fQrI`;GkWJifl!yKb1jAB;_40x-V|bN7I~Q_IAK`lnbbykXbGhrq7@&=u*1_jiT0pFdRJCOR59!bKLY)j7|TPSM6_Dnk&#k8^ERHJ@_%$`$ofaDrX5haIJ@i@#l|ljZe5<eC+r;D~f^;l`|KVR4oG8ex}Nyc&3TW4jFtKP;hQg<Td8W{DZgZ=~!6c#9DTmhkc(V9j#htYo5+<wrlFqQR;u{~tP4yr#-8qY)}%ak}+QRUSe*Nvot%dB|v?k*auF#ZX-tauI5!n)JWIN=q_SrBXF@s`BB(th;Tjs?s18=9~H11T|?Cj?uv|sfQV%Iit^bG_3_nG|D|f&4W-_jyln1Z0Zq;swviUHS{?jVHPONGqyoZW~k!a3opM2S7t`#;D9|UAc}iXL6^eM5UR(<DFTOLqfikF%O~E9ZX7^GU03}Ol|zVwQPP7-k5IWd1;29$3M*0iP_srAQ?|T5M{!WAF&O0sp(c%*Z-RQKW{6+uMU(&S{rDaM!{fdeDo-Aa@*6*V(FxHPsf)I#$qW^$0%a^*E_xtJk+pbNRD@-!QTg<xm^d)mRO)HePJ(PBDpkps*sYRuIWHzFnwE)vrAqanFbgdIzF`C9)==&-YHEFseeHNtFDhSkbCq<7%{QGcQqCDueih~MYHBOI4uesA03{|UR_RgGY=g?LQn5k>-ElJ=K~1eI<uEmB+D`F3cAsc6;r2elECpLra6Kl0(J3>8$Z(=ht~O)6yT?xMcBZdbTAzuv2}j7{beO37Yf6Jj8t)Q+Ow?l{i1HPtux9em=@3guOH*hy31$lg?lEB@Yi-IQ&%#6xP0j11$Kgt+Y1XDxnI=66J;0k}u5j*NC&mM;4wGn8T1>1>e$7P2CXZ3};QLKnnY=dTN1}iU!|itWh}1>mio}}aD-t$#-6Ng9MSR^Mwv&+$lSt<a*7MpD#M6tgpwTM1f^@zJ7D=-{#=%yMSV)Wo<=*T@PWW*R{UisZ2={^GBr&`2*q)T%iHe4qSCQN<>3&hbj>Y@B6DIh+8<r}M(|!HNo)iPT6UrYhQ-08+uoE>KpbpMi=BfeUZ;!lPl(eF@TR*p(c*9hTPUUL$a`};p%ES%3LH>DTG&9kLiL{C8xyywqDU*9_n$YCu(<V7=auC=oOskC-f6GNgmZ1T=BvmHq&tH11lW8YixEtVRu|uL&5+Nx)Cg}pn*@VQ$NFFjd_ehMS_?V=kwBoHuevKp>B(F)uP473yMZRCg9+134(%1iNNCNk~qLE}y1==DN52xQj0|!ZDL@N3da@BwVlb4Xh)rIHpLlS6DNIIoG=+vbN-sy4d@*q+;O=9@9MGATjQh>1SZ@Xht(%eHLohysgoJjI8Cn##tPYimGG_{hZPLgXOVXQA;)kr~7VT#9FSI>BW!>*r1K#IDRUvc4Wk;<F6+POa7xO$HynoLNtM#9uGoNI#}S${IxJ4uA6HxxF<KDUrOB%>pV;8I*A{ham|B()dkmJ5%+_qp!$qZUcLM#4O3Bspy^NvV+}cy`l45={~~6Y%<mmecL?XUXX+(~cCnNFL5!JT&f;D(NM6{B@9eZ%LZe_{%O5-oCw_U0swY79`#$g*KAR2T8XJ`ROO{ij+1Z&_CBB@trG$TYbM5^F!a)zj#j2?>?x|G6Gq46aSh~(^%BO;m5q2_-BOTepFm*1Bc^~@uo<-iGMouvV!tkUD6lSY-yqm6RnN$AS=^v!*&0ib2V=iWpY#F$bC|gcI9*#%r=SPaP<i3`*%JsDr$d2i%6jHm~2Lqj)|hB2>Wc;gN<2F9H>RnMD)AYN{h&wi0XmHv?dZQs!vNHh<QvD3Q_16krs&-VG3Cx`Z?8aTqD`K>Le_Ggk~Z(5qT83$D+CT{;l_UJ~F%*H{gXRcP341BHj_H-l>m8qT<ZwMMW}Zf_Q6DeT1SJM6@M}n<7~ic{7oJB>MiZ&y|SUL~|kHO;NBCeP2$K4xs0u?lUBg%{nffR(E%)Q8Z!5#aJZzF#7w7$@5gOj2VagO!p9po->zpcVBEfT8MIuT^0o^5hb{fnu(+mrAMN;CE|HiM4KXSBEqT%k746SBHmadxEmi6sYWlxBB?@QGej%5M3a@M>!M>FpPV5ey9%NUKsW>EBxtId|8WJvvENuRZx8Z&pxXub&O3kppEn*pGR#J9bZGB&SbnVqAQr}Ae#pI90xVhU0GPjC^zAWarDCI=`c<OGJjh1ek96*YscIgmq74;k6`89%6|W#CRZ?Y%)~X!*bMPKaLsV>|Dk^WnTA*)L<(8nOsmkLKy@6^!*cYL`a-^z!!Lm^$-6aoIaZMEttI{D=z)t#Rs(DRCprSSvHL7MCl~k&<7MzU`R3Zq}8mlH(ybzyPVaOR(qU&C<GAu%doT-Y;RCsDOueHf5f=dK1dDbe%Y!Mrk+fb2KIap6?l`mA&X%$tfdQwW%Rc~0lXsVjbR1Wg{P=!zDqz5f0$j`d9DnIqowu*EW-*>oekjleRgs}<(x)B00hgICDQf*xgRC)NxzKWo6#dox3j4Jh@{4vyg5i05ElMQNKLwP{4Za~?Ka?eDilPGCJ1qb!aFElgcyz^(-Z(R91%=Wyx-+Pf(JO5!kE$G3xs|kR&Ajw*MFdHzKhHa!`4tLy;#B0GpB;_+A>?N0rC)k)Y_lsyPgoYy75Q&LM>J#Pj<-XW<cY=|;6Fk834nv^BI%d!C=7TsMdJxaUMO=xf5+%$+D@49c6v7ZutVFCuMefLqeepWiDAiZ#D3Kf!(dHV3w$BkyySXF&c$2?_BCqGjnTg0uG(n&u>QS2eA_pR_Mbqgu5_3_JotZ-~1c?dKAe!3l4D5PDvMUPPB8In=pWtn$s0@$wigNZ?sDged%DEN<0o`>`D6XPMqGTiDW1<8if$14DhN25mY!rpDBHkA9BJ%s9)F_&Z9IW#-z7vF$^B$mRtdrnMqcsujiRg$Zx*{BACQ4eAYcF%ok^@nKu4JWXZWF;8b&1@Xh#N(;_JoCgAIH{+bXu7WXx5-mfk=bm0`hwxcL>BfTy!23wn5kcc@-3PKwKP@JpxVFfMgdm?SOnE2oHm{LAML&H9O~GYxt*zKHM{+HxBpA@xOOcg^i!y>qK_{c=&ItDminNK<u#|k*k{aLBoehXEhcoX<VyVswSJkzX7TYYL$l;NvzxanW+4VDp{d;10{eWKn0_ZRUC<;jnUH#C<myxfogp&J0nyvA3K+bVluFYM>nDvCia=EloUCC15gZ~uc%R?QL_;$lql{;c_<X!LP-m%@$&n96=BBj?=(f2XvxqvDe8Je1{2vW6j_=A^m?zS;ua=`q?a5dGB&v$6IbPLNl(xg7zv&O7&$%Z-X;$w0m>1R)tzrz|Nc(X3_~nMw|`<dvN>p?#(RVmL9!>9^5-eqY>*)Ew}1ReM*@HQCf1WX1ge>jni>z+$aR{64o(y%4@2tFM9`M;@t!X>hMWydY1ibn$&WJq#+FD`E}k}F%*E?ANFIuC&?Jvc+_+AYy@@MR@xDQ@g(cWW1f$PWk+IlCnjvJiMe-Gi9=$?s+?pSMoVrM~OA7i;ieYD-NwQ6v+DK*S*}q;KFq}Gkqm78?)E_8&iZ34YJ+HstT}WXg3>emiWb7yRHIu?fl3&ZRD#qcmPVVE|l42DA%<o*Ri%w~|#iyJ-*La(!&8KnDatji#k!YLb*ZPq)lTuOYK?co5iZ*z7r6nBOt2@Hy`EIhgXKGy~Ba-ZP_8URk{w&#%un}HSL7Jd{Btzxz9;tQ9<S!(-H4;IuvUSq==aR=g`}w{$qU(7JQiSap!wX5kws>Z{qi#|WjEGf^U&h2WQrsfR4M<qYi;vVy$~iGnH=DFsrFaP`tdXc9u?Z;*yYOaB!sZjXlULGBPHB}iJ$se%%;kdQVKPpFWRc>u$JHC6R?=)lB2Ahh{Y~^7Rf6thvwk$2kbd8Le<GOEX_4O$6*EV9O@#H!of~mT^fMD-<GVt{8zM}`^qsfxsSvpyQP>b+<Y-GY8?DjrZYWrR>NGM0Nd@w7k*>Tdg|qi>GY}sD;nZwjeCj$u#~R|bv@GPRlizWW^n+%d==Ule{?0ppj;*))s@-CM$1vR!!+W<P`A1oPVKwa6M}ll5Ba&>??iTZUJ#@D5Fb%D)-R&UlcYkUS@kU=i(Nla0dV~aw#cYbEQ+X4XqPqKCfN6n+C<pz@n?r0AO*SIYhlBef+#qI=%YC{#MbSo7L|CS^(4OBGMHs}_DN08>b2V%%+?pt7kfA7PQCt<3@zmqFI>AtcIkG59S`?3nenUXgRue(qP!x}e!V%G2=iMAjI`0+<h!Pg*LxO2qVlSd6SfZ%7*G;ZbL}sGmBOi6wwETWc5LOCMr2IQ{uT#Xu_n#LPec-}cAGlgXkdO38bf}yyd7UO<2AXz3*xWONe%>PsP`-%fL!O{L=L0LGLq*d@-7Y~Y)gg~GdFG<(>!iow6|;EUS~EL_PNlVnY7gr_@WboV>v4}fxyNAbNjo0j<e7_{9JcZV@L;vIK+G;cop?SX?DVj$hoMK^j)&loDSKuMj~r@-cGyGEp3Xs1z^W%Tc@Dkf&65renR$}-@S0~n;=w-D2RzBplSX)AlZPB10^Kf#*X)!c4VL_!r|^#BJ+oZ*9xB-`*A3OsDS2G3dk+<+-qopk#kezuQdd7x#r>+Fr<+ZBKp2jtBdB$iQ7Y<E1+DTMDymfZ9p6M%ymb(rF4rwGAQH@jncz@x(&Y`L3wT#e;p|F1!xWC0rbbh-*&;eu-{p00{QxJ>Mbv155~u)&@v?35jV7`*#Wj=YXk}<O$=OX*z{#U0%36^$>2~{dS+au&Geec@Dv3|-bN2(VhYEEcil#LY*@~(UlMN|6B2h)6P10`+c4~XMvJv4}SInHskD>@=P*InPZ;4Wyh)qPSMXAc1l1e0cf`FYUT8U(BzDSV_f+E(UovW_xsg&ZekQg0_k_RnvYoY`NYT=lu?U|IOV{P>tL{y2e5p#lD!F24-;7_iRnTU^xoGt;~5w+dEe~+7tMX3_u=O~N(5`?i6(XmipgGee-(MEo-NDM`BSL7jwfZ>eup~y9f;=%BxrHG+814mn5D!O0JULTYEy-RY79LiERZ8Z_w*FASC?`=?iw<Nc1Chzl5s}1->7ZwKy>fs&d(ImFH4Mhct`casmSGTP4(84YqMWuaI*hifl1c)ocIup^a%|dB3#b=m;Hev3E=<fPOjg3Dvh;nK&1#e=CyQZK`4*F?$-DA+k6irNNtsqU{(h?Z)GTLNx?Im5lg=q$?O;VZYu}Qkt>Ex)!S*N@O*bCO}>l{>64>8T-Or%@AVF4)V3@lqydF@R-*WLsPv3bvorb)kcgh3`TF~x0@Xp@8PO#w1SEKR}6ly^ON?G@VxG~uOqc=YKplQT34TuZfy;S36op~&3ChYG!pnHa*dv=PK~(7rCf1m0sK)laQcmx&;Z$?(|4fD%<EerV#k?OvXSn(B#i*uKun^x$Q~z(kA59Wy<?_Bb_}4i-*!n5N3)D$|2Gt{mG;akMGCp()<gbh`jxCzCebKhlx2QQH9>m$)8XlNgl<8*S=BHLYSh?s*rKR8jSyn}tW6%2Qx1QN=TXrXCcw&d5J)PKd@>3s+&LT~ug8g&`>HI}@uhrvaMLWb7_#YC}ynC|X0sZIpw-oAYB7H=(9_VY^IHMJ6JYrwBx6&?FB`ZPE0JtW20TDv<pVp@it9iP~-xUaU+6{R0L1vqX67KvRI6tVbr_WD-6!0qn4ebRj6i=P4&vMLpy$JvPZxO|CK}NV%fQ6qjpq*VOiTDsL%r`eshBr^WV72_DA|O!2sBeg;W2iJ*M4Ah9N;<zu!-YJ29E7pgl=%6}fdsw_kjmh2uSwLNi(4M|@AH9;w*heFE$Yn7Ip<ZeKziIhf&Fx3)81kbKq?D|+lZ675QQDMP(ylE|K7QOziBGRMp@=iNdwKo%_oF-jwb1M<+5rz1Qv6E17XAxSwUW*-3ys^k{i1x=$hPM+<*NOi5|NVd6YlD3"
)).decode("utf-8"))
_V22_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_V22_ANIMALS = ("COW", "SHEEP", "GOOSE")
_V22_KINDS = ("PASTURE", "COOP")
_V22_QUADRANTS = ("NW", "NE", "SW", "SE")
_V22_MAX_ACTORS = 13
_V22_THRESHOLD = 8.0
_V22_WARMUP_STEP = 48
_V22_MIN_STEP = 96
_V22_MIN_RATIO = 0.9
_V22_TERMINAL_STEP = 717
_V22_SELLABLE = (
    "STRAWBERRY", "MELON", "MILK", "WOOL", "EGG",
    "TOMATO", "CARROT", "WHEAT", "FERTILIZER",
)
_V22_PRODUCT_BY_ANIMAL = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}
_V22_GLUT_WEIGHT = {
    "STRAWBERRY": 2.0, "MELON": 3.6, "MILK": 2.0, "WOOL": 3.2,
    "EGG": 1.5, "TOMATO": 1.3, "CARROT": 1.0, "WHEAT": 1.0,
    "FERTILIZER": 1.0,
}
_V22_STATE = {0: {}, 1: {}}


def _v22_position(value):
    try:
        return (int(value[0]), int(value[1]))
    except (IndexError, TypeError, ValueError):
        return (-1, -1)


def _v22_signature(farm):
    hands = list(_get(farm, "hands", []) or [])
    unlocks = set(_get(farm, "unlocked_quadrants", []) or [])
    positions = [_v22_position(_get(farm, "farmer", (-1, -1)))]
    positions.extend(_v22_position(item) for item in hands)
    positions = (positions + [(-1, -1)] * _V22_MAX_ACTORS)[:_V22_MAX_ACTORS]
    counts = {key: 0 for key in (*_V22_CROPS, *_V22_ANIMALS, *_V22_KINDS, "WEED")}
    yields = {key: 0 for key in (*_V22_CROPS, *_V22_ANIMALS)}
    for row in (_get(farm, "tiles", []) or []):
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
            if kind in _V22_KINDS:
                counts[kind] += 1
            if kind == "WEED":
                counts["WEED"] += 1
    return {
        "workers": len(hands),
        "unlocks": sum(1 << i for i, name in enumerate(_V22_QUADRANTS) if name in unlocks),
        "positions": [coordinate for point in positions for coordinate in point],
        "counts": [counts[key] for key in (*_V22_CROPS, *_V22_ANIMALS, *_V22_KINDS, "WEED")],
        "yields": [yields[key] for key in (*_V22_CROPS, *_V22_ANIMALS)],
    }


def _v22_distance(left, right):
    total = 12.0 * abs(int(left["workers"]) - int(right["workers"]))
    total += 7.0 * (int(left["unlocks"]) ^ int(right["unlocks"])).bit_count()
    left_positions = list(left["positions"])
    right_positions = list(right["positions"])
    for actor in range(_V22_MAX_ACTORS):
        offset = 2 * actor
        left_point = left_positions[offset:offset + 2]
        right_point = right_positions[offset:offset + 2]
        if left_point == [-1, -1] and right_point == [-1, -1]:
            continue
        weight = 0.8 if actor == 0 else 0.25
        total += weight * sum(abs(a - b) for a, b in zip(left_point, right_point))
    left_counts = list(left["counts"])
    right_counts = list(right["counts"])
    for index, (a, b) in enumerate(zip(left_counts, right_counts)):
        total += (0.25 if index == len(left_counts) - 1 else 3.0) * abs(a - b)
    total += 0.15 * sum(abs(a - b) for a, b in zip(left["yields"], right["yields"]))
    return total


def _v22_state(seat, step):
    state = _V22_STATE[seat]
    if step == 0 or step < state.get("last_step", -1):
        state.clear()
    state.setdefault("hits", 0)
    state.setdefault("total", 0)
    state.setdefault("early", {})
    state["last_step"] = step
    return state


def _v22_track(seat, step):
    yarn = bool(_V16_ROUTE_STATE[seat].get("yarn"))
    track = _V22_TRACKS["yarn_on" if yarn else "yarn_off"] or _V22_TRACKS["yarn_off"]
    return track[step] if track and step < len(track) else None


def _v22_detect(obs, state, step):
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return False
    expected = _v22_track(_seat(obs), step)
    if expected is None:
        return False
    opponent = farms[1 - _seat(obs)]
    distance = _v22_distance(_v22_signature(opponent), expected)
    if step >= _V22_WARMUP_STEP:
        state["total"] += 1
        if distance <= _V22_THRESHOLD:
            state["hits"] += 1
    return (
        step >= _V22_MIN_STEP
        and distance <= _V22_THRESHOLD
        and state["total"] > 0
        and state["hits"] / state["total"] >= _V22_MIN_RATIO
    )


def _v22_consume_early(action, state, step):
    """Remove quantities already sold early from this step's sells so the
    per-product totals stay equal to the base engine's plan."""
    owed = state["early"].pop(step, None)
    for stale in [key for key in state["early"] if key <= step]:
        state["early"].pop(stale, None)
    if not owed:
        return action
    market = []
    for order in (action.get("market") or []):
        order = list(order)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in owed:
            try:
                quantity = max(0, int(order[2]))
            except (TypeError, ValueError):
                quantity = 0
            used = min(int(owed.get(order[1], 0) or 0), quantity)
            owed[order[1]] = int(owed.get(order[1], 0) or 0) - used
            if quantity - used <= 0:
                continue
            order[2] = quantity - used
        market.append(order)
    action["market"] = market
    return action


def _v22_shed_access(size):
    half = size // 2
    return {
        (half - 1, half - 1), (half, half - 1),
        (half - 1, half), (half, half),
    }


def _v22_projected_shed(obs, action):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    private = _get(obs, "private", {}) or {}
    projected = {
        key: max(0, int(value or 0))
        for key, value in dict(_get(private, "shed", {}) or {}).items()
    }
    inventories = list(_get(private, "inventories", []) or [])
    positions = [_get(farm, "farmer", [0, 0]), *list(_get(farm, "hands", []) or [])]
    actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    tiles = list(_get(farm, "tiles", []) or [])
    access = _v22_shed_access(len(tiles) or 10)
    for index, unit_action in enumerate(actions):
        if index >= len(positions) or index >= len(inventories):
            continue
        position = positions[index]
        if not isinstance(position, (list, tuple)) or len(position) < 2:
            continue
        x, y = int(position[0]), int(position[1])
        if (x, y) not in access or not (0 <= y < len(tiles) and 0 <= x < len(tiles[y])):
            continue
        if tiles[y][x] == "LOCKED" or not isinstance(unit_action, list) or not unit_action:
            continue
        inventory = {
            key: max(0, int(value or 0))
            for key, value in dict(inventories[index] or {}).items()
        }
        if unit_action[0] == "DROP":
            deposits = inventory.items()
        elif unit_action[0] == "PLACE" and len(unit_action) >= 2:
            item = unit_action[1]
            tile = tiles[y][x]
            structure = {"COW": "PASTURE", "SHEEP": "PASTURE", "GOOSE": "COOP"}.get(item)
            if (
                structure is not None and isinstance(tile, dict)
                and tile.get("kind") == structure and "animal" not in tile
            ):
                continue
            try:
                requested = int(unit_action[2]) if len(unit_action) >= 3 else 1
            except (TypeError, ValueError):
                continue
            deposits = ((item, min(max(0, requested), inventory.get(item, 0))),)
        else:
            continue
        for item, quantity in deposits:
            room = max(0, 100 - sum(projected.values()))
            amount = min(max(0, int(quantity or 0)), room)
            if amount:
                projected[item] = projected.get(item, 0) + amount
    return projected


def _v22_remaining_after(obs, action):
    remaining = _v22_projected_shed(obs, action)
    for order in (action.get("market") or []):
        if len(order) >= 3 and order[0] == "SELL":
            try:
                quantity = max(0, int(order[2]))
            except (TypeError, ValueError):
                quantity = 0
            remaining[order[1]] = max(0, int(remaining.get(order[1], 0) or 0) - quantity)
    return remaining


def _v22_relay_covered(step):
    """True when the base engine's RC2 relay would move this route step's
    FERTILIZER sale three steps earlier (so a copy sells it at step-3)."""
    return step % 24 == 17 and 281 <= step <= 665


_V22_SENSITIVE = ("MILK", "STRAWBERRY", "MELON", "WOOL")
_V22_QUIET_HORIZON = 4
_V22_PREDUMP_STEP = 712
_V22_ROUTE_SELLS = []
for _v22_step_action in _LEGACY_ACTIONS:
    _v22_bucket = {}
    for _v22_order in (_v22_step_action.get("market") or []):
        if isinstance(_v22_order, (list, tuple)) and len(_v22_order) >= 3 and _v22_order[0] == "SELL":
            try:
                _v22_bucket[_v22_order[1]] = _v22_bucket.get(_v22_order[1], 0) + max(0, int(_v22_order[2]))
            except (TypeError, ValueError):
                pass
    _V22_ROUTE_SELLS.append(_v22_bucket)


def _v22_frontrun(obs, action, state, step):
    """Against a detected copy: fertilizer four steps ahead (beating its
    3-step relay by one), everything else one step ahead, wool the step
    before its 713 terminal wool dump.  All route quantities are debt-
    accounted; adaptive wool needs no debt (the base controller self-clamps
    on the emptied shed)."""
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]
    remaining = _v22_remaining_after(obs, action)
    moved = {}

    def queue(item, requested, debt_step):
        if len(market) >= 10 or requested <= 0:
            return
        quantity = min(requested, max(0, int(remaining.get(item, 0) or 0)))
        if quantity <= 0:
            return
        remaining[item] = max(0, int(remaining.get(item, 0) or 0) - quantity)
        market.append(["SELL", item, quantity])
        if debt_step is not None:
            bucket = moved.setdefault(debt_step, {})
            bucket[item] = bucket.get(item, 0) + quantity

    # Endgame: dump the whole shed at 712, one step before the copy's staged
    # 713-718 liquidation (and its wool controller's 713 full dump).  Later
    # route sells then no-op on the emptied shed; the 717/718 terminal pass
    # catches anything harvested afterwards.
    if step == _V22_PREDUMP_STEP:
        prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
        order_by_value = sorted(
            _V22_SELLABLE,
            key=lambda item: -_V22_GLUT_WEIGHT.get(item, 1.0)
            * max(1.0, float(prices.get(item, 1) or 1)),
        )
        for item in order_by_value:
            queue(item, int(remaining.get(item, 0) or 0), None)
        action["market"] = market[:10]
        return action

    # Lead-4 fertilizer: beat the copy's own 3-step relay.
    future = step + 4
    if _v22_relay_covered(future) and future < len(_LEGACY_ACTIONS):
        queue("FERTILIZER", int(_V22_ROUTE_SELLS[future].get("FERTILIZER", 0)), future)

    # Glut-sensitive products: sell only into turns where the copy is quiet on
    # that product, pre-empting its next scheduled batch within the horizon.
    # Solo turns capture the top of the price curve; the copy's batch then
    # lands on the crashed price.
    for item in _V22_SENSITIVE:
        if _V22_ROUTE_SELLS[step].get(item):
            continue  # the copy sells this product this turn: not a quiet turn
        for future in range(step + 1, min(step + 1 + _V22_QUIET_HORIZON, len(_LEGACY_ACTIONS))):
            target = int(_V22_ROUTE_SELLS[future].get(item, 0))
            if target > 0:
                already = int(state["early"].get(future, {}).get(item, 0) or 0)
                if target > already:
                    queue(item, target - already, future)
                break

    # Lead-1 for the remaining staples (wheat and friends): small but free.
    upcoming = step + 1
    if upcoming < len(_LEGACY_ACTIONS):
        for item, requested in _V22_ROUTE_SELLS[upcoming].items():
            if item in _V22_SENSITIVE:
                continue
            if item == "FERTILIZER" and _v22_relay_covered(upcoming):
                continue
            queue(item, int(requested), upcoming)

    for debt_step, bucket in moved.items():
        merged = state["early"].setdefault(debt_step, {})
        for item, quantity in bucket.items():
            merged[item] = merged.get(item, 0) + quantity
    action["market"] = market[:10]
    return action


def _v22_opponent_exposure(obs):
    seat = _seat(obs)
    farms = list(_get(obs, "farms", []) or [])
    opponent = farms[1 - seat] if len(farms) >= 2 else {}
    exposure = {item: 0.0 for item in _V22_SELLABLE}
    for row in (_get(opponent, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            crop = str(tile.get("crop", "")).upper()
            if crop in exposure:
                exposure[crop] += max(1.0, float(tile.get("yield_units", 0) or 0))
            product = _V22_PRODUCT_BY_ANIMAL.get(str(tile.get("animal", "")).upper())
            if product:
                exposure[product] += 1.0 + max(0.0, float(tile.get("yield_units", 0) or 0))
            if tile.get("fertilizer_available", False):
                exposure["FERTILIZER"] += 1.0
    return exposure


def _v22_terminal_market(obs, action):
    action = _align_hands(action, obs)
    shed = _v22_projected_shed(obs, action)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    exposure = _v22_opponent_exposure(obs)
    rows = []
    for index, item in enumerate(_V22_SELLABLE):
        quantity = max(0, int(shed.get(item, 0) or 0))
        if quantity <= 0:
            continue
        score = (
            (1.0 + exposure.get(item, 0.0))
            * _V22_GLUT_WEIGHT.get(item, 1.0)
            * max(1.0, float(prices.get(item, 1) or 1))
            * math.log1p(quantity)
        )
        rows.append((score, -index, item, quantity))
    rows.sort(reverse=True)
    action["market"] = [
        ["SELL", item, quantity] for _score, _index, item, quantity in rows[:10]
    ]
    return action


def agent(obs):
    try:
        configuration = _V16_OFFICIAL_CONFIGURATION
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_REBALANCE_ACTIONS) - 1)
        state = _v22_state(_seat(obs), step)
        action = _v16_agent_impl(obs, configuration)
        action = _v22_consume_early(action, state, step)
        if _v22_detect(obs, state, step):
            action = _v22_frontrun(obs, action, state, step)
        else:
            action = _rc2_market_relay(obs, action, step, configuration)
        if step >= _V22_TERMINAL_STEP:
            action = _v22_terminal_market(obs, action)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }
