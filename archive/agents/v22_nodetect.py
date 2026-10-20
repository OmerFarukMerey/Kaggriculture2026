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
    "c-rmV?T+j?k{;k&S?upMz=)to%C}-H48tG5!p4lTwqY2C@7+_UN~||XNhyj!r7|ahGlTBx>OS=xDkUlyAOH6s|IdH;*T4Mxzy9SP|Ls5gyZ`%-|NF21`d|O^zy6QE{f+;pfB47$^_Tzl*Z=rmzy6N?_ILmNum9s;{^!5^^)Fw4|L^|xkN@^-`t$$ae=)(|{u}D~-#`EDH~Wu&{a=6ipMQQQ_fP+@_v`DM|Ifet=l}MfcE0(a|KC6TL$mGsm%OV@{`~UqWRr!#3-4+hjknPs7+-1oR`FFfy2eJ!uOl`xvbndkxymNCHfpiaYuR|iCTljfw(-R_zQiUM*rdfKrZ#$S8)+MlvvG@!?{D)PHos=`b~b*BO)j*#%WTqOll$AI7TYw^Chun>u*t`E##Zdj_ig?aZT><VeQXA{sl_&J+T4*?P@m!HMmip+d}pEmdl1UI3gshw2cg*PpFhHnaO~$${vL$#_Co&=euN+4NB9wbgdgEY_z`}DAK@orx@+Xt%+7c8jf<Mz%qMT_8x*OzneXlHFY^9Ad=R=f^zrh^yO}Q-`3SPeKfddH(Za{z<G1z69ev5dM~hFEWSNieBHwJ`bKr9y-<3Xcra=Dzet;j~2lxU0Jpx}l7J3jV=gQpQiief%{*8IY0pI)Z1j_m4U3qL9?tMB>)_9}uob+6tdncYil<7u18pD(EJbogN-;C#>Zi#IJO*i3*E^!{slZ!7-(Ut!6PCN!)ZshSkJc6@LH<A~ccx=RT_vDE+&)tgWEqHue-ek?Y*Toq=ybtfgyD{%}(awD&jab7gqn%IV6~Eq=CnKYs&*TYYpUJ!OXk@hW2|QWjz0aMKb+nU4h6A6#Bi&i|M!aajbHL-lys3#NMm)KS*S31zh{w81)4TBqqMbA{6#q<~EOE}e@Ft@>XOS%^H@UTt5zk%43)kN{ujI9@o-^fn-7EF!y!h6-WUZsYI^Ux6ucm9duY`~8qkCc9Ylk`CJIWbeEv576x@>$ioj}^$yXtt!XM1Cve-|BwZ~3V@H$cZa{&$VeKSM`P(uE6k?kXK$t8*}^=ACqMi7vM2l4+W%=qW>QsmuTWt~wsCn?5>IT|Te;=sI=bqqEl0TkG7r>-<O8t&3*5+eI}yjePU4=F@oBByT>SCnE!!oxDGZ5#7m~{Kh;Q8QSdSndGLr`|-kQUXh#XMuw2?!n?z>eYWK>r0MX7H=3ss$U?ru^o8Et$YSRYZ=)JGTJZ4C>#cZlL!P(b6=6Uc*(Tx%JYVtnhP-s}m0k9DJUDTB1kdmDCY=aD5Ss9Bh?|zH{5H6`4~I9-u>6+qf}5_yC5=lDagZE-R>xWwN9*KLUCx4t%kTLLI(OuG@RT6us*=tr;}K;Y<?M@o-plnJ`3ssOXTqMhbNS^?>GffLW3l?}T=K_-8L4!pO8s^&{^R1x)mWas;hL{=$(oBcTy(jMx?MRj6I}svb6SdGH(cay0m~QVFxdRCAQS=&9kB0>NUUJ(?{ix)f~Uw}7+(tGBQVTTgo@C1m;g*PEJ9^AzbGs(OM=7{YnU8?VdW>>Ng81UFsEU%z?|8o=r!!;AvH|qw`B=r-b^+<kl`^EO-3^R=L)H1yu?cSWYdK*zCf0LQVK_8><ncAiVEiCc7dNWqcuAu)3?TcS-$7b3&k(@f44l?u30mE2kDpjWvL2TK4OdpviLk1ZOCZZxLU|UA#+#A9DL4D=6Ynm?^XwC^Eetmm&Wvpv}8%UU9hnm8rGq~D&F||I9~-FPfpCaBTkmzSE{eSK8}~IN)ck^C*zz2jv(CQA<jy#iW3Mn5d`TF=Z4|vF)mo(1kMk~<EA|vkH(1|Zf>*bSJY@>!=q7KTkFE<E#_&QKs1P9|DU5lH^8N{xFUu}RjA9KOANXNj@EGbH0lBzuij5o@MJ!Vb2>=*jS~nfo8VUNCt=5?!zZ1#pl#mTwzhD)IJ{Z1>$@rg<YN!U%@^Vrw#utGIhRM-iJPr(UgKss5q=sj4#n{x9J@m}KN=^?jne=}jkw7imjgw4Xr>vC8*$;4aMFlN@4RyUomcMQXYPIxOathj&*TkLChuSq4O@+DzLHI<)JaSOogm#XoKBrIv2nLeAQcpCIj;G_Hk^y=tH>X}qAeV=J>@=0r)~JSV@O)?aDB?#+v0ULwZG(i5Zay35GoqKGA(KvZP45^XwpH;u~%2+nFomYT}X?zG_Gh2DMejrD1EOx{w$4vMvx?mG<P*^u4(=(E$Lj?RoeU{+H{uYG|ewZ1O<&>la@J{fQZpbx1{gU%hGbzC_}8$Ur$pfA46zT(fAqBu6xtEo@=Mm**>%n?L#x7y?%7EgvyaMj4u(KJV+yNYuo$!Ek&XFfs3I-Mc$?Q`dvk$AvwyGzm8}8=;FJIcuj;~r)8^*Lx=oNnZ_MOv?hx1brdmt-C4dyhtr}WO*cUEpIVf&U=ySsx<ex0xTANcMZ6};@x}?V5D0?Ah3F@5rt=+zirAZ_C~k;&5zSg8k3|R8h>JAHD@6Gvx)A*|GVB!jqT;+uG_{BXa(-wD>2Uv5Hx=c*=S9V-rGwm^uqN`0$b*Rb*C^<IS-qgC0_7yS8kF?hqXVD=OH@o1z6dmFP!1!yJ<#|2OAF}yZGjGha!as$D)C$NZURb%pu8{3O}-G6Hwd(R1^W`^R+zL0N^PJt0_4FF^|>-u1my;%+ndzz=TqJSI)77ek3b$k`Pd7qfW!(kAL<Ht7!;sCNCCq4hP*!_Na;8LBG)F`X_#b0O4XLn0f`@w(suzt6N!3Ap_?QRNb@sE2{xg}N&Wzd8%aExH208%OiAv@3+!{Ed0SFCC!NQIyq@YJH#(O03aqeJ0gic<n1?7Y!-}xGE24T6#J#4?!8G?|rK;&<eoLI-sCe2ONONZvZ?H(STnmf8yO1@p<TR@Y^6j&n?sB*`faad8S?2&v@RqpB5@VLQfh^i)VTZ%Di7Z>$2qNF{p+~C~j<t(B#d2mWX=NoF7G_4uHfsWwz)`XJYE5P=f!NCoW%#W7tc5<7KgMEX7FR3`$Y4{XoYvHI5gufT*=H-~)$s<)>3(s@B5RhnVfl)cwprNHaAQ7BE6a^xO^^w)#UdS0JI9)iv5ao;VS|OY5(XASmLxr9aVyK{vlSPXEU*7b_ww^q9U>-zny=Pm#$pJZ9%RMM9=yG*_+%D0vcfS|dOk}&tfQ>?`7HlD)}3RA$E5ld?B{T1t>86{h_T&+cANO&(_LEu#I3Ktgv&28#)>9zlm5DgH_-7e?sv&DT&9kUMm>1eH--?;yHY=kb;3o#${Jao758QZodZ~~XpO~VSY*R0f>I6+^F&8)A|#(>Ryh3563*>{?OCi(7f!J(HXt^vRIvnDxi*xSJRaNCT6q=or&&0-Bd)OmY!`7BO0-_BV9CNm@SwW{7cA1h%vsTf#X95O!O<7PU)L;mh}C=%iY1FRiy`1!u$*S4n_h$r!_-8lI$=B6c#=hpEJ~Ivr&(@|HCGp*8?ai=@{GvAekfG^aYeIuB#X>g6P%vZEWgHbM=wG)xCl?O!Xp-Mu=v)i6<b)`#%jK0h}mIEY`F-z?ILVlEt<?&;Q%Ya<_THzeOc2nR=gAI^+Sli(%<jDeKoPM?e(Ig17urG95IF{FDb)(!y<}^t=V2v7W6D{%&N=<MDoHis$^J=_aZXUo$~f&w7jrgB=hDnS4G}lT;_IVSV1{f7GU3PCX3Lw5mWeHQ0C#l*)55`MJg#y*mSQXo1ijtuEJGMkR>ZwfP^-bVRjhjq4%#Oi%`8gLna44ol!RY-Z)#yQkAG!$OQTt(t$2eH<s1$)91)srwlc7H8C33Y$N^mg=Ac%AE8X%N|w`5FOVG#ecQ-<hm21@sqZdpz8d34_O7xwh(MOoc_YIrScU2C$-7U1_p@OSTO0cQ$t!n*VeNL|k?QO5LYVZ!a@tq{V?8t{_XK|#ST1zlf{E^TIQUJp4~ADDEs?AOMj*!~fwzV+G!LaE?o%uj!C!c2cy!IqzZd4==MHNrjkzc=H-@@q<3A840F&V`wud>L*;u4C<{cz0iK=&p$r?<a1`{(_esH;}du{F+fgKcbe*0^{1QsM#QLGDL-V8=MkWW>EK`drxX#VyZFggsAp_||;A@wATV8f9U;u2heIm5?6I5G^p-CqKW+b|vlTZtH)hhdwGt&WNgj&%1X^W6#-0mjE*?hRmaDJ)sS((a`w@C~mGo1Y1r55itQ-uO$Up9GPwOlnSVkr>#3d$oAu7}|c?W6^u@wP;&;k9GgWa5>F)(=hR|2=z==CD%o?uhcU$8fltaXr!}#M$;H*r~A^bral(otD<S)OVC93eh+Ij0ovG&vbYg6w?^X)nj3UD|GQNt_e)!CFwsVfFdC=G5yS?Dm+UDC&YSvW31qS%^A~L@O=JP0+-XA=Ko$pHjuX^ib{r83oWJbD@a-;M@k-ha!<imA+e~z*7;}ty?23soEa%G2)ryfG+d^Yk%p1cPU``*$5FF&va{C+)3pOxJ?#bQBCNLu`4TJ?77(=UxBBQf_{SLqx3yXE-MK8=(=~(%+`aFzJuUH=pyJ#S+sG`CCo3F8AUc+(<wb#e<0>##YVJqq2XJFF-n7b18yT|W?g$fq+rHEJQtzhrewsCn)<F`tAJnsAYPd|H*^F2_$rE}xsS<a_WlLbnum}-&i7$GK!c|ZA2fK5?hdw<np;$=bnS~_4pvB7{429N2cCSOgm@l~t5oEn0ub>^mY-Xz*2)w~y9bv3L_KgV!pjT*m9^LbO=>#~lC<_PhsY1RpKKR<?9?2W&piAE+`Gu3SxS50iWKV;fz>)K{=dMHoO_dU@^y$+&vT;I&k2c<aA-!?L(HB*2hR)W%)J(F}@dmSdy;SHQiTbo#$2ux(KPJ$-iYmzlnk>(emB_5h&%OqXbUWduSB0V%YFcBn&{QT&>>x6C2IFDrQBGEP}_hE3`B;Q-(h-n@jB)szWNwFfi{Z;B}gU6wVByfk$Ip=kvV$>fd_mI@pu&|GWEyN2_)TA7@o}mSv-72|)<OY#)4qt?b^$g7l?N%w+liVYc*DWL1c9m2e6(q{qk^&?o79=vi@T$+!5YnU@6xO8K^1}1CCw28(+#$VFzs0X9Y=0)p(|ULK*Y3FZNcVEp&f{eJQ9ij?7ENTb7A_M=jGEv$PhL{CI{uj<zik?q#8$}Cax&GQF1j@-nKbNz8_3t=W<Cq6!^<@+SGnM|=*Gi-{?`w~Y}X<SHbA%h!LXoUWC!!rbZcx2?MG*?6)?7dIURaOScK%ft6@|3&0`0a05&#x?f3QN>y9YW0h{y~7lw@T30f68s7D<MOJ=YD_XC8<28@Ot`U5O{&rUrJi%`-WpyE<se0Pqijfef7FZfPaf@zsG3|sbPc^deD{)O@Pztjm!kQFa$FxD_04|AQcd3kR}80+4c7=@>cI+A>S+9dVCcv%FTLg6(`G|Z2O1ru0=<oIHEH^S0r*l)1(4=n$wpN0h(wJW-<oh%2eXJF?;rhf|W`(e{D*gU!;$?wkN>zlpnhWY!!*aRj3^Sdy257;|3SX`)SqfGJDJ1jo(eT9FnNH@GaE3Ezaq53w_p~w*|GGMJvgr0PgHbznz0tkK>Ype9~6w6nvs2_k6Y@j`CCT&?i;my#=@_KS|%?eO=L^`f;W7f2=xXOEtu)!?e3Ou~5-G+sql~A$5E{g}V#Ej)Pvh@PIzzD=iczFe|X1Q+`+puK$*^jVjFzcrzlKWY_#>#J^5vpTx5cXYJ9s)W^v!r5q$Y-IEtazTqP-hu(L2AXC^gqIyOEP4o6;|p|<+F!bx8PV+r9mo8H}kUzYSJj2xr0$s4+BMWLZ9&*TMLwElzW7l2cfVmb;?D#%_yoyUeDEp=zM}%pfJtY1~r+XieoRl{32YL8I@xL_Nag;?m-1z6+c6y9$TphoQaJ>MJO?!euw3rKt)|&{ScKSh=WnmgG!H3xi$sAa|j9xQTkA`MinEuygo*8P^vK)<p-fAjhb(QdZ!MFU)e>I{~bW{9s$GSz89)b9*puEKYY<1(HEJEwy4Pr6{`AVtXnP`BTA99cvn<}WvWs6@THhZFxeF9Y1B`CtN|)jxtG|&l5{mM<|>+2iGF2D^`I~bETh5(%B`W?W7O389Q)ewre0LO>gFov5<7A_U89^6ru-_(<JHtwcO3?!_y9^wP^_|}rr8FSU!`J&3c3qtI)a*7SIS{#)HLVa=(+nulL@!?5e6;Tnu6;w3CvcRAw-5#fAWvRdUuZ<-tA0Zv9vxDYZK0!#qlvwH{6s4lQiBX{+Ou8L=fdGOkvIBq3t17kd~&<Y7$Hq3fyDDI@a2hL!O0+9-5lhNzcxePSdPSsWMG^Y<hq<$z0&vy-tjWSRE$OrnHz?oBW!Ij7=V+?7{b&xH5Td%8x_=6NcOE?h&br#1)A($yX$7^SVbme~b9~#=LVmPa>TzSdVl|5Kk|{f<~+43ex!+SR~E*7zaBtVjVHolY6rpIpN1O^phNrBHRa#lf>-8V|!A5Co1}8UPW@dr29nyI~MQjPMH3D_gxE>hvB~dTThAr-pJ$+mnc7IP}pgj`%MRjF>}@X@3%ePu1Q)=zoVY|O}t?$CaZEapSk=zMP=fKogn|bEt;8V!$jId^=Rh8l$6OmHce>q^J$YDHaQ4t7N*sni@%j3^8N68L{b%!{`{rKI+u3RHM;@s6+0waB@vR+W0J0ooJ~l4jN~DcbC1MGijPSuLMz^i<kv{DLGqeZ-1L6)TO{A`_DJ3#iIWvc;GS3Xkj!a7TcqOI^gD0hAc>4fMQcK?dM{w&5|X&O@cey90-Xs-r?dy1wlu-}JdR`@NAl-L48OKWK~F^r5VHO4bZknRdq|`+WwDSGNgiefMNRsNKkt#IR?^f-axEl`^93v#DM%_r@p$Lz84qvR^^*ulQFrkxF1#&Lc@tMV*T)-I?~z242}#ySm{x}KZLk^ZPeOYqiSXoxa@&+Hl801uBoSPStE8Wk-h!m|;@ooK@%KJ=E9&Bp%p`Y^#9fmx2O3FEn@dt^Bnh6|bdW@o1kMAzzM<t@`}|pQ`pUE;g)WkZa~BUi`=m;E$<2Npq}^MRCN&SUi-fmtujg481&RfU_er6RB=bSi?ZSQf3A`eu&FJ&b^+;RQNViD(YxVtJ%nyBE|KK?xzx$v<%S>e1P5Ns_O=D39ry=uh(w`BE`%!VN102pr#+xGTCjIHq%L>YGHAr7jv!#hPOtdz^gRD%yz1IDAzSX?(3d~JCBlk%~%9Yb4Fxw=C$-_rT-@o&DQBnIFT0{ap$7C~_bW9X2Mc87y9&^lk*g!3cCZgZHR$4^fL{v{VrZtghQGHShLCj;KP>4dmh_pzw2-C+3(a(u~;~L4<RVO(}V<ut~kw=kxESl@@cPB)m(-vz{Zc3WgM7$$XZBrkMM8%oUi;6_d1o76Q@(4vUh-ga`H$}24@@69cNc8<*pDPiyiDDt*O;NBCeP2$K4xr}=?=vKg%{nffR(E%)Q8Z!5#aJZzF#7wGl1Hgv2{X?3neHJHJz_5D#=h8bv=HU`x-1G-B1&){H4{lCN{>WwOT_c4h&DyuM1&O&9>d0uM7*&^a5p|CQjK1WMN);rW{6g9i6$#i*G0!VJ~=}`b`?YyfN=cHNzhdF{o@LRqrb6Q-X7%lK(`C<op*}cyQAMAn{O12+~~mG%c%TX_dl$N#pIA%s{~ZC*8DGjz3A6ts!GKsUHVm`r#r|-%#U>5gsEyCsG<!OX%(5PJQc4WCsk5qh}Nnc_;c_MOhZ&`qbe$H!dj4TRppj|rK!r}@w|a*KhPJUu5zTRe7UkwCEXtnRdG!f4y)23Rlo-NW~zBjMWCWK6*a168<kY5v=*3+5Ktlr(i*EKckpG{9Sr={D$(_>SP>Q>JI+)^W-2@}o7dXo6@ev!7d&efW2T6W%5A7fs~oJSwaS~Rs8ZDfQlhSQ!=gn~)nuk}klTkUd^#sRUpYZ;)~!`J;Gectq^tM7Lv4dpyKnw|Dh%dE2*w;%aidE0b2U)qnJ4=yf`%2}k(x28)PwTJQ1eBobSU!Fh?>_>9#E_sPxhkRGg0XzO4?AtK^^le#RyM3f0mtoO2_XQBphXXUd8XdNUI(HFrF6lJlxgfzgv)GEk2kH7)-<VQ89-*Zb;&_;2@In`4IMy%Y_qcOp5&?S_`3}NH#=bB9i(vIi4={#df<BOyZs30hV_d0-e<{bA~q`#PQIBcpfg|N<@_?VFp?u@@=9JhKOP%Vl682MrQ1X*SSWizDh@l<d}#y*C@1ojyV4a=kE-$MdbDPI5QEMi6#hCL_I-sU*tf<wP-rMMq(~1GBb1Ng&-+G8bnjuoq=7CNOnbGTg32|@)Nx66qVtzUQx~*3suk$MLExcAfUT03dL3QNR(_ud`y%;Brr8&#!z%2ijAT$R>a#PUPOLhlo~~Ik$-hkM9Vutj<ZC#x+W0KkX%}eXir2(M9~%DFf&ooqFi^G^OYQk5_BUgMRS`7)~HM5)<oPWqO~V1^!hlqMx;~9Y(TRHg$hI(6c>=+1Gz&W*5RV_ps)?X#>cCmumj@apzIN7x&|b>plJu>8$l|Jya~EpK(E<37h6MGo&`6I=#9fYbMEh*RAJ+%_d1E)KOXzrs!GmWB@lb8$K$GoebDS-(n*blN*dQH)^A>aX7qKU0u&h3C=cC{Sa<j{L9M(X|LM<bg5nL70Ez$=j6PLyB#JhMPBWk!pyCFq^|9=XP{m~I06Q@$nj*m(`8*73+0C1*loTm{15gZ~uc%R?QL_;$6ew?i@=znXg_0Ij<K_4JCc^vM!ZuTcL6!_1lcFv~WH6E4LXo8@K#TW!7;a%=$a%^0ON~vg$HZ0TThha`1*U=L_(jf6y0^)LNq}<1WOe5&D->-^Gt90O-T8^(#O9!h8t)NuFh(}els`|=W`hKAKZeKT8PoL0#Cl+dKq2!{Q{&m%Z&c}|Dd^ZlVe&AZ9!&%t86WTYVq?VFz?61PUYq<V({E^rRF>6g6NX&8?ttW>1_w>@$i$87G})WDG8OL|1Y1~weMB(&JQWFxU8ETzW?Lj*k?7GYRC#MY{Bi0c(Jm?IHz|glc_zs=X=)>_M4sJ?g#p8<vp3qPx}5ssWKZ$MgTCjr_PYxyY(xRW+I)=t+`eW~7)kPLNmj)aT-LdLd|Ohi0)Y9Qi*?N@Ew}iTljj<5^R)RiF60&@UL(;q$*;8{YbK?l(t`~8iWD92@JdTKtyedL&tu(WbI;VeN=78vZR$6IwEbDKBViA`qJT6(>qv&e-#t?6mdRg8a%&`lHf8Ii^Uo!(%8X98v=Lp-TaY4b&lp}v0(QhR+Z}b2ieN;nQv5O|u94yvNp3*GLSB5NW>QXxiMr3E%__x9NMVgc6^TtqVc3N?YZCUJ$W6SG?r%z~r0LnKlt(QWBo9Mz66A^$r#-IT5VewKBNA!S4B2m@$EOlBCY$x6*@X1_-un~5oKB1UhNu`d%4;GlU+&z9L!O_R2z%ZYBHj>TE~f9ig-?aZ^@zfT2qQ;ZqS<JTes@E`3RGv2AxJ8ahl_OORVkdkf182$00@U=`{GmA2|CsbucccdS55qmgQOoc>pZ_#Dcn8p{B747?>f3;6z++^y*r8gqYS^W8uRNDK`N4sNH)rLi!r?(n%a06f>xL9c8KzkYp;kmTKb6|-b>IPBw!q7Q#75*nXnYqjqd^s2`of8;8)%mVxwrX5s5w++!x{IFpFGn&)q4CHliZBGOdO6{I)2<{Jl<5T4~A^J2w?>O_a08P?WSNu8PW7>hV0CU?{@;SQI5Kibq7h;U8%$hxqLzZXk-sMB#|2tV}zcZ{95u5GAb7hvd?<#9c%Wu0&CBubW(>h|EOAM?UI?Y5CojAfyzaKKXanUZ;rbZto{WMGLsF)&i~;5#%C05*?~!OTOy%ZUdTjLD<(bgMQv23sAm@=0l!PdF0#+F6l7Qv{AB4kVbXLBTb&!=@<5s9*0-V;&E$z>=>Gq)*h-otpC6duTQVXJ@VxCg0&~@czly*rYfLf;|buwLTiC|U4Rntd_36cVOtMFd%7JD!2whD%oZN0`k-}r2s+a_NC;T<q$baycf5J3Vna5bq&>XmnU8p|1@!?>GW4Vop4j9e$A>_-i{CXnrAUGOGaYokYXol`@0pdl_fW}prEaKZP08a*-Fv7o?XFJKE2f+=l)3tms;OTU^iZ=&&jrJ2bOd#-GDtOdp@K&F4HQ+V{EBaaDqcF~pSQ0QrXu+v!6cXo&I2c1*+9B>chwZmF4Qwj;h1S^G!=WT`CMg}*G=^UoIMvYqY1VE0gmBio8%iwWJro@B+;SD&`y%GJE*XGE<?vByt<_o3s<Co866N!%H^%ABtE&x4Jt}~szUdnXj&7It*H7a*^t5`5>+JHB>e_pr?xjM8xf9j#gwW1Ac|1`6m^aGmMFD}*hIuyl&X{|sYIeD2iS?Cl}Og+iWFHOC}J(zx$4@UNhuzShtZJ`dC(%aCQ4A57LJM99!Y7cGIDxFREe+wbAnsJbnMRHPp*-fh>wY!uKnB*wcWmx8zf4V2tP+z<d+DHorsRb`5Hu0iHi2|gGFK}in}5Y2?PuWoDW5=NfZypE-gh2RT((W`cl#TlJ)wS8;{+)l;RdEQsSnq=3%?I=T73ii^=a6;<nA<eVS>t>7M9n;sDV+yxTmQzBad+sJeOdnlLf1Zd2u<ZCyHQO8cg;Z*u2MxG=0U5dGTtlSWf~hAC(h=6r~5s9)68_(QWNrzTVICZ@P+3fknLhlbaE1#L{x#FW;G&;%|mfvGN|O-9#V(j{A%UclNUm5Cmk<QeNU>r}S@+rYYIor5asA*OkpiFA86Eczs!d1Y%dz4j(Zgv~EDXqxmJM;K%h+xuQ^5^ZwOu_-{Nh@~l5newIwuf1aXfF`^Y4^KNiW^#rmforKYF&sYO`4gF&_)u}zF%v^XmNw#-4qDa)7`l6Giu&1gI&UI~U@|;*F_uJ?i65GHZo8MKp{9C>9JZ{pGEEQf<-I0aOzxQJ@wLaP$#k$-vcoi0CRdprjBe%FW{RUt;SEjkuBO|?{yLfTlT2AU(~)CQ+nF4fxE@`T7?lVct?5EFpkh1bc^8ya0rj98gh!pjQ(!Go#WR7X9u&6A$UkjPgvMA4S7D}IRA@tmAt>xM6RXLl0UFR`>@I3*Lrpd)T0_Ncl!IBD^J5e@p{8P`=1!ATk%<UpDFV?MG|2-~TP%GdD-))R3M76+C>=U!qPE+F7b_D%&p?5mED_#1&=epY>ygPfnS`q|k1iAG0#Js}Q_iW1I=?18Hpx>>t}-RawxY@umuqs@)b@EQZz*#6W=^oD#g<J89>)$$@wjPz21zuDplq@ru_mSEW41?Xd*)Id`8!F<GXQ*5QHUfg)jdjTd*TuslDz)^1SOOn3M>PxRa$P6y8)#pQW_z`EK3v-JiBs{>thkMeUwZ@g#}0OrnQ7w^!mGsNKd=VJMC1}+)R*dnslAbtwgM+65=byPCCV%MQHJQEp|ll#v;EV+MhHT-cB@qMCV0+zUx2y>tFu;U;oR0`T9Qe>8ZlhmMdl%>{~yZ`3+Vo>9K>HLpB_3@P;;lr_!6)1hU<*lihVT8gC=r0qzPLVG8$n8(m`~IEH;_BO{x8OPi}~Vr!!o8@-l|H*BkE>}+l0i*0;~O)juWi%m>z^xihoHXdi=78~E+<~MA9&F1ZF{1ls9Xmgj@q{Sxpw@od!X{1fw&qiRAkL`@D*qiU${43i0g*N)w3~W=2Z915^M>puuXK$qAamsfV`o9OEysJ<?!gmmg&Hni#{0PT>4(0DbC~q(HAK^#%5q^Xp;YaupeuN+4NB9wbBBr}WZq4j`N8h-p>CJrdw!T4;nw$CF?*1b0?-Sjy>Fs>1n>XFY7mR!aS>zwzb-rlfWAO3Y`s9wjWZ@$i+C?AVmA=`+=fLMazAJsI<wHNve}Et02lxSgfPas`*N%lAM9R4`_qXEts<-2N@{9w%_u<LfkmGmbv2D2b={#BEjlOfzb9wHacmh$T8}VoiPsa23i9CKYo`<?6whc7hgeSVhc{EQhzBol!`qMk{7<jpn$NTUI&NkghUTEU65zpO|C)PZ7E1tLD@ojmNHSb;*XZY|wybtfjyxT=PpRk5kMmwLzt6Q?ZCr?I3JD<rD-EjLoc{DQG`2?P<@#vkNei-efk>S86@JM&oy%8^3@Eq`XFmJm4rPk?a=Z#j+8}V3oX?iyvL9~-bhT@;e6PU;B-X<hLRkonKQ>;3-D!zdCgmB=MytdVIraZ5Er9Pb(-&&Wfbu?J#TXg=_bWQh_@X>vAFRXj*Fz0(mIm4@^bUs~|jc=wCNSk|CU7qFp#ybBlIt<_PRXTr_j&=O+jdeH?<Vsz*RwtL}_*$JCtcxwWXs46=>5^%hsz4U*yXtaQ=SO#1H+^)bx_n;w(RJ#=M`x|0x7N9L*ZGgGTNllAw~K0a8u{j7&8P9MN#1-uPeukdJ9&Q+Bf66}`HgurGPK#tGs#VL_v3}rydpQ%jSP_8g?EQ%`)tc&NYmjDZ!}LOkcE7Q=?lHPk;Tp*-bOWWwBX^N*IV)AhCFY<E5d*@vQ5Mjc)sHC4SDI{E4%FRcyQwM2%g{PO*#>RAT;6M5H~GX`E77>9}aJvVfiiJ1vg!ZOB$CR;vhNvtd6xVj@HSgx_lZNm*4XhbneLW;3+}QRVAHM#v{r)%GnqFyqD`c@)tBm&V)U0=km*)((A+g#$xr`x#W)vGg9eHmHO>m{Kv(WtFb(N!!=*$k~J4?xae{hb-Qw6Cc47%UeH(+yWt{t3s}A=hr#Am7#4&=fT08Sy%C8Oto?m%3r6r184Tk~VSEIJIharp+71(diH1d}%;pz`<z-2bm|_i+BQVS>g*!<ji~!~|Oct0kyA-{K{XC?G$^5n~fy|r9rUx=SrlQG6=KowFwTzcoNuO-GP{tR?@=r?Ph>V?~EI`S`yxcDEb7r(=hh+NJ*e}cX{CT1H<^J!M2irAkrtcvAGQTWUA<IXM(LffTC!-A+EgM%0Stw-g3Ymk?8OmIb?DyU3AZ;E;<LA<tUXhk8X}1eDc0<EDG+4zOUmxeIpySDjId{a#^7~5l_1DMovQ;TUto&r0v%nFAdpyKh=~Zz8!6t$r9pc<D96iPb3!K3D;b2^RfaB3PvBS-6HvNhkEo^u+YHMp<IK9O@jT49lG3@_yH0TDnbQV{{@TdxP`E!Xux4_XFE}uqSfaBHsi3*;~XK_vkDZg<7VPz9sc|S?}HXT0cv;}SR*0yTl9^vq2$*%9J43LjK7&l*tW7sOM;^bT&WhZX7!g-CG;Y9dpxHuHYgK+E);rwWvEH_RA95v!5b6gG-<)N8oIBvv+SHejnF1_>0`FCEqgP*zkMKBGZe?F5pOqslcO*CvZviV9jsZu8~4RnHZ!*Duv(!|EyHi1-7wB@+w3)^rmuCF40{ED`4%=VP~B%QY5<BlO|!Nc__Z*Pm&+0_1$^Fe5LK0~Nz{K~YbX|zFe&!9;MEyrG6m1iCx;&&k}+S0h9F{BiArJ?k_?)bAb0vbV*DAL^3w7I7Fv$UjhVOMGMlW5afn$tAD91#>Weob2DU;-jWE8UX5M=wjuS)&ZGN`E~~oqP<TNk!vlM7!=y>w2!8PG|ejKC}<bi1zx?$r36@)-b+AaPlCHysd5T>$enz>IW`{4i$Nq>g#tEiH77TSN=Ml@uQ3HD&jQ}ew~)BG7cT`KV=$s6w#U}!q-v6@O5YT8XZoHiZtB-&3|f9&Vo&ldgu;`eB+MZofh$$D90No$U-0p5*MPMyqV5-6e?nGmZG>J;zcxTkvtY1SR*ddAg>VRm*_(D)5x$><co^)F45E?63F?XC8WdsSKU;U_nsFOr<M+Kcfy*;FCq^j>R+Rv`(^clrV5mk=xR{XbB_*y4lGeIv*;qwq(M21==MP0?=LN&^S1>$49YFR@~Omc(YpyK8G`b@EI0W=P~ITW@)hh$lv`oa9w@be(g=_TN7U!aSP_&Pm~L-U!=F!i3+Vh!!94<b0OeyZtO61%(0r&X;9*dJ{vZVi-y8D&h#;lo0Ek?hXs2P45h+z$J_jUzKuX^Q1WhFBA%$*|JRr@_Bqi8{9w+$&ByJ?}Xwuw65;7&ZBQLPeiRNud>6~;P7xH?li`?i~-Yc-eS_L@fRbn2ZybLSC?yiXHO%V5*HV4z(la;Eblld)if}`STb0E!~S-im_&2lX){_aB7#FEpjBFMMTa=Odm+5nn+vSytFG{IZqDoc!6;s&y4n}r<?*Cw)TWh01u$A=!RRyfu!?i9<Jv80uiY*?5XDch_GSOQ1I=BqWCu>@i-GnC=8?z0y9SpFD`jagi=Fd&0Xk#bs7(?xiYC1#(koL9#iET{X$A&ab8-iGBXR@!D^OT&%%IIS!<hBZMZ$QFxqK<ylBI>s`(!G{eN-bxr)3|W%&n8mFuqt8}cShBqSC*8}>S9OS(2x`7slNpO4aC(pxH+%5*vf`6j+{g;YSn2sJ`LK?%=I68g^H_I|9UhbFSFoSMnYDt~G$O`!587?whfjBH1rWEs{t_;~%or=0z)kw=9^OF5ySU#a%W#=GG8*;ZS>G5!Jnu^VEY=AZ1uJW0c~;z;6?6_@!J;)5k71Dws|ZRtILs3ry@`-~mRaHOJ4-mX3$|ymK3zD)ve<ywuu{bmVCC9SUh;TsS8L@}%%5iA;EuS)3b0+oSt!wZwSpxJ55a@(5?ruI|1xJq8y4$~dk05f41Zm-+#y!;MJSdm)+~mAZ^3e!m2P?wG7M7_o$7?`WaCK|HL@sKvYckQHP&2Rgl@oUIm<I52m7H=^~V*>;*l&eV@+^+QnUOT%N@N4+2A5P$qJ8HyuspIuU2efaT}}omLX<`DY4}u<hF~jb+u?RV}%2(1e+&h&G%(Z$5`=Btk(}A{z`woKfFLSv9ay-qN4+3TTL7>hA1y7!+gUciioY*UQ-tIEN{%J%mqa9!ZNC4SdI50GSQv#_GPrZuw5kc<}z1B-d<ehc4b&WIaU^6-)$y~(6<p&_+C)v;lSA~iN8fEDNfjQuOyqGGIOrNRZoy5D_MYqHk4s@80Vq)uOy35y*ooD2R@xqHvHZ=Tgg(Ds94AZ`Wn)KE>Jg?)$!Bk$XurkHFGsF8rN(i{r81rT%{kOOx{YC(@-yv9Swck$b5&4Pd};eE^EFT<45+cvNwo8meTpi%$)e7dC{YE_bKmwvg=`AL%%<E<z_Cd+b%d#eLY_2l5SVd7%N<?=jG&f;IHD!CC*ze(VY$lzk_zU@baT2gjKi*;Mg7T&Mt<gp|t#t#WE56g@;B**X;N^T^@eyu$IY~YXNgVsB8B7<6HtR8SY|pm(%HtMJ{9BHqw%vdUKbox#Vdsv2x`Hma7`p<~9-7G$E(7zl2L*Ibs#Jy3pmVT%;rSRCN@@>UD;0Z!h7Z!!8-R@2wJ0&$$S;89Dzg!R40|dK^R_!@&Fe6|T7L;!&=H@qt4w>}j#pKGDJX?cNx^JGmmb_?XMRzDq83B|}%*y$%Jw;iX;kGhKf-#nHb~`bh-&%9wtW^5_QKt3?*a(Du_Ciyn)wMcc}6totm6%W2$A!vx17v@=x|TNly3Qq0U~q-k!Uk<RWJP2*o$IxAbva4f=AMQ_4akcsZ_9@b<6vavg4aRX#-O~xBCH|PZZcaKc&SLVBA5ysyXd4SlY@RHpm{T?gz!xF$`1LiN<PFlbM1hmrzEC4JHycQ>@vOIqdC~(fQ@4|Pwc*T2YuM1~(<ZLq0VPVW6=CSJ~wyvBCH&^RLdMXQzT`zCzVsJTq>_Tu>OUsROyepWvFmorj9-DxSt~AgUOk50YB#La!!u31cW~?h7tEy;l`6|;YpGTi}@#*#Ia$$cAbQSe6*je)>*2`;G&W-l^{9T}mda&zYp7;E)C+$O*yVCW$tM77!$`$o>h?nS{T<_G3@khEm;@%^X@i6b}zx?ds%(pQ4mS&8P$1|TYO$H{ZqNha)V}$4<=Je!005&y+@7Q9miI?^8YiWM@Xa<8n7$&BhntU~z##hbnaKg+4+3mKbblxP|B-I2LU-c=hO+V*tW~~>$O!IkD-r}+jf96>5s%h5Aaz8(YS)h%-XSf=fXw6hNUR*V?<;L*O*~4UFa(c{8(DyyjXSxo8b6nrc&j+FSd!n|TDXp0Tl%*0ByX={y>)Puukq&9#q}kfU+C*R?gLM)#`CgN(nTj;N08Q@DBwHrwy7oFu4i@R5$$^O=3FPNT?_DQsT=oT=`$@D-%AFP5Hp%x^En+@L2MMpdeNwDQZhw`!8r%I06Fx~2xI^cB@;VnW>JO89Na|`q*hj*q-~}maQVvzm(A3Uum0UpzgGf13FG7@hhW3MYs}$@>?h(oBCJ=19N~$~xa$#*r0rCzD5}99k)n{o4Y0@nRYtn3a;rZK>x;iNCklv|-;@4cYKeOWL9eXG~(!E>-^ElalkWVg_MH88<h06qzpe8uQlb4jO4s>QnWt+z3s}-`e><9W2L$_uhlZIVz1NnN~%x7VBc)5n<QWm@x-FVo~|N3E=*IMMe2Izl37#0+a>|nl{SB;IH{pe)10>&0Fr$g@ui;#<VHEim>dF;Rvz{X~){l30@-4R7PV3Quq!jL;YLGwWe1*aon$qW|Yet<C9fYH$Net?DVX{e`R5lWT=R8<NL<jyg*@vz_X1>XrvF#ocKVH3VAPXiy&zcBv(mpWkyGT>zm#u~=sVXhN4FYnC=W8Li%qwsW5uaU1$o1{J%FN=V4CA@}-hWYWZU;>Mf3tx=mMpzmR`wf=<f#rj>)35-;b453*ljVT*4D5W!^iOSlKWsV%n@9H>`Q3SZeY1DnFn>Q7o4^EMei!EM0eh#Gi3{~lu~c}&u89wUUjd*i(hcwL3Tr=qsJ=~fG;)NCEL^K|o+q86jnPzwAc7y~+Nx?k<?@v)>ZjlYyJ!zPN?R9yyHY31>w(BMD?q^!>EObRS<}MeD)}|SF0*(w@bJcV8y0?8Ld6QZEFR1fGnU^-*$eO%BM>a%<vqZf<-S?TL?z3QendrsRa5>KI#s-;$}gi4Dq?ZE^-WbCLOMySq*8gvXrYm+cv{6!T^Vu_YNeX=Kf+2&GE}8fHFc`;;lr%EZLF%&AQk4D`Pl?DX%vpp!7!<Z8KF6&&v-Pg1xhr^JwnZcP*{#S(PnJw5sIoQ)^j!VIUivbD9kgqK}}|;;@k@_zX(@mM&;muJt`oIdr(1_!p{(@$HplFhhn2p5emyE-i&S>Kt)|w{ScKyh=WnmgG!H3xi|&Ca|jA6QTkA`Mio=Gygo;9P^&Q*<p-fAjhb(QdZ%WHU+G1Y|Ly(w9s$GSz85M_9*puEKYY;%(HE(Uwy4Pr6{-SdEL<*nAWD(7cvn<}WvWs6^re_MFxgb<Y1B@FY$GaF$(Puzl5{yQCM%kjiGHO@^`I~dEdRb?1Lf9G?lEd=eU5$YcvCMbUv+bpbcxM3oi0+&8B=~0<?(82E4&VaQG5U;CMZ_vQPXUL%CAzfLIvG%GaW%qtt;g)HEP;U@jZ5*XfomUKEf;oTT^g7CV|l@Gla-+qED_iW4*h_PVRQ5uUJ~2iM0tw$l`REsQYV5gGn0i5`Rq8V<L$16{fIe^3drJOGryoXf+9D3kB{mVIga6$|29fL=R2P>!iowN~dYorc{|GJqbO)n`EwV?p`Ox1FQ~{Xj58DtWAE+M8+nMQTE{bO<bA0Hswd6fC<CxcK3+XMdFIYn&c}IHg?@3oxeqV-66J<kq?td=L^>J+7iUmi?E>4D!GDmz6cgcvp&YbR*YCkj0NT1>_$%baSi<>2c!u1f#W1GyYSeal;4SphM8B9+%D;UQNWJH`??b*_`VyKDv#5B{l}gZ1H2Q;A1+gV(4(*uH5;G~&ROQF0pM?syj_&EqPAN<x0`swRE$pLYW8yZk&4R14ZA`9d1Ev)(T0h%iR!t_g()eMdu*D}<mb~SIc#ze*epz|jTe8*MMRdN0lOqsCh5;#daRRaCtbK3;AXKyqE!+hDLp3X0?FBg#K%Y;GCB81jHLLOq@uLqtw?^2BpW2JNySa?H^)W3U&bDgyhGC0|7=JC_q?K!WKIRzA{7s(-$4ThNn}JS`V(^1fB}=2ki^x6=kG%jXirEwr9J4>r3v2YaqRLSQaDXw__aj}dJa;6u<dWVV^h-HLn56ki`AS+@-QbTYSK>(dXF@<lBQ0QYawB*FJRS3K~iCg$6Hs=c!0yMpF}{4x|LsX;cb!1o4DG!KHj)`k0hE*NU}!4)H0lFgB@9aGTJ*ygr_$YHpf1<kUS)#BZ=TrTqXUS_7)_y7w47>kH7c1?)0M;NxVkFJZL02Z7xZvktBF_(?JqV5;zm^`i7R%?ek~J=_}KY6uL+r&R#q;?vpC%C3pOFka}-Pn$-BqE)w3py`EiNlqeP?-Y11NlFSE5w+s2{C-91tHY3nK*CX+rD}`HqzZdgE-`78QPSEc@sL(P3S#}funo-kO)WPA$yqoxEgyMcwTx$b|<B;*DNV|!DI`p!F@>^Zf7u0NNq74(RjqxBW({ICd|DAI+Zxm&6Q{%{eQjvD$bQ#PxiQ#bd2<iKGJ})Y2e?yB%pz)Y&Mw5<-qNND?Y}bR0Sx+3OMbSj`yVpvK$eW1jfyT5Z5-qAvOCgAPOcV-H=ogU|i56iBSt0s4)o)xQ*}Cc^EPsS%A~q3u6uHNux%mFA_jx`tycjp&g(!C>O=}|F5vks(k42*5%;!Z#GG>B!Yf*iKq8UWAC5oFOSrvIRk$)um{;$uKh}uMRA>vI@uo8V=PLmFx=b`R1B#zBGE}d3)cd1b{VaUZ;B>FJ=`-;i)RIrR0hx|<U5Q&~MmvnbuY&%+ra*bUU1uGFHxR08Nq!Oh^qPQjEc~wN4B5xwXst1o@<3}RiSR=R_9}}rYFUBINLSZvRE4M_Gm8k2YV;!HIAt1X7q6<Jc1Lq`Ys+#|C1;Vl4STS!8@_V4$1^CW8fBwxI4<8w3BR4v<_c|=U)&dX<V=+JE-Yfx@taSj)UoZOhn6gr_QBVCU(PJKDBko5!cfwRP4^+{HinNN%Ri27hkdrE@vP5fD4*ofK52hh1wow(8H(@Q%x2keW(9%@p@rd3)wIA$@P+vJxRlZ=^sFLoIhpM=y3WrtckSbs&eKXa(rXo;Ln~EA$vyDnBRay(qMhGeq1Zs^{lPg|`&#N%xj4IJ}uUHutAw$koMP@2IHJjJk<Q2gsf|opN6=SxDjmmAPNUI#Ir?tu#s_C?fDpfrxCF-g-EM7EKO=c<w`F*Iur*qPSmJ{S>-CC8OdTColx{B{R+%`z%;V8mbg#q0N0hz-pZd9qZt_G?+{A6E6(756|S~EtKdQkotYQ6}Sbo9vvHLsyOpjbDc>_xd}qS8r}w4s87dgd3J8FJqFv+Osn{2gX{Ufu7#NUNRyFrF6lVBFONz*~@HEk2kH7)--9QZa`+Zb;&_;2@In84>o9%f%CHOq%;ev=%}`k!*;>L?rcz^7(RKY`Z(bNZtt^V0nij&|w|3XL$2L91lH+=iwr*L{y0qW}y`#-zExSh$vPf)}kVJWX8UDookfpt8|n|j)`b<jY8Y!h^O7$5r4eN-$9YrbL7lKWG0#*P!aVg&3%yr5!a&W^csn|sL0ODp%;S01ZfaWZFdHCJtEl^g>4bTTgp%Hwo_Dw$9hFMdn{BzKNRI$3xa^|x+oM^(IZi^5%Dom0+GP<j2T1Gg(x<P!dMY+i+B<FeNk!@%|#B@`5NB|Ldtm$P&C#_aHY|ji1tKuL=;^S4l@%aEy}f*IcLd%C_z`UQZ%=TV2!#&ZcW6EB3gUGLcfn=YeYJ&%my@TP^dtpL2&{3J&-#DVjV6z4+`5LY=FE93OgV!4$2;ZrfWd53z~L7z7d3nLEE6)1@xMobFnr2Q$ru_8POYud*=AxJE_9PPw#aiyMH|Vw^fy#xk@1RSdYk6P5YqX!=$qs3zamkRV-DL&EVevRR*=nLyIKVZT?JDenpk6P`rT>KoOvV(Z?!|MA63RX$F)7RNO$dK9`*ls+f<ROGGgl*u$e6Q4ACNOjb&YoWB7mhR;{jDAB0d2o*{c_oF-%if*B#1=V=@{l1DY<M(%(B22VoXqyyuJtBjN>=ueFO#ynn*Hdu|6GPHV4iXugT#t#X^0%ZXXbX%4&jE~_o^)@M2a^Ehh{@{CH?4nvr)h>EmZIA~F&x<(G*RO{LW&^S6HNK@6m2$05cu0a{-h&;zkL(y$sGdK%tuX)hil|IO+g1I3X_K+^=Kk!%lLTD7aK#)2Bx%Y^4jD_nSNtSq$(Frn=t0$bsHoPML1}ZM<#Aur^(*Lm8p2&AlSkZ>?4BF=c&k8>>|w&GTS2gibRiIp*C*Kk3UXbB-$kf{U*h*GtVU1CQWUmGW6_UFAf+^9lp^<#B=Hols&~45Bi?h-|sG@un`6fYeO>jllz)UVI;|~Wmy&Da9Jn!@oh=53IOJJF4je-wA|uT&Yo+$&C}-7IB2;AiPuQ9P4a8~$eKy1DD@zN<|0KKJiO8pj_uVQ;q!bq+1xX=u96W+c02oxAZ>q^>`2%Muc#nR&_9x)@^_Eax@GbglH3}JpjX*C>HKra<DUI|UmMZ&yag%3_Ke|$Bw$-Sv)xfQsR%~ID#tHl;u<M#k>my>tmMT<Y9{5Jn5dgg+N@H%gcR0DRFT+(6oy@RvnFBliQLI6=_aSNN}8U%N_pmTLGmyeCqc4EaoXeR4N)s;HX@NG&5-^kdX6eVcd}VOnoUT*@4Y_}%;~hqZ-|PSqr4`<`sL1zI3)U+iLmiqA>s`YCS&@}TliFnT#qPhh%j=rC7O-a=yx|1tUz@d8G@t&dALYdUX{Yx`?nd04}frLwl6+)ouFe4@mg9Ia@EQ2I7s?IvrhDTl@5RBoj=FcTYc4TF~DP(?up^OTao;uEWfZC_Uj`-Hj)uZHfnc^dA%Mw+jy9UR@d%!koLPjHHdhlub=2Cz63o&0>)xCMboLg2}@Dk{Vu??z(SORe&x*}Hi{-2k?6z0eGzUDv&iK>-JPOnBPt>+(^_cHZ;K)f;_DQpqn)`LHWqG8lrzXsl(Z<WipqHE@m!r?D8d|B6eTT+M?}9NAZe?KAa5v&$3)?XXs+{ajwPLUiv&aoi}WGEG%c|g(Gx6DRNU((*C--0QSp(Fx@%f~za<DO1t?Pf9lF;k;^O<yi;6yQVXY5bEh5NAdL%kj&X&ARlQ08KyC7`tnL$7Akp(DUMDrm}(4O;w71E)iX`^nJAeHKnN18lyQT27w<M4`EJZ`O-9Yd$m+C#O6^&j}*_38DvN1ohcu=b=Kk8kqKMNSS|c>;K_+FBrH7obi&9}#wX*w(|)qi)ATaLANBvxP?vHA6e>A!twMASqzglbSq--tp#12Zzi&NqczBGavC_AL;|1WavpFJh90`jt_xu7sG3IN|6Rj{?1c)$MK$7u6qxaY?teXYUq?aF4w(>3RCauRJ~%{8AGY7AF1MgRnXJTCOsew$I=nhy2>aOb*X|@`3)6Ss{D>`qAK1xh)$R578wu;=D|#GC^+fz2GRw*tEO;vrJi95$4pbBsn~20ovZKiy0?CS6X+spG(ibefWvs%Hu**qS(@USNp!R_w43DYCMw|M(Gz8@NSbuJ{kkmKL4=v1%5{~*C-=Gg0oX%@x(`Lunuu&g)rZN36dsYNBGD%4HwHVky<FLdaI7n4PUS~Ygfgh8OU1WDsZGQtBG#f*Wll*Y5<Nk{P86*~vNm6&NCrU>YthbC*Y;FO@mNTVjzr0W7P&Q1f&#U0Ow{&FO4G5n`VAtgMA(Qq!L49Ac4zP>*T_u7$3#w-fbNLeZr{JhO~#^BiSTojMScmw*oo*^sINgJm8fVVKUgG&qPQ#akVC+5#`#d>nndwn_|j6uP@I9ItuGbbFK4fhN&em?xkV0TshhT%i0$j1JC*k~D8E~h+cuN;d8pL}e4-1B0|fQ(j`L^|+uVkt0!95OOwg-aR(WV)myV*+J}T^^P7VUZm0_KU=+|bUG@9ZwOhKD4_d|4d{i4Rk9~wkCHJO4pF~wa|&?X1{G`#LHXk&^drnFX&CU9v9jCdJsGP?GXF5kj51J)*~O!U|!UF&pmRO75u-U93e>-KdHDyoN==5Z#{t=_NzlynA`t*N~Brk-nWf`r(-XGYVcUpvAelbD#|wn?<fLHDKr86%daU}eg?9=!I7?E{+dQan8R^q9#Rngp(;+Qe`Mg~w22ZsJ3QUdK!fVOiP;VmfGF7hnSKv61Sh)~U-x5XNM9>|#KPDic36@!WPVPeV=hL^*6<XJvZuvSDDN#pI5e9$$N$noI`^Cp%12Wpb72!5mkPZKgQd6yDGj?`pbT0I-uu8}A?K$l0jvfR0OCkFH6KN`#Fzb)lM8u^sok3reb}deF_nqfX^1u$HLenLtwy3R`F7pEf5%W2}X%Fw-t7w4uTf6!x8o)tJ)&&1f=q7d5q^CL0v3q2e~m!QjpLF^Zc|Q@yZVCaEG55z12pqBCfc2d1`Y`b1VHOdA!*{)kXQbkam^w+Sy+CW8Kf0{vMcymg={Ku*>plW#H!ADRGm*hIPzl;QJ~6RV;ga+e;P<f$fCnG&R2QDutDHMwhQ`#hDm6ghn}C)m?s`=$hsV+W>q+%!LfB$`A}K3R}hlhX1r+at9-bIS|WohIc!4_{RlA_+@&kCNJ+xWtAeum3+mDW!)(%K&SYmYd{mK&gq8Mu;%g5=8{hu3YT;SVV0fB@<C$!FjxCEo&CN{;nd@qwn%gJ5{we6QrCbU2k(M5$h3!_=>TUP;qAwTD)G19Z|fo$Zv@D$4-W~6HOn{dC@=rzyA-sNqze"
)).decode("utf-8"))
_V22_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_V22_ANIMALS = ("COW", "SHEEP", "GOOSE")
_V22_KINDS = ("PASTURE", "COOP")
_V22_QUADRANTS = ("NW", "NE", "SW", "SE")
_V22_MAX_ACTORS = 13
_V22_THRESHOLD = -1.0
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

    # Lead-4 fertilizer: beat the copy's own 3-step relay.
    future = step + 4
    if _v22_relay_covered(future) and future < len(_LEGACY_ACTIONS):
        target = sum(
            max(0, int(order[2]))
            for order in (_LEGACY_ACTIONS[future].get("market") or [])
            if len(order) >= 3 and order[0] == "SELL" and order[1] == "FERTILIZER"
        )
        queue("FERTILIZER", target, future)

    # Lead-1 for every other scheduled route sale (terminal steps included:
    # the 717/718 shed dump only ever sells what actually remains, so moved
    # quantities cannot double-sell there).
    upcoming = step + 1
    if upcoming < len(_LEGACY_ACTIONS):
        for order in (_LEGACY_ACTIONS[upcoming].get("market") or []):
            if len(order) < 3 or order[0] != "SELL":
                continue
            if order[1] == "FERTILIZER" and _v22_relay_covered(upcoming):
                continue
            try:
                requested = max(0, int(order[2]))
            except (TypeError, ValueError):
                continue
            queue(order[1], requested, upcoming)

    # Pre-empt the copy's step-713 full wool dump.
    if step == 712 and bool(_V16_ROUTE_STATE[_seat(obs)].get("yarn")):
        queue("WOOL", int(remaining.get("WOOL", 0) or 0), None)

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
