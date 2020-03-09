#!/bin/bash

for VAR in hmBlowq_ncut hmBjpsi_nocut hBpt hBslxy hBprob hBcos hmBlowq hmBjpsi
do
   python combinePlots.py --two-plot-ratio -i plots_Sep12 nofix_slxy -p ${VAR} -o ${VAR} -l Sep12 Nov29 -c LogY -o bugged
done
