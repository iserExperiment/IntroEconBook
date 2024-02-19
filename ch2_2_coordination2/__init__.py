from otree.api import *
import random

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch2_2_coordination2"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = "ch2_2_coordination2/instructions.html"
    PAYOFF_A = cu(85)
    PAYOFF_B = cu(30)
    PAYOFF_C = cu(65)
    PAYOFF_D = cu(45)
    PAYOFF_E = cu(100)
    PAYOFF_F = cu(50)

    choice_list = ["A", "B"]


class Subsession(BaseSubsession):
    num_participants_p1 = models.IntegerField(initial=0)
    num_A_p1 = models.IntegerField(initial=0)
    num_B_p1 = models.IntegerField(initial=0)

    num_participants_p2 = models.IntegerField(initial=0)
    num_A_p2 = models.IntegerField(initial=0)
    num_B_p2 = models.IntegerField(initial=0)

    err_message = models.StringField()

    pair_num = models.IntegerField(initial=0)
    pair_num_AA = models.IntegerField(initial=0)
    pair_num_AB = models.IntegerField(initial=0)
    pair_num_BA = models.IntegerField(initial=0)
    pair_num_BB = models.IntegerField(initial=0)
    pair_err_message = models.StringField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    flg_non_input = models.IntegerField(initial=0)
    flg_pair_non_input = models.IntegerField(initial=0)

    individual_choice = models.StringField(
        choices=[["A", "A"], ["B", "B"]],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    # 相手のグループID
    pair_id = models.IntegerField(initial=0)
    # 相手の意思決定
    pair_choice = models.StringField()

    # 意思決定の理由
    individual_choice_comment = models.LongStringField(verbose_name="", initial="")

    q1 = models.StringField(
        # widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["UL", "プレイヤー1がU,プレイヤー2がL"],
            ["UR", "プレイヤー1がU,プレイヤー2がR"],
            ["DL", "プレイヤー1がD,プレイヤー2がL"],
            ["DR", "プレイヤー1がD,プレイヤー2がR"],
        ],
    )
    q2 = models.StringField(
        # widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["UL", "プレイヤー1がU,プレイヤー2がL"],
            ["UR", "プレイヤー1がU,プレイヤー2がR"],
            ["DL", "プレイヤー1がD,プレイヤー2がL"],
            ["DR", "プレイヤー1がD,プレイヤー2がR"],
        ],
    )
    q3 = models.StringField(
        # widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["UL", "プレイヤー1がU,プレイヤー2がL"],
            ["UR", "プレイヤー1がU,プレイヤー2がR"],
            ["DL", "プレイヤー1がD,プレイヤー2がL"],
            ["DR", "プレイヤー1がD,プレイヤー2がR"],
        ],
    )


# FUNCTIONS
def keisan(player: Player):
    sub = player.subsession
    group = player.group

    if player.id_in_group == 1:
        if player.individual_choice != "":
            sub.num_participants_p1 += 1
            s = player.individual_choice
            if s == "A":
                sub.num_A_p1 += 1
            elif s == "B":
                sub.num_B_p1 += 1
            else:
                sub.err_message = "エラーあり"
        else:
            player.flg_non_input = 1
            player.individual_choice = random.choice(C.choice_list)
    else:
        if player.individual_choice != "":
            sub.num_participants_p2 += 1
            s = player.individual_choice
            if s == "A":
                sub.num_A_p2 += 1
            elif s == "B":
                sub.num_B_p2 += 1
            else:
                sub.err_message = "エラーあり"
        else:
            player.flg_non_input = 1
            player.individual_choice = random.choice(C.choice_list)


def keisans(subsession: Subsession):
    for p in subsession.get_players():
        keisan(p)


def set_graph(subsession: Subsession):
    for p in subsession.get_players():
        graph_pair(p)


def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)


def other_player(player: Player):
    return player.get_others_in_group()[0]


def graph_pair(player: Player):
    sub = player.subsession
    sub.pair_num += 1
    # グラフ用集計
    s = player.individual_choice
    sp = player.pair_choice
    print("graph_____プレイヤー1,プレイヤー2________________", s, sp)
    if player.id_in_group == 1:
        if (s == "A") and (sp == "A"):
            print("graph1_____________________AA", s, sp)
            sub.pair_num_AA += 1
        elif (s == "A") and (sp == "B"):
            print("graph1_____________________AB", s, sp)
            sub.pair_num_AB += 1
        elif (s == "B") and (sp == "A"):
            print("graph1_____________________BA", s, sp)
            sub.pair_num_BA += 1
        elif (s == "B") and (sp == "B"):
            print("graph1_____________________BB", s, sp)
            sub.pair_num_BB += 1
        else:
            sub.pair_err_message = "エラーあり"
    # else:
    #    if (sp == "A")and(s == "A"):
    #        print("graph_2____________________AA", s, sp)
    #        sub.pair_num_AA += 1
    #    elif (sp == "A")and(s == "B"):
    #        print("graph_2____________________AB", s, sp)
    #        sub.pair_num_AB += 1
    #    elif (sp == "B") and (s == "A"):
    #        print("graph_2____________________BA", s, sp)
    #        sub.pair_num_BA += 1
    #    elif (sp == "B") and (s == "B"):
    #        print("graph_2____________________BB", s, sp)
    #        sub.pair_num_BB += 1
    #    else:
    #        sub.pair_err_message = "エラーあり"


