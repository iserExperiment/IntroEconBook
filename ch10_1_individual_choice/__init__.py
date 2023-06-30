from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ch10_1_individual_choice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ADD_TIME = 180
    CHOICE_LIST_SENTE = [
        ["A", 'A：80%の確率で4000円を獲得、20%の確率で0円を獲得'],
        ["B", 'B：100%の確率で3000円を獲得'],
        ["C", 'C：20%の確率で4000円を獲得、80%の確率で0円を獲得'],
        ["D", 'D：25%の確率で3000円を獲得、75%の確率で0円を獲得'],
        ["E", 'E：80%の確率で4000円を失う、20%の確率で0円を失う'],
        ["F", 'F：100%の確率で3000円を失う'],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(
        widget=widgets.RadioSelect,
        verbose_name='',
        choices=C.CHOICE_LIST_SENTE[0:2]
    )
    q1_why = models.LongStringField(
        label="""なぜその選択をしましたか？"""
    )

    q2 = models.StringField(
        widget=widgets.RadioSelect,
        verbose_name='',
        choices=C.CHOICE_LIST_SENTE[2:4]
    )
    q2_why = models.LongStringField(
        label="""なぜその選択をしましたか？"""
    )

    q3 = models.StringField(
        widget=widgets.RadioSelect,
        verbose_name='',
        choices=C.CHOICE_LIST_SENTE[4:6]
    )
    q3_why = models.LongStringField(
        label="""なぜその選択をしましたか？"""
    )

# グラフ描画用
def graph(subsession: Subsession):
    session = subsession.session
    graph_list = [0]*6
    graph_name_list = ['A', 'B', 'C', 'D', 'E', 'F']

    num_participants = 0
    for p in subsession.get_players():
        num_participants += 1
        if p.q1 != "":
            graph_list[graph_name_list.index(p.q1)] += 1
        if p.q2 != "":
            graph_list[graph_name_list.index(p.q2)] += 1
        if p.q3 != "":
            graph_list[graph_name_list.index(p.q3)] += 1

    # 割合計算
    graph_list = [round((n / num_participants) * 100, 2) for n in graph_list]

    print("グラフリスト",graph_list, graph_name_list,type(graph_name_list))

    # 最終結果用
    if 'graph_data' not in session.vars:
        session.graph_data = {}
    session.graph_data['ch10_1'] = {
        'num_participants': num_participants,
        'graph_list': graph_list,
        'graph_name_list': graph_name_list,
        }


# PAGES

class Question1(Page):
    #timeout_seconds = 45+C.ADD_TIME
    timeout_seconds = C.ADD_TIME
    form_model = 'player'
    form_fields = ['q1', 'q1_why']

class Question2(Page):
    #timeout_seconds = 45+C.ADD_TIME
    timeout_seconds = C.ADD_TIME
    form_model = 'player'
    form_fields = ['q2', 'q2_why']

class Question3(Page):
    #timeout_seconds = 45+C.ADD_TIME
    timeout_seconds = C.ADD_TIME
    form_model = 'player'
    form_fields = ['q3', 'q3_why']

class Instruction(Page):
    pass


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = graph


class Results(Page):
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        return player.session.graph_data
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            graph_choice_list = [c[1] for c in C.CHOICE_LIST_SENTE]
        )


page_sequence = [Question1,
                 Question2,
                 Question3,
                 ResultsWaitPage,
                 Results
                 ]
