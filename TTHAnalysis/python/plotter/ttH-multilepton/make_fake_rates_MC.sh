################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

ANALYSIS=$1; if [[ "$1" == "" ]]; then exit 1; fi; shift;
case $ANALYSIS in
sos) 
    YEAR=$1; shift; 
    case $YEAR in 2016) L=35.9;; 2017) L=41.5;; 2018) L=59.7;; esac
    T=/eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_230819_v5/$YEAR
    #test -d /tmp/$USER/TREES_ttH_FR_nano_v5/$YEAR && T="/tmp/$USER/TREES_ttH_FR_nano_v5/$YEAR -P $T"
    #test -d /data/$USER/TREES_ttH_FR_nano_v5/$YEAR && T="/data/$USER/TREES_ttH_FR_nano_v5/$YEAR -P $T"
    #hostname | grep -q cmsco01 && T=/data1/gpetrucc/TREES_94X_FR_240518
    #hostname | grep -q cmsphys10 && T=/data/g/gpetrucc/TREES_94X_FR_240518
    PBASE="~/www/FakeRate/104X/${ANALYSIS}/fr-mc/$YEAR"
    TREE="NanoAOD";
    ;;
susy) 
    echo "NOT UP TO DATE"; exit 1; 
    ;;
*)
    echo "Unknown analysis '$ANALYSIS'";
    exit 1;
esac;


BCORE=" --s2v --tree ${TREE} susy-sos-v2-clean/lepton-fr/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt"
BCORE="${BCORE} -L susy-sos-v2-clean/functionsSOS.cc"
#if [[ "$TREE" == "treeProducerSusyMultilepton" ]]; then
    BCORE="${BCORE} --mcc susy-sos-v2-clean/mcc_sos.txt"
    #Not sure if we need it
    #BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
#else
    BCORE="${BCORE} --Fs {P}/recleaner"
    #BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
#fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PLOTTER="python mcPlots.py $BCORE   "


BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi
HAS_CUSTOM_RECOIL=false


