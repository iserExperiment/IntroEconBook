from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ch3_0_shortandlong'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    choice_list = ["A", "B"]

    CHOICE_LABEL_1 = "仕事する"
    CHOICE_LABEL_2 = "仕事しない"


    INSTRUCTIONS_TEMPLATE = 'ch3_0_shortandlong/instructions.html'

class Subsession(BaseSubsession):
    num_participants_1 = models.IntegerField(initial=0)
    num_A_1 = models.IntegerField(initial=0)
    num_B_1 = models.IntegerField(initial=0)
    err_message_1 = models.StringField()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    flg_non_input_1 = models.IntegerField(initial=0)
    individual_choice_1 = models.StringField(
        choices=[['A', '仕事する'], ['B', '仕事しない']],
        verbose_name='',
        widget=widgets.RadioSelect,
    )

    # 意思決定の理由
    individual_choice_comment_1  = models.LongStringField(
        verbose_name='',
        initial=""
    )

# FUNCTIONS------------------------------------------
def keisan_1(player: Player):
    sub = player.subsession
    if player.individual_choice_1 != "":
        # グラフ用集計
        sub.num_participants_1 += 1
        s = player.individual_choice_1
        if s == "A":
            sub.num_A_1 += 1
        elif s == "B":
            sub.num_B_1 += 1
        else:
            sub.err_message_1 = "エラーあり"
    else:
        player.flg_non_input_1 = 1
        player.individual_choice_1 = random.choice(C.choice_list)

def keisans_1(subsession: Subsession):
    for p in subsession.get_players():
        keisan_1(p)

# PAGES ------------------------------------------
class Introduction(Page):
    timeout_seconds = 100

class Decision_1(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = ['individual_choice_1','individual_choice_comment_1']


class keisanWaitPage_1(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = keisans_1


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            my_decision=player.field_display('individual_choice_1'),
        )

    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        sub = player.subsession
        # 割合に計算
        if sub.num_A_1 > 0:
            prop_num_A_1 = round((sub.num_A_1 / sub.num_participants_1) * 100, 2)
        else:
            prop_num_A_1 = 0
        if sub.num_B_1 > 0:
            prop_num_B_1 = round((sub.num_B_1 / sub.num_participants_1) * 100, 2)
        else:
            prop_num_B_1 = 0

        return dict(
            num_participants=sub.num_participants_1,
            num_A_1=prop_num_A_1,
            num_B_1=prop_num_B_1,
        )


page_sequence = [
                 Introduction,
                 Decision_1,
                 keisanWaitPage_1,
                 Results1,
                 ]
