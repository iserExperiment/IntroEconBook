from otree.api import *
import time

c = Currency  # old name for currency; you can delete this.


class Constants(BaseConstants):
    name_in_url = "ch1_1_risk"
    players_per_group = None
    num_rounds = 1
    Q_num = 5
    categories = (["Aが1つ", "Aが2つ", "Aが3つ", "Aが4つ", "Aが5つ"],)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 1：Decision_1
    risk_List = models.StringField(initial="")
    individual_choice_r_comment = models.StringField(initial="", label="")
    List_A = models.LongStringField(initial="")
    List_B = models.LongStringField(initial="")
    num_A = models.IntegerField()
    multiple_switch = models.BooleanField()

    start = models.FloatField(initial=0.0)
    read_time = models.LongStringField(initial="0")
    time = models.LongStringField(initial="0")

    # Decision_2
    individual_choice = models.StringField(initial="", label="")
    individual_choice_comment = models.StringField(initial="", label="")

    # Decision_3
    u_individual_choice = models.StringField(
        widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["A", "Aをえらぶ"],
            ["B", "Bをえらぶ"],
        ],
    )

    individual_choice_u_comment = models.StringField(initial="", label="")

    # Decision_4
    s_individual_choice = models.StringField(
        widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["A", "Aをえらぶ"],
            ["B", "Bをえらぶ"],
        ],
    )

    individual_choice_s_comment = models.StringField(initial="", label="")

    # Decision_5
    e_individual_choice = models.StringField(
        widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["A", "Aをえらぶ"],
            ["B", "Bをえらぶ"],
        ],
    )
    individual_choice_e_comment = models.StringField(initial="", label="")


# PAGES-----
class Decision(Page):
    form_model = "player"
    form_fields = ["individual_choice_r_comment"]

    #  html to サーバー
    @staticmethod
    def live_method(player: Player, data):
        if data["first"] == 1:
            player.time = str(time.time() - player.start)
            player.risk_List = "A" * len(data["A"]) + "B" * len(data["B"])
            player.multiple_switch = 0
            player.num_A = player.risk_List.count("A")
        else:
            player.time = str(time.time() - player.start)
            risklist = player.risk_List
            if data["select_type"] == "A":
                player.risk_List = (
                    risklist[: int(data["position_num"]) - 1]
                    + "A"
                    + risklist[int(data["position_num"]) :]
                )
            else:
                player.risk_List = (
                    risklist[: int(data["position_num"]) - 1]
                    + "B"
                    + risklist[int(data["position_num"]) :]
                )
            player.num_A = player.risk_List.count("A")
            player.multiple_switch = "B" in player.risk_List[: player.num_A]

    # @staticmethod
    # def before_next_page(self, timeout_happened):
    #    self.participant.vars['MPL_result'] = self.MPL_List


class Decision_2(Page):
    form_model = "player"
    form_fields = ["individual_choice", "individual_choice_comment"]


class Decision_3(Page):
    form_model = "player"
    form_fields = ["u_individual_choice", "individual_choice_u_comment"]


class Decision_4(Page):
    form_model = "player"
    form_fields = ["s_individual_choice", "individual_choice_s_comment"]


class Decision_5(Page):
    form_model = "player"
    form_fields = ["e_individual_choice", "individual_choice_e_comment"]


