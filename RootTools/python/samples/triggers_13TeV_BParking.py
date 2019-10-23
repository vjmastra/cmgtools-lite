# Triggers for 2018 DATA
triggers_mu12ipX = ["HLT_Mu12_IP6_*"]
triggers_mu10ipX = ["HLT_Mu10p5_IP3p5_*"]
triggers_mu9ipX = ["HLT_Mu9_IP4_*","HLT_Mu9_IP5_*","HLT_Mu9_IP6_*"]
triggers_mu8ipX = ["HLT_Mu8_IP3_*","HLT_Mu8_IP5_*","HLT_Mu8_IP6_*","HLT_Mu8p5_IP3p5_*"]
triggers_mu7ipX = ["HLT_Mu7_IP4_*"]

triggers_muXipY= triggers_mu12ipX + triggers_mu10ipX + triggers_mu9ipX + triggers_mu8ipX + triggers_mu7ipX



### Wrap all in a dictionary for easier importing of multiple years
all_triggers = dict((x.replace("triggers_",""),y) for (x,y) in locals().items() if x.startswith("triggers_") and isinstance(y,list))
