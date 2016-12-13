#!/bin/bash

for i in {1..1000}
do
    ./halite -q -d "30 30" "python3 BorderBot4.py" "python3 BorderBot1.py" >> output.txt
    echo $i
done
rm *.hlt
python3 analyze_battle.py
rm output.txt
