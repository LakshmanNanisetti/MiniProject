@echo off
echo "train and test of Brest Cancer dataset"
:top
set d=
set debug=Y
set /P debug=debug[Y/n]?
if /I "%debug%" EQU "Y" set d=-d 
python main.py  id3 Nephritis_of_renal_pelvis_origin %d% -a tests/ai-attributes.txt -l tests/ai-train.csv -t tests/ai-test.csv
Pause
set c=Y
set /P c=want to continue[Y/n]?
if /I "%c%" EQU "Y" goto :top
Pause