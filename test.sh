#!/bin/bash
rm $(find . -name "*.hack")
for asm in $(find * -name "*.asm"); do
	base=${asm/.asm/}
	echo "Testing $base"
	./assemble.js $base
	mv $base.hack $base-actual.hack
	~/nand2tetris/tools/Assembler.sh $base > /dev/null
	diff --ignore-all-space $base-actual.hack $base.hack
done