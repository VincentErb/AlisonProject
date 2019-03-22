#!/bin/bash
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd $dir

Green='\033[0;42m'
Red='\033[0;41m'
Yellow='\033[0;43m'
End='\033[0;0m'

if [ -d "env" ]
then
    echo -e $Green"virtualenv already set up"$End
else
    echo -e $Yellow"Setting up virtualenv"$End
    virtualenv env &&
    source env/bin/activate &&
    pip install -r requirements.txt
fi
