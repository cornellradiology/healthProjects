#!/bin/bash -e
# $File: exec-in-virtualenv.sh
# $Date: Sun Jul 13 15:38:35 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

# start a python script in virtualenv, with appropriate envrionment variables
# set

if [ `uname` = 'Darwin' ]; then
	realdir=$(dirname $(realpath "$0"))
else
	realdir=$(dirname $(readlink -f "$0"))
fi

source $realdir/setenv.sh

if [ -z "$1" ]
then
	echo "usage: $0 <python script>"
	exit
fi

/usr/bin/env python2 ${@: 1}

