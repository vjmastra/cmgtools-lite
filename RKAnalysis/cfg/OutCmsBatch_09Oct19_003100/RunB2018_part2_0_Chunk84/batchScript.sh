#!/bin/bash
echo '==== environment (before) ===='
echo
env | sort
echo

pushd $CMSSW_BASE/src
eval $(scram runtime -sh)
popd
echo
mkdir cache
export TMPDIR=$PWD/cache
mkdir job
cd job
echo '==== copying job dir to worker ===='
echo
cp -rvf $LS_SUBCWD/* .

echo '==== environment (after) ===='
echo
env | sort
echo
echo '==== running ===='
nanopy.py --single Loop pycfg.py config.pck --options=options.json
echo
echo '==== sending the files back ===='
echo
rm Loop/cmsswPreProcessing.root 2> /dev/null
echo '==== sending root files to remote dir ===='
echo
export LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH # 
for f in Loop/*.root
do
   ff=`echo $f | cut -d/ -f2`
   ff="${ff}_`basename $f | cut -d . -f 1`"
   echo $f
   echo $ff
   export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
   source $VO_CMS_SW_DIR/cmsset_default.sh
   for try in `seq 1 3`; do
      echo "Stageout try $try"
      echo "eos mkdir /eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0"
      eos mkdir /eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0
      echo "eos cp `pwd`/$f /eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0/${ff}_84.root"
      eos cp `pwd`/$f /eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0/${ff}_84.root
      if [ $? -ne 0 ]; then
         echo "ERROR: remote copy failed for file $ff"
         continue
      fi
      echo "remote copy succeeded"
      remsize=$(eos find --size /eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0/${ff}_84.root | cut -d= -f3) 
      locsize=$(cat `pwd`/$f | wc -c)
      ok=$(($remsize==$locsize))
      if [ $ok -ne 1 ]; then
         echo "Problem with copy (file sizes don't match), will retry in 30s"
         sleep 30
         continue
      fi
      echo "everything ok"
      rm $f
      echo root://eoscms.cern.ch//eos/cms/store/group/cmst3/group/bpark/gkaratha/cmg_ntuples_test/RunB2018_part2_0/${ff}_84.root > $f.url
      break
   done
done
echo
echo '==== sending local files back ===='
echo

cp -rv Loop/* $LS_SUBCWD
if [ $? -ne 0 ]; then
   echo 'ERROR: problem copying job directory back'
else
   echo 'job directory copy succeeded'
fi

