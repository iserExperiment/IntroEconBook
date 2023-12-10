from os import environ


SESSION_CONFIGS = [
    dict(
        name="ch1_1_risk",
        display_name="第1章：個人の意思決定(リスクあり)",
        app_sequence=["b_input_id", "ch1_1_risk"],
        num_demo_participants=1,
    ),
    dict(
        name="ch1_2_prisoner",
        display_name="第1章：囚人のジレンマ",
        app_sequence=["b_input_id", "ch1_2_prisoner"],
        num_demo_participants=2,
    ),
    dict(
        name="ch2_1_coordination",
        display_name="第2章：調整ゲーム１",
        app_sequence=["b_input_id", "ch2_1_coordination"],
        num_demo_participants=2,
    ),
    dict(
        name="ch2_2_coordination2",
        display_name="第2章：調整ゲーム２",
        app_sequence=["b_input_id", "ch2_2_coordination2"],
        num_demo_participants=2,
    ),
    dict(
        name="ch2_3_chicken",
        display_name="第2章：チキンゲーム（同時手番）",
        app_sequence=["b_input_id", "ch2_3_chicken"],
        num_demo_participants=2,
    ),
    dict(
        name="ch2_4_extensive",
        display_name="第2章：チキンゲーム（展開形）",
        app_sequence=["b_input_id", "ch2_4_extensive"],
        num_demo_participants=2,
    ),
    dict(
        name="ch2_4_PK",
        display_name="第2章：PKゲーム",
        app_sequence=["b_input_id", "ch2_4_PK"],
        num_demo_participants=2,
    ),
    dict(
        name="ch3_0_shortandlong",
        display_name="第3章：個人の意思決定",
        app_sequence=["b_input_id", "ch3_0_shortandlong"],
        num_demo_participants=1,
    ),
    dict(
        name="ch3_1_repeated_oneshot",
        display_name="第3章：繰り返しゲーム(１回)",
        app_sequence=["b_input_id", "ch3_1_repeated_oneshot"],
        num_demo_participants=2,
    ),
    dict(
        name="ch3_2_repeated_finite",
        display_name="第3章：繰り返しゲーム(有限)",
        app_sequence=["b_input_id", "ch3_2_repeated_finite"],
        num_demo_participants=2,
    ),
    dict(
        name="ch3_3_repeated_infinite",
        display_name="第3章：繰り返しゲーム(無限)",
        app_sequence=["b_input_id", "ch3_3_repeated_infinite"],
        num_demo_participants=2,
    ),
    dict(
        name="ch3_4_public_goods_game",
        display_name="第3章：公共財",
        app_sequence=["b_input_id", "ch3_4_public_goods_game"],
        num_demo_participants=10,
    ),
    dict(
        name="ch3_5_time_discount",
        display_name="第3章：時間割引",
        app_sequence=["b_input_id", "ch3_5_time_discount"],
        num_demo_participants=1,
    ),
    dict(
        name="ch4_double_auction",
        display_name="第4章：通常の市場",
        app_sequence=["b_input_id", "ch4_double_auction"],
        num_demo_participants=200,
    ),
    dict(
        name="ch5_externality",
        display_name="第5章：公害のある市場",
        app_sequence=["b_input_id", "ch5_externality"],
        num_demo_participants=200,
    ),
    dict(
        name="ch5_externality_tax",
        display_name="第5章：税のある市場",
        app_sequence=["b_input_id", "ch5_externality_tax"],
        num_demo_participants=200,
    ),
    dict(
        name="ch6_individual",
        display_name="第6章：独占",
        app_sequence=["b_input_id", "ch6_quiz", "ch6_individual"],
        num_demo_participants=2,
        use_browser_bots=False,
    ),
    dict(
        name="ch6_mutual",
        display_name="第6章：寡占",
        app_sequence=["b_input_id", "ch6_quiz", "ch6_mutual"],
        num_demo_participants=2,
        use_browser_bots=False,
    ),
    dict(
        name="ch7_1_adverse_selection",
        display_name="第7章：逆選択",
        app_sequence=["b_input_id", "ch7_1_adverse_selection"],
        num_demo_participants=12,
    ),
    dict(
        name="ch7_2_hidden_action",
        display_name="第7章：隠された情報１",
        app_sequence=["b_input_id", "ch7_2_hidden_action"],
        num_demo_participants=2,
    ),
    dict(
        name="ch7_2_hidden_action_nonlottery",
        display_name="第7章：隠された情報２",
        app_sequence=["b_input_id", "ch7_2_hidden_action_nonlottery"],
        num_demo_participants=2,
    ),
    dict(
        name="ch8_comparative_advantage1",
        display_name="第8章：比較優位（自給自足）",
        num_demo_participants=3,
        app_sequence=[
            "b_input_id",
            "ch8_comparative_advantage1_instruction",
            "ch8_comparative_advantage1",
        ],
    ),
    dict(
        name="ch8_comparative_advantage2",
        display_name="第8章：比較優位（同じタイプ）",
        num_demo_participants=3,
        app_sequence=[
            "b_input_id",
            "ch8_comparative_advantage2_instruction",
            "ch8_comparative_advantage2",
        ],
    ),
    dict(
        name="ch8_comparativeAdvantage3",
        display_name="第8章：比較優位（全員と取引可能）",
        num_demo_participants=3,
        app_sequence=[
            "b_input_id",
            "ch8_comparative_advantage3_instruction",
            "ch8_comparative_advantage3",
        ],
    ),
    dict(
        name="ch9_auction_firstprice",
        display_name="第9章：第一価格オークション",
        app_sequence=["b_input_id", "ch9_auction_firstprice"],
        num_demo_participants=3,
    ),
    dict(
        name="ch9_auction_secondprice",
        display_name="第9章：第二価格オークション",
        app_sequence=["b_input_id", "ch9_auction_secondprice"],
        num_demo_participants=3,
    ),
    dict(
        name="ch9_matching_ia",
        display_name="第9章：IAマッチング",
        app_sequence=["b_input_id", "ch9_matching_ia"],
        num_demo_participants=6,
    ),
    dict(
        name="ch9_matching_da",
        display_name="第9章：DAマッチング",
        app_sequence=["b_input_id", "ch9_matching_da"],
        num_demo_participants=6,
    ),
    dict(
        name="ch10_1_individual_choice",
        display_name="第10章：個人の意思決定（プロスペクト）",
        app_sequence=["b_input_id", "ch10_1_individual_choice"],
        num_demo_participants=1,
    ),
    dict(
        name="ch10_2_ultimatum",
        display_name="第10章：最後通牒ゲーム",
        app_sequence=["b_input_id", "ch10_2_ultimatum"],
        num_demo_participants=2,
    ),
    dict(
        name="ch10_3_dictator",
        display_name="第10章：独裁者ゲーム",
        app_sequence=["b_input_id", "ch10_3_dictator"],
        num_demo_participants=2,
    ),
    dict(
        name="ch10_4_extended_dictator",
        display_name="第10章：拡張版独裁者ゲーム",
        app_sequence=["b_input_id", "ch10_4_extended_dictator"],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = ["graph_data"]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "ja"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True

ROOMS = [
    dict(
        name="econ101",
        display_name="Econ 101 class",
        participant_label_file="_rooms/econ101.txt",
    ),
    dict(name="live_demo", display_name="Room for live demo (no participant labels)"),
]

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = "3436257800282"

INSTALLED_APPS = ["otree"]
