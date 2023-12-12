import random
import time

from otree.api import *


class Constants(BaseConstants):
    name_in_url = "ch8_comparative_advantage2"
    players_per_group = None
    num_rounds = 3
    autoClearFlg = 1  # 成立後の注文全削除（1ならオン,-1ならオフ）
    timeout_question1 = 120
    timeout_question2 = 180
    timeout_question_result = 30
    working_hours = 20
    cheese_cost_A = 1
    bread_cost_A = 1.5
    cheese_cost_B = 3
    bread_cost_B = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    gameNum = models.IntegerField(initial=0)
    start_time = models.FloatField(initial=0)


class Player(BasePlayer):
    buyCount = models.IntegerField(initial=0)
    sellCount = models.IntegerField(initial=0)
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


# Scoreには取引ごとの記録が蓄積される
class Score(ExtraModel):
    player = models.Link(Player)
    price = models.IntegerField()  # 提案価格
    order_type = models.StringField()  # sell or buy
    time = models.FloatField()  # 取引時刻
    tradePrice = models.IntegerField()  # 取引価格
    tradePartner = models.IntegerField()  # 取引相手


# FUNCTIONS
def custom_export(players):
    # header row
    yield [
        "sessionID",
        "groupID",
        "round_number",
        "playerID",
        "player_type",
        "price",
        "order_type",
        "Gamenumber",
        "time",
        "tradePrice",
        "tradePartner",
    ]

    scores = Score.filter()
    for score in scores:
        player = score.player
        session = player.session
        Gamenumber = 2
        yield [
            session.code,
            player.group.id_in_subsession,
            player.round_number,
            player.id_in_group,
            player.player_type,
            score.price,
            score.order_type,
            Gamenumber,
            score.time,
            score.tradePrice,
            score.tradePartner,
        ]


def nextGame(group: Group):
    group.gameNum += 1


def init_player(group: Group):
    players = group.get_players()
    for p in players:
        p.player_type = "A" if p.id_in_subsession % 3 == 1 else "B"


# def init_group(group: Group):
#    if group.id_in_subsession == 1:
#        players = group.get_players()
#        for p in players:
#            p.player_type = 'A'
#    else:
#        players = group.get_players()
#        for p in players:
#            p.player_type = 'B'


def compute(group: Group):
    players = group.get_players()
    for p in players:
        for num in range(p.bread):
            kakuritu = random.random()
            if kakuritu >= 0.5:
                p.cheese += 20
            p.buyCount = 0
            p.sellCount = 0


def computeResult(group: Group):
    players = group.get_players()
    for p in players:
        if p.cheese < p.bread:
            p.payoff = p.cheese
        else:
            p.payoff = p.bread
        # point = p.cheese/500
        # p.payoff = c(point*2)


# def set_payoffs(group: Group):
#    for p in group.get_players():
#        point = c(p.cheese / 500)
#        p.payoff = c(point * 2)


