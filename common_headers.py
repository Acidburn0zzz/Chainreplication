from enum import Enum
class serverRole(Enum):
    undefined = 0
    head = 1;
    internal = 2
    tail = 3
    transient_tail = 4
    waiting_tobe_tail = 5
    stand_alone=6

class opOutcome(Enum):
    processed= 0
    incon_with_hist = 1
    insuf_funds = 2
    invalid_amount = 3
    illegal=4
