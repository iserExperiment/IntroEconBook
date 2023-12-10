from otree.api import *


doc = """ """


class Constants(BaseConstants):
    name_in_url = "ch8_comparative_advantage1_instruction"
    players_per_group = None
    num_rounds = 1
    timeout_question1 = 120
    timeout_question1_min = timeout_question1 // 60
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
class instruction0(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


class instruction1(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


class instruction2(Page):
    timeout_seconds = Constants.timeout_question_per_page
    pass


page_sequence = [instruction0, instruction1, instruction2]
