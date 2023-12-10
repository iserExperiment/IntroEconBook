from otree.api import *
import random


doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch10_2_ultimatum"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 1000
    INSTRUCTIONS_TEMPLATE = "ch10_2_ultimatum/instructions.html"
    ADD_TIME = 180

    CHOICE_LIST_SENTE = [
        [0, "あなた0ポイント、相手1000ポイント"],
        [100, "あなた100ポイント、相手900ポイント"],
        [200, "あなた200ポイント、相手800ポイント"],
        [300, "あなた300ポイント、相手700ポイント"],
        [400, "あなた400ポイント、相手600ポイント"],
        [500, "あなた500ポイント、相手500ポイント"],
        [600, "あなた600ポイント、相手400ポイント"],
        [700, "あなた700ポイント、相手300ポイント"],
        [800, "あなた800ポイント、相手200ポイント"],
        [900, "あなた900ポイント、相手100ポイント"],
        [1000, "あなた1000ポイント、相手0ポイント"],
    ]

    CHOICE_LIST_GOTE_TMP = [
        [1000, "あなたに1000ポイント"],
        [900, "あなた900ポイント"],
        [800, "あなた800ポイント"],
        [700, "あなた700ポイント"],
        [600, "あなた600ポイント"],
        [500, "あなた500ポイント"],
        [400, "あなた400ポイント"],
        [300, "あなた300ポイント"],
        [200, "あなた200ポイント"],
        [100, "あなた100ポイント"],
        [0, "あなた0ポイント"],
    ]

    CHOICE_LIST_GOTE = [[0, "承諾"], [1, "拒否"]]


class Subsession(BaseSubsession):
    num_participants_p1 = models.IntegerField(initial=0)
    num_participants_p2 = models.IntegerField(initial=0)
    num_1000 = models.IntegerField(initial=0)
    num_900 = models.IntegerField(initial=0)
    num_800 = models.IntegerField(initial=0)
    num_700 = models.IntegerField(initial=0)
    num_600 = models.IntegerField(initial=0)
    num_500 = models.IntegerField(initial=0)
    num_400 = models.IntegerField(initial=0)
    num_300 = models.IntegerField(initial=0)
    num_200 = models.IntegerField(initial=0)
    num_100 = models.IntegerField(initial=0)
    num_0 = models.IntegerField(initial=0)
    num_accept = models.IntegerField(initial=0)
    num_reject = models.IntegerField(initial=0)

    #
    num_participants = models.IntegerField(initial=0)
    num_1000_accept = models.IntegerField(initial=0)
    num_1000_reject = models.IntegerField(initial=0)
    num_900_accept = models.IntegerField(initial=0)
    num_900_reject = models.IntegerField(initial=0)
    num_800_accept = models.IntegerField(initial=0)
    num_800_reject = models.IntegerField(initial=0)
    num_700_accept = models.IntegerField(initial=0)
    num_700_reject = models.IntegerField(initial=0)
    num_600_accept = models.IntegerField(initial=0)
    num_600_reject = models.IntegerField(initial=0)
    num_500_accept = models.IntegerField(initial=0)
    num_500_reject = models.IntegerField(initial=0)
    num_400_accept = models.IntegerField(initial=0)
    num_400_reject = models.IntegerField(initial=0)
    num_300_accept = models.IntegerField(initial=0)
    num_300_reject = models.IntegerField(initial=0)
    num_200_accept = models.IntegerField(initial=0)
    num_200_reject = models.IntegerField(initial=0)
    num_100_accept = models.IntegerField(initial=0)
    num_100_reject = models.IntegerField(initial=0)
    num_0_accept = models.IntegerField(initial=0)
    num_0_reject = models.IntegerField(initial=0)

    err_message = models.StringField()
    err_message_pair = models.StringField()


class Group(BaseGroup):
    p1_amount = models.IntegerField()
    p2_amount = models.IntegerField()

    p1_decision = models.StringField(
        choices=C.CHOICE_LIST_SENTE, widget=widgets.RadioSelect, label=""
    )

    p2_decision = models.StringField(
        choices=C.CHOICE_LIST_GOTE, widget=widgets.RadioSelect, label=""
    )

    p1_decision_why = models.LongStringField(label="なぜその選択をしましたか？")

    p2_decision_why = models.LongStringField(label="なぜその選択をしましたか？")

    flg_non_input_p1 = models.IntegerField(initial=0)
    flg_non_input_p2 = models.IntegerField(initial=0)


