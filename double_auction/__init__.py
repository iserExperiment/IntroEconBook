from otree.api import *
import time
import random
import json

from sqlalchemy import false, true

doc = "Double auction market"


class C(BaseConstants):
    NAME_IN_URL = 'double_auction'
    PLAYERS_PER_GROUP = 26
    NUM_ROUNDS = 2
    ITEMS_PER_SELLER = 1
    VALUATION_MIN = 20
    VALUATION_MAX = 100
    PRODUCTION_COSTS_MIN = 10
    PRODUCTION_COSTS_MAX = 90
    #buyer_value = [50,47,44,41,38,35]
    #seller_value = [23,26,29,32,35,38]
    buyer_value = [45,40,35,30,25,20]
    seller_value = [3,8,13,18,23,28]


class Subsession(BaseSubsession):    
    pass

def creating_session(subsession: Subsession):    
    players = subsession.get_players()    
    i = 0
    for p in players:
        # this means if the player's ID is not a multiple of 2, they are a buyer.
        # for more buyers, change the 2 to 3
        # 買い手かどうかを決定する        
        p.is_buyer = p.id_in_group % 2 > 0
        if p.is_buyer: # 
            p.num_items = 0
            tmp = i%len(C.buyer_value)  
            p.break_even_point = C.buyer_value[tmp]
            C.PLAYERS_PER_GROUP
            # p.break_even_point = random.randint(C.VALUATION_MIN, C.VALUATION_MAX)
            p.current_offer = 0
        else:
            p.num_items = C.ITEMS_PER_SELLER
            # p.break_even_point = random.randint(
            #     C.PRODUCTION_COSTS_MIN, C.PRODUCTION_COSTS_MAX
            # )
            tmp = i%len(C.buyer_value)  
            p.break_even_point = C.seller_value[tmp]
            p.current_offer = C.VALUATION_MAX + 1
            i += 1 

class Group(BaseGroup):
    # buyer_bids = models.StringField()  # 買い注文
    # seller_asks = models.StringField() # 売り注文
    start_timestamp = models.IntegerField()


class Player(BasePlayer):
    finish_frag = models.BooleanField(initial = False)
    is_buyer = models.BooleanField()
    break_even_point = models.IntegerField()
    num_items = models.IntegerField()
    total_payoff = models.IntegerField()
    offers = models.StringField(initial="") # 注文    
    offer_seconds = models.StringField(initial="") # 注文時間  
    offers_win = models.StringField(initial="") # 取引成立時の注文
    partners = models.StringField(initial="") # 取引相手 
    prices = models.StringField(initial="")  # 取引価格
    seconds = models.StringField(initial="") # 取引時間
    mili_seconds = models.FloatField(initial=0.0) # 取引時間(グラフ用)
    current_offer = models.IntegerField()
    current_seconds = models.IntegerField()
    


class Transaction(ExtraModel):
    group = models.Link(Group)
    buyer = models.Link(Player)
    seller = models.Link(Player)
    price = models.CurrencyField()
    seconds = models.IntegerField(doc="Timestamp (seconds since beginning of trading)")


