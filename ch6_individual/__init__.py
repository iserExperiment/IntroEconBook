from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "ch6_individual"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    PURCHASE = 4
    TABLE_ONE = [
        {"val": 21, "member": 3},
        {"val": 16, "member": 6},
        {"val": 11, "member": 3},
    ]
    TABLE_TWO = [
        {"val": 21, "member": 2},
        {"val": 18, "member": 2},
        {"val": 15, "member": 4},
        {"val": 12, "member": 2},
        {"val": 9, "member": 2},
    ]
    TABLE_THREE = [
        {"val": 21, "member": 2},
        {"val": 18, "member": 2},
        {"val": 15, "member": 2},
        {"val": 12, "member": 3},
        {"val": 9, "member": 2},
        {"val": 6, "member": 1},
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 入力があったかどうかのフラグ
    flg_non_input = models.IntegerField()

    sellingPrice = models.IntegerField(label="")
    pass


# FUNCTIONS
def cal_amount1(player: Player):
    purchasePrice = C.PURCHASE
    p = player.sellingPrice
    if 11 - p > 0:
        return (p - purchasePrice) * 12
    elif 16 - p > 0:
        return (p - purchasePrice) * 9
    elif 21 - p > 0:
        return (p - purchasePrice) * 3
    else:
        return 0


def cal_amount2(player: Player):
    purchasePrice = C.PURCHASE
    p = player.sellingPrice
    if 9 - p > 0:
        return (p - purchasePrice) * 12
    elif 12 - p > 0:
        return (p - purchasePrice) * 10
    elif 15 - p > 0:
        return (p - purchasePrice) * 8
    elif 18 - p > 0:
        return (p - purchasePrice) * 4
    elif 21 - p > 0:
        return (p - purchasePrice) * 2
    else:
        return 0


def cal_amount3(player: Player):
    purchasePrice = C.PURCHASE
    p = player.sellingPrice
    if 6 - p > 0:
        return (p - purchasePrice) * 12
    elif 9 - p > 0:
        return (p - purchasePrice) * 11
    elif 12 - p > 0:
        return (p - purchasePrice) * 9
    elif 15 - p > 0:
        return (p - purchasePrice) * 6
    elif 18 - p > 0:
        return (p - purchasePrice) * 4
    elif 21 - p > 0:
        return (p - purchasePrice) * 2
    else:
        return 0


# PAGES
class Exp(Page):
    timeout_seconds = 60
    form_model = "player"
    form_fields = ["sellingPrice"]

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == 1:
            return dict(list=C.TABLE_ONE, num=player.round_number)
        elif player.round_number == 2:
            return dict(list=C.TABLE_TWO, num=player.round_number)
        else:
            return dict(list=C.TABLE_THREE, num=player.round_number)

    # 追加
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            # 入力なし
            player.flg_non_input = 1


class ExpResults(Page):
    timeout_seconds = 30

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number == 1:
            amount = cal_amount1(player)
            player.payoff = amount
            return dict(
                selectedVal=player.sellingPrice, payoff=amount, list=C.TABLE_ONE
            )
        elif player.round_number == 2:
            amount = cal_amount2(player)
            player.payoff = amount
            return dict(
                selectedVal=player.sellingPrice, payoff=amount, list=C.TABLE_TWO
            )
        else:
            amount = cal_amount3(player)
            player.payoff = amount
            return dict(
                selectedVal=player.sellingPrice, payoff=amount, list=C.TABLE_THREE
            )


class ResultsWaitPage(WaitPage):
    body_text = "相手の確認を待っています。"
    pass


page_sequence = [Exp, ExpResults, ResultsWaitPage]
