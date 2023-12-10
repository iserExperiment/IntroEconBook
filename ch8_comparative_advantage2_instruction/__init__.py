from otree.api import *


doc = """ """


class Constants(BaseConstants):
    name_in_url = "ch8_comparative_advantage2_instruction"
    players_per_group = None
    num_rounds = 1
    timeout_question2 = 180
    timeout_question2_min = timeout_question2 // 60
    timeout_question_per_page = 40
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
    pass


# FUNCTIONS
# PAGES
class instruction1(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


class instruction2(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


class instruction3(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


page_sequence = [instruction1, instruction2, instruction3]
