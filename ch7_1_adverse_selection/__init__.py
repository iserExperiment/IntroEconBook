import os
import random
import time

from otree.api import *


doc = ""


class C(BaseConstants):
    NAME_IN_URL = "ch7_1_adverse_selection"
    PLAYERS_PER_GROUP = 12
    NUM_ROUNDS = 2

    INSTRUCTIONS1_TEMPLATE = "ch7_1_adverse_selection/Instruction1.html"

    VALUE_GOOD_BUYER = 3500  # 買い手にとって状態の良い中古品の価値
    VALUE_BAD_BUYER = 500  # 買い手にとって状態の悪い中古品の価値
    VALUE_GOOD_SELLER = 1600  # 売り手にとって状態の良い中古品の価値
    VALUE_BAD_SELLER = 0  # 売り手にとって状態の悪い中古品の価値
    BUYER_NUM = 6  # Buyer数＝Seller数とする
    OWN_RATE = [[1, 1], [1, 2]]  # 保有数の割合をラウンド毎に設定([良い中古品：悪い中古品の比率])

    VALUE_GOOD_SELLER_ONE = 1601  # 売り手にとって状態の良い中古品を売却する価格
    VALUE_BAD_SELLER_ONE = 1  # 売り手にとって状態の悪い中古品の価値

    A1 = "1601"
    A2 = "6"
    A3 = "0"

    A4 = "1601"
    A5 = "4"
    A6 = "0"
    A7 = "8"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    good_players = models.IntegerField(initial=0)
    bad_players = models.IntegerField(initial=0)
    update_good = models.IntegerField(initial=0)
    update_bad = models.IntegerField(initial=0)
    start_timestamp = models.IntegerField()


class Player(BasePlayer):
    quiz_cnt = models.IntegerField(label="", initial=1)
    type = models.StringField(initial="none")
    player_number = models.IntegerField(initial=0)
    used_status = models.BooleanField(initial=False)  # Trueなら良い中古品
    buy_value = models.IntegerField(initial=0)
    bought_number = models.IntegerField(initial=0)
    buyer_history = models.StringField(initial="")
    seller_min_cost = models.IntegerField(initial=0)
    sell_flg = models.BooleanField(initial=False)
    torihiki_num = models.IntegerField(initial=0)
    history2 = models.StringField(initial="")
    instruction_q1 = models.IntegerField(
        verbose_name="利得を最大にする購入価格を入力してください", initial=0
    )
    instruction_q2 = models.IntegerField(
        verbose_name="利得を最大にする購入価格を入力してください", initial=0
    )

    q1 = models.StringField(
        choices=[["1601", "1601"], ["1600", "1600"], ["500", "500"]],
        label="ケース１：[あ]あなたが状態のよい中古品を購入する価格",
        widget=widgets.RadioSelect,
    )

    q2 = models.StringField(
        choices=[["6", "6"], ["12", "12"]],
        label="ケース１：[い]あなたが状態のよい中古品を購入する個数",
        widget=widgets.RadioSelect,
    )

    q3 = models.StringField(
        choices=[["0", "0"], ["6", "6"], ["12", "12"]],
        label="ケース２：[う]あなたが状態のよい中古品を購入する個数",
        widget=widgets.RadioSelect,
    )

    q4 = models.StringField(
        choices=[["1601", "1601"], ["1600", "1600"], ["1", "1"]],
        label="ケース３：[か]あなたが状態のよい中古品を購入する価格",
        widget=widgets.RadioSelect,
    )

    q5 = models.StringField(
        choices=[["0", "0"], ["6", "6"], ["4", "4"]],
        label="ケース３：[き]あなたが状態のよい中古品を購入する個数",
        widget=widgets.RadioSelect,
    )

    q6 = models.StringField(
        choices=[["0", "0"], ["6", "6"], ["4", "4"]],
        label="ケース４：[く]あなたが状態のよい中古品を購入する個数",
        widget=widgets.RadioSelect,
    )

    q7 = models.StringField(
        choices=[["0", "0"], ["8", "8"]],
        label="ケース４：[け]あなたが状態の悪い中古品を購入する個数",
        widget=widgets.RadioSelect,
    )


class Transaction(ExtraModel):
    player = models.Link(Player)
    buyer = models.Link(Player)
    seller = models.Link(Player)
    offer_price = models.CurrencyField()
    tradePartner = models.IntegerField()
    goods_status = models.StringField()
    seller_payoff = models.CurrencyField()
    buyer_payoff = models.CurrencyField()
    seconds = models.FloatField(doc="Timestamp (seconds since beginning of game)")


