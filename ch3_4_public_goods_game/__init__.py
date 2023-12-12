from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = "ch3_4_public_goods_game"
    PLAYERS_PER_GROUP = 10
    NUM_ROUNDS = 10
    ENDOWMENT = cu(40)
    MULTIPLIER = 2
    INSTRUCTIONS_TEMPLATE = "ch3_4_public_goods_game/instructions.html"


class Subsession(BaseSubsession):
    num_participants = models.IntegerField(initial=0)
    sum_decisinon = models.IntegerField(initial=0)


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    start_timestamp = models.IntegerField()


class Player(BasePlayer):
    # 入力がなかった場合
    flg_non_input = models.IntegerField(initial=0)

    individual_choice = models.StringField(
        label="あなたはいくら投資しますか？",
    )


# FUNCTIONS-----------------------
def keisan(player: Player):
    sub = player.subsession
    if player.individual_choice != "":
        # グラフ用集計
        sub.num_participants += 1
        # tmp = random.randint(0, 40)
        # player.individual_choice = str(tmp)
        s = player.individual_choice
        sub.sum_decisinon = sub.sum_decisinon + int(s)
    else:
        player.flg_non_input = 1
        tmp = random.randint(0, 40)
        player.individual_choice = str(tmp)
        s = player.individual_choice
        sub.sum_decisinon = sub.sum_decisinon + int(s)


def set_payoffs(group: Group):
    players = group.get_players()

    contributions = [int(p.individual_choice) for p in players]
    print(contributions)
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.individual_choice + group.individual_share


def keisans(subsession: Subsession):
    for p in subsession.get_players():
        keisan(p)


# PAGES-------------------------
class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())


class Introduction(Page):
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Contribute(Page):
    timeout_seconds = 40
    form_model = "player"
    form_fields = ["individual_choice"]


class keisanWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = keisans


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    timeout_seconds = 30


class Summarize_Result(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        sub = player.subsession
        list_counts = []
        list_data = []

        # prev_player = player.in_round(1)
        # print("test",prev_player.payoff)

        for i in range(C.NUM_ROUNDS):
            i = i + 1
            all_sub_round = sub.in_round(i)
            list_counts.append(str(i) + "回目")
            list_data.append(all_sub_round.sum_decisinon)

        # print(list_average.replace('[', ''))
        # print(list_average.replace(']', ''))
        return dict(
            list_counts=list_counts,
            list_data=list_data,
        )


page_sequence = [
    WaitToStart,
    Introduction,
    Contribute,
    keisanWaitPage,
    ResultsWaitPage,
    Results,
    Summarize_Result,
]
