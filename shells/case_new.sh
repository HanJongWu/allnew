#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Enter the Coutry name~!!"
else
	case "$1" in
		ko) echo "Seoul" ;;
		us) echo "washington" ;;
		cn) echo "Beijing" ;;
		jp) echo "Tokyo" ;;
		*) echo "Enter the contry name~!!"
esac

if [ "$1" = uk ]; then
	echo "Your entery => uk is not the list."
else
	echo "Enter the Contry name~!!"
fi

