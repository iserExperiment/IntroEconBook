from otree.api import *
import random
import re

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch10_4_extended_dictator"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 500
    INSTRUCTIONS_TEMPLATE = "ch10_4_extended_dictator/instructions.html"
    ADD_TIME = 180

    CHOICE_LIST_SENTE = [
        ["0", "何もしない"],
        ["u100", "100ポイント奪う"],
        ["u200", "200ポイント奪う"],
        ["u300", "300ポイント奪う"],
        ["u400", "400ポイント奪う"],
        ["u500", "500ポイント奪う"],
        ["a100", "100ポイント与える"],
        ["a200", "200ポイント与える"],
        ["a300", "300ポイント与える"],
        ["a400", "400ポイント与える"],
        ["a500", "500ポイント与える"],
    ]


class Subsession(BaseSubsession):
    num_participants_p1 = models.IntegerField(initial=0)
    num_participants_p2 = models.IntegerField(initial=0)
    num_0 = models.IntegerField(initial=0)
    num_u100 = models.IntegerField(initial=0)
    num_u200 = models.IntegerField(initial=0)
    num_u300 = models.IntegerField(initial=0)
    num_u400 = models.IntegerField(initial=0)
    num_u500 = models.IntegerField(initial=0)

    num_a100 = models.IntegerField(initial=0)
    num_a200 = models.IntegerField(initial=0)
    num_a300 = models.IntegerField(initial=0)
    num_a400 = models.IntegerField(initial=0)
    num_a500 = models.IntegerField(initial=0)

    num_participants = models.IntegerField(initial=0)

    err_message = models.StringField()
    err_message_pair = models.StringField()


class Group(BaseGroup):
    p1_amount = models.IntegerField()
    p2_amount = models.IntegerField()

    p1_decision = models.StringField(
        choices=C.CHOICE_LIST_SENTE, widget=widgets.RadioSelect, label=""
    )
    p1_decision_why = models.LongStringField(label="なぜその選択をしましたか？")

    flg_non_input_p1 = models.IntegerField(initial=0)


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_P1(player: Player):
    sub = player.subsession
    group = player.group

    sub.num_participants += 1
    if group.p1_decision != "":
        sub.num_participants_p1 += 1
        print("++++++++++++++++", group.p1_decision)
        s = group.p1_decision
        if s == "0":
            sub.num_0 += 1
        elif s == "u100":
            sub.num_u100 += 1
        elif s == "u200":
            sub.num_u200 += 1
        elif s == "u300":
            sub.num_u300 += 1
        elif s == "u400":
            sub.num_u400 += 1
        elif s == "u500":
            sub.num_u500 += 1
        elif s == "a100":
            sub.num_a100 += 1
        elif s == "a200":
            sub.num_a200 += 1
        elif s == "a300":
            sub.num_a300 += 1
        elif s == "a400":
            sub.num_a400 += 1
        elif s == "a500":
            sub.num_a500 += 1
        else:
            sub.err_message = "エラーあり"
    else:
        group.flg_non_input_p1 = 1
        tmp = random.randint(0, 10)
        group.p1_decision = str(C.CHOICE_LIST_SENTE[tmp][0])
        s = group.p1_decision
    # 配分計算
    suuji = re.sub(r"\D", "", s)
    print(";;;;;;;;;;;;;", suuji, s)
    if "u" in s:
        group.p1_amount = C.ENDOWMENT + int(suuji)
        group.p2_amount = C.ENDOWMENT - int(suuji)
    elif "a" in s:
        group.p1_amount = C.ENDOWMENT - int(suuji)
        group.p2_amount = C.ENDOWMENT + int(suuji)
    elif s == "0":
        group.p1_amount = C.ENDOWMENT
        group.p2_amount = C.ENDOWMENT
    else:
        sub.err_message = "エラーあり_配分計算"


