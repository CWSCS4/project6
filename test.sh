#!/bin/bash
for asm in $(find . -name "*.asm"); do
	base=${asm/.asm/}
	~/nand2tetris/tools/Assembler.sh $asm > /dev/null
	mv $base.hack $base-actual.hack
	./assemble.js $asm
	diff --ignore-all-space $base-actual.hack $base.hack
done