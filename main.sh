#!/bin/bash

rtx-comp eng.rtx eng.bin
cat eng-input.txt | rtx-proc -T eng.bin
