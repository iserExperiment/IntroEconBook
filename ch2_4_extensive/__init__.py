from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ch2_4_extensive'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'ch2_4_extensive/instructions.html'

    CHOICE_LABEL_1 = "キャンパスA"
    CHOICE_LABEL_2 = "キャンパスB"

    PAYOFF_A = cu(20)
    PAYOFF_B = cu(-10)
    PAYOFF_C = cu(10)
    PAYOFF_D = cu(30)

    choice_list = ["A", "B"]

    CHOICE_LIST_SENTE = [
        ["A", CHOICE_LABEL_1],
        ["B", CHOICE_LABEL_2]
    ]

    CHOICE_LIST_GOTE = [
        ["A", CHOICE_LABEL_1],
        ["B", CHOICE_LABEL_2]
    ]


class Subsession(BaseSubsession):
    num_participants_p1 = models.IntegerField(initial=0)
    num_A_p1 = models.IntegerField(initial=0)
    num_B_p1 = models.IntegerField(initial=0)

    num_participants_p2 = models.IntegerField(initial=0)
    num_A_p2 = models.IntegerField(initial=0)
    num_B_p2 = models.IntegerField(initial=0)

    pair_num = models.IntegerField(initial=0)
    pair_num_AA = models.IntegerField(initial=0)
    pair_num_AB = models.IntegerField(initial=0)
    pair_num_BA = models.IntegerField(initial=0)
    pair_num_BB = models.IntegerField(initial=0)
    pair_err_message = models.StringField()

class Group(BaseGroup):
    flg_non_input_p1 = models.IntegerField(initial=0)
    flg_non_input_p2 = models.IntegerField(initial=0)

    p1_decision = models.StringField(
        choices=C.CHOICE_LIST_SENTE,
        widget=widgets.RadioSelect,
        label=""
    )

    # 意思決定の理由
    p1_individual_choice_comment  = models.LongStringField(
        verbose_name='',
        initial=""
    )

    p2_decision = models.StringField(
        choices=C.CHOICE_LIST_GOTE,
        widget=widgets.RadioSelect,
        label=""
    )

    # 意思決定の理由
    p2_individual_choice_comment  = models.LongStringField(
        verbose_name='',
        initial=""
    )



class Player(BasePlayer):
    pass

# FUNCTIONS-------------------------
def set_P1(player: Player):
    if player.id_in_group == 1:
        sub = player.subsession
        group = player.group

        if group.p1_decision != "":
            sub.num_participants_p1 += 1
            print("++++++++++++++++",group.p1_decision)
            s = group.p1_decision
            if s == "A":
                sub.num_A_p1 += 1
            elif s == "B":
                sub.num_B_p1 += 1
            else:
                sub.err_message = "エラーあり"
        else:
            group.flg_non_input_p1 = 1
            group.p1_decision = random.choice(C.choice_list)

def set_P2(player: Player):
    if player.id_in_group == 2:
        sub = player.subsession
        group = player.group

        if group.p2_decision != "":
            sub.num_participants_p2 += 1
            s = group.p2_decision
            if s == "A":
                sub.num_A_p2 += 1
            elif s == "B":
                sub.num_B_p2 += 1
            else:
                sub.err_message = "エラーあり"
        else:
            group.flg_non_input_p2 = 1
            group.p2_decision = random.choice(C.choice_list)

def set_P1s(subsession: Subsession):
    for p in subsession.get_players():
        set_P1(p)

def set_P2s(subsession: Subsession):
    for p in subsession.get_players():
        set_P2(p)

def graph_pair(player: Player):
    sub = player.subsession
    group = player.group
    sub.pair_num += 1
    # グラフ用集計
    s1 = group.p1_decision
    s2 = group.p2_decision
    #sp = player.pair_choice
    if (s1 == "A")and(s2 == "A"):
        sub.pair_num_AA += 1
    elif (s1 == "A")and(s2 == "B"):
        sub.pair_num_AB += 1
    elif (s1 == "B") and (s2 == "A"):
        sub.pair_num_BA += 1
    elif (s1 == "B") and (s2 == "B"):
        sub.pair_num_BB += 1
    else:
        sub.pair_err_message = "エラーあり"

def set_payoff(player: Player):
    group = player.group
    payoff_matrix = {
        ("A", "A"): C.PAYOFF_B,
        ("A", "B"): C.PAYOFF_D,
        ("B", "A"): C.PAYOFF_A,
        ("B", "B"): C.PAYOFF_C,
    }
    other = other_player(player)
    #player.pair_choice = other.individual_choice
    #player.pair_id = other.id_in_group
    #if other.flg_non_input == 1:
    #    player.flg_pair_non_input = 1
    print((group.p1_decision, group.p2_decision))
    if player.id_in_group == 1:
        player.payoff = payoff_matrix[(group.p1_decision, group.p2_decision)]
    else:
        player.payoff = payoff_matrix[(group.p2_decision, group.p1_decision)]

def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)

def set_graph(subsession: Subsession):
    for p in subsession.get_players():
        graph_pair(p)

def other_player(player: Player):
    return player.get_others_in_group()[0]

# PAGES-------------------------
class Introduction(Page):
    timeout_seconds = 100

class First_mover(Page):
    form_model = 'group'
    form_fields = ['p1_decision','p1_individual_choice_comment']
    print("testtest")
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForFirstMover(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P1s

class Second_mover(Page):
    form_model = 'group'
    form_fields = ['p2_decision','p2_individual_choice_comment']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

class WaitForSecondMover(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P2s

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class GraphWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_graph


class PreResults(Page):
    pass

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            my_decision=group.p1_decision,
            opponent_decision=group.p2_decision
        )

    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
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

        print(prop_num_A_p1,";;;;;;;;;;;;;;;;;;;;;")
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
        if sub.pair_num_AA > 0:
            prop_pair_num_AA = round((sub.pair_num_AA / sub.pair_num) * 100, 2)
        else:
            prop_pair_num_AA = 0
        if sub.pair_num_AB > 0:
            prop_pair_num_AB = round((sub.pair_num_AB / sub.pair_num) * 100, 2)
        else:
            prop_pair_num_AB = 0
        if sub.pair_num_BA > 0:
            prop_pair_num_BA = round((sub.pair_num_BA / sub.pair_num) * 100, 2)
        else:
            prop_pair_num_BA = 0
        if sub.pair_num_BB > 0:
            prop_pair_num_BB = round((sub.pair_num_BB / sub.pair_num) * 100, 2)
        else:
            prop_pair_num_BB = 0

        return dict(
            num_participants_P1=sub.num_participants_p1,
            num_participants_P2=sub.num_participants_p2,
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


page_sequence = [
                 Introduction,
                 First_mover,
                 WaitForFirstMover,
                 Second_mover,
                 WaitForSecondMover,
                 ResultsWaitPage,
                 GraphWaitPage,
                 PreResults,
                 Results
                 ]
