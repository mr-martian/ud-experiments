#!/bin/bash

rtx-comp eng.rtx eng.bin
cat eng-input.txt | rtx-proc -T eng.bin

./compile.py eng.ud eng-comp.rtx
rtx-comp eng-comp.rtx eng-comp.bin
cat eng-input.txt | rtx-proc -T eng-comp.bin
