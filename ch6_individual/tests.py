from otree.api import Bot, SubmissionMustFail
from . import *
import random
class PlayerBot(Bot):
    def play_round(self):
        yield Exp, dict(sellingPrice = random.randint(4,25))
        yield ExpResults
        