def set_payoff(player: Player):
    payoff_matrix_p1 = {
        ("A", "A"): C.PAYOFF_A,
        ("A", "B"): C.PAYOFF_A,
        ("B", "A"): C.PAYOFF_C,
        ("B", "B"): C.PAYOFF_E,
    }
    payoff_matrix_p2 = {
        ("A", "A"): C.PAYOFF_B,
        ("A", "B"): C.PAYOFF_B,
        ("B", "A"): C.PAYOFF_D,
        ("B", "B"): C.PAYOFF_F,
    }
    other = other_player(player)
    player.pair_choice = other.individual_choice
    player.pair_id = other.id_in_group
    if other.flg_non_input == 1:
        player.flg_pair_non_input = 1

    print(player.individual_choice, other.individual_choice)
    if player.id_in_group == 1:
        player.payoff = payoff_matrix_p1[
            (player.individual_choice, other.individual_choice)
        ]
    else:
        player.payoff = payoff_matrix_p2[
            (other.individual_choice, player.individual_choice)
        ]
    print(player.id_in_group, player.payoff)


# PAGES-----
class Introduction(Page):
    timeout_seconds = 100


class Decision(Page):
    form_model = "player"
    form_fields = ["individual_choice", "individual_choice_comment"]


class Question(Page):
    form_model = "player"
    form_fields = ["q1", "q2", "q3"]


class keisanWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = keisans


class GraphWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_graph


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)

        print(
            player.id_in_group,
            "*************************************",
            player.individual_choice,
            opponent.individual_choice,
        )
        if player.id_in_group == 1:
            if player.individual_choice == "A":
                disp_my_decision = "U"
            else:
                disp_my_decision = "D"
            if opponent.individual_choice == "A":
                disp_opponent_decision = "L"
            else:
                disp_opponent_decision = "R"
        else:
            if player.individual_choice == "A":
                disp_my_decision = "L"
            else:
                disp_my_decision = "R"
            if opponent.individual_choice == "A":
                disp_opponent_decision = "U"
            else:
                disp_opponent_decision = "D"

        print(disp_my_decision)
        return dict(
            opponent=opponent,
            same_choice=player.individual_choice == opponent.individual_choice,
            # my_decision=player.field_display('individual_choice'),
            my_decision=disp_my_decision,
            opponent_decision=disp_opponent_decision,
            # opponent_decision=opponent.field_display('individual_choice'),
        )

    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        sub = player.subsession
        print("js_vars", sub.num_A_p1)
        # 割合に計算
        if sub.num_A_p1 > 0:
            prop_num_A_p1 = round((sub.num_A_p1 / sub.num_participants_p1) * 100, 2)
        else:
            prop_num_A_p1 = 0
        if sub.num_B_p1 > 0:
            prop_num_B_p1 = round((sub.num_B_p1 / sub.num_participants_p1) * 100, 2)
        else:
            prop_num_B_p1 = 0

        print(prop_num_A_p1, ";;;;;;;;;;;;;;;;;;;;;")
        # 割合に計算
        if sub.num_A_p2 > 0:
            prop_num_A_p2 = round((sub.num_A_p2 / sub.num_participants_p2) * 100, 2)
        else:
            prop_num_A_p2 = 0
        if sub.num_B_p2 > 0:
            prop_num_B_p2 = round((sub.num_B_p2 / sub.num_participants_p2) * 100, 2)
        else:
            prop_num_B_p2 = 0

        print("ここから追加")
        # 割合に計算s

        pair_num = sub.pair_num / 2#ここまで計算されたsub.pair_numはpairの数ではなくて、参加人数になっちゃた。その原因はまだわからなくて、一応sub.pair_numを２で割ってpair数にした
        
        if sub.pair_num_AA > 0:
            prop_pair_num_AA = round((sub.pair_num_AA / pair_num) * 100, 2)
        else:
            prop_pair_num_AA = 0

        if sub.pair_num_AB > 0:
            prop_pair_num_AB = round((sub.pair_num_AB / pair_num) * 100, 2)
        else:
            prop_pair_num_AB = 0

        if sub.pair_num_BA > 0:
            prop_pair_num_BA = round((sub.pair_num_BA / pair_num) * 100, 2)
        else:
            prop_pair_num_BA = 0

        if sub.pair_num_BB > 0:
            prop_pair_num_BB = round((sub.pair_num_BB / pair_num) * 100, 2)
        else:
            prop_pair_num_BB = 0

        return dict(
            num_participants_p1=sub.num_participants_p1,
            num_participants_p2=sub.num_participants_p2,
            num_A_p1=prop_num_A_p1,
            num_B_p1=prop_num_B_p1,
            num_A_p2=prop_num_A_p2,
            num_B_p2=prop_num_B_p2,
            num_pairs=sub.pair_num,
            num_AA=prop_pair_num_AA,
            num_AB=prop_pair_num_AB,
            num_BA=prop_pair_num_BA,
            num_BB=prop_pair_num_BB,
        )


class PreResults(Page):
    pass


page_sequence = [
    Introduction,
    Decision,
    Question,
    keisanWaitPage,
    ResultsWaitPage,
    GraphWaitPage,
    PreResults,
    Results,
]