class Player(BasePlayer):
    # 戦略法
    tmp_first_player = models.StringField(
        choices=C.CHOICE_LIST_SENTE, widget=widgets.RadioSelect, label=""
    )
    tmp_first_player_why = models.LongStringField(label="なぜその選択をしましたか？")

    tmp_second_player = models.StringField(
        choices=C.CHOICE_LIST_GOTE_TMP, widget=widgets.RadioSelect, label=""
    )
    tmp_second_player_why = models.LongStringField(label="なぜその選択をしましたか？")


# FUNCTIONS
def set_P1(player: Player):
    sub = player.subsession
    group = player.group

    if group.p1_decision != "":
        sub.num_participants_p1 += 1
        print("++++++++++++++++", group.p1_decision)
        s = group.p1_decision
        if s == "1000":
            sub.num_1000 += 1
        elif s == "900":
            sub.num_900 += 1
        elif s == "800":
            sub.num_800 += 1
        elif s == "700":
            sub.num_700 += 1
        elif s == "600":
            sub.num_600 += 1
        elif s == "500":
            sub.num_500 += 1
        elif s == "400":
            sub.num_400 += 1
        elif s == "300":
            sub.num_300 += 1
        elif s == "200":
            sub.num_200 += 1
        elif s == "100":
            sub.num_100 += 1
        elif s == "0":
            sub.num_0 += 1
        else:
            sub.err_message = "エラーあり"
    else:
        group.flg_non_input_p1 = 1
        tmp = random.randint(0, 10)
        group.p1_decision = str(C.CHOICE_LIST_SENTE[tmp][0])
    # 先手の配分計算
    # group.p1_amount = C.ENDOWMENT - int(group.p1_decision)
    group.p1_amount = int(group.p1_decision)
    group.p2_amount = C.ENDOWMENT - int(group.p1_decision)


def set_P2(player: Player):
    sub = player.subsession
    group = player.group
    s = group.p2_decision
    if s != "":
        # グラフ用集計
        sub.num_participants_p2 += 1
        if s == "0":
            sub.num_accept += 1
        elif s == "1":
            sub.num_reject += 1
        else:
            sub.err_message = "エラーあり"
    else:
        group.flg_non_input_p2 = 1
        tmp = random.randint(0, 1)
        group.p2_decision = str(C.CHOICE_LIST_GOTE[tmp][0])


def set_pair(player: Player):
    sub = player.subsession
    group = player.group
    p1 = group.p1_decision
    p2 = group.p2_decision

    sub.num_participants += 1

    if p1 == "1000" and p2 == "0":
        sub.num_1000_accept += 1
    elif p1 == "1000" and p2 == "1":
        sub.num_1000_reject += 1
    elif p1 == "900" and p2 == "0":
        sub.num_900_accept += 1
    elif p1 == "900" and p2 == "1":
        sub.num_900_reject += 1
    elif p1 == "800" and p2 == "0":
        sub.num_800_accept += 1
    elif p1 == "800" and p2 == "1":
        sub.num_800_reject += 1
    elif p1 == "700" and p2 == "0":
        sub.num_700_accept += 1
    elif p1 == "700" and p2 == "1":
        sub.num_700_reject += 1
    elif p1 == "600" and p2 == "0":
        sub.num_600_accept += 1
    elif p1 == "600" and p2 == "1":
        sub.num_600_reject += 1
    elif p1 == "500" and p2 == "0":
        sub.num_500_accept += 1
    elif p1 == "500" and p2 == "1":
        sub.num_500_reject += 1
    elif p1 == "400" and p2 == "0":
        sub.num_400_accept += 1
    elif p1 == "400" and p2 == "1":
        sub.num_400_reject += 1
    elif p1 == "300" and p2 == "0":
        sub.num_300_accept += 1
    elif p1 == "300" and p2 == "1":
        sub.num_300_reject += 1
    elif p1 == "200" and p2 == "0":
        sub.num_200_accept += 1
    elif p1 == "200" and p2 == "1":
        sub.num_200_reject += 1
    elif p1 == "100" and p2 == "0":
        sub.num_100_accept += 1
    elif p1 == "100" and p2 == "1":
        sub.num_100_reject += 1
    elif p1 == "0" and p2 == "0":
        sub.num_0_accept += 1
    elif p1 == "0" and p2 == "1":
        sub.num_0_reject += 1
    else:
        sub.err_message_pair = "エラーあり"


def set_P2s(subsession: Subsession):
    for p in subsession.get_players():
        set_P2(p)


def set_P1s(subsession: Subsession):
    for p in subsession.get_players():
        set_P1(p)


