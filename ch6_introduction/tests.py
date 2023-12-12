from otree.api import Bot, SubmissionMustFail
from . import *

class PlayerBot(Bot):
    def play_round(self):
        if self.player.in_round(1).cnt==0:
            yield Instruction1
            yield Instruction2
            yield Check1, dict(check_q1=False)
            yield Incorrect1
            yield Check1, dict(check_q1=True)
            yield Correct1
        if self.player.in_round(1).cnt == 1:
            yield Check2, dict(check_q2=False)
            yield Incorrect2
            yield Check2, dict(check_q2=True)
            yield Correct2
        if self.player.in_round(1).cnt == 2:
            yield Check3, dict(check_q3=False)
            yield Incorrect3
            yield Check3, dict(check_q3=True)
            yield Correct3
        if self.player.in_round(1).cnt == 3:
            yield Check4, dict(check_q4_int1=10, check_q4_int2=30)
            yield Incorrect4
            yield Check4, dict(check_q4_int1=50, check_q4_int2=10)
            yield Correct4
            yield Lastpage