#if [[ "$*" == "" ]]; then WPs="090iv01f60E3"; else WPs="$1"; fi;
#for WP in $WPs; do
        #MuIdDen=0; 
        #All these cuts should be implemented in the FO definition in the sos_module
        #Just written here as a x-check
        EleRecoPt=5; MuRecoPt=3.5; # what should we ask fot Jets ??AwayJetPt=30; EleTC=0; IDEMu=1
        #SIP2p5="LepGood_sip3d < 2.5";
        #Dxy="0.05";
        #Dz="0.1";
        #AbsIso="LepGood_pfRelIso03_all*LepGood_pt<(20+300/LepGood_pt)"
        #bVeto="nBJetLoose25 == 0"
	#VETOCONVERSIONS="LepGood_mcPromptGamma==0"
        
        # case $WP in 
        #     000*) WNUM="0.00" ;; 030*) WNUM="0.30" ;; 060*) WNUM="0.60" ;;
        #     075*) WNUM="0.75" ;; 080*) WNUM="0.80" ;; 085*) WNUM="0.85" ;;  090*) WNUM="0.90" ;;
        #     sM*) WNUM="if3(abs(LepGood_pdgId)==13,-0.2,0.5)";; sV*) WNUM="if3(abs(LepGood_pdgId)==13,0.45,0.75)";;
        # esac
        # case $WP in
        #     0??)     SelDen="-A pt20 den '$SIP8'"; MuIdDen=1 ; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";;
        #     0??i)    SelDen="-A pt20 den '$SIP8'"; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";; 
        #     # This below was the 2017 version
        #     #0??ov010*) SelDen="-A pt20 den '$SIP8 && $VDCSVM && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VDCSVVL && LepGood_segmentComp > 0.3) || (abs(LepGood_pdgId)==11 && $VDCSVVL && LepGood_mvaIdFall17noIso > +0.5))'"; Num="mvaPt_${WP%%o*}"i; XVar="mvaPt${WP%%o*}";;

        #     0??v00*) SelDen="-A pt20 den '$SIP8 && $VDFM'"; MuIdDen=1 ; Num="mvaPt_${WP%%v*}"i; XVar="mvaPt${WP%%v*}";;
        #     0??iv00*) SelDen="-A pt20 den '$SIP8 && $VDFM'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";;
        #     0??iv01*) SelDen="-A pt20 den '$SIP8 && $VDFM && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VDFL) || (abs(LepGood_pdgId)==11 && $VDFL))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";;
        #     0??iv070*) VSMOOTH="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year)";
        #                SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VSMOOTH) || (abs(LepGood_pdgId)==11 && $VSMOOTH))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 
        #     0??iv08WP80*) VSMOOTH="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year)";
        #                SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VSMOOTH) || (abs(LepGood_pdgId)==11 && LepGood_mvaFall17V2noIso_WP80))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 
        #     0??iRun2v1.0*) 
        #                IDEmu="LepGood_idEmu3"
        #                MUEXTRA="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year) && LepGood_jetRelIso < 0.50";
        #                ELEXTRA="LepGood_mvaFall17V2noIso_WP80 && LepGood_jetRelIso < 0.70"
        #                SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $MUEXTRA) || (abs(LepGood_pdgId)==11 && $ELEXTRA))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 

        #     RA5*)    SelDen="-A pt20 den '$SIP4'"; MuIdDen=1 ; Num="ra5_tight"; XVar="${WP}";;
        #     RA7*)    SelDen="-A pt20 den '$SIP4 && met_pt<20 && mt_2(LepGood_pt,LepGood_phi,met_pt,met_phi)<20'"; MuIdDen=1 ; MuRecoPt=10; EleRecoPt=10; AwayJetPt=40; Num="ra7_tight"; XVar="${WP}";;
        #     s?i*)   SelDen="-A pt20 den '$SIP8'"; Num="mvaSusy_${WP}" ; XVar="mvaSusy_${WP}";;
        # esac
        # case $WP in
        #     *f30*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.30)' " ;;
        #     *f40*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.40)' " ;;
        #     *f45*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.45)' " ;;
        #     *f50*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.50)' " ;;
        #     *f60*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.60)' " ;;
        #     *f65*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.65)' " ;;
        #     *j40*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.40)' " ;;
        #     *j50*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.50)' " ;;
        #     *j60*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.60)' " ;;
        #     *j70*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.70)' " ;;
        #     *j80*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.80)' " ;;
        #     *j90*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.90)' " ;;
        # esac
        # case $WP in
        #     *X0*) Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X1*) SelDen="$SelDen -A pt20 vcsvm '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVM && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X2*) SelDen="$SelDen -A pt20 vcsvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X3k*) SelDen="$SelDen -A pt20 vcsvvl '$VCSVM && ((LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVVL && $PTF30))'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X3*) SelDen="$SelDen -A pt20 vcsvvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X4v*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X4mr*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL2} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}"; MuIdDen=1; MuRecoPt=10; EleRecoPt=10;;
        #     *X4*) SelDen="$SelDen -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        #     *X5*) SelDen="$SelDen -A pt20 vcsvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
        # esac
        # case $WP in
        #     *E2) IDEMu="LepGood_idEmu2";;
        #     *E2ptc30) IDEMu="LepGood_idEmu2 || LepGood_pt*if3(LepGood_mvaTTH>${WNUM}, 1.0, 0.90*(1+LepGood_jetRelIso)) < 30" ;;
        #     *E3) IDEMu="LepGood_idEmu3";;
        # esac
        # case $WP in
        #     *ptJ75*)    ptJI="ptJI75";;
        #     *ptJ80*)    ptJI="ptJI80";;
        #     *ptJ85*)    ptJI="ptJI85";;
        #     *ptJ90*)    ptJI="ptJI90";;
        #     *ptJ95*)    ptJI="ptJI95";;
        #     090*)    ptJI="ptJI90";;
        #     085*)    ptJI="ptJI90";;
        #     080*)    ptJI="ptJI90";;
        #     075*)    ptJI="ptJI90";;
        #     RA*)  ptJI="conePt";;
        #     sViX0*)    ptJI="ptJI85";;
        #     sMiX0*)    ptJI="ptJI85";;
        #     sVi*)    ptJI="ptJIMIX3";;
        #     sMi*)    ptJI="ptJIMIX4";;
        # esac

        Num="LepGoo1_tigh && LepGood2_tight"

        #usy-sos-v2-clean/lepton-fr/make_fake_rates_xvars.txt ??
        B0="$BASE -P $T susy-sos-v2-clean/lepton-fr/make_fake_rates_sels.txt susy-sos-v2-clean/lepton-fr/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        #B0="$B0 --legend=TR --showRatio --ratioRange 0.41 1.59   --yrange 0 0.20 " 
        B0="$B0 --legend=TR --showRatio --ratioRange 0.00 1.99   --yrange 0 0.35 " 
	B1="${PLOTTER} -P $T susy-sos-v2-clean/lepton-fr/make_fake_rates_plots.txt"
        B1="$B1 --showRatio --maxRatioRange 0 2 --plotmode=norm -f "
        CommonDen="'nLepGood==2'"
        MuDen="${CommonDen} -A 'abs(LepGood_pdgId) == 13'"
        ElDen="${CommonDen} -A 'abs(LepGood_pdgId) == 11'"
        #for BVar in bAny; do # bMedium; do 
        #RVar=${AwayJetPt}; 
        #case $BVar in
        #    bAny)    BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
        #    bVeto)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.5426' " ;;
        #    bLoose)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.5426' " ;;
        #    bMedium) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.8484'  " ;;
        #    bTight)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.9535'  " ;;
        #esac;
        #Me="wp${WP}_rec${RVar}_${BVar}"
        #Me="wp${WP}_recJet30"
        #BDen="-A pt20 jet 'LepGood_awayJet_pt >= 30'"
        #Me="wp${WP}_twoOrThreeLoose"
        #BDen="-A pt20 jet 'LepGood_awayNBJetLoose25 == 1 && LepGood_awayNJet25 > 1 && LepGood_awayNJet25 <= 3'"
        #Me="wp${WP}_oneM"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 2 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetMedium25 == 1' "
        #Me="wp${WP}_oneT"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 2 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetTight25 == 1' "
        #Me="wp${WP}_oneExT"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 1 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetTight25 == 1' "
        #if $HAS_CUSTOM_RECOIL; then
        #    Me="wp${WP}_${RECOIL_NAME}"
        #    BDen="-A pt20 jet '${RECOIL_VALUE}'"
        #fi

        MuFakeVsPt="$MuDen --sP 'pt_coarse'" 
        #ElFakeVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_SS_redNC --xcut 10 999 --xline 15 --xline 30 " 
        #MuFakeVsPtLongBin="$MuDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_red   --xcut 10 999 --xline 15 " 
        #ElFakeVsPtLongBin="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_redNC --xcut 10 999 --xline 15 " 
        echo "( $B0 $MuFakeVsPt -p WJets_light -o $PBASE/$what/testMuFakeVsPt.root  ${BG} )"
       # echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red,QCDMu_red -o $PBASE/$what/mu_lbin_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       # echo "( $B0 $ElFakeVsPtLongBin -p TT_SS_red,TT_SS_redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_lbin_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
       # echo "( $B0 $ElFakeVsPtLongBin -p TT_SS_red,TT_SS_redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_lbin_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
	#break;
     
        #for C in 15_17.5 17.5_22.5 20_30 45_60 45_999; do
        #    conePtCut="-A pt20 conePt '${C%_*} < LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) && LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) < ${C#*_}' ";
        #    echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets --pdir $PBASE/$what/mu_bnb_${Me}_eta_00_12_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.2'   --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets --pdir $PBASE/$what/mu_bnb_${Me}_eta_12_24_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.2'   --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets --pdir $PBASE/$what/el_bnb_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets --pdir $PBASE/$what/el_bnb_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sum_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sum_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sumold_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sumold_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
        #    echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_redB --ratioNums ".*" -p TT_SS_red[BE],QCDMu_red[BE],QCDMu_bjets[BE] --pdir $PBASE/$what/mu_BE_${Me}_ptC_${C}/ -X pt20  --sP 'lep_.*' ${BG} )"
        #done

       ##AwayJet pt variations
       #MuFakeVsPt0J="$MuDen --sP '${ptJI}_${XVar}_coarsecomb' --sp TT_red --xcut 10 999 --xline 15" 
       #ElFakeVsPt0J="$ElDen --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_red --xcut 10 999 --xline 15" 

       ###AwayJet b-tag
       #MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_coarsecomb' --sp TT_red,TT_SSbt_black ${BDen} --xcut 10 999 --xline 15" 
       #ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_red,TT_SSbt_black ${BDen} --xcut 10 999 --xline 15" 
        ## Efficiencies 
        #BE="${B0/--yrange 0 0.25/--yrange 0 1.25}"
        #echo "( $BE $MuFakeVsPt -p TT_SS_red,TT_red,TT_fromW,TT_fromTau -o $PBASE/$what/mu_tteff_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2' -X jet -X mll  ${BG} )"

        #MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_fine' --sp TT_SS_red ${BDen} --xcut 10 999 --xline 15" 
        #ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_fine' --sp TT_SS_redNC ${BDen} --xcut 10 999 --xline 15" 
        ## TTbar by composition
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC,TT_SS.*_redNC -o $PBASE/$what/el_ttvarsNC_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC,TT_SS.*_redNC -o $PBASE/$what/el_ttvarsNC_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        ## TT by flavour
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets,TT_ljetsNC -o $PBASE/$what/el_ftt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets,TT_ljetsNC -o $PBASE/$what/el_ftt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,TT_cjets,TT_ljetsNC -o $PBASE/$what/el_fttNC_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,TT_cjets,TT_ljetsNC -o $PBASE/$what/el_fttNC_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #done;
#done
