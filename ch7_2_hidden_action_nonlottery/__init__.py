from otree.api import *
import random

doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch7_2_hidden_action_nonlottery"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3

    A_ROLE = "A"
    B_ROLE = "B"

    INSTRUCTIONS_TEMPLATE = "ch7_2_hidden_action_nonlottery/instruction.html"

    # 配点を変えた場合はconfirmation/__init__.pyのclass Cでも定数を変更すること（確認問題に反映される．）
    pt_D_A = 5
    pt_D_B = 5
    pt_NR_A = 0
    pt_NR_B = 14
    pt_R15_A = 12
    pt_R15_B = 10
    pt_R6_A = 0
    pt_R6_B = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    SKIP = models.BooleanField(initial=False)

    # ランダムの数
    lottery_random = models.IntegerField()


class Player(BasePlayer):
    # 入力があったかどうかのフラグ
    flg_non_input = models.IntegerField()

    UD = models.StringField(
        label="",
        choices=[["U", "U"], ["D", "D"]],
        widget=widgets.RadioSelect,
    )

    NR = models.StringField(
        label="",
        choices=[["R", "R"], ["NR", "NR"]],
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES
class wait_confirmation(WaitPage):
    body_text = "相手の確認を待っています。"


class Shuffle_Wait_Page(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly(fixed_id_in_group=True)
        # print(subsession.get_group_matrix())


# 最初のページ
class Introduction(Page):
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


# 最後のページ
class over(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class page_1A(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.A_ROLE

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            choices = ["U", "D"]
            # 入力なし
            player.flg_non_input = 1
            player.UD = choices[random.randint(0, 1)]
            print(player.UD)

    form_model = "player"
    form_fields = ["UD"]
    timeout_seconds = 30


class page_1B(WaitPage):
    # 実際にはBだけに表示
    template_name = "Wait.html"

    @staticmethod
    def vars_for_template(player):
        return dict(other_player=other_player(player))

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.get_player_by_role(C.A_ROLE).payoff = C.pt_D_A
        group.get_player_by_role(C.B_ROLE).payoff = C.pt_D_B


class result1(Page):
    # AがDを選択した時に表示
    @staticmethod
    def is_displayed(player: Player):
        if player.group.get_player_by_role(C.A_ROLE).UD == "D":
            player.group.SKIP = True
        return player.group.get_player_by_role(C.A_ROLE).UD == "D"

    @staticmethod
    def vars_for_template(player):
        return dict(other_player=other_player(player))

    timeout_seconds = 50


class page_2B(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.B_ROLE and player.group.SKIP == False

    @staticmethod
    def vars_for_template(player):
        return dict(other_player=other_player(player))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            choices = ["R", "NR"]
            # 入力なし
            player.flg_non_input = 1
            player.NR = choices[random.randint(0, 1)]
            print(player.NR)

    form_model = "player"
    form_fields = ["NR"]
    timeout_seconds = 30


class page_2A(WaitPage):
    # 実際にはAだけに表示
    template_name = "Wait.html"

    @staticmethod
    def is_displayed(player: Player):
        return player.group.SKIP == False

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player=other_player(player))

    @staticmethod
    def after_all_players_arrive(group: Group):
        choice = group.get_player_by_role(C.B_ROLE).NR
        if choice == "NR":
            group.get_player_by_role(C.A_ROLE).payoff = C.pt_NR_A
            group.get_player_by_role(C.B_ROLE).payoff = C.pt_NR_B
        else:
            group.get_player_by_role(C.A_ROLE).payoff = C.pt_R15_A
            group.get_player_by_role(C.B_ROLE).payoff = C.pt_R15_B
            # rnd = random.randint(1, 10)
            # rnd = random.randint(1, 6)
            # group.lottery_random = rnd

            # if rnd == 6:
            #    group.get_player_by_role(C.A_ROLE).payoff = C.pt_R6_A
            #    group.get_player_by_role(C.B_ROLE).payoff = C.pt_R6_B
            # else:
            #    group.get_player_by_role(C.A_ROLE).payoff = C.pt_R15_A
            #    group.get_player_by_role(C.B_ROLE).payoff = C.pt_R15_B


class result2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.group.SKIP == False

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_player=other_player(player),
            B_choice=player.group.get_player_by_role(C.B_ROLE).NR,
        )

    timeout_seconds = 50


page_sequence = [
    Introduction,
    Shuffle_Wait_Page,
    wait_confirmation,
    page_1A,
    page_1B,
    result1,
    wait_confirmation,
    page_2B,
    page_2A,
    result2,
    wait_confirmation,
    over,
]