def custom_export(players):
    yield [
        "sessionID",
        "groupID",
        "round_number",
        "playerID",
        "player_type",
        "buyer_offerPrice",
        "tradePartner",
        "goods_status",
        "seller_payoff",
        "buyer_payoff",
        "time",
    ]

    scores = Transaction.filter()
    for score in scores:
        player = score.player
        session = player.session
        yield [
            session.code,
            player.group.id_in_subsession,
            player.round_number,
            player.id_in_group,
            player.type,
            score.offer_price,
            score.tradePartner,
            score.goods_status,
            score.seller_payoff,
            score.buyer_payoff,
            score.seconds,
        ]


# FUNCTIONS
def init_player(group: Group):
    buyers_ID = random.sample(range(C.PLAYERS_PER_GROUP), C.BUYER_NUM)
    buyers_ID.sort()
    buy_count = 0
    sell_count = 0
    p1_rate = C.OWN_RATE[group.round_number - 1][0]
    p2_rate = C.OWN_RATE[group.round_number - 1][1]
    good_num = C.BUYER_NUM // (p1_rate + p2_rate) * p1_rate
    good_seller_p_num = random.sample(range(C.BUYER_NUM), C.BUYER_NUM)[:good_num]

    for p in group.get_players():
        if buy_count < C.BUYER_NUM and p.id_in_group == buyers_ID[buy_count] + 1:
            p.type = "buy"
            p.player_number = buy_count + 1
            buy_count += 1
        else:
            p.type = "sell"
            p.player_number = sell_count + 1

            if p.player_number - 1 in good_seller_p_num:
                p.used_status = True
                p.seller_min_cost = C.VALUE_GOOD_SELLER
                group.good_players += 1
                group.update_good += 1
            else:
                p.seller_min_cost = C.VALUE_BAD_SELLER
                group.bad_players += 1
                group.update_bad += 1
            sell_count += 1


def instruction_q1_error_message(player: Player, value):
    if value != 1601:
        return "間違っています。もう一度回答ください。"


def instruction_q2_error_message(player: Player, value):
    if value != 1:
        return "間違っています。もう一度回答ください。"


def live_bid(player: Player, data):
    buyVal_list = [0] * C.BUYER_NUM  # 提示する購入価格
    bought_list = [0] * C.BUYER_NUM  # これまでに購入した中古品数
    sold_list = [False] * C.BUYER_NUM  # 誰に売ったか？
    seller_payoff = [0] * C.BUYER_NUM
    buyer_payoff = [0] * C.BUYER_NUM
    if len(data) == 0:  # 空のliveSend
        for p in player.group.get_players():
            if p.type == "buy":
                buyVal_list[p.player_number - 1] = p.buy_value
                bought_list[p.player_number - 1] = p.bought_number
                buyer_payoff[p.player_number - 1] = p.payoff
            if p.type == "sell":
                sold_list[p.player_number - 1] = p.sell_flg
                seller_payoff[p.player_number - 1] = p.payoff
        response = dict(
            formSyubetu="nan",
            player_number=player.player_number,
            buyVal_list=buyVal_list,
            bought_list=bought_list,
            sold_list=sold_list,
            update_good=player.group.update_good,
            update_bad=player.group.update_bad,
            seller_payoff=seller_payoff,
            buyer_payoff=buyer_payoff,
        )
        return {0: response}

    if data["type"] == "sell":  # 売り手からのlivesend
        if player.sell_flg == False:
            b_payoff = 0
            s_payoff = 0
            players = player.group.get_players()
            player.sell_flg = True
            for p in players:
                if (
                    p.type == "buy" and p.player_number == data["buyerNum"]
                ):  # この買い手に売却したということ
                    p.bought_number += 1
                    p.torihiki_num += 1
                    if player.used_status == False:
                        b_payoff = C.VALUE_BAD_BUYER - p.buy_value
                        s_payoff = p.buy_value - C.VALUE_BAD_SELLER
                        player.payoff += s_payoff
                        p.payoff += b_payoff
                        p.buyer_history += str(p.buy_value) + "-" + "悪,"
                        p.history2 += (
                            str(p.torihiki_num) + "-" + str(p.buy_value) + "-悪,"
                        )
                        player.group.update_bad -= 1
                        Transaction.create(
                            player=player,
                            seller=player,
                            buyer=p,
                            offer_price=p.buy_value,
                            tradePartner=p.id_in_group,
                            goods_status="bad",
                            seller_payoff=player.payoff,
                            buyer_payoff=p.payoff,
                            seconds=round(
                                time.time() - player.group.start_timestamp, 2
                            ),
                        )
                    else:
                        b_payoff = C.VALUE_GOOD_BUYER - p.buy_value
                        s_payoff = p.buy_value - C.VALUE_GOOD_SELLER
                        player.payoff += s_payoff
                        p.payoff += b_payoff
                        p.buyer_history += str(p.buy_value) + "-" + "良,"
                        p.history2 += (
                            str(p.torihiki_num) + "-" + str(p.buy_value) + "-良,"
                        )
                        player.group.update_good -= 1
                        Transaction.create(
                            player=player,
                            seller=player,
                            buyer=p,
                            offer_price=p.buy_value,
                            tradePartner=p.id_in_group,
                            goods_status="good",
                            seller_payoff=player.payoff,
                            buyer_payoff=p.payoff,
                            seconds=round(
                                time.time() - player.group.start_timestamp, 2
                            ),
                        )

            # listの作成
            for p in players:
                if p.type == "buy":
                    buyVal_list[p.player_number - 1] = p.buy_value
                    bought_list[p.player_number - 1] = p.bought_number
                    buyer_payoff[p.player_number - 1] = p.payoff
                if p.type == "sell":
                    sold_list[p.player_number - 1] = p.sell_flg
                    seller_payoff[p.player_number - 1] = p.payoff
            response = dict(
                formSyubetu="sell",
                seller_payoff=seller_payoff,
                buyer_payoff=buyer_payoff,
                used_status=player.used_status,
                buyer_id=data["buyerNum"],
                update_good=player.group.update_good,
                update_bad=player.group.update_bad,
                seller_id=player.player_number,
                buyVal_list=buyVal_list,
                bought_list=bought_list,
                sold_list=sold_list,
            )
            return {0: response}
    elif data["type"] == "buy":  # 買い手からのlivesend
        player.buy_value = data["value"]
        for p in player.group.get_players():
            if p.type == "buy":
                buyVal_list[p.player_number - 1] = p.buy_value
                bought_list[p.player_number - 1] = p.bought_number
                buyer_payoff[p.player_number - 1] = p.payoff
            if p.type == "sell":
                sold_list[p.player_number - 1] = p.sell_flg
                seller_payoff[p.player_number - 1] = p.payoff
        response = dict(
            formSyubetu="buy",
            player_number=player.player_number,
            buyVal_list=buyVal_list,
            bought_list=bought_list,
            sold_list=sold_list,
            seller_payoff=seller_payoff,
            buyer_payoff=buyer_payoff,
            update_good=player.group.update_good,
            update_bad=player.group.update_bad,
        )
        Transaction.create(
            player=player,
            buyer=player,
            offer_price=player.buy_value,
            seconds=round(time.time() - player.group.start_timestamp, 2),
        )

        return {0: response}