def live_bid(player: Player, data):
    if player.player_type != data["player_type"]:
        return
    transaction_time = round(time.time() - player.group.start_time, 2)
    syubetu = data["type"]  # 買い手か売り手か
    player.session.vars["1"] = 1
    myID = player.id_in_group
    yourID = -1
    players = player.get_others_in_group()
    seiritu = 1
    torihikigaku = -1
    tmpSell = 0
    buyValue = -1
    sell = 0
    buy = 0
    currentKey = ""
    timeValue = time.time()
    # seirituPlayer = self
    group = player.group
    gameNumber = group.gameNum
    closedTransaction = False
    value = data["value"]
    if syubetu == "buy" and data["buyOffer_flg"] == False:
        for p in players:
            if p.player_type != data["player_type"]:
                continue
            loopRange = p.sellCount
            for num in range(loopRange):
                compID = str(p.id_in_group) + "_sell_" + str(num)
                tmpSell = p.session.vars[compID]
                if closedTransaction:
                    # 取引が成立する売値を見つけた後にまた取引が成立する売値を見つけたとき
                    if value >= tmpSell:
                        # 今見てる値のほうが後に入力されたとき
                        if (
                            player.session.vars[currentKey + "_time"]
                            > player.session.vars[compID + "_time"]
                        ):
                            sell = tmpSell
                            currentKey = compID
                            yourID = p.id_in_group
                    # if(tmpSell < sell):
                    #    sell=tmpSell
                    #    currentKey = compID
                    # currentKey=compID
                    #    yourID = p.id_in_group
                    # elif(tmpSell==sell):
                    #    if(self.session.vars[currentKey+'_time']>self.session.vars[compID+'_time']):#今見てる値のほうが後に入力されたとき
                    #        sell=tmpSell
                    #        currentKey=compID
                    #        yourID = p.id_in_group

                # 買いの値段のほうが高かった時
                elif value >= tmpSell:
                    sell = tmpSell
                    yourID = p.id_in_group
                    currentKey = compID
                    closedTransaction = True
                    buyValue = value
        if closedTransaction == False:
            dictID = str(myID) + "_buy_" + str(player.buyCount)
            dictID_time = (
                str(myID) + "_buy_" + str(player.buyCount) + "_time"
            )  # タイムスタンプを追加
            player.session.vars[dictID] = value
            player.session.vars[dictID_time] = time.time()
            timeValue = player.session.vars[dictID_time]
            player.buyCount += 1
            seiritu = 0
        else:
            for p in players:
                if p.player_type != data["player_type"]:
                    continue
                if p.id_in_group == yourID:
                    p.cheese = round(p.cheese + sell, 2)  # 相手の現金に買った分を足す
                    p.bread -= 1  # 資産が1つ減る
                    if Constants.autoClearFlg == 1:
                        p.sellCount = 0
                        p.buyCount = 0
                        player.sellCount = 0
                        player.buyCount = 0
                    else:
                        p.sellCount -= 1
                        flg = False
                        for num in range(p.sellCount + 1):
                            compID = str(p.id_in_group) + "_sell_" + str(num)
                            if flg:
                                prvSellValue = (
                                    str(p.id_in_group) + "_sell_" + str(num - 1)
                                )
                                p.session.vars[prvSellValue] = p.session.vars[compID]
                                p.session.vars[prvSellValue + "_time"] = p.session.vars[
                                    compID + "_time"
                                ]
                            elif p.session.vars[compID] == sell:
                                flg = True
            torihikigaku = sell
            player.cheese = round(player.cheese - sell, 2)  # 自分の現金から買った分を引く
            player.bread += 1  # 資産が1つ増える
            closedTransaction = True
        response = dict(
            formSyubetu="buy",
            formData=value,
            seiritu=seiritu,
            formInputPlayerID=myID,
            seirituAitePlayerID=yourID,
            torihikigaku=torihikigaku,
            buyValue=buyValue,
            time=timeValue,
            sellValue=sell,
            player_type=player.player_type,
        )
        print("yourID:", yourID, type(yourID))
        if seiritu:
            Score.create(
                player=player,
                price=value,
                order_type="buy",
                time=transaction_time,
                tradePrice=torihikigaku,
                tradePartner=yourID,
            )
        else:
            Score.create(
                player=player,
                price=value,
                order_type="buy",
                time=transaction_time,
            )
        print(response)
        # self.buyCount += 1
        return {0: response}
    elif syubetu == "sell":
        for p in players:
            if p.player_type != data["player_type"]:
                continue
            loopRange = p.buyCount
            for num in range(loopRange):
                compID = str(p.id_in_group) + "_buy_" + str(num)
                tmpBuy = p.session.vars[compID]
                if closedTransaction:
                    if value <= tmpBuy:
                        if (
                            player.session.vars[currentKey + "_time"]
                            > player.session.vars[compID + "_time"]
                        ):  # 今見てる値のほうが後に入力されたとき
                            buy = tmpBuy
                            buyValue = buy
                            currentKey = compID
                            yourID = p.id_in_group

                elif value <= tmpBuy:  # 買いの値段のほうが高かった時
                    buy = tmpBuy
                    currentKey = compID
                    yourID = p.id_in_group
                    buyValue = buy
                    closedTransaction = True
        if closedTransaction == False:
            dictID = str(myID) + "_sell_" + str(player.sellCount)
            dictID_time = (
                str(myID) + "_sell_" + str(player.sellCount) + "_time"
            )  # タイムスタンプを追加
            player.session.vars[dictID] = value
            player.session.vars[dictID_time] = time.time()
            timeValue = player.session.vars[dictID_time]
            player.sellCount += 1
            seiritu = 0
        else:
            for p in players:
                if p.player_type != data["player_type"]:
                    continue
                if p.id_in_group == yourID:
                    p.cheese = round(p.cheese - buyValue, 2)  # 相手の現金に買った分を足す
                    p.bread += 1  # 資産が1つ減る
                    if Constants.autoClearFlg == 1:
                        p.sellCount = 0
                        p.buyCount = 0
                        player.sellCount = 0
                        player.buyCount = 0
                    else:
                        p.buyCount -= 1  #
                        flg = False
                        for num in range(p.buyCount + 1):
                            compID = str(p.id_in_group) + "_buy_" + str(num)
                            if flg:
                                prvBuyValue = (
                                    str(p.id_in_group) + "_buy_" + str(num - 1)
                                )
                                p.session.vars[prvBuyValue] = p.session.vars[compID]
                                p.session.vars[prvBuyValue + "_time"] = p.session.vars[
                                    compID + "_time"
                                ]
                            elif p.session.vars[compID] == buyValue:
                                flg = True
            torihikigaku = buyValue
            player.cheese = round(player.cheese + buyValue, 2)  # 自分の現金から買った分を引く
            player.bread -= 1  # 資産が1つ増える
        response = dict(
            formSyubetu="sell",
            formData=value,
            seiritu=seiritu,
            formInputPlayerID=myID,
            seirituAitePlayerID=yourID,
            torihikigaku=torihikigaku,
            buyValue=buyValue,
            time=timeValue,
            sellValue=value,
            player_type=player.player_type,
        )  # 買い注文buyValue
        print(response)
        if seiritu:
            Score.create(
                player=player,
                price=value,
                order_type="sell",
                time=transaction_time,
                tradePrice=torihikigaku,
                tradePartner=yourID,
            )
        else:
            Score.create(
                player=player, price=value, order_type="sell", time=transaction_time
            )

        return {0: response}

    # 入力がわがbuyかsellか
    elif syubetu == "buy_clear" and data["clearBuyer_flg"] == True:  # 買い手の消去
        flg = False
        if player.id_in_group == data["id"]:
            flg = False
            for num in range(player.buyCount):
                compID = str(player.id_in_group) + "_buy_" + str(num)
                if flg:
                    prvBuyValue = str(player.id_in_group) + "_buy_" + str(num - 1)
                    player.session.vars[prvBuyValue] = player.session.vars[compID]
                    player.session.vars[prvBuyValue + "_time"] = player.session.vars[
                        compID + "_time"
                    ]
                elif (
                    player.session.vars[compID] == data["value"]
                    and player.session.vars[compID + "_time"] == data["time"]
                ):  # 時間と値が同じだったら
                    flg = True
                else:
                    print("value:" + str(player.session.vars[compID]))
        if flg == False:
            seiritu = -2
            print("value:" + str(data["value"]) + ",time:" + str(data["time"]))
            print("sellcount" + str(player.buyCount))
            print(player.session.vars)
        else:
            seiritu = -1
            player.buyCount -= 1
        response = dict(
            formSyubetu="buy_clear",
            formData=data["value"],
            seiritu=seiritu,
            formInputPlayerID=data["id"],
            seirituAitePlayerID=-1,
            torihikigaku=-1,
            buyValue=-1,
            time=data["time"],
            player_type=player.player_type,
        )
        Score.create(
            player=player, price=value, order_type="buy_delete", time=transaction_time
        )
        print(response)
        return {0: response}
    elif syubetu == "sell_clear" and data["clearSeller_flg"] == True:  # 売り手の消去
        flg = False
        if player.id_in_group == data["id"]:
            flg = False
            for num in range(player.sellCount):
                compID = str(player.id_in_group) + "_sell_" + str(num)
                if flg:
                    prvSellValue = str(player.id_in_group) + "_sell_" + str(num - 1)
                    player.session.vars[prvSellValue] = player.session.vars[compID]
                    player.session.vars[prvSellValue + "_time"] = player.session.vars[
                        compID + "_time"
                    ]
                elif (
                    player.session.vars[compID] == data["value"]
                    and player.session.vars[compID + "_time"] == data["time"]
                ):  # 時間と値が同じだったら
                    flg = True
        if flg == False:
            seiritu = -2
            print("value:" + str(data["value"]) + ",time:" + str(data["time"]))
            print("sellcount" + str(player.sellCount))
            print(player.session.vars)
        else:
            seiritu = -1
            player.sellCount -= 1
        response = dict(
            formSyubetu="sell_clear",
            formData=data["value"],
            seiritu=seiritu,
            formInputPlayerID=data["id"],
            seirituAitePlayerID=-1,
            torihikigaku=-1,
            buyValue=-1,
            time=data["time"],
            player_type=player.player_type,
        )
        Score.create(
            player=player, price=value, order_type="sell_delete", time=transaction_time
        )
        print(response)
        return {0: response}
    return {0: str(value)}


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
        if (
            len(str(values["bread"]).split(".")[1]) != 1
            or len(str(values["cheese"]).split(".")[1]) != 1
        ):
            return "小数点以下1桁までで入力してください"
        if player.player_type == "A":
            if (
                round(
                    values["bread"] * Constants.bread_cost_A
                    + values["cheese"] * Constants.cheese_cost_A
                )
                != Constants.working_hours
            ):
                return "20時間丁度になるように入力してください"
        elif player.player_type == "B":
            if (
                round(
                    values["bread"] * Constants.bread_cost_B
                    + values["cheese"] * Constants.cheese_cost_B
                )
                != Constants.working_hours
            ):
                return "20時間丁度になるように入力してください"


class Game(Page):
    live_method = live_bid
    timeout_seconds = Constants.timeout_question2

    @staticmethod
    def js_vars(player: Player):
        return dict(
            id_in_group=player.id_in_group,
            player_type=player.player_type,
            cheese=player.cheese,
            bread=player.bread,
            autoClearFlg=Constants.autoClearFlg,
        )


class waitpage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        nextGame(group)
        group.start_time = time.time()


class preResultsPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        computeResult(group)


class Results(Page):
    timeout_seconds = Constants.timeout_question_result


page_sequence = [Init, Screen1, waitpage, Game, preResultsPage, Results]