def live_method(player: Player, data):
    print("受信")    
    print(data)            
    my_id = player.id_in_group
    group = player.group    
    players = group.get_players()
    buyers = [p for p in players if p.is_buyer]
    sellers = [p for p in players if not p.is_buyer]      
    news = None
    match = None               
    if data['offer_frag'] and player.finish_frag == False :  # オファー時の処理                
        seconds = int(time.time() - group.start_timestamp)
        mili_seconds = time.time() - group.start_timestamp
        offer = int(data['offer'])
        player.current_offer = offer
        player.current_seconds = seconds
        if len(player.offer_seconds) ==0:
            player.offer_seconds =   str(seconds)
            player.offers =  str(offer) 
        else:
            player.offer_seconds =  player.offer_seconds + "," + str(seconds)
            player.offers = player.offers+ "," + str(offer)

        print("++++++++++++++++++++++++++", mili_seconds)
        if player.is_buyer : #買手の処理                                                 
            prices = {p.id_in_group:p.current_offer for p in sellers }                        
            price =  min(prices.values())            
            if price <= offer:
                candidate = [p for p in prices.keys() if prices[p]==price]  #　候補者                  
                second = {p.offer_seconds:p.id_in_group for p in sellers if p.current_offer == price}
                #player.mili_seconds = {p.mili_seconds:p.id_in_group for p in sellers if p.current_offer == price}
                #mili_seconds = {p.mili_seconds:p.id_in_group for p in sellers if p.current_offer == price}
                partner = second[sorted(second)[0]]
                # partner = random.choice(candidate)
                match = [player,group.get_player_by_id(partner)]                               
        else: # 売手の処理
            prices = {p.id_in_group:p.current_offer for p in buyers }            
            price =  max(prices.values())                                    
            if  offer <= price and player.num_items >0:      
                candidate = [p for p in prices.keys() if prices[p]==price]         
                second = {p.offer_seconds:p.id_in_group for p in buyers if p.current_offer == price}
                #player.mili_seconds = {p.mili_seconds:p.id_in_group for p in buyers if p.current_offer == price}
                #mili_seconds = {p.mili_seconds:p.id_in_group for p in buyers if p.current_offer == price}
                partner = second[sorted(second)[0]]
                # partner = random.choice(candidate)
                match = [group.get_player_by_id(partner),player]            
                    
        if match is not None: # find_match　が　空でなければ作動 #
            [buyer, seller] = match                        
            Transaction.create(
                group=group,
                buyer=buyer,
                seller=seller,
                price=price,
                seconds=seconds,
                #mili_seconds = mili_seconds,
            )
            # 売手    
            buyer.num_items += 1
            buyer.finish_frag =  seller.num_items == 1 # 終了条件
            if len(buyer.offers_win)==0:
                buyer.offers_win =  str(buyer.current_offer)
                buyer.partners =  str(seller.id_in_group)  
                buyer.prices =  str(price)
                buyer.seconds = str(seconds)
                buyer.mili_seconds = mili_seconds
            else:
                buyer.offers_win =  "," + str(buyer.current_offer)
                buyer.partners =  "," + str(seller.id_in_group)  
                buyer.prices =  "," + str(price)
                buyer.seconds =  buyer.seconds + "," + str(seconds)
                buyer.mili_seconds = buyer.mili_seconds
            buyer.current_offer = 0
            # 買手    
            seller.num_items -= 1
            seller.finish_frag = seller.num_items == 0 # 終了条件            
            if len(seller.offers_win)==0:            
                seller.offers_win =  str(seller.current_offer)
                seller.partners =  str(buyer.id_in_group) 
                seller.prices =   str(price)
                seller.seconds =   str(seconds)
                seller.mili_seconds = mili_seconds
            else:
                seller.offers_win = seller.offers_win + "," + str(seller.current_offer)
                seller.partners = seller.partners + ','  + str(buyer.id_in_group) 
                seller.prices = seller.prices + "," + str(price)
                seller.seconds = seller.seconds +  "," + str(seconds)
                seller.mili_seconds = seller.mili_seconds
            seller.current_offer = C.VALUATION_MAX + 1 

            buyer.payoff += buyer.break_even_point - price
            seller.payoff += price - seller.break_even_point  
            news = dict(buyer=buyer.id_in_group, seller=seller.id_in_group, price=price)            
    bids_dict = {p.id_in_group:p.current_offer for p in buyers if p.current_offer > 0}
    tmp = sorted(bids_dict.items(), key=lambda x:x[1], reverse=True)
    bids_dict = {i[0]:i[1] for i in tmp}    

    asks_dict = {p.id_in_group:p.current_offer for p in sellers if p.current_offer <= C.VALUATION_MAX}    
    tmp = sorted(asks_dict.items(), key=lambda x:x[1])
    asks_dict = {i[0]:i[1] for i in tmp}
    bids_player = [p for p in bids_dict]
    asks_player = [p for p in asks_dict]
    bids = [bids_dict[p] for p in bids_dict]
    asks = [asks_dict[p] for p in asks_dict]

    highcharts_series = [[tx.seconds, tx.price] for tx in Transaction.filter(group=group)]    
    results_series = [[tx.seconds, tx.price,tx.buyer.id_in_group,tx.seller.id_in_group] for tx in Transaction.filter(group=group)]    
    return {
        p.id_in_group: dict(
            player=my_id,            
            num_items=p.num_items,
            current_offer=p.current_offer,
            payoff = p.payoff,
            bids_dict = bids_dict,            
            bids=bids,
            bids_player=bids_player,
            asks_dict = asks_dict,            
            asks=asks,
            asks_player=asks_player,
            highcharts_series=highcharts_series,
            news=news,
            partners=p.partners,
            prices=p.prices,
            finish_frag=p.finish_frag,
            results_series=results_series
        )
        for p in players
    }
        
    

