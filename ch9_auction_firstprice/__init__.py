from otree.api import *
import random
import time
c = Currency


class C(BaseConstants):
    NAME_IN_URL = 'ch9_auction_firstprice'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'ch9_auction_firstprice/instructions.html'
    EVALUATE_MIN = 0
    EVALUATE_MAX = 100


class Subsession(BaseSubsession):
    rate_of_true_telling_sub = models.IntegerField(initial=0)


class Group(BaseGroup):
    # 一番目に高い入札額
    highest_bid = models.CurrencyField()
    # 二番目に高い入札額
    second_highest_bid = models.CurrencyField()
    # 落札価格
    contract_payoff = models.CurrencyField()
    # グループでの正直申告率
    rate_of_true_telling_group = models.IntegerField(initial=0)

class Player(BasePlayer):
    # 評価値
    item_value = models.CurrencyField()
    # 入札額
    individual_choice = models.StringField(
        label="あなたはいくら入札しますか？",
    )
    # 入力がなかった場合
    flg_non_input = models.IntegerField(initial=0)

    # 計算で使用する入札額
    bid = models.IntegerField()

    # 計算で使用する入札額
    is_winner = models.BooleanField(
        initial=False, doc="""Indicates whether the player is the winner"""
    )
    # 利得累計
    sum_payoff = models.CurrencyField(initial=0)

    # 正直かどうか
    flg_true_bid_this_round = models.IntegerField(initial=0)



# FUNCTIONS-----------------------
def set_winner(group: Group):
    import random
    players = group.get_players()
    # 追加------------------------
    for p in group.get_players():
        # print(p.input_contribution, p.contribution)
        if p.individual_choice == '':
            # rangeの範囲は画面で入力できる範囲に合わせる
            p.bid = random.randint(C.EVALUATE_MIN, C.EVALUATE_MAX)
            # 入力なし
            p.flg_non_input = 1
        else:
            p.bid = int(p.individual_choice)
    # 追加------------------------
    group.highest_bid = max([p.bid for p in players])
    players_with_highest_bid = [p for p in players if p.bid == group.highest_bid]
    not_winners = [p for p in players if p.bid < group.highest_bid]
    if len(not_winners)>0:
        group.second_highest_bid = max([p.bid for p in not_winners])
    else:
        group.second_highest_bid = group.highest_bid
    winner = random.choice(
        players_with_highest_bid
    )  # if tie, winner is chosen at random
    winner.is_winner = True

    for p in players:
        set_payoff(p)

def set_payoff(player: Player):
    group = player.group

    if player.is_winner:
        player.payoff = player.item_value - player.bid
        #if player.payoff < 0:
        #    player.payoff = 0
    else:
        player.payoff = 0
    player.sum_payoff = player.sum_payoff + player.payoff



# PAGES-------------------------
class Introduction(Page):
    timeout_seconds = 30
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Bid(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['individual_choice']

    @staticmethod
    def vars_for_template(player: Player):
        player.item_value = random.randint(C.EVALUATE_MIN,C.EVALUATE_MAX)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'


class Results(Page):
    timeout_seconds = 30
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(is_greedy=player.item_value - player.bid < 0)
        

class Summarize_WaitPage(WaitPage):
        wait_for_all_groups = True
        @staticmethod
        def is_displayed(player):
            return player.round_number == C.NUM_ROUNDS
            
            
class Summarize_Result(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


    # グラフ描画用
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        # 全体
        sub = player.subsession
        players = sub.get_players()
        graph_data_sub = []
        sub.rate_of_true_telling_sub = 0 # リロード対応
        print("サブ",len(players))
        for p in players:
            for i in range(C.NUM_ROUNDS):
                i = i + 1
                #all_sub_round = sub.in_round(i)
                this_round = p.in_round(i)
                tmp = [this_round.item_value,this_round.bid]
                graph_data_sub.append(tmp)
                # 正直申告
                print("sub:this_round.flg_true_bid_this_round", this_round.flg_true_bid_this_round)
                sub.rate_of_true_telling_sub = sub.rate_of_true_telling_sub + this_round.flg_true_bid_this_round
        # グループ
        group = player.group
        players = group.get_players()
        list_value= []
        list_data = []
        graph_data_group = []
        print("グループ",len(players))
        group.rate_of_true_telling_group = 0 # リロード対応
        for p in players:
            for i in range(C.NUM_ROUNDS):
                i = i + 1
                #all_sub_round = sub.in_round(i)
                this_round = p.in_round(i)
                tmp = [this_round.item_value,this_round.bid]
                graph_data_group.append(tmp)
                print(graph_data_group)
                # 正直申告率
                print("this_round.flg_true_bid_this_round",this_round.flg_true_bid_this_round)
                group.rate_of_true_telling_group = group.rate_of_true_telling_group + this_round.flg_true_bid_this_round
                #list_value.append(this_round.item_value)
                #list_data.append(this_round.bid)
        print("評価値",list_value)
        print("入札額",list_data)
        
        #group.rate_of_true_telling_group = sum(p.flg_true_bid_this_round for p in players.in_all_rounds())
        #print(group.rate_of_true_telling_group)

        #tmp_group = group.rate_of_true_telling_group * C.NUM_ROUNDS

        #print(list_average.replace('[', ''))
        #print(list_average.replace(']', ''))
        return dict(
            #list_value=list_value,
            #list_data = list_data,
            graph_data_group = graph_data_group,
            graph_data_sub=graph_data_sub,
        )

page_sequence = [Introduction,
                 Bid,
                 ResultsWaitPage,
                 Results,
                 Summarize_WaitPage,
                 Summarize_Result]
