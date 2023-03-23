#!/bin/bash

a=$1

if [ $a -ge 80 -a $a -lt 90 ]; then
	echo " b "
elif [ $a -ge 90 ]; then
	echo " a "
else
	echo " f "
fi
