from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot


#Uncompleted
class PlayerBot(Bot):
    def play_round(self):      
        if self.player.round_number == 1:
            yield Instruction1
            yield Instruction2, dict(instruction_q1=1601)
            yield Instruction3, dict(instruction_q2=1) 