def set_pairs(subsession: Subsession):
    for p in subsession.get_players():
        set_pair(p)
    graph(subsession=subsession)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    # 0：承諾
    if group.p2_decision == "0":
        # p1.payoff = C.ENDOWMENT - int(group.p1_decision)
        # p2.payoff = int(group.p1_decision)
        p1.payoff = int(group.p1_decision)
        p2.payoff = C.ENDOWMENT - int(group.p1_decision)
    # 1：拒否
    else:
        p1.payoff = 0
        p2.payoff = 0


# グラフ描画用
def graph(subsession: Subsession):
    sub = subsession
    session = sub.session
    graph_list_accept = []
    graph_list_reject = []

    ch10_2_result = []

    # 割合に計算(accept)
    if sub.num_0_reject > 0:
        tmp = round((sub.num_0_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_100_reject > 0:
        tmp = round((sub.num_100_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_200_reject > 0:
        tmp = round((sub.num_200_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_300_reject > 0:
        tmp = round((sub.num_300_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_400_reject > 0:
        tmp = round((sub.num_400_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_500_reject > 0:
        tmp = round((sub.num_500_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_600_reject > 0:
        tmp = round((sub.num_600_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_700_reject > 0:
        tmp = round((sub.num_700_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_800_reject > 0:
        tmp = round((sub.num_800_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_900_reject > 0:
        tmp = round((sub.num_900_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)
    if sub.num_1000_reject > 0:
        tmp = round((sub.num_1000_reject / sub.num_participants) * 100, 2)
        graph_list_reject.append(tmp)
    else:
        graph_list_reject.append(0)

    # accept
    if sub.num_0_accept > 0:
        tmp = round((sub.num_0_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_100_accept > 0:
        tmp = round((sub.num_100_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_200_accept > 0:
        tmp = round((sub.num_200_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_300_accept > 0:
        tmp = round((sub.num_300_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_400_accept > 0:
        tmp = round((sub.num_400_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_500_accept > 0:
        tmp = round((sub.num_500_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_600_accept > 0:
        tmp = round((sub.num_600_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_700_accept > 0:
        tmp = round((sub.num_700_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_800_accept > 0:
        tmp = round((sub.num_800_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_900_accept > 0:
        tmp = round((sub.num_900_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)
    if sub.num_1000_accept > 0:
        tmp = round((sub.num_1000_accept / sub.num_participants) * 100, 2)
        graph_list_accept.append(tmp)
    else:
        graph_list_accept.append(0)

    print(graph_list_accept, graph_list_reject)

    for player in subsession.get_players():
        group = player.group
        participant = player.participant

        p2_decision = ""
        if group.p2_decision == "0":
            p2_decision = "承諾"
        else:
            p2_decision = "拒否"

        participant.vars["ch10_2_result"] = (
            "++++++++++++++++++++++++++++++++++++++++++++++++++<br>"
            "最後通牒ゲーム：あなたの結果："
            "プレイヤー1（先手）は、プレイヤー1に"
            + str(group.p1_amount)
            + "ポイント、プレイヤー2に"
            + str(group.p2_amount)
            + "という提案をしました。<br>"
            "プレイヤー2（後手）は、プレイヤー1の提案を" + (p2_decision) + "しました。<br>"
            "++++++++++++++++++++++++++++++++++++++++++++++++++"
        )

    ch10_2_result.append(participant.vars["ch10_2_result"])

    # 最終結果用
    if "graph_data" not in session.vars:
        session.graph_data = {}
    session.graph_data["ch10_2"] = {
        "num_participants": sub.num_participants,
        "graph_list_accept": graph_list_accept,
        "graph_list_reject": graph_list_reject,
        "ch10_2_result": ch10_2_result,
    }


# PAGES-----
class Introduction(Page):
    timeout_seconds = 60


class Strategy(Page):
    timeout_seconds = 120 + C.ADD_TIME
    form_model = "player"
    form_fields = [
        "tmp_first_player",
        "tmp_first_player_why",
        "tmp_second_player",
        "tmp_second_player_why",
    ]


class Send(Page):
    # timeout_seconds = 60
    timeout_seconds = C.ADD_TIME
    form_model = "group"
    form_fields = ["p1_decision", "p1_decision_why"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P1s


class SendBack(Page):
    # timeout_seconds = 60
    timeout_seconds = C.ADD_TIME
    form_model = "group"
    form_fields = ["p2_decision", "p2_decision_why"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class WaitForP2(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P2s


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class ResultWaitPair(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_pairs


class Results(Page):
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        return player.session.graph_data


page_sequence = [
    Introduction,
    Strategy,
    Send,
    WaitForP1,
    SendBack,
    WaitForP2,
    ResultsWaitPage,
    ResultWaitPair,
    Results,
]