# 微妙な関数 (最適マッチでない)
# def find_match(buyers, sellers):
#     for buyer in buyers:
#         for seller in sellers:
#             if seller.num_items > 0 and seller.current_offer <= buyer.current_offer:
#                 # return as soon as we find a match (the rest of the loop will be skipped)
#                 return [buyer, seller]

# def live_method(player: Player, data):
#     print("受信")
#     print(data)
#     group = player.group
#     players = group.get_players()
#     buyers = [p for p in players if p.is_buyer]
#     sellers = [p for p in players if not p.is_buyer]
#     news = None
#     if data:
#         offer = int(data['offer'])
#         player.current_offer = offer
#         if player.is_buyer:
#             match = find_match(buyers=[player], sellers=sellers)
#         else:
#             match = find_match(buyers=buyers, sellers=[player])
#         if match: # find_match　が　空でなければ作動 #
#             [buyer, seller] = match
#             price = buyer.current_offer
#             Transaction.create(
#                 group=group,
#                 buyer=buyer,
#                 seller=seller,
#                 price=price,
#                 seconds=int(time.time() - group.start_timestamp),
#             )
#             buyer.num_items += 1
#             seller.num_items -= 1
#             buyer.payoff += buyer.break_even_point - price
#             seller.payoff += price - seller.break_even_point
#             buyer.current_offer = 0
#             seller.current_offer = C.VALUATION_MAX + 1
#             news = dict(buyer=buyer.id_in_group, seller=seller.id_in_group, price=price)

#     bids = sorted([p.current_offer for p in buyers if p.current_offer > 0], reverse=True)
#     group.buyer_bids =  ",".join(list(map(str,bids)))    
#     asks = sorted([p.current_offer for p in sellers if p.current_offer <= C.VALUATION_MAX])
#     group.seller_asks = ",".join(list(map(str,asks)))
#     highcharts_series = [[tx.seconds, tx.price] for tx in Transaction.filter(group=group)]
    
#     # is not None

#     return {
#         p.id_in_group: dict(
#             num_items=p.num_items,
#             current_offer=p.current_offer,
#             payoff=p.payoff,
#             bids=bids,
#             asks=asks,
#             highcharts_series=highcharts_series,
#             news=news,
#         )
#         for p in players
#     }


        

# PAGES
class WaitToStart(WaitPage):     
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())  

class Trading(Page):
    live_method = live_method

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        players = group.get_players()
        buyers = [p for p in players if p.is_buyer]
        sellers = [p for p in players if not p.is_buyer]
        return dict(num_sellers=len(sellers),
                    num_buyers=len(buyers))

    @staticmethod
    def js_vars(player: Player):
        group = player.group    
        players = group.get_players()
        buyers = [p for p in players if p.is_buyer]
        sellers = [p for p in players if not p.is_buyer]
        return dict(num_sellers=len(sellers),
                    num_buyers=len(buyers),
                    id_in_group=player.id_in_group,
                    is_buyer=player.is_buyer,
                    max_value=C.VALUATION_MAX)

    @staticmethod
    def get_timeout_seconds(player: Player):
        import time
        group = player.group
        #return (group.start_timestamp + 10 * 60) - time.time()
        return (group.start_timestamp + 3 * 60) - time.time()


class ResultsWaitPage(WaitPage):
        
    pass


class Results(Page):
    @staticmethod
    def js_vars(player: Player):
        if player.is_buyer :
            return dict(Num = player.num_items)
        else:
            return dict(Num = C.ITEMS_PER_SELLER - player.num_items)

    @staticmethod
    def live_method(player: Player,data):        
        group = player.group    
        highcharts_series = [[tx.seconds, tx.price] for tx in Transaction.filter(group=group)]    
        players = group.get_players()
        print("***************************",players)
        return {
            p.id_in_group: dict(                
                highcharts_series=highcharts_series,                 
            )
            for p in players
        }
    pass


class Room_waiting(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

page_sequence = [Room_waiting,
                 WaitToStart,
                 Trading,
                 ResultsWaitPage,
                 Results]

