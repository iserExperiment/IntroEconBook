from otree.api import *
import random
import time

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch3_3_repeated_infinite"
    PLAYERS_PER_GROUP = 2

    LIST_PROB = []
    LIST_PROB.append(0)
    # LIST_MAX = 0
    # if LIST_MAX <= 80:
    for i in range(100):
        # tmp = random.randrange(0, 100, 1)
        tmp = random.randint(1, 100)
        # print(tmp)
        if tmp <= 80:
            # print("以下")
            LIST_PROB.append(tmp)
        else:
            # print("80より多い")
            LIST_PROB.append(tmp)
            NUM_ROUNDS = i + 1
            break

        # if tmp >= 80:
        #    print("以上")
        #    LIST_PROB.append(tmp)
        #    NUM_ROUNDS = i + 1
        #    break
        # else:
        #    LIST_PROB.append(tmp)

    # print("LIST_PROB",LIST_PROB, NUM_ROUNDS, "回実施")

    # if random.random() > 1:
    #    NUM_ROUNDS = 2
    # else:
    #    NUM_ROUNDS = 5

    INSTRUCTIONS_TEMPLATE = "ch3_3_repeated_infinite/instructions.html"
    PAYOFF_A = cu(2)
    PAYOFF_B = cu(1)
    PAYOFF_C = cu(3)
    PAYOFF_D = cu(0)
    CHOICE_LABEL_1 = "A"
    CHOICE_LABEL_2 = "B"

    choice_list = ["A", "B"]


class Subsession(BaseSubsession):
    this_rounds_dice = models.IntegerField(initial=0)
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
    start_timestamp = models.IntegerField()


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

    # 相手はどちらを選ぶと思うか
    think_other_player_choice = models.StringField(
        widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["Aを選ぶと予想する", C.CHOICE_LABEL_1 + "を選ぶと予想する"],
            ["Bを選ぶと予想する", C.CHOICE_LABEL_2 + "を選ぶと予想する"],
        ],
    )

    # 意思決定の理由
    individual_choice_comment = models.LongStringField(verbose_name="", initial="")

    # 相手の予想のの理由
    think_other_player_choice_comment = models.LongStringField(
        verbose_name="", initial=""
    )

    # 相手が映画１を選んだ際に、あなたは何ポイント獲得しますか？
    q1 = models.StringField(
        # widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["5", "5"],
            ["10", "10"],
            ["2", "2"],
            ["3", "3"],
        ],
    )

    # 相手が映画2を選んだ際に、あなたは何ポイント獲得しますか？
    q2 = models.StringField(
        # widget=widgets.RadioSelectHorizontal,
        verbose_name="",
        choices=[
            ["5", "5"],
            ["10", "10"],
            ["2", "2"],
            ["3", "3"],
        ],
    )


# FUNCTIONS
def keisan(player: Player):
    sub = player.subsession

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


def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)

    for p in group.get_players():
        graph_pair(p)


def other_player(player: Player):
    return player.get_others_in_group()[0]


def graph_pair(player: Player):
    sub = player.subsession
    sub.pair_num += 1
    # グラフ用集計
    s = player.individual_choice
    sp = player.pair_choice
    if (s == "A") and (sp == "A"):
        sub.pair_num_AA += 1
    elif (s == "A") and (sp == "B"):
        sub.pair_num_AB += 1
    elif (s == "B") and (sp == "A"):
        sub.pair_num_BA += 1
    elif (s == "B") and (sp == "B"):
        sub.pair_num_BB += 1
    else:
        sub.pair_err_message = "エラーあり"


def set_payoff(player: Player):
    payoff_matrix_p1 = {
        ("A", "A"): C.PAYOFF_A,
        ("A", "B"): C.PAYOFF_D,
        ("B", "A"): C.PAYOFF_C,
        ("B", "B"): C.PAYOFF_B,
    }
    payoff_matrix_p2 = {
        ("A", "A"): C.PAYOFF_A,
        ("A", "B"): C.PAYOFF_C,
        ("B", "A"): C.PAYOFF_D,
        ("B", "B"): C.PAYOFF_B,
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
class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())


class Introduction(Page):
    # timeout_seconds = 100
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Decision(Page):
    # timeout_seconds = 120
    timeout_seconds = 90
    form_model = "player"
    form_fields = [
        "individual_choice",
        "individual_choice_comment",
        "think_other_player_choice",
        "think_other_player_choice_comment",
    ]

    @staticmethod
    def vars_for_template(player: Player):
        sub = player.subsession
        sub.this_rounds_dice = C.LIST_PROB[sub.round_number]


class Question(Page):
    form_model = "player"
    form_fields = ["q1", "q2"]


class keisanWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = keisans


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    # timeout_seconds = 45
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            # same_choice=player.individual_choice == opponent.individual_choice,
            # my_decision=player.field_display('individual_choice'),
            my_decision=player.individual_choice,
            opponent_decision=opponent.individual_choice,
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
    timeout_seconds = 25


page_sequence = [
    WaitToStart,
    Introduction,
    Decision,
    # Question,
    keisanWaitPage,
    ResultsWaitPage,
    # PreResults,
    Results,
]
