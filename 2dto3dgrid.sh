#!/bin/bash

file2d=$1
file3d=$2

cp $file2d $file3d



#insert z
sed -i '3inzlev	1' $file3d

#first data at 7
zllcorner=`awk 'NR==7{print $1}' $file2d`
sed -i "6izllcorner\t$zllcorner" $file3d
cellsize=`awk 'NR==5{print $2}' $file2d`
sed -i -e 's/cellsize/xcellsize/g' $file3d
sed -i "8iycellsize\t$cellsize" $file3d
sed -i "9izcellsize\t$cellsize" $file3d
sed -i "11idatatype\tfloat" $file3d
