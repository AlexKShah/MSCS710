#!/bin/bash

#execute test files, write logs
exec python3 -m pytest tests.py    | tee -a /tmp/tests.log && echo "pytest done" | tee -a /tmp/tests.log;
exec python3 -m pytest db_utils.py | tee -a /tmp/tests.log && echo "pytest done" | tee -a /tmp/tests.log;
exec python3 -m pytest sys_poll.py | tee -a /tmp/tests.log && echo "pytest done" | tee -a /tmp/tests.log;

sleep 5;

#read logs
cat /tmp/tests.log;
echo "tests done - bash exit";

wait &;
