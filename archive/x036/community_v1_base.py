"""v25 fresh-meta sparse market controller for Kaggriculture.

The complete farm backbone is a fit-only public THUNDER THUNDER trajectory
selected on a later current-meta panel. Runtime feedback is deliberately
limited to actor-local WEED recovery and ordering route-existing SELL slots
by the official nonlinear price impact plus bounded current Town demand.
No ordinary SELL is created, removed, or resized.
"""
import base64
import copy
import json
import math
import zlib


_LEGACY_ACTIONS = json.loads(zlib.decompress(base64.b85decode(
    (
    'c-'
    'rk<%WhoP5&RdfXW@BJkL+maIwC@g0!d}y2!vrE4gv(u!pSbkzlRp*dAqv0y3e^oTG4Jq&D?w5r@Okk`qO{T{`S+azx@2`*&jZgeY'
    'm*2J-eTs{r#tZ{`FrEe|Y%#%TK@l<L7@reExLy?($}M_+RbAw;zA_@#6jE_ZL@Zv$HqX>$BP1{Q36XFnl<ht+xMhI}C3h{=9xST-'
    '=?_&PRX#ez>}RfAHrIH`i}JzPUU6!To<{N8P!6^QVs=4&J}(*r&7gaC`T;p}P;8&L8~juzipJdpIE8%Qme!e%<@)o4a?PpT7TOU%'
    '2_H_QFlW)t7wx@$%~Jj}QO6`?#5+@D1ai$o;vxcr)zAPaD0>Pkx)JqZd8=$NRh8>^m>~?r`Bq?;HK%aA92B4L9D4-dw0-'
    'xA`U<vTdKn?FH{-LpIv1=(+pOw5$XBru}ol_9@K1eZlUr{#fN_-M;7c`r~H2!BFY5?a#%2-'
    'P)0An(Tx2`a{%bvUf+N9ilFit&CNV$(Dw!Y0|e30V6f)Qti3><?8;a_Fy{&eb*2hnLcZ1`?TR=ilw6r)Kn{H^da$FWWR;?)Z;>BS'
    'KIZ~)$r!-$M1%lyUVM~zkF`5z35V=%VRTA_bF-ydBFCtO*Is}HEd`wI>}~lw|CD8+B~yzQ5F{U*Pnd-'
    '$us)N@tJr#T>a*W9_*Ay2NOHA#^ro*pYj5CHb8vx_znv67Ar@Y@!^h#26lLUpFC^K<y*fU_P1lDq2T<7ZC6_8-'
    'zB(>@z2dLg@^psQ0P2NVDRxMRT?<<BvOmuz*Q@}+757`3Ht#yEs)0-Oq(;nVFQ^vTR2L4*vZ5OR!0at6c1378UO$A+v-'
    '(!bmtv|vh&fOZ|`m{*53{{H$R-'
    'smc`3(^r8Eu*z0<Hnv1ga%G^4v2Q$^$6Uh~u0VuV6rRw*FZJa&U@Q5_KRpaZo>7D?7AH9fsbijbF*%1Phhyd2umsBjI{qiV1Z{IK'
    '%nD1m}dZveFgjjn)ffVcJo{K~k8#%(`TCTpY5BW3!ESR+mnmk@|CXS=OU+?~2?s8k>lOAEQ&BlK&x@e9g{oCrjxcPJ80t16du8A_'
    '}kT7w;LqUkH;v|n<Y^gb$172IsPcaF)%e`xz)bahdu?KFW@lnqOpFFcWh<m=fm6Zw6J#rgXm1jwciB<ai<zL;~ll$doW4Pw#J6tW'
    '@`(L%Ouj-'
    '!C`1)UDjDrTq0oe$#3l_Vlv8B{*a6GkzfE>&dm<xo^=GzVNsqJys`i`={64lX;4`GiD5RJ3i2Wu<r@5|kl^!TA|6OA9+1J-'
    'd+krN=@30IuO1X^5i6-'
    'DdGed#l%eHmDj(74*DNGF<srvw$2c~C(y*1>C@mvM0DketFUVD3ifPx?4S7Z4?X|0Ti?3<6@fMz4Vfo@aLeq=j^XVjFccK#w4uVC'
    'dJCac721!uGI_!3!aL(A%5q55YPh_SN2#yuQBLoYde1UvAyMhl}U!S!~-'
    '`v;n=ExS@+m5PFt&9JlYv94WfB%Kg*bb9T#6e=>1r_K!7y*~nZNJ*492fJB+Z(p4@|8%-'
    ')W2{=<p433v@na{gvPPbDksZN1z7DasI^N*K!C2A2CIkvMT`}eh;-q#utQa|;AbM~L4FHLym`G(m{W{#v<xTr%$ARRCKYR2+Yj-Q'
    'AavHzw$&MS+^rre;u5zwQLl@_d`<NE-'
    'e8_`ngfc`25aC8MG)>A1uw;KjHL1xr?jEW6;A;fg|N*lEr&s3970@ib|qe4eiF#!OF%B)#1$JT6R)=a~cgs9~#jI@o0t;zKuK~{I'
    ')g5m2xqOvFA$nHaQG8pUEID=ZgRQ@uz@zB^?Ao#6)FogbQY_n$*bB}fldhG6<Z!iA{FT*yN*|7YO`7VroEliFUnID$!7oZNNccN%'
    '?oO?P6Fnk!c-uoy$J)#-*LV5<0xvylP24XyO6_i6?Y2o@x3*A?ee3AWiZO5o3kJfqJ;qkp2*amN-l9O9@-'
    '5T@8urFpUs7a9Y5Im+939_tei-NdvXbvEWY2w9U?RL{F<NgR-'
    'HHqn99jvig)G1`JzxA9^$Ry<{JXK%;yUuX#UBN6mR@TvyR=9G&%%>)+8GAR-9xomiln8Cd-DI#V(!>j)XBC~Z;UWSqoqrlYr`i=s'
    's-'
    '09m<uUe|l=W0SoxtcLB1jK<=J<x51uWPW6PZc)FyN=bJjM~Z&L+68N7VO4Cp7WDzr6a>Zwd)G_%Z*+TK)6ph)9z~zi<p5ZqYM$AT'
    'sVNXl7(D*8&+r<X^IebLMe(z5tD9G|^F(S+fz``r$>`fyh!IghW1Hd|+32Bco+Y4(~eVn&+7a#ylIBUOopk8TSjiuv{AQSi#Z={R'
    '0rxsHD6Sy0>F@Bydl=Wn7v^xM=fhV|kzOAb<%+7AoCA$5-'
    '$2J~1fBtB4k*nVHJA0oFfvkAp>NI9o|M8yk}Xu?R6L+l1E=fAVm>)<xW)op|_Y<`DJEl!EJh0?s^n|489xqLi>%pn5aiYo`t}O!6'
    'W|zk1<>7xqNP&Q8Z<gD?SGY>q|NUzZa7bT7-~29gki?{0y^mN9YMw1Jqowi%WdBpv7^1g7|;-'
    'O~{+Lf+89OAic7_dCVTt6^s@ugQf-BT7WK9$Bl*w*&Xh&N-X5g%D8HVa~P=`t~iSWrS2cpgK-{3%_S=o-'
    'wdS<9!7iXboU=CP4SQgn>sGj2vk|Gf9>C2{m&+oju@nI)J&2Ma_0VFX2A#sJp2k4d@g&p{$TPa3vhAd&X`ISDGt%jcanyLA0x4lP'
    'QC03}B?6aq9M9_oIRE0-'
    'IASVop5*;hO(D?oBX4BDGS!w88ljF$GC!2R^ReXt{%>;3z?Kl3eeAf5<L;vc=PU)zSFbmgJ5h`+IPh+Ar<<vD-kPL+*Ys)Acg5w('
    'T^C{8#^*p!euB1pQy@Xo?_#?B2*kI5B7OfX%vF;E!|3XE3}@$QsR<H0T_MaS5;*B+P`Tw#ADtKI|+;6fIK@VxtR<!2@FM4Ox{eP#'
    'gknyOTj?v}QXPtWBk~kf-'
    'F3{XnU~Esz<mkW=CV!w<V%!=|gp*i*`M5fhu97)`hgJrXugi5<#lqHAn*MEVY4FOe*L_(z6rW%Ey04KQ9Nbu+xmnzTU}uOV~WW*g'
    'RvAdxd$8J`371zP20jxfR9fI*k*8En16e(%8QrdIGap@%y--'
    'O2xD|MbXxf2QdJ%*SNqJKORv`z_XWjE~e+Ucvg8=5!XYt(v4_Va}VGDek-wk&nuBQXnRCW1&`Ob~XSkEOKCz6^whdx6Zj|B*YIGO'
    '9MT;%ESY!zD++Uf^+yzU^QAZT8LKv(f3C9>L;iGXjzY9N6BpfPYTCdYIWcMQeo(Xv9H;kc@ZR+1E;ym02Tf0Cm5iDWBs&k$PYxAp'
    '8LqkA2Id6`JH*d8jU8ULfOIHT?*6|`{TpOS-'
    'Af*&+uC|uYPr}sAk4TD|IV?^+JQ}4Jw@0;?QWk0RUYWFJF`y>Y<OJ@PGqXpA~58&TNMP^@!Qdf+s#beIi{UVBd=gj-ENU``Phc&K'
    'j3+*8-ng%B_wQCmkMCc~7K;UW4IvGdJ*F=F(YXB5A3VkWZisdx*RZ#~Wxb;f`Np4^#SezwO05c%1E)K-'
    'VzO1GF=a@Jiy9M5V@G3GDY2g{e@v)T|ns&PADJJ(T#@zW;l)-'
    '=mdap$X>F_A1CkV&RBoKv9dtpn}E)gf4)q?>`;eP5yP|(in<m1lbHZ6Hd&!6x7<9I1_?R78LOF*j#;srmT8{K`^Z5AQi`*e>%X!?'
    'On(G^<<d2c4UhB0DCdCD7G$P9W1S7aX+cNz!PNZtU#j9N|6s}i_T90K*(7;f+oOo2)esTCTWF(=|b(f#y*Ge`ty#e^Av-IEM6r(8'
    'QS%F_DYxf7n0U82UV&iKFHEk(!ry`W)c&7vKToG$&sZ<Df*pK${9nt$hFq6sY=rr48Z;KN*)IAk^N-'
    ')Bd%dy99DaMCgR8Je=|hM1Qn7gzz9p4OV_~crL{S#M5Rj6J}FKrr6FNwbUH}|;9!7u_Dznb;Rzx2X*#t9BY%LHOjDHalf&1taDw&'
    'RCU0_v<UEyvMyn_Kgq-Dyb9u;UcGc*X#+?MR5v$*$huKRQkLwpSi8jFa^)eUHP=I(v2`!2Zl%g3znIIdadIApjqFhKQG#NDivdz<'
    '6-glG%ZnyNkbo_4AUA2x?sluVZp}-'
    'DS!dRS}pNL(iN~l|}GAy{>TuG_Ejg*Lrw=h|JU(IIMx`Rp_B}ym_X|lw+5KPPp7y_S0pd~f81kILo(DMLcDL0wka{m4SW1_6%hRS'
    '4`N`CC;l0r|uwqK{>PYf~8Wi_d?PzlMfK|zeZ(J>?QpCDJTcre<yN<A%JKdJ>opipM0O-'
    '=|lot;wsB$gd%KLk6KL!C<`W`XKaA6oIFE=lF5tK&3z&h%@?<9_``63E9Ii?{EF;R92xnNP(z_vP!Cr5tOYW8R#7T_l-'
    '{J`Xi&5((HDmU*PnuR88sT=;Gbb5X8cFH2CbZ>sC34{@BxLNAKwUsL;mOTaX~b;WmVs}ag~rS;l|O=MdJ1a6uk-'
    '$jEFWpk2Rq7bB4nUQUwe?5$@@J+dXsqEoa=;WBXYdkWE^;lE+r@Op?nNP`^l?qpsqt4j)I8v%sSCqFA&*=#eS4Z>A&pJt|3^1y@z'
    '|O!ydq!{Xk$s^#t26^$S(X)R0*HySYT{-W?Rc>oNd=5K@ipcPFT4jbSjRovv<z|hb)7k6p6>-'
    'm0~5)mrx4EUD@=n0W3arh=)w~DFgAmB*EUrZlp02vE(ugH^nUG`0?RDMTnaL{1*aTZWwAD0AYj*2@lKAvWf&+=Od*&b(bSzy=<y6'
    '*wWrc|ggd&{mLQb&WgY%lbca7WF%#hbtfGPp@K@(O1?vdgL4j}_lJXGg7u9PtB&ZPyl5?_lMjJ`LJ8eRv<#VMe%HD5CK#<S$X7)5'
    'N#x=j1z&PFmijL#KigX*sVMj`Z5UNo0$!2KO5u;TS);UT2ig+NQTC0@<BN1+8;W%4p)m=}pDE-cu72x4Ql59@4j%KY7w>iR)5@N1'
    'kSxg-}DiDD&SHzbhrCQ=H)<!)-EEC&Zt-(2TDgG%)I;zzhN=hrqDh@>2uUUSR=8)+-'
    'tFW*@#Ddx%ak2Sqrc(0!5gV)*U%<$^yNse!p>hy`TaE5vC^D3_rtBFS@+#6<!D@QF-SwjMgLLwuvNj=~rQS1IYr!w4s+?hH{X(6B'
    '*g>lS3{<I0;pGUJ)FgAkx?(<bhRbU0+e=Lld##!AatySe-'
    '<M<_HtzEI0Sa~qtu4A~Iy~3ftZ0#zv9VP*A&5hoQdS7Um!;IJkAk~8V~;|Hlc-'
    '5nDVAEJ0%^B%sxs=+@_|x}@Q98wU5*lGbVStfOx=+aP=f3_2`NFkT|1FL2H64(k-'
    '&tHE|M<THsAd>_OkGH)rN6mbr(b#6AfeFdBK5iD_9_oCQHa*e`?^e0lJOd`*!)I$dV*vu2V4*F(7=_@&W>Zo5ge=gYun+rpGv+y3'
    '8Y^pgPs7q*Wd(i#u@2nL@K1IPocEIVPEoEQ?HPr65LSTPoS7(RfGSWLOm`^_#fBBesLBwX}2Q0;!uA`)0+8Hynk81p?uiZ$DmMz5'
    'VgwzwSP6(Fz`mrxcx$!<}WiSf~7mPxWTl`8i>XjnHul+Lf$fLai$*GpQst6<`OeUTLprUAKe*5mB{8NMxJ!L*De_E2rieEp%$%OM'
    'A60f4@>Cbrq9&Zxxee0uTv62$fv4Y9_NoJ5Of#=vQeXq*}=Cf(=pxT%@?=RCy%8!_3v?K!$c7lG3U-'
    '5QMZ{WKqt@^u?tqqHxs|@Da@t(Yqn?VQ3~-'
    '+ZJOGqr#sHaioImE{kynpaFGB2_l&@r@PAB#>rdRx*!0UV44<+j7o!~1<imG8CePKNm0Q;?U3bd@IsjaMFZeHgK{#2{#{x3hQC$V'
    'G)m>k1l<R;mJcAfb&`5L$|yGgidr#{OyLq$hHmiTj9Lv7R|1FUlnxRFnSQN7(7AjrG40uWL3h}Lpm-Ehf0IR9f-pq{nq{ajLY}@-'
    'Pu4o&glVC;007BRY$)sO0{n+GAG|h2<MZH&J{md_i~({L324HS-'
    'B|Iotujm(upvyD3qY&36{0juYGFDru4m<y`3r}UGq;qS*R&$b7Y8}1*wgBC*prVN!6VSk`f`%drb%I2_ACU$+NTNssEG$dJv{|Ds'
    'FVW4EemD|$o9uml$f!eX;R*j&6y`_(O|N$C|E+@0+^M7-'
    'bk#NxeXE$rHS_VD)px15{v1)HlCf*MPfT5{f9++24xHS3wH{kD}<`#(g9d?(Ok9+M(lfJn#B2RisGh}e%7zvqLQPHni3r-'
    'O7K5O{4iyC?DwnXV~4cE3P#*k3zG6{S&h)bLez<+MVw5iLZsIc%MtQYFbp4mxtcN!hPIW%qNWhj-'
    't`Z^Ox%fBB87G59~`3XCqnH~zmnOUbzlfIKUL^EeJs-G8`n!q@xr2GL_vVvE1g?hB;!(2Xg7ygVKrNS9vltW4-'
    '$B+%(z4|+@!P|z;?Mn4q;1qv@`e@*SJj6qZpjW5W-@XSyo#i3m!tkoPr-Jcpd9b9}({wiYYy(sC$-B{a#u|+G_`5T&}*b9KTfh-'
    '|GAs0gKrzzw;1Diy+2E_lalFsajTIreN0!MdTvSXY@yM<JszE-'
    'N6Y33RN=RHQ<OlQI3$P294_2gb?|wsCwrhnP@psozZSU;yNwg5Lk#@e<rmwiZY)JE;>l+@H6uf7Q-'
    'y76eDPV84p+2@3&FBK6~1S)xZEK7+eklk4T6GE;38?Ma0|`11d4|YzAMr6S&YfWO&T%R$znpxd^UmA~Zv^vR`Cyg(HW+jfyf_nGN'
    'aZbpOy67y3Bs&t)c;Y#7@C2OPh08MCS|$71z2Y7cTkmj+p;R&J@dy}}IUdZ5z!<mB3x#E7V198J9sB_r&?MPlf+Ev7Kq$b}H>Daq'
    '7@CQuTiZ{V{=XNo2X4E{5Vm<I+O4MP-zBm483jXT(`f^?=>cs5+N7IzWAKig@DmSxmnBTJo_i2?eXWGxRao@Z@1Rv=PRFf1UwX{4'
    '4)VuD`EYRZvM6>Qp!8lwo$TIdxV?EuXWipYRp<kRExl>(0T=f)M&vw9bxR>11XkkM1s3Rpa&Bwv=Z3x8~<k3>%^S5tx-spyBrf*A'
    'heIwi{HGnD<CC)?~(Nv4U|E-OCOs_Q@AWV7z-'
    'YKnwBEn<+5>nqgCKIO#;moS6q68B1|;@Bl?Q;{z!;Ish^(EGe4dab7+?zT2t$$LY!a*6dH0+dkPMk`gPz^%LK-VMEwqF$Mf$LFIy'
    '#AJ^^Qmf!i_uNC{_modVxk>{+H)=X&%&AC=^8uGRa2_P3t$lT^>gmSNiPUWk!Q(^w5>aU_k5$rg5GzoS>~a=%kiNu_mYAvu&oGb?'
    '!9R)O8T^wn;H2On^ip?g+~PyQ?O`2V&b%%cnp=rL5EDH>?MEvg`d|P>P=Y4B7%++5r~7F=5M3ZM0B0dA!LmW(#zsdKOP$UT4efvB'
    '067rXU}Yv*WDE%0E3FJeFSgJtd6SaFOGM-VdbN(K*e39xrI)t5if={*bE65~0=H7?wMtNhKQ_XEV})6#(tr!ieJKgd&pcgu?t}td'
    'dAUa5DGE05OMpv#XoA$I;|Qt}CDI5_#|5N);OVo};;TS@{fU0-'
    '7EFkQlsjcP3$(qAL=kdE@kWc2=8BX&l6se<Lr@A6=+zY4MGLP=Ic}=+H1yR#M;n)s=#<4@FA|bw#fcTxa&`KYQp6QvDzWu#@LQ^T'
    'Mq4;psg_9cF$35H&@Q=GYNag*8bdH+F!UCf&BWd)u`I}(2nwJmg&gT%wqH)-A+77sQY^Dc2PWdMivWXgR7`slacU>k-'
    '3e?rk8YGpoKrHmK`ZfDKvwp;OYKB@84yceC+z@~<#BP=iWb0Y9B(fGb|`vlU5WxEG90AN5+q2>D@~PE<lqfyG06$7rLlI_m*Xh)q'
    'h{O~2XY{r)t3a%xNNB2WgzFLQJy14rJn=J<U0hJxhVwYIBQCgcM(9XRz0~vWYB7I!3s$9^fGdpnmI`?UzGC-JpYUgHx;g;^&vFDL'
    'llE<kW^OeanPP3V8*8it!@zEGJok-s+?K+VkWs5|D+iP5*pedZbfG{vPK!VD5oW-'
    'V}n%WN+}WHLv8{YLLlumX^{c9KFaWCMQJ$wkoiMt#m!(l`DcrkLz6pX6p^S}=@~d!$AX<PE4L!FC&77{v^wx}mnqakJ&y)JkO#aS'
    'RkkffzI3-+!Ja;Tb~=RyQ`v9HrK%}sH79yfxei*kCy;I-'
    'SWl$UR=U^?I~myaku^gAUe0veerp2Z%A~?d6w>3RgOwwf=A{=vL3EYHv`$R=lWrk}wAewRjh>kdAGQXW<?(ParTD;S<uiO()iS_H'
    'JyF0%BFk&PgC2&tS#fSI%#Wyl&B}^UT|rWqdyKi3b1@l9uckm(HP(7oxHz{!<6_~UlII=*`FxA2B5d`^0Ll6307<b7D^X?`n~W(B'
    'lSlSMZ30(eyl-14k)V^xt}1}!3CpgsYlS8#Qc$pixj9++Rb++-'
    'W@{|H`}uaAw%}@_>S7ilT@QlkNrfA{Be&!%iV%&&@`|U9V27zAC1ps55<g02r4Oqz!v8oEk?5SN1TO`028T&hPDBII7Kx0+Xa%&D'
    'Wu*=Y_sJ8LfYA}0t3=7kHleSVKHQluO(f%_R|#g^Gsz82w3^9VQt>~QNEBF3VkX@25ghj^ie5nDH2P6aHfRK9_E=wFw}_S+FLV=i'
    '+zl3Vz&qRoTxP;W1_FTTna0psDg85AovWP4k8;ABv573W@a(3N{*iD4TIIf9>QMv;WW=<{4RmFH<q1o)A|>1#0N4p5kLc005je&M'
    'Sw0zU=j?$_?K1+@QSDcy^cd@BpDiXhWPnN+wK(P~ApWCEip_hK5%fPIuSVD-'
    'WgZZaYW$^Xd4#V3y62^SE*D=IkMOjtK}+ka$f#+0nhiA~Vzi6H15&vN(Bw+ur-'
    'iYIu@>6ST1m==)X2WPKH!Pki-z4VDH>nevt}+)f*Mb8#R!@ykTDZ98!9p+XVlOjy%Hwv%EJR2(;4JYAS!@wx-je{dYWDULlds;hi'
    'uT3)Zf(s78WQ1^(Y^t`%0`hji!y;qhuT9gApD;7#GMTKy}!=avtcAN)OhQpzK3x8K1QF3uS0%bo{VwfD|f9#?j44o9WZ(N}CZilV'
    '*++4-D|CNF1cY?xS9A9BY#t;shO}|2E_WsQgl-gBTTXxgw3V6Qy$C#Mvd1SuFdrh;owDz34iEgNY0asr`kPqHI$+Vg^=ph$u`l-'
    'mC$|>ZS#3v9YY@sgpYAa}Q|*LR^b)JW|!ytj=ed)j5v@6Qp>g#(Z5C)QJ+MKSLf>WHThB8!NJ2Yl#h^$;im^WfLk!)M#1jK{4k|T'
    'qjA&I)U<6g_uQ)kVz636>3%mCBodECM9c?P~U@~RZ8YOPUGU6Q)1EUf*zeSI5qC0?@&b<=SkUUZIW2MKaQ7%`%X)#Lek!e(!xp~$'
    '<Cv@BPT5-!L=lG4i1*uF5|j}zSAbvT+L2z_7qt(_|fC76*+jKy%Pwhwb48!>3F?-s1?QMjNdSMD8C>PaK?iaB%M!NWI9Y-'
    'J|~q@+)Oo1LEL9_HM6)&PS7w2ldVNgQt)dnuvk6y)C6d2-6kc$*jh};g-'
    'yhECnT?=VIrnBQ~WC(&ZtqTqO^07Wxk{6ZLbSsqnWQrTp}Gk0Yexymhi$Ts-|Qmi^*?``-'
    '#vt2@Q<D^gMCF$&kW@2mZZEK!~ru45aY1IhB3rTJXny*uQgLB3D%7oaIs@(_+z4c1)nVD`ipksbrZByo);6i20#sBR2Gifdf+Ho6'
    '4;f%8S=)m6eDoGA}F0F|HJh<LW`GmL3Zvx0dl@-b>&c=<JyUV}s$1QDS&b;-6-'
    'jWlOi^REtIM!p~K!m1=8O2V+$>>AFcZI6_mktiC}gOIF=0lv7A^q@sva%lt}?RI(Tj8_-'
    '$>hTy<06$bXXWa*8p)w&CgMo~GUJ%qtrt6j2^q&z_!=Ty~2>SWr*%Vp15a&35qDIF=aZ>=;=sRp+$lsPSE2O&V#FT*$HEwMzp^Va'
    'E2`IS}^D!!|=5j<IQ5^_wokm-'
    'B{s`t6@z`PHes3SBmfgV#IHinll<RSwL*W=eN{EEy#(N3c|Sxs$>M%9)8)^cXKlc@#Ec`oE4Q50ME+PjE$PeC@SW`f1$cU!1bR=H'
    '^`-'
    '&ig2zE(}sg!?Nd2Xv_BuE{F~8C*QCE~rim1~;C3P4jqN3EP8^ww8D6)I$}NTyjf~yEv6>iIRjd7$;8eNyzcAQW35BJel%xYBl=OX'
    'wd{oJzq3Tyll>UA}-'
    'BZEdX2^puzV@)<)1nlo2Uc4PV`7ZiOJ91pFzGjunmyzcTqc*A#HN>fuaal(KlPFNQ)1c%9l~#w7~LNBNMGjg$2wT}`Ka2%7o7c8o'
    '|pv~^1(M(dYZ5ijSmYR${m%#%Xp(sD{i$2L%gnxgDiC=?UL`&dijRwf1avUQs&n4K`$KwDz*ub>)?Yj8IWkr<r`l7W1jy}hbeq?F'
    'f@t_xv)POS}=cB~)U8jKC9__8W6eo9HIE%927Yv(i;QD=d{1l2W|p=@M}I&KtO3j$x@z$^x%IRh4tM+78xi&jPnKAQ4FC<d!cWl%'
    'CqkAX)B5d~i>&YWCRM^`1T0-'
    'TlR%gxh=IC|39ofI9#Bif$;C9}>Z#+phM0q0GS_<rm^1?YirG5C}Hz!eCN!dfqkdH))W_DjDSav>lETw+j4C#kD20zXTl3aM6jKW'
    'EKaOvds~@}lqm2Vk5Tdj'
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


def agent(obs, configuration=None):
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
        return _align_hands(_rank_sell_slots(obs, action, configuration), obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }


def _kaggle_submission_entrypoint(obs, configuration=None):
    return agent(obs, configuration)

