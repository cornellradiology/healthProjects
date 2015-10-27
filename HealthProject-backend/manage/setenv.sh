#!/bin/bash -e
# $File: setenv.sh
# $Date: Thu Jan 1 11:43:21 2015 +0800
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

# zsh compatibility when direct sourcing from shell
[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/config.sh

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` = 'Darwin' ]
then
  project_root=`realpath $script_dir/..`
else
  project_root=$(readlink -f $script_dir/..)
fi

env_dir=$project_root/.env

if [ ! -d "$env_dir" ]
then
	echo "$env_dir not found; please first run 'quickinstall'"
fi

. $env_dir/bin/activate


# zsh compatibility
[[ -n $ZSH_VERSION ]] && set -o shwordsplit

for i in $proj_modules
do
	PYTHONPATH=$PYTHONPATH:$project_root/$i
done
export PYTHONPATH=$PYTHONPATH:$project_root
