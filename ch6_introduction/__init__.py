from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "ch6_introduction"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 30
    # NUM_ROUNDS = 99 # サーバーが重すぎるので変更
    INCORRECT_TEMPLATE = "ch6_introduction/templates/Incorrect.html"
    INSTRUCTION_TEMPLATE = "ch6_introduction/templates/Instruction.html"
    INSTRUCTION_TEMPLATE_SEC = "ch6_introduction/templates/Instruction2.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cnt = models.IntegerField(initial=0)
    check_q1 = models.BooleanField(
        label="",
        choices=[
            [True, "売り手"],
            [False, "買い手"],
        ],
    )
    check_q2 = models.BooleanField(
        label="",
        choices=[
            [False, "1単位"],
            [True, "何単位でも売れるだけ"],
        ],
    )
    check_q3 = models.BooleanField(
        label="",
        choices=[
            [False, "販売価格が20"],
            [False, "販売価格が21"],
            [True, "販売価格が19"],
        ],
    )
    check_q4_int1 = models.IntegerField(label="")
    check_q4_int2 = models.IntegerField(label="")
    pass


# FUNCTIONS
def check_q4(player: Player):
    return player.check_q4_int1 == 50 and player.check_q4_int2 == 10


# PAGES
class Instruction1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instruction2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Check1(Page):
    form_model = "player"
    form_fields = ["check_q1"]

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 0:
            return True
        else:
            return False


class Check2(Page):
    form_model = "player"
    form_fields = ["check_q2"]

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 1:
            return True
        else:
            return False


class Check3(Page):
    form_model = "player"
    form_fields = ["check_q3"]

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 2:
            return True
        else:
            return False


class Check4(Page):
    form_model = "player"
    form_fields = ["check_q4_int1", "check_q4_int2"]

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 3:
            return True
        else:
            return False


class Incorrect1(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 0:
            return player.check_q1 == False
        else:
            return False


class Incorrect2(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 1:
            return player.check_q2 == False
        else:
            return False


class Incorrect3(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 2:
            return player.check_q3 == False
        else:
            return False


class Incorrect4(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 3:
            return check_q4(player) == False
        else:
            return False


class Correct1(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 0:
            return player.check_q1 == True
        else:
            return False

    def before_next_page(player: Player, timeout_happened):
        if player.check_q1 == True:
            player.in_round(1).cnt += 1


class Correct2(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 1:
            return player.check_q2 == True
        else:
            False

    def before_next_page(player: Player, timeout_happened):
        if player.check_q2 == True:
            player.in_round(1).cnt += 1


class Correct3(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 2:
            return player.check_q3 == True
        else:
            False

    def before_next_page(player: Player, timeout_happened):
        if player.check_q3 == True:
            player.in_round(1).cnt += 1


class Correct4(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 3:
            return check_q4(player) == True
        else:
            False

    def before_next_page(player: Player, timeout_happened):
        if check_q4(player) == True:
            player.in_round(1).cnt += 1


class Lastpage(Page):
    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).cnt == 4:
            return True
        else:
            False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return "individual"


page_sequence = [
    Instruction1,
    Instruction2,
    Check1,
    Incorrect1,
    Correct1,
    Check2,
    Incorrect2,
    Correct2,
    Check3,
    Incorrect3,
    Correct3,
    Check4,
    Incorrect4,
    Correct4,
    Lastpage,
]
