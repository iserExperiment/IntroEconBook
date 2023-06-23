from otree.api import *
import random
import time
c = Currency


class C(BaseConstants):
    NAME_IN_URL = 'ch9_secondprice'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    INSTRUCTIONS_TEMPLATE = 'ch9_secondprice/instructions.html'
    min_allowable_bid = c(0)
    max_allowable_bid = c(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()

class Player(BasePlayer):
    item_value = models.CurrencyField(
        doc="""Common value of the item to be auctioned, random for treatment"""
    )
    bid_amount = models.IntegerField(
        #min=C.min_allowable_bid,
        #max=C.max_allowable_bid,
        min = 0,
        max=999,
        doc="",
        label="",
    )
    is_winner = models.BooleanField(
        initial=False, doc="""Indicates whether the player is the winner"""
    )
    sum_payoff = models.CurrencyField(initial=0)


# FUNCTIONS-----------------------
def set_winner(group: Group):
    import random

    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    losers = [p for p in players if p.bid_amount < group.highest_bid]
    if len(losers)>0:
        group.second_highest_bid = max([p.bid_amount for p in losers])
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
        player.payoff = player.item_value - group.second_highest_bid
        #if player.payoff < 0:
        #    player.payoff = 0
    else:
        player.payoff = 0
    player.sum_payoff = player.sum_payoff + player.payoff



# PAGES-------------------------
class Introduction(Page):
    pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group

        player.item_value = random.randint(0,100)

class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(is_greedy=player.item_value - player.bid_amount < 0)

page_sequence = [Introduction,
                 Bid,
                 ResultsWaitPage,
                 Results]