# PAGES
class Introduction(Page):
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instruction2(Page):
    timeout_seconds = 60
    form_model = "player"
    form_fields = ["instruction_q1"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instruction3(Page):
    timeout_seconds = 60
    form_model = "player"
    form_fields = ["instruction_q2"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Correct(Page):
    timeout_seconds = 20

    @staticmethod
    def vars_for_template(player: Player):
        return dict(cnt=player.in_round(1).quiz_cnt)

    def before_next_page(player: Player, timeout_happened):
        player.in_round(1).quiz_cnt += 1

    def is_displayed(player: Player):
        return player.round_number == 1


class Game(Page):
    live_method = live_bid

    @staticmethod
    def js_vars(player: Player):
        return dict(
            player_type=player.type,
            player_number=player.player_number,
            min_sell_cost=player.seller_min_cost,
            buyer_num=C.BUYER_NUM,
            players=C.BUYER_NUM,
            used_status=player.used_status,
            payoff=player.payoff,
            good_used_num=player.group.update_good,
            bad_used_num=player.group.update_bad,
        )

    def get_timeout_seconds(player: Player):
        group = player.group
        return (group.start_timestamp + 120) - time.time()


class quizwait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        init_player(group)
        group.start_timestamp = int(time.time())


class wait(WaitPage):
    pass


class Results(Page):
    timeout_seconds = 30

    @staticmethod
    def js_vars(player: Player):
        return dict(
            history=player.history2,
        )


class Last(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Room_waiting(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class quizPage1(Page):
    form_model = "player"
    form_fields = ["q1", "q2", "q3"]
    timeout_seconds = 270

    def is_displayed(player: Player):
        return player.round_number == 1


class quizResult1(Page):
    timeout_seconds = 120

    def is_displayed(player: Player):
        return player.round_number == 1


class quizPage2(Page):
    form_model = "player"
    form_fields = ["q4", "q5", "q6", "q7"]
    timeout_seconds = 270

    def is_displayed(player: Player):
        return player.round_number == 1


class quizResult2(Page):
    timeout_seconds = 120

    def is_displayed(player: Player):
        return player.round_number == 1


page_sequence = [
    # Room_waiting,
    Introduction,
    quizPage1,
    quizResult1,
    quizPage2,
    quizResult2,
    # Instruction2,
    # Correct,
    # Instruction3,
    # Correct,
    quizwait,
    Game,
    Results,
    Last,
]
