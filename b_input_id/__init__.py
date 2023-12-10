from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'b_input_id'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 入力されるID
    input_id = models.StringField(
        verbose_name='',
        initial=""
    )


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['input_id']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage,
                 #ResultsWaitPage,
                 #Results
                 ]
