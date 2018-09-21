@echo off
echo "train and test of Brest Cancer dataset"
:top
set d=
set /P debug=debug[Y/n]?
if /I "%debug%" EQU "Y" set d=-d 
python main.py -a tests/bcw-attributes.txt -l tests/bcw-train.csv -t tests/bcw-test.csv id3 Class %d%
Pause
set /P c=want to continue[Y/n]?
if /I "%c%" EQU "Y" goto :top
Pause