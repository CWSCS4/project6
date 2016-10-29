#!/bin/bash
for asm in $(find . -name "*.asm"); do
 	base=${asm/.asm/}
 	~/nand2tetris/tools/Assembler.bat $asm > /dev/null #make this .sh to run on linux
 	mv $base.hack $base-actual.hack
 	./assemble.js $asm
	diff --ignore-all-space $base-actual.hack $base.hack
done