def set_P1s(subsession: Subsession):
    for p in subsession.get_players():
        set_P1(p)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    # p1.payoff = C.ENDOWMENT - int(group.p1_decision)
    # p2.payoff = int(group.p1_decision)
    p1.payoff = group.p1_amount
    p2.payoff = group.p2_amount


# PAGES-----
class Introduction(Page):
    timeout_seconds = 60


class Send(Page):
    # timeout_seconds = 60+C.ADD_TIME
    timeout_seconds = C.ADD_TIME
    form_model = "group"
    form_fields = ["p1_decision", "p1_decision_why"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P1s


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        sub = player.subsession
        graph_list = []
        graph_name_list = []

        ch10_4_result = []

        # 割合に計算(accept)
        if sub.num_0 > 0:
            tmp = round((sub.num_0 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("なにもしない")
        # 奪う----------------------------------------
        if sub.num_u100 > 0:
            tmp = round((sub.num_u100 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("100ポイント奪う")
        if sub.num_u200 > 0:
            tmp = round((sub.num_u200 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("200ポイント奪う")
        if sub.num_u300 > 0:
            tmp = round((sub.num_u300 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("300ポイント奪う")
        if sub.num_u400 > 0:
            tmp = round((sub.num_u400 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("400ポイント奪う")
        if sub.num_u500 > 0:
            tmp = round((sub.num_u500 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("500ポイント奪う")

        # 与える----------------------------------------
        if sub.num_a100 > 0:
            tmp = round((sub.num_a100 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("100ポイント与える")
        if sub.num_a200 > 0:
            tmp = round((sub.num_a200 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("200ポイント与える")
        if sub.num_a300 > 0:
            tmp = round((sub.num_a300 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("300ポイント与える")
        if sub.num_a400 > 0:
            tmp = round((sub.num_a400 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("400ポイント与える")
        if sub.num_a500 > 0:
            tmp = round((sub.num_a500 / sub.num_participants) * 100, 2)
            graph_list.append(tmp)
        else:
            graph_list.append(0)
        graph_name_list.append("500ポイント与える")

        print("グラフリスト", graph_list, graph_name_list, type(graph_name_list))

        group = player.group
        participant = player.participant

        p1_decision = ""
        if group.p1_decision == "u100":
            p1_decision = "100ポイント奪う"
        elif group.p1_decision == "u200":
            p1_decision = "200ポイント奪う"
        elif group.p1_decision == "u300":
            p1_decision = "300ポイント奪う"
        elif group.p1_decision == "u400":
            p1_decision = "400ポイント奪う"
        elif group.p1_decision == "u500":
            p1_decision = "500ポイント奪う"
        elif group.p1_decision == "a100":
            p1_decision = "100ポイント与える"
        elif group.p1_decision == "a200":
            p1_decision = "200ポイント与える"
        elif group.p1_decision == "a300":
            p1_decision = "300ポイント与える"
        elif group.p1_decision == "a400":
            p1_decision = "400ポイント与える"
        elif group.p1_decision == "a500":
            p1_decision = "500ポイント与える"
        else:
            p1_decision = "なにもしない"

        participant.vars["ch10_4_result"] = (
            "++++++++++++++++++++++++++++++++++++++++++++++++++<br>"
            "[直接法]最後通牒ゲーム：あなたの結果："
            "プレイヤー1（先手）は、" + p1_decision + "という提案をしました。<br>"
            "プレイヤー2（後手）は、プレイヤー1の提案をそのまま受け入れます。<br>"
            "++++++++++++++++++++++++++++++++++++++++++++++++++"
        )

        ch10_4_result.append(participant.vars["ch10_4_result"])

        if "graph_data" not in player.session.vars:
            player.session.graph_data = {}
        player.session.graph_data["ch10_4"] = {
            "num_participants": sub.num_participants,
            "graph_list": graph_list,
            "graph_name_list": graph_name_list,
            "ch10_4_result": ch10_4_result,
        }
        print("graph_data")
        print(sub.session.graph_data)
        return player.session.graph_data


page_sequence = [Introduction, Send, WaitForP1, ResultsWaitPage, Results]
