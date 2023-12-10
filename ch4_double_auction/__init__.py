from otree.api import *
import time
import random

doc = "Double auction market"


class C(BaseConstants):
    NAME_IN_URL = "ch4_double_auction"
    PLAYERS_PER_GROUP = 200
    NUM_ROUNDS = 1
    ITEMS_PER_SELLER = 1
    VALUATION_MIN = 20
    VALUATION_MAX = 100
    PRODUCTION_COSTS_MIN = 10
    PRODUCTION_COSTS_MAX = 90
    buyer_value = [45, 40, 35, 30, 25, 20]
    seller_value = [3, 8, 13, 18, 23, 28]
    ideal_eqPrice = 24  # 理想値の均衡価格


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    players = subsession.get_players()
    i = 0
    for p in players:
        # if player's ID is not a multiple of 2, they are a buyer.
        # for more buyers, change the 2 to 3
        # 買い手かどうかを決定する
        p.is_buyer = p.id_in_group % 2 > 0
        if p.is_buyer:  #
            p.num_items = 0
            tmp = i % len(C.buyer_value)
            p.break_even_point = C.buyer_value[tmp]
            C.PLAYERS_PER_GROUP
            # p.break_even_point = random.randint(C.VALUATION_MIN, C.VALUATION_MAX)
            p.current_offer = 0
        else:
            p.num_items = C.ITEMS_PER_SELLER
            # p.break_even_point = random.randint(
            #     C.PRODUCTION_COSTS_MIN, C.PRODUCTION_COSTS_MAX
            # )
            tmp = i % len(C.buyer_value)
            p.break_even_point = C.seller_value[tmp]
            p.current_offer = C.VALUATION_MAX + 1
            i += 1


class Group(BaseGroup):
    # buyer_bids = models.StringField()  # 買い注文
    # seller_asks = models.StringField() # 売り注文
    start_timestamp = models.IntegerField()


class Player(BasePlayer):
    finish_frag = models.BooleanField(initial=False)
    is_buyer = models.BooleanField()
    break_even_point = models.IntegerField()
    num_items = models.IntegerField()
    total_payoff = models.IntegerField()
    offers = models.StringField(initial="")  # 注文
    offer_seconds = models.StringField(initial="")  # 注文時間
    offers_win = models.StringField(initial="")  # 取引成立時の注文
    partners = models.StringField(initial="")  # 取引相手
    prices = models.StringField(initial="")  # 取引価格
    seconds = models.StringField(initial="")  # 取引時間
    mili_seconds = models.FloatField(initial=0.0)  # 取引時間(グラフ用)
    current_offer = models.IntegerField()
    current_seconds = models.IntegerField()


class Transaction(ExtraModel):
    group = models.Link(Group)
    buyer = models.Link(Player)
    seller = models.Link(Player)
    price = models.CurrencyField()
    seconds = models.IntegerField(doc="Timestamp (seconds since beginning of trading)")


class offerRecord(ExtraModel):
    group = models.Link(Group)
    player = models.Link(Player)
    offer_price = models.CurrencyField()
    tradePrice = models.IntegerField()
    tradePartner = models.IntegerField()
    time = models.FloatField(doc="Timestamp (seconds since beginning of trading)")


# FUNCTIONS
def custom_export(players):
    # header row
    yield [
        "sessionID",
        "groupID",
        "round_number",
        "playerID",
        "is_buyer",
        "offer_price",
        "trade_price",
        "tradePartner",
        "time",
    ]

    scores = offerRecord.filter()
    for score in scores:
        player = score.player
        session = player.session
        yield [
            session.code,
            player.group.id_in_subsession,
            player.round_number,
            player.id_in_group,
            player.is_buyer,
            score.offer_price,
            score.tradePrice,
            score.tradePartner,
            score.time,
        ]


