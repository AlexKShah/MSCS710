#!/bin/bash

#execute test files, write logs
exec python3 tests.py 2&>1 | tee -a /tmp/tests.log;
echo "py done" | tee -a /tmp/tests.log;
sleep 5;

#read logs
cat /tmp/tests.log;
echo "bash done";