class Results(Page):
    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        group = player.group
        players = group.get_players()
        # 参加者-----
        num_participants = 0
        # リスクグラフ-----
        r_count_A0 = 0
        r_count_A1 = 0
        r_count_A2 = 0
        r_count_A3 = 0
        r_count_A4 = 0
        r_count_A5 = 0

        for p in players:
            r = p.risk_List
            if r != "":
                num_participants += 1
                r_count_A = r.count("A")
                if r_count_A == 0:
                    r_count_A0 += 1
                elif r_count_A == 1:
                    r_count_A1 += 1
                elif r_count_A == 2:
                    r_count_A2 += 1
                elif r_count_A == 3:
                    r_count_A3 += 1
                elif r_count_A == 4:
                    r_count_A4 += 1
                elif r_count_A == 5:
                    r_count_A5 += 1

        print(
            num_participants,
            r_count_A0,
            r_count_A1,
            r_count_A2,
            r_count_A3,
            r_count_A4,
            r_count_A5,
        )
        print("追加：割合に計算")
        if r_count_A0 > 0:
            prop_num_A0 = round((r_count_A0 / num_participants) * 100, 2)
        else:
            prop_num_A0 = 0
        if r_count_A1 > 0:
            prop_num_A1 = round((r_count_A1 / num_participants) * 100, 2)
        else:
            prop_num_A1 = 0
        if r_count_A2 > 0:
            prop_num_A2 = round((r_count_A2 / num_participants) * 100, 2)
        else:
            prop_num_A2 = 0
        if r_count_A3 > 0:
            prop_num_A3 = round((r_count_A3 / num_participants) * 100, 2)
        else:
            prop_num_A3 = 0
        if r_count_A4 > 0:
            prop_num_A4 = round((r_count_A4 / num_participants) * 100, 2)
        else:
            prop_num_A4 = 0
        if r_count_A5 > 0:
            prop_num_A5 = round((r_count_A5 / num_participants) * 100, 2)
        else:
            prop_num_A5 = 0

        # Decision_2:-----
        num_participants_c = 0
        sum_decision = 0
        average_decision = 0
        for p in players:
            c = p.individual_choice
            print("CCCCCCCCCCCCCCCCCCCC", c)
            if c != "":
                num_participants_c += 1
                sum_decision = sum_decision + int(c)

        if sum_decision > 0:
            average_decision = round(sum_decision / num_participants_c, 2)
        else:
            average_decision = 0

        # Decision_3:不確実性の質問グラフ-----
        print("Decision_3:不確実性の質問グラフ")
        num_participants_u = 0
        u_count_A = 0
        u_count_B = 0
        for p in players:
            u = p.u_individual_choice
            if u != "":
                num_participants_u += 1
                if u == "A":
                    u_count_A += 1
                elif u == "B":
                    u_count_B += 1

        u_prop_num_A, u_prop_num_B = keiosan_ratio(
            u_count_A, u_count_B, num_participants_u
        )
        print("Decision_3:不確実性の質問グラフー", u_prop_num_A, u_prop_num_B)

        # Decision_4:10倍の質問グラフ-----
        num_participants_s = 0
        s_count_A = 0
        s_count_B = 0
        for p in players:
            s = p.s_individual_choice
            if s != "":
                num_participants_s += 1
                if s == "A":
                    s_count_A += 1
                elif s == "B":
                    s_count_B += 1

        s_prop_num_A, s_prop_num_B = keiosan_ratio(
            s_count_A, s_count_B, num_participants_s
        )

        # 期待値が高い質問グラフ-----
        num_participants_e = 0
        e_count_A = 0
        e_count_B = 0
        for p in players:
            e = p.e_individual_choice
            if e != "":
                num_participants_e += 1
                if e == "A":
                    e_count_A += 1
                elif e == "B":
                    e_count_B += 1

        e_prop_num_A, e_prop_num_B = keiosan_ratio(
            e_count_A, e_count_B, num_participants_e
        )

        return dict(
            name_of_categories=Constants.categories,
            num_participants=num_participants,
            num_A0=prop_num_A0,  # r_count_A0,
            num_A1=prop_num_A1,  # r_count_A1,
            num_A2=prop_num_A2,  # r_count_A2,
            num_A3=prop_num_A3,  # r_count_A3,
            num_A4=prop_num_A4,  # r_count_A4,
            num_A5=prop_num_A5,  # r_count_A5,
            num_participants_c=num_participants_c,
            average_decision=average_decision,
            num_participants_u=num_participants_u,
            u_numA=u_prop_num_A,
            u_numB=u_prop_num_B,
            num_participants_s=num_participants_s,
            s_numA=s_prop_num_A,
            s_numB=s_prop_num_B,
            num_participants_e=num_participants_e,
            e_numA=e_prop_num_A,
            e_numB=e_prop_num_B,
        )


def keiosan_ratio(num_A, num_B, num_participants):
    # 割合に計算
    if num_A > 0:
        prop_num_A = round((num_A / num_participants) * 100, 2)
    else:
        prop_num_A = 0
    if num_B > 0:
        prop_num_B = round((num_B / num_participants) * 100, 2)
    else:
        prop_num_B = 0
    # print(prop_num_A, prop_num_B)
    return prop_num_A, prop_num_B


class ResultsWaitPage(WaitPage):
    pass


class PreResults(Page):
    pass


page_sequence = [
    Decision,
    # Decision_2,
    Decision_3,
    Decision_4,
    Decision_5,
    ResultsWaitPage,
    PreResults,
    Results,
]