def live_method(player: Player, data):
    my_id = player.id_in_group
    group = player.group
    players = group.get_players()
    buyers = [p for p in players if p.is_buyer]
    sellers = [p for p in players if not p.is_buyer]
    news = None
    match = None

    # offer時の処理
    if data["offer_frag"] and player.finish_frag == False:
        seconds = int(time.time() - group.start_timestamp)
        mili_seconds = round(time.time() - group.start_timestamp, 3)
        offer = int(data["offer"])
        player.current_offer = offer
        player.current_seconds = seconds
        if len(player.offer_seconds) == 0:
            player.offer_seconds = str(seconds)
            player.offers = str(offer)
        else:
            player.offer_seconds = player.offer_seconds + "," + str(seconds)
            player.offers = player.offers + "," + str(offer)

        # 買い手の処理
        if player.is_buyer:
            prices = {p.id_in_group: p.current_offer for p in sellers}
            price = min(prices.values())

            # 取引成立時
            if price <= offer:
                second = {
                    p.offer_seconds: p.id_in_group
                    for p in sellers
                    if p.current_offer == price
                }
                partner = second[sorted(second)[0]]
                match = [player, group.get_player_by_id(partner)]

                # record
                offerRecord.create(
                    group=group,
                    player=player,
                    offer_price=offer,
                    tradePrice=price,
                    tradePartner=partner,
                    time=mili_seconds,
                )
            else:
                # record
                offerRecord.create(
                    group=group,
                    player=player,
                    offer_price=offer,
                    time=mili_seconds,
                )

        # 売り手の処理
        else:
            prices = {p.id_in_group: p.current_offer for p in buyers}
            price = max(prices.values())

            # 取引成立時
            if offer <= price and player.num_items > 0:
                second = {
                    p.offer_seconds: p.id_in_group
                    for p in buyers
                    if p.current_offer == price
                }
                partner = second[sorted(second)[0]]
                match = [group.get_player_by_id(partner), player]

                # record
                offerRecord.create(
                    group=group,
                    player=player,
                    offer_price=offer,
                    tradePrice=price,
                    tradePartner=partner,
                    time=mili_seconds,
                )
            else:
                # record
                offerRecord.create(
                    group=group,
                    player=player,
                    offer_price=offer,
                    time=mili_seconds,
                )

        # 取引成立
        if match is not None:  # find_match　が　空でなければ作動 #
            [buyer, seller] = match
            Transaction.create(
                group=group,
                buyer=buyer,
                seller=seller,
                price=price,
                seconds=seconds,
            )
            # 売手
            buyer.num_items += 1
            buyer.finish_frag = seller.num_items == 1  # 終了条件
            if len(buyer.offers_win) == 0:
                buyer.offers_win = str(buyer.current_offer)
                buyer.partners = str(seller.id_in_group)
                buyer.prices = str(price)
                buyer.seconds = str(seconds)
                buyer.mili_seconds = mili_seconds
            else:
                buyer.offers_win = "," + str(buyer.current_offer)
                buyer.partners = "," + str(seller.id_in_group)
                buyer.prices = "," + str(price)
                buyer.seconds = buyer.seconds + "," + str(seconds)
                buyer.mili_seconds = buyer.mili_seconds
            buyer.current_offer = 0
            # 買手
            seller.num_items -= 1
            seller.finish_frag = seller.num_items == 0  # 終了条件
            if len(seller.offers_win) == 0:
                seller.offers_win = str(seller.current_offer)
                seller.partners = str(buyer.id_in_group)
                seller.prices = str(price)
                seller.seconds = str(seconds)
                seller.mili_seconds = mili_seconds
            else:
                seller.offers_win = seller.offers_win + "," + str(seller.current_offer)
                seller.partners = seller.partners + "," + str(buyer.id_in_group)
                seller.prices = seller.prices + "," + str(price)
                seller.seconds = seller.seconds + "," + str(seconds)
                seller.mili_seconds = seller.mili_seconds
            seller.current_offer = C.VALUATION_MAX + 1

            buyer.payoff += buyer.break_even_point - price
            seller.payoff += price - seller.break_even_point
            news = dict(buyer=buyer.id_in_group, seller=seller.id_in_group, price=price)
    bids_dict = {p.id_in_group: p.current_offer for p in buyers if p.current_offer > 0}
    tmp = sorted(bids_dict.items(), key=lambda x: x[1], reverse=True)
    bids_dict = {i[0]: i[1] for i in tmp}

    asks_dict = {
        p.id_in_group: p.current_offer
        for p in sellers
        if p.current_offer <= C.VALUATION_MAX
    }
    tmp = sorted(asks_dict.items(), key=lambda x: x[1])
    asks_dict = {i[0]: i[1] for i in tmp}
    bids_player = [p for p in bids_dict]
    asks_player = [p for p in asks_dict]
    bids = [bids_dict[p] for p in bids_dict]
    asks = [asks_dict[p] for p in asks_dict]

    highcharts_series = [
        [tx.seconds, tx.price] for tx in Transaction.filter(group=group)
    ]
    results_series = [
        [tx.seconds, tx.price, tx.buyer.id_in_group, tx.seller.id_in_group]
        for tx in Transaction.filter(group=group)
    ]
    return {
        p.id_in_group: dict(
            player=my_id,
            num_items=p.num_items,
            current_offer=p.current_offer,
            payoff=p.payoff,
            bids_dict=bids_dict,
            bids=bids,
            bids_player=bids_player,
            asks_dict=asks_dict,
            asks=asks,
            asks_player=asks_player,
            highcharts_series=highcharts_series,
            news=news,
            partners=p.partners,
            prices=p.prices,
            finish_frag=p.finish_frag,
            results_series=results_series,
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
        return dict(num_sellers=len(sellers), num_buyers=len(buyers))

    @staticmethod
    def js_vars(player: Player):
        group = player.group
        players = group.get_players()
        buyers = [p for p in players if p.is_buyer]
        sellers = [p for p in players if not p.is_buyer]
        return dict(
            num_sellers=len(sellers),
            num_buyers=len(buyers),
            id_in_group=player.id_in_group,
            is_buyer=player.is_buyer,
            max_value=C.VALUATION_MAX,
        )

    @staticmethod
    def get_timeout_seconds(player: Player):
        group = player.group
        return (group.start_timestamp + 3 * 60) - time.time()


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.start_timestamp = int(time.time())


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # roundごとの変数dict
        # player_list = []
        p_list = []
        p_list2 = []
        for i in range(player.round_number):
            p = player.in_round(i + 1)
            players = p.group.get_players()

            # 役割
            if p.is_buyer:
                role = "買い手"
            else:
                role = "売り手"

            # 取引量
            buyer_offer = []  # buyerのofferリスト
            seller_offer = []  # sellerのofferリスト
            transact_cnt = 0  # 取引量
            for q in players:
                transact_cnt += q.finish_frag
                if q.prices != "":
                    if q.is_buyer:
                        buyer_offer.append(int(q.offers_win))
                    else:
                        seller_offer.append(int(q.offers_win))
            buyer_offer.sort(reverse=True)
            seller_offer.sort()
            transact_cnt //= 2  # 取引量

            # 均衡価格
            eq_cnt = -1  # 均衡価格となる量の初期値
            for j in range(len(buyer_offer)):
                if buyer_offer[j] < seller_offer[j]:
                    if j == 0:
                        eq_cnt = 0
                    else:
                        eq_cnt = j - 1
                    break

            if len(buyer_offer) == 0:
                eq_price = 0
            elif eq_cnt == -1:
                eq_price = (buyer_offer[-1] + seller_offer[-1]) // 2
            else:
                eq_price = (buyer_offer[eq_cnt] + seller_offer[eq_cnt]) // 2

            # 余剰の計算
            # prod_surplus = sum(buyer_offer) - len(buyer_offer)*eq_price
            # cons_surplus = len(seller_offer)*eq_price - sum(seller_offer)
            # total_surplus = prod_surplus + cons_surplus
            cons_surplus = 0
            prod_surplus = 0
            for p in players:
                if p.prices != "":
                    if p.is_buyer == True:
                        tmp = p.break_even_point - int(p.prices)
                        cons_surplus = cons_surplus + tmp
                    else:
                        tmp = int(p.prices) - p.break_even_point
                        prod_surplus = prod_surplus + tmp
            total_surplus = prod_surplus + cons_surplus

            # 利益の計算
            # if p.is_buyer:
            profit = p.payoff
            # else:
            #    profit = p.tax_payoff

            p_dict = dict(
                round=p.round_number,
                role=role,
                break_even_point=p.break_even_point,
                prices=p.prices,
                payoff=p.payoff,
                profit=profit,
            )
            p_dict2 = dict(
                round=p.round_number,
                eq_price=eq_price,
                prod_surplus=prod_surplus,
                cons_surplus=cons_surplus,
                total_surplus=total_surplus,
            )
            p_list.append(p_dict)
            p_list2.append(p_dict2)

            # 理想値の計算(均衡価格、余剰)
            ideal_prodSurplus = 0
            ideal_consSurplus = 0
            # for j in range(C.PLAYERS_PER_GROUP):
            #     tmp = j % len(C.buyer_value)
            #     ideal_prodSurplus += C.buyer_value[tmp] - C.ideal_eqPrice
            #     ideal_consSurplus += C.ideal_eqPrice - C.seller_value[tmp]
            # ideal_totalSurplus = ideal_prodSurplus + ideal_consSurplus

            buyer_count = 0
            seller_count = 0
            for p in players:
                if p.is_buyer:
                    tmp = buyer_count % len(C.buyer_value)
                    if C.buyer_value[tmp] > C.ideal_eqPrice:
                        print(tmp, C.buyer_value[tmp])
                        ideal_prodSurplus += C.buyer_value[tmp] - C.ideal_eqPrice
                    buyer_count = buyer_count + 1
                else:
                    tmp = seller_count % len(C.seller_value)
                    if C.seller_value[tmp] < C.ideal_eqPrice:
                        ideal_consSurplus += C.ideal_eqPrice - C.seller_value[tmp]
                    seller_count = seller_count + 1
            ideal_totalSurplus = ideal_prodSurplus + ideal_consSurplus

            # 理想値の余剰
            ideal_dict = dict(
                ideal_prodSurplus=ideal_prodSurplus,  # 理想値の生産者余剰
                ideal_consSurplus=ideal_consSurplus,  # 理想値の消費者余剰
                ideal_totalSurplus=ideal_totalSurplus,  # 理想値の総余剰
            )

            return dict(p_list=p_list, p_list2=p_list2, ideal_dict=ideal_dict)

        #     player_dict = dict(
        #         round=p.round_number,
        #         role = role,
        #         break_even_point=p.break_even_point,
        #         prices=p.prices,
        #         payoff=p.payoff,
        #         transact_cnt = transact_cnt,
        #         eq_price = eq_price,
        #         prod_surplus = prod_surplus,
        #         cons_surplus = cons_surplus,
        #         total_surplus = total_surplus,
        #         ideal_prodSurplus = ideal_prodSurplus, #理想値の生産者余剰
        #         ideal_consSurplus = ideal_consSurplus, #理想値の消費者余剰
        #         ideal_totalSurplus = ideal_totalSurplus #理想値の総余剰
        #     )
        #     player_list.append(player_dict)
        # return dict(player_list=player_list)

    @staticmethod
    def js_vars(player: Player):
        if player.is_buyer:
            return dict(Num=player.num_items)
        else:
            return dict(Num=C.ITEMS_PER_SELLER - player.num_items)

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        highcharts_series = [
            [tx.seconds, tx.price] for tx in Transaction.filter(group=group)
        ]
        players = group.get_players()

        # 需要と供給グラフ用の変数
        buyer_offer = []  # buyerのofferリスト
        seller_offer = []  # sellerのofferリスト
        highcharts_buyer = []
        highcharts_seller = []
        chart_time = []
        chart_buyer_seller = []
        for p in players:
            if p.prices != "":
                if p.is_buyer:
                    # buyer_offer.append(int(p.offers_win))
                    # highcharts_buyer.append([int(p.seconds), int(p.offers_win)])
                    buyer_offer.append(p.break_even_point)
                    highcharts_buyer.append([int(p.seconds), int(p.break_even_point)])
                    # 取引相手
                    pair_id = p.partners
                    # tmp = player.group.get_player_by_id(pair_id).offers_win
                    tmp = player.group.get_player_by_id(pair_id).break_even_point
                    print(tmp)
                    seller_offer.append(tmp)
                    highcharts_seller.append([int(p.seconds), int(tmp)])
                    tmp_pair = []
                    tmp_pair.append(int(p.mili_seconds))
                    tmp_pair.append(p.break_even_point)
                    tmp_pair.append(tmp)
                    chart_buyer_seller.append(tmp_pair)
        # 時間順に並び替える
        # print("時間前", chart_buyer_seller)
        # chart_buyer_seller = sorted(chart_buyer_seller, reverse=True, key=lambda x: x[2])
        # chart_buyer_seller = ([sorted(l) for l in chart_buyer_seller])
        chart_buyer_seller.sort()

        # print(chart_buyer_seller)
        for row in chart_buyer_seller:
            tmp = round(row.pop(0), 1)
            chart_time.append(tmp)
        print(chart_buyer_seller, chart_time)

        # for p in players:
        #     if p.prices != '':
        #         if p.is_buyer:
        #             buyer_offer.append(int(p.offers_win))
        #         else:
        #             seller_offer.append(int(p.offers_win))
        # buyer_offer.sort(reverse=True)
        # seller_offer.sort()
        # highcharts_buyer = [[0,0] for _ in range(len(buyer_offer))]
        # highcharts_seller = [[0,0] for _ in range(len(seller_offer))]
        # for i in range(len(buyer_offer)):
        #     highcharts_buyer[i] = [i+1,buyer_offer[i]]
        #     highcharts_seller[i] = [i+1,seller_offer[i]]
        #
        # 取引が無かったことを表すFlag．(取引なければTrue)
        if len(buyer_offer) == 0:
            noBuyer = True
        else:
            noBuyer = False

        # 最後のラウンドであることを示すFlag
        if p.round_number == C.NUM_ROUNDS:
            last_flag = True
        else:
            last_flag = False

        # 理想値の需要供給グラフ
        tmp_buyer = []
        tmp_seller = []
        for j in range(C.PLAYERS_PER_GROUP // 2):
            tmp_buyer.append(C.buyer_value[j % len(C.buyer_value)])
            tmp_seller.append(C.seller_value[j % len(C.seller_value)])
        # if C.buyer_value[j%len(C.buyer_value)] >= C.seller_value[j%len(C.seller_value)]:
        #    tmp_buyer.append(C.buyer_value[j%len(C.buyer_value)])
        #    tmp_seller.append(C.seller_value[j%len(C.seller_value)])
        tmp_buyer.sort(reverse=True)
        tmp_seller.sort()
        chart_idealBuyer = [[j, tmp_buyer[j]] for j in range(len(tmp_buyer))]
        chart_idealBuyer.append([len(tmp_buyer), tmp_buyer[-1]])
        chart_idealSeller = [[j, tmp_seller[j]] for j in range(len(tmp_seller))]
        chart_idealSeller.append([len(tmp_seller), tmp_seller[-1]])
        # 供給（税あり）
        print(chart_buyer_seller)
        # chart_idealBuyer = [[j+1,tmp_buyer[j]] for j in range(len(tmp_buyer))]
        # chart_idealSeller = [[j+1,tmp_seller[j]] for j in range(len(tmp_seller))]

        return {
            p.id_in_group: dict(
                highcharts_series=highcharts_series,
                highcharts_buyer=highcharts_buyer,
                highcharts_seller=highcharts_seller,
                last_flag=last_flag,
                noBuyer=noBuyer,
                chart_idealBuyer=chart_idealBuyer,
                chart_idealSeller=chart_idealSeller,
                chart_time=chart_time,
                chart_buyer_seller=chart_buyer_seller,
            )
            for p in players
        }


#  @staticmethod
#  def get_timeout_seconds(player: Player):
#      return (player.group.start_timestamp + 30) - time.time()


class Room_waiting(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Finish(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Room_waiting, WaitToStart, Trading, ResultsWaitPage, Results, Finish]
