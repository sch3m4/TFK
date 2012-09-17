#!/bin/sh

PYBIN=`which python`

if [ -z "$PYBIN" ]
then
  echo "[e] Python binary not found!"
  exit -1
fi

$PYBIN ./tfk.py

exit $?
