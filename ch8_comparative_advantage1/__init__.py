from otree.api import *


class Constants(BaseConstants):
    name_in_url = "ch8_comparative_advantage1"
    players_per_group = None
    num_rounds = 1
    timeout_question1 = 120
    timeout_question_result = 30
    working_hours = 20
    cheese_cost_A = 1
    bread_cost_A = 1.5
    cheese_cost_B = 3
    bread_cost_B = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 追加
    initial_cheese = models.FloatField(
        label="チーズ",
    )

    initial_bread = models.FloatField(
        label="パン",
    )
    cheese = models.FloatField(
        label="チーズ",
    )
    bread = models.FloatField(
        label="パン",
    )
    player_type = models.StringField(initial="none")


# FUNCTIONS
def init_player(group: Group):
    players = group.get_players()
    for p in players:
        p.player_type = "A" if p.id_in_subsession % 3 == 1 else "B"


# PAGES
class Init(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        init_player(group)


class Screen1(Page):
    timeout_seconds = Constants.timeout_question1
    form_model = "player"
    form_fields = ["cheese", "bread"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.initial_cheese = player.cheese
        player.initial_bread = player.bread

    @staticmethod
    def error_message(player: Player, values):
        if (values["bread"] < 0.1 and values["bread"] > 0) or (
            values["cheese"] < 0.1 and values["cheese"] > 0
        ):
            return "小数点以下1桁までで入力してください"
        if (
            len(str(values["bread"]).split(".")[1]) != 1
            or len(str(values["cheese"]).split(".")[1]) != 1
        ):
            return "小数点以下1桁までで入力してください"
        if player.player_type == "A":
            if (
                round(
                    values["bread"] * Constants.bread_cost_A
                    + values["cheese"] * Constants.cheese_cost_A,
                    2,
                )
                != Constants.working_hours
            ):
                return "20時間丁度になるように入力してください"
        elif player.player_type == "B":
            if (
                round(
                    values["bread"] * Constants.bread_cost_B
                    + values["cheese"] * Constants.cheese_cost_B,
                    2,
                )
                != Constants.working_hours
            ):
                return "20時間丁度になるように入力してください"


class Results(Page):
    timeout_seconds = Constants.timeout_question_result
    pass


page_sequence = [Init, Screen1, Results]
