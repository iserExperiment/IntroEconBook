from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = "ch6_mutual"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    PURCHASE = 4
    TABLE_LIST = [
        {"val": 21, "member": 3},
        {"val": 16, "member": 6},
        {"val": 11, "member": 3},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # 追加
    same_amout_flg = models.IntegerField(initial=0)
    random_cnt = models.IntegerField(initial=0)
    get_payoff_id = models.IntegerField()
    pass


class Player(BasePlayer):
    # 入力があったかどうかのフラグ
    flg_non_input = models.IntegerField()
    sellingPrice = models.IntegerField(label="")
    pass


# DEFINITION
def get_payoff_player(group: Group):
    group.random_cnt = (group.random_cnt + 1) % 2
    if group.random_cnt == 1:
        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)
        if p1.sellingPrice > p2.sellingPrice:
            group.get_payoff_id = 2
        elif p1.sellingPrice < p2.sellingPrice:
            group.get_payoff_id = 1
        else:
            group.get_payoff_id = random.randrange(1, 3)
            # 追加
            group.same_amout_flg = 1


def mutual_amount(group: Group):
    num = group.get_payoff_id
    if num == 1:
        list = [cal_amount(group.get_player_by_id(num)), 0]
        return list
    else:
        list = [0, cal_amount(group.get_player_by_id(num))]
        return list


def cal_amount(player: Player):
    p = player.sellingPrice
    if 11 - p > 0:
        return (p - C.PURCHASE) * 12
    elif 16 - p > 0:
        return (p - C.PURCHASE) * 9
    elif 21 - p > 0:
        return (p - C.PURCHASE) * 3
    else:
        return 0


# PAGES
class Exp(Page):
    timeout_seconds = 60
    form_model = "player"
    form_fields = ["sellingPrice"]

    @staticmethod
    def vars_for_template(group: Group):
        return dict(list=C.TABLE_LIST, new_round_num=group.round_number + 3)

    # 追加
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            # 入力なし
            player.flg_non_input = 1


class ExpResults(Page):
    timeout_seconds = 35

    @staticmethod
    def vars_for_template(player: Player):
        get_payoff_player(player.group)
        list = mutual_amount(player.group)
        player.group.get_player_by_id(1).payoff = int(list[0])
        player.group.get_player_by_id(2).payoff = int(list[1])
        amount = list[player.id_in_group - 1]
        return dict(
            list=C.TABLE_LIST,
            selectedVal=player.sellingPrice,
            payoff=amount,
            player_id=player.id_in_group,
        )


class ResultsWaitPage(WaitPage):
    body_text = "相手の入力を待っています。"
    pass


class Over(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Exp, ResultsWaitPage, ExpResults, Over]
