from os import environ


SESSION_CONFIGS = [
    dict(
        name='ch1_1_risk',
        display_name="第一章：リスク",
        app_sequence=['b_inputid','ch1_1_risk'],
        num_demo_participants=1,
    ),
    dict(
        name='ch1_2_prisoner',
        display_name="第一章：囚人のジレンマ",
        app_sequence=['b_inputid','ch1_2_prisoner'],
        num_demo_participants=2,
    ),
    dict(
        name='ch2_1_coordination',
        display_name="第二章：調整ゲーム１",
        app_sequence=['b_inputid','ch2_1_coordination'],
        num_demo_participants=2,
    ),
    dict(
        name='ch2_2_coordination2',
        display_name="第二章：調整ゲーム２",
        app_sequence=['b_inputid','ch2_2_coordination2'],
        num_demo_participants=2,
    ),
    dict(
        name='ch2_3_chicken',
        display_name="第二章：チキンゲーム（同時手番）",
        app_sequence=['b_inputid','ch2_3_chicken'],
        num_demo_participants=2,
    ),
    dict(
        name='ch2_4_extensive',
        display_name="第二章：チキンゲーム（展開形）",
        app_sequence=['b_inputid','ch2_4_extensive'],
        num_demo_participants=2,
    ),
    dict(
        name='ch2_4_PK',
        display_name="第二章：PKゲーム",
        app_sequence=['b_inputid','ch2_4_PK'],
        num_demo_participants=2,
    ),
    dict(
        name='ch3_0_shortandlong',
        display_name="第三章：繰り返し",
        app_sequence=['b_inputid', 'ch3_0_shortandlong'],
        num_demo_participants=1,
    ),
    dict(
        name='ch3_1_repeated_oneshot',
        display_name="第三章：繰り返し(１回)",
        app_sequence=['b_inputid','ch3_1_repeated_oneshot'],
        num_demo_participants=2,
    ),
    dict(
        name='ch3_2_repeated_finite',
        display_name="第三章：繰り返し(有限)",
        app_sequence=['b_inputid','ch3_2_repeated_finite'],
        num_demo_participants=2,
    ),
    dict(
        name='ch3_3_repeated_infinite',
        display_name="第三章：繰り返し(無限回)",
        app_sequence=['b_inputid','ch3_3_repeated_infinite'],
        num_demo_participants=2,
    ),
    dict(
        name='ch3_4_public_goods_game',
        display_name="第三章：公共財ゲーム",
        app_sequence=['b_inputid','ch3_4_public_goods_game'],
        num_demo_participants=10,
    ),
    dict(
        name='ch3_5_time_discount',
        display_name="第三章：時間割引",
        app_sequence=['b_inputid', 'ch3_5_time_discount'],
        num_demo_participants=1,
    ),
    dict(
        name='ch4_double_auction',
        display_name="第四章：通常の市場",
        app_sequence=['b_inputid','ch4_double_auction'],
        num_demo_participants=200,
    ),
    dict(
        name='ch5_externality',
        display_name="第五章：公害のある市場",
        app_sequence=['b_inputid','ch5_externality'],
        num_demo_participants=200,
    ),
    dict(
        name='ch5_externality_tax',
        display_name="第五章：税のある市場",
        app_sequence=['b_inputid', 'ch5_externality_tax'],
        num_demo_participants=200,
    ),
    dict(
        name='ch6_individual',
        display_name='第六章：独占',
        app_sequence=['b_inputid', 'ch6_quiz', 'ch6_individual'],
        num_demo_participants=2,
        use_browser_bots=False
    ),
    dict(
        name='ch6_mutual',
        display_name='第六章：寡占',
        app_sequence=['b_inputid', 'ch6_quiz', 'ch6_mutual'],
        num_demo_participants=2,
        use_browser_bots=False
    ),
    dict(
        name='ch7_1_adverseSelection',
        display_name="第七章：逆選択",
        app_sequence=['b_inputid','ch7_1_adverseSelection'],
        num_demo_participants=12,
    ),
    dict(
        name='ch7_2_hiddenAction',
        display_name="第七章：隠された情報１",
        app_sequence=['b_inputid', 'ch7_2_hiddenAction'],
        num_demo_participants=2,
    ),
        dict(
        name='ch7_2_hiddenAction_nonlottery',
        display_name="第七章：隠された情報２",
        app_sequence=['b_inputid', 'ch7_2_hiddenAction_nonlottery'],
        num_demo_participants=2,
    ),
    dict(
       name='ch8_comparativeAdvantage1',
       display_name="第八章：自給自足",
       num_demo_participants=3,
       app_sequence=['b_inputid','ch8_comparativeAdvantage1_instruction', 'ch8_comparativeAdvantage1']
    ),
    dict(
       name='ch8_comparativeAdvantage2',
       display_name="第八章：同じタイプ",
       num_demo_participants=3,
       app_sequence=['b_inputid','ch8_comparativeAdvantage2_instruction', 'ch8_comparativeAdvantage2']
    ),
    dict(
       name='ch8_comparativeAdvantage3',
       display_name="第八章：全員と取引可能",
       num_demo_participants=3,
       app_sequence=['b_inputid','ch8_comparativeAdvantage3_instruction', 'ch8_comparativeAdvantage3']
    ),
    dict(
        name='ch9_matching_ia',
        display_name="第九章：IAマッチング",
        app_sequence=['b_inputid', 'ch9_matching_ia'],
        num_demo_participants=6,
    ),
    dict(
        name='ch9_matching_da',
        display_name="第九章：DAマッチング",
        app_sequence=['b_inputid', 'ch9_matching_da'],
        num_demo_participants=6,
    ),
    dict(
        name='ch9_firstprice',
        display_name="第九章：第一価格オークション",
        app_sequence=['b_inputid', 'ch9_auction_firstprice'],
        num_demo_participants=3,
    ),
    dict(
        name='ch9_secondprice',
        display_name="第九章：第二価格オークション",
        app_sequence=['b_inputid', 'ch9_auction_secondprice'],
        num_demo_participants=3,
    ),
    dict(
        name='ch10_1_individual_choice',
        display_name="第十章：個人の意思決定",
        app_sequence=['b_inputid', 'ch10_1_individual_choice'],
        num_demo_participants=1,
    ),
    dict(
        name='ch10_ultimatum',
        display_name="第十章：最後通牒",
        app_sequence=['b_inputid', 'ch10_2_ultimatum'],
        num_demo_participants=2,
    ),
    dict(
        name='ch10_dictator',
        display_name="第十章：独裁者",
        app_sequence=['b_inputid', 'ch10_3_dictator'],
        num_demo_participants=2,
    ),
    dict(
        name='ch10_4_extended_dictator',
        display_name="第十章：拡張版",
        app_sequence=['b_inputid', 'ch10_4_extended_dictator'],
        num_demo_participants=2,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = ['graph_data']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3436257800282'

INSTALLED_APPS = ['otree']
