from otree.api import *
import random

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'ch2_prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'ch2_prisoner/instructions.html'
    PAYOFF_A = cu(200)
    PAYOFF_B = cu(100)
    PAYOFF_C = cu(50)
    PAYOFF_D = cu(10)

    choice_list = ["A","B"]

class Subsession(BaseSubsession):
    num_participants = models.IntegerField(initial=0)
    num_A = models.IntegerField(initial=0)
    num_B = models.IntegerField(initial=0)
    err_message = models.StringField()


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    flg_non_input = models.IntegerField(initial=0)
    flg_pair_non_input = models.IntegerField(initial=0)

    individual_choice = models.StringField(
        choices=[['A', 'A'], ['B', 'B']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    # 相手のグループID
    pair_id = models.IntegerField(initial=0)
    # 相手の意思決定
    pair_choice = models.StringField()

    # 相手はどちらを選ぶと思うか
    think_other_player_choice = models.StringField(
    widget=widgets.RadioSelectHorizontal,
        verbose_name='',
        choices=[
            ["Aを選ぶと予想する", 'Aを選ぶと予想する'],
            ["Bを選ぶと予想する", 'Bを選ぶと予想する'],
        ],
    )

    # 意思決定の理由
    individual_choice_comment  = models.LongStringField(
        verbose_name='',
        initial=""
    )


# FUNCTIONS
def keisan(player: Player):
    sub = player.subsession
    if player.individual_choice != "":
        # グラフ用集計
        sub.num_participants += 1
        s = player.individual_choice
        if s == "A":
            sub.num_A += 1
        elif s == "B":
            sub.num_B += 1
        else:
            sub.err_message = "エラーあり"
    else:
        player.flg_non_input = 1
        player.individual_choice = random.choice(C.choice_list)


def keisans(subsession: Subsession):
    for p in subsession.get_players():
        keisan(p)

def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)


def other_player(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    payoff_matrix = {
        ("A", "A"): C.PAYOFF_B,
        ("A", "B"): C.PAYOFF_D,
        ("B", "A"): C.PAYOFF_A,
        ("B", "B"): C.PAYOFF_C,
    }
    other = other_player(player)
    player.pair_choice = other.individual_choice
    player.pair_id = other.id_in_group
    if other.flg_non_input == 1:
        player.flg_pair_non_input = 1
    player.payoff = payoff_matrix[(player.individual_choice, other.individual_choice)]


# PAGESー－－－－－－－
class Introduction(Page):
    timeout_seconds = 100


class Decision(Page):
    form_model = 'player'
    form_fields = ['individual_choice','think_other_player_choice','individual_choice_comment']


class keisanWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = keisans

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            same_choice=player.individual_choice == opponent.individual_choice,
            my_decision=player.field_display('individual_choice'),
            opponent_decision=opponent.field_display('individual_choice'),
        )

    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        sub = player.subsession
        # 割合に計算
        if sub.num_A > 0:
            prop_num_A = round((sub.num_A / sub.num_participants) * 100,2)
        else:
            prop_num_A = 0
        if sub.num_B > 0:
            prop_num_B = round((sub.num_B / sub.num_participants) * 100,2)
        else:
            prop_num_B = 0

        return dict(
                    num_participants = sub.num_participants,
                    num_A  = prop_num_A,
                    num_B  = prop_num_B,
                )

class PreResults(Page):
    pass

page_sequence = [
                 Introduction,
                 Decision,
                 keisanWaitPage,
                 ResultsWaitPage,
                 PreResults,
                 Results
                 ]
