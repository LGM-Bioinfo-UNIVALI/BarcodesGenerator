#!/bin/bash 

source $1
conda activate rsat

length=$2
number=$3
outputfile=$4

rsat random-seq -l $length -n $number > $outputfile
