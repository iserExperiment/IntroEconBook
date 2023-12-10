from otree.api import *
import time

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ch3_5_time_discount'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    multiple_switch_MPL0 = models.BooleanField()
    multiple_switch_MPL1 = models.BooleanField()
    multiple_switch_MPL2 = models.BooleanField()

    Decision_MPL_0 = models.StringField(initial='')
    num_A_risk = models.IntegerField()
    num_B_risk = models.IntegerField()

    Decision_MPL_1 = models.StringField(initial='')
    num_A_MPL_1 = models.IntegerField()
    num_B_MPL_1 = models.IntegerField()

    Decision_MPL_2 = models.StringField(initial='')
    num_A_MPL_2 = models.IntegerField()
    num_B_MPL_2 = models.IntegerField()


    start = models.FloatField(initial=0.0)
    read_time = models.LongStringField(initial='0')
    time = models.LongStringField(initial='0')


# PAGESー－－－－－－－－－－－－－
class Decision0(Page):
    #  html to サーバー
    @staticmethod
    def live_method(player: Player, data):
        print("data",data)
        if data["first"] == 1:
            player.time = str(time.time() - player.start)
            player.Decision_MPL_0 = "A" * len(data["A"]) + "B" * len(data["B"])
            player.multiple_switch_MPL0 = 0
            print("************",player.Decision_MPL_0)
            player.num_A_risk = player.Decision_MPL_0.count("A")
            player.num_B_risk = player.Decision_MPL_0.count("B")
        else:
            player.time = str(time.time() - player.start)
            mpl_list = player.Decision_MPL_0
            if data["select_type"] == "A":
                player.Decision_MPL_0 = mpl_list[:int(data["position_num"]) - 1] + 'A' + mpl_list[int(data["position_num"]):]
            else:
                player.Decision_MPL_0 = mpl_list[:int(data["position_num"]) - 1] + 'B' + mpl_list[int(data["position_num"]):]
            player.num_A_risk = player.Decision_MPL_0.count("A")
            player.num_B_risk = player.Decision_MPL_0.count("B")
            player.multiple_switch_MPL0 = "B" in player.Decision_MPL_0[:player.num_A_risk]

    @staticmethod
    def before_next_page(self, timeout_happened):
        self.participant.vars['Decision_1'] = self.Decision_MPL_0

class Decision1(Page):
    #  html to サーバー
    @staticmethod
    def live_method(player: Player, data):
        if data["first"] == 1:
            player.time = str(time.time() - player.start)
            player.Decision_MPL_1 = "A" * len(data["A"]) + "B" * len(data["B"])
            player.multiple_switch_MPL1 = 0
            print(player.Decision_MPL_1)
            player.num_A_MPL_1 = player.Decision_MPL_1.count("A")
            player.num_B_MPL_1 = player.Decision_MPL_1.count("B")
        else:
            player.time = str(time.time() - player.start)
            mpl_list = player.Decision_MPL_1
            if data["select_type"] == "A":
                player.Decision_MPL_1 = mpl_list[:int(data["position_num"]) - 1] + 'A' + mpl_list[int(data["position_num"]):]
            else:
                player.Decision_MPL_1 = mpl_list[:int(data["position_num"]) - 1] + 'B' + mpl_list[int(data["position_num"]):]
            player.num_A_MPL_1 = player.Decision_MPL_1.count("A")
            player.num_B_MPL_1 = player.Decision_MPL_1.count("B")
            player.multiple_switch_MPL1 = "B" in player.Decision_MPL_1[:player.num_A_MPL_1]

    @staticmethod
    def before_next_page(self, timeout_happened):
        self.participant.vars['Decision_MPL_1'] = self.Decision_MPL_1

class Decision2(Page):
    #  html to サーバー
    @staticmethod
    def live_method(player: Player, data):
        if data["first"] == 1:
            player.time = str(time.time() - player.start)
            player.Decision_MPL_2 = "A" * len(data["A"]) + "B" * len(data["B"])
            player.multiple_switch_MPL2 = 0
            print(player.Decision_MPL_2)
            player.num_A_MPL_2 = player.Decision_MPL_2.count("A")
            player.num_B_MPL_2 = player.Decision_MPL_2.count("B")
        else:
            player.time = str(time.time() - player.start)
            mpl_list2 = player.Decision_MPL_2
            if data["select_type"] == "A":
                player.Decision_MPL_2 = mpl_list2[:int(data["position_num"]) - 1] + 'A' + mpl_list2[int(data["position_num"]):]
            else:
                player.Decision_MPL_2 = mpl_list2[:int(data["position_num"]) - 1] + 'B' + mpl_list2[int(data["position_num"]):]
            player.num_A_MPL_2 = player.Decision_MPL_2.count("A")
            player.num_B_MPL_2 = player.Decision_MPL_2.count("B")
            player.multiple_switch_MPL2 = "B" in player.Decision_MPL_2[:player.num_A_MPL_2]

    @staticmethod
    def before_next_page(self, timeout_happened):
        self.participant.vars['Decision_MPL_2'] = self.Decision_MPL_2

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results0(Page):
    pass


page_sequence = [#Decision0,
                 #Results0,
                 Decision1,
                 Decision2
                 ]
