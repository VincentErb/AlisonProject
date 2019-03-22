#!/bin/bash
dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd $dir

yapf -i -r alison/
yapf -i -r tests/
