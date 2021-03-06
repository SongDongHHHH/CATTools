#!/bin/bash

eval `scramv1 runtime -sh`

rm invmass/res_[0-9]*.txt

type='null'

if [ $# != "0" ]; then
	type=$1
fi

#cut='d0_L3D>0.2 && d0_LXY>0.1&& dstar_L3D>0.2 && dstar_LXY>0.1 && abs(dstar_diffMass-0.145)<0.01'
#cut='abs(dstar_diffMass-0.145)<0.02 && dstar_LXY>0.09'
cut_d0='d0_L3D>0.2&&d0_LXY>0.1&&abs(d0.M()-1.8648)<0.040'

./massPlot.py -c "${cut_d0}"  -s 5 -b [30,0,150] -p 'd0_lepSV_lowM' -x 'M_{l+D0} [GeV/c^2]' -t $type >> invmass/res_001.txt & 
./massPlot.py -c "${cut_d0}"  -s 5 -b [30,0,150] -p 'd0_lepSV_dRM' -x 'M_{l+D0} [GeV/c^2]' -t $type >> invmass/res_002.txt &
#./massPlot.py -s 0 -b [30,0,150] -p 'd0_lepSV_correctM' -x 'M_{l+D0} [GeV/c^2]' -t $type >> invmass/res_003.txt &


