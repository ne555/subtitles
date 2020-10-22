#!/bin/bash
url=https://wiki2.org/download/en/Kindaichi_Case_Files?s=%5BARR%5D%20Kindaichi%20Shounen%20no%20Jikenbo%20%281997%29%20-%20
cola=%20%5BAVC%5D.srt
for K in {01..99}; do 
	echo $K
	wget ${url}${K}${cola}
done
