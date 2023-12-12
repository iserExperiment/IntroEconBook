from otree.api import *


doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch6_quiz"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    INSTRUCTIONS1_TEMPLATE = "ch6_quiz/instruction1.html"
    INSTRUCTIONS2_TEMPLATE = "ch6_quiz/Instruction2.html"

    A1 = "売り手"
    A2 = "何個でも売れるだけ"
    A3 = "購入しない"
    A4 = "販売価格が19"
    A5 = "50"
    A6 = "-10"
    A7 = "0人または5人"

    K1 = "あなたは(a) 売り手になります。買い手はコンピュータです。"
    K2 = "あなたは、１回あたり(b) 何個でも売れるだけの商品を販売できます。"
    K3 = "買い手は利得（= 商品評価額− 販売価格）が1 以上となる場合しか購入しないので、10 の商品の価値を持っていて販売価格が10 であれば利得が0 となり(b) 購入しません。"
    K4 = "買い手は利得（= 商品評価額− 販売価格）が1 以上となる場合しか購入しません。商品の価値が20 の買い手は(c) 販売価格が19 であれば1 の利得を得ることができるので購入します。"
    K5 = "あなた（売り手）の利得は、（販売価格− 費用）× 販売個なので、(15 − 10) × 10 = 50 となります。"
    K6 = "あなた（売り手）の利得は、（販売価格− 費用）× 販売個なので、(9 − 10) × 10 = −10 となります。"
    K7 = "最安値で販売している売り手が複数いる場合は、ランダムにそのうちのどちらか1 人から購入するので 0 人または5人です"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # あなたはどちらの役割になりますか？
    q1 = models.StringField(
        choices=[["売り手", "売り手"], ["買い手", "買い手"]],
        label="（1）あなたはどちらの役割になりますか？",
        widget=widgets.RadioSelect,
    )

    # あなたは、１回あたり何個の商品を販売することができますか？
    q2 = models.StringField(
        choices=[["1個", "1個"], ["何個でも売れるだけ", "何個でも売れるだけ"]],
        label="（2）あなたは、１回あたり何個の商品を販売することができますか？",
        widget=widgets.RadioSelect,
    )

    # 買い手がひとりいて、彼にとっての商品の価値が10 だったとし
    # ます。売り手があなたしかおらず、販売価格を10 と設定した場
    # 合、買い手は購入しますか？
    q3 = models.StringField(
        choices=[["購入する", "購入する"], ["購入しない", "購入しない"]],
        label="（3）買い手がひとりいて、彼にとっての商品の価値が10 だったとします。売り手があなたしかおらず、販売価格を10 と設定した場合、買い手は購入しますか？",
        widget=widgets.RadioSelect,
    )

    # 商品の価値が20 の買い手は、次のどの場合で、商品を購入しますか？売り手は1 人しかいないとします。
    q4 = models.StringField(
        choices=[
            ["販売価格が20", "販売価格が20"],
            ["販売価格が21", "販売価格が21"],
            ["販売価格が19", "販売価格が19"],
        ],
        label="（4）商品の価値が20 の買い手は、次のどの場合で、商品を購入しますか？売り手は1 人しかいないとします。",
        widget=widgets.RadioSelect,
    )

    # あなたの商品の1 個当たりの費用が10 だとします。販売価格15で、10 個の商品を売却した場合の利得はいくらですか？
    q5 = models.StringField(
        choices=[["50", "50"], ["60", "60"], ["70", "70"]],
        label="（5）あなたの商品の1 個当たりの費用が10 だとします。販売価格15で、10 個の商品を売却した場合の利得はいくらですか？",
        widget=widgets.RadioSelect,
    )

    # あなたの商品の1 個当たりの費用が10 だとします。販売価格9で、10 個の商品を売却した場合の利得はいくらですか？
    q6 = models.StringField(
        choices=[["-1", "-1"], ["-10", "-10"], ["-100", "-100"]],
        label="（6）あなたの商品の1 個当たりの費用が10 だとします。販売価格9で、10 個の商品を売却した場合の利得はいくらですか？",
        widget=widgets.RadioSelect,
    )

    # 売り手が二人いる場合を考えます。買い手が5 人いるとします。あなたも相手も同じ販売価格としたときに、買い手は何人あなたから購入する可能性がありますか？当てはまるものをすべて選んでください。
    q7 = models.StringField(
        choices=[
            ["0人または5人", "0人または5人"],
            ["1人または4人", "1人または4人"],
            ["2人または3人", "2人または3人"],
        ],
        label="（7）売り手が二人いる場合を考えます。買い手が5 人いるとします。あなたも相手も同じ販売価格としたときに、買い手は何人あなたから購入する可能性がありますか？当てはまる組み合わせを選んでください。",
        # widget=widgets.CheckboxInput
    )


# PAGES-----
class Introduction(Page):
    timeout_seconds = 40


class quizPage(Page):
    form_model = "player"
    form_fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]
    timeout_seconds = 270


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    timeout_seconds = 120


page_sequence = [Introduction, quizPage, ResultsWaitPage, Results]
