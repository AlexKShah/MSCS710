#######
#TESTS#
#######

from sys_poll import sys_poll
from db_utils import database_obj

def test_ans():
    result = sys_poll.main()
    assert result == 0
