from otree.api import *
import copy


doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch9_matching_da"
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 1

    MATCHING = "DA"
    INSTRUCTIONS_TEMPLATE = "ch9_matching_da/instructions.html"

    # ロール：名前を _ROLE で終わらせます:次に、oTreeはそれぞれの role を異なるプレイヤーに自動的に割り当てます。:id_in_group による順番に従う。
    STUDENT_1_ROLE = "student1"
    STUDENT_2_ROLE = "student2"
    STUDENT_3_ROLE = "student3"
    STUDENT_4_ROLE = "student4"
    STUDENT_5_ROLE = "student5"
    STUDENT_6_ROLE = "student6"

    # 学生
    student = [
        STUDENT_1_ROLE,
        STUDENT_2_ROLE,
        STUDENT_3_ROLE,
        STUDENT_4_ROLE,
        STUDENT_5_ROLE,
        STUDENT_6_ROLE,
    ]
    # 先生
    teacher = ["A", "B", "C", "D", "E", "F"]
    # 定員
    capacity_lim = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 1, "F": 1}
    # 研究室の学生に対する選好
    teacher_choices = {
        "A": ["student6", "student5", "student3", "student2", "student1", "student4"],
        "B": ["student1", "student3", "student4", "student6", "student2", "student5"],
        "C": ["student6", "student1", "student2", "student3", "student5", "student4"],
        "D": ["student1", "student2", "student6", "student4", "student3", "student5"],
        "E": ["student2", "student6", "student1", "student5", "student4", "student3"],
        "F": ["student2", "student4", "student5", "student1", "student6", "student3"],
    }

    student_true_choices = {
        "student1": ["A", "E", "C", "B", "F", "D"],
        "student2": ["B", "C", "D", "F", "A", "E"],
        "student3": ["F", "A", "B", "C", "E", "D"],
        "student4": ["A", "B", "F", "D", "C", "E"],
        "student5": ["B", "F", "A", "E", "D", "C"],
        "student6": ["F", "D", "E", "A", "C", "B"],
    }

    # 研究室の学生に対する選好(表示用)
    teacher_true_choices = {
        "A": ["6", "5", "3", "2", "1", "4"],
        "B": ["1", "3", "4", "6", "2", "5"],
        "C": ["6", "1", "2", "3", "5", "4"],
        "D": ["1", "2", "6", "4", "3", "5"],
        "E": ["2", "6", "1", "5", "4", "3"],
        "F": ["2", "4", "5", "1", "6", "3"],
    }

    # 第1志望とマッチした時
    payoff_list = [0, 700, 550, 450, 400, 375, 350]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # グループでのマッチング結果
    student1Status = models.CharField()
    student2Status = models.CharField()
    student3Status = models.CharField()
    student4Status = models.CharField()
    student5Status = models.CharField()
    student6Status = models.CharField()


class Player(BasePlayer):
    # 個人結果
    partner = models.CharField()
    # 個人結果のランキング
    partner_index = models.IntegerField()
    # 提出した順位でのランキング
    submitted_partner_index = models.IntegerField()

    # プルダウンの選択肢 ここから
    student_first_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    student_second_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    student_third_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    student_fourth_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    student_fifth_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    student_sixth_choice = models.CharField(
        verbose_name="", choices=C.teacher, initial=None
    )

    individual_choice_comment = models.TextField(verbose_name="", initial=None)
    flg_non_input = models.IntegerField(initial=0)
    input_role_flg = models.IntegerField()

    true_telling_flg1 = models.IntegerField(initial=0)
    true_telling_flg2 = models.IntegerField(initial=0)
    true_telling_flg3 = models.IntegerField(initial=0)
    true_telling_flg4 = models.IntegerField(initial=0)
    true_telling_flg5 = models.IntegerField(initial=0)
    true_telling_flg6 = models.IntegerField(initial=0)


# FUNCTION------------------------------
def da_algorithm(
    group, student_choices, totyu_studentStatus, totyu_teacherStatus, student_choices1
):
    print("totyu_studentStatus", totyu_studentStatus, student_choices1)
    for s in C.student:
        if totyu_studentStatus[s] is None:  # 相手が決まっていない学生がいれば・・・
            t = student_choices1[s].pop(0)  # まだ断られていない学類の中で一番選好の高い学類に申し込む
            if len(totyu_teacherStatus[t]) < C.capacity_lim[t]:  # 定員に空きがあれば・・・
                totyu_teacherStatus[t].append(s)  # 先生のマッチング相手のリストに申し込んできた学生を追加
                totyu_studentStatus[s] = t  # 学生のマッチング相手を更新
            elif len(totyu_teacherStatus[t]) == C.capacity_lim[t]:  # 定員がいっぱいなら
                for x in totyu_teacherStatus[
                    t
                ]:  # 現在マッチしている学生の中で最も順位が低い学生をcurrentPartnerに
                    if totyu_teacherStatus[t].index(x) == 0:
                        currentPartner = x
                    elif C.teacher_choices[t].index(x) >= C.teacher_choices[t].index(
                        currentPartner
                    ):
                        currentPartner = x
                if C.teacher_choices[t].index(s) <= C.teacher_choices[t].index(
                    currentPartner
                ):  # currentPartnerより順位が高ければマッチング成功
                    totyu_teacherStatus[t].remove(currentPartner)  # currentPartnerを削除
                    totyu_studentStatus[
                        currentPartner
                    ] = None  # currentPartnerだった学生のマッチングを解除
                    totyu_teacherStatus[t].append(s)  # 先生のマッチング相手のリストに申し込んできた学生を追加
                    totyu_studentStatus[s] = t  # 学生のマッチング相手を更新
    if len([1 for y in totyu_studentStatus if totyu_studentStatus[y] is None]) != 0:
        da_algorithm(
            group,
            student_choices,
            totyu_studentStatus,
            totyu_teacherStatus,
            student_choices1,
        )
    else:
        # DAの結果を格納
        group.student1Status = totyu_studentStatus["student1"]
        group.student2Status = totyu_studentStatus["student2"]
        group.student3Status = totyu_studentStatus["student3"]
        group.student4Status = totyu_studentStatus["student4"]
        group.student5Status = totyu_studentStatus["student5"]
        group.student6Status = totyu_studentStatus["student6"]
    return True


def input_checks(group: Group):
    for p in group.get_players():
        input_check(p)

    print("-------------------------", group.get_player_by_role(C.STUDENT_1_ROLE))
    # preference listの形成
    student1_part = group.get_player_by_role(C.STUDENT_1_ROLE)
    student2_part = group.get_player_by_role(C.STUDENT_2_ROLE)
    student3_part = group.get_player_by_role(C.STUDENT_3_ROLE)
    student4_part = group.get_player_by_role(C.STUDENT_4_ROLE)
    student5_part = group.get_player_by_role(C.STUDENT_5_ROLE)
    student6_part = group.get_player_by_role(C.STUDENT_6_ROLE)

    student_choices = {
        C.STUDENT_1_ROLE: [
            student1_part.student_first_choice,
            student1_part.student_second_choice,
            student1_part.student_third_choice,
            student1_part.student_fourth_choice,
            student1_part.student_fifth_choice,
            student1_part.student_sixth_choice,
        ],
        C.STUDENT_2_ROLE: [
            student2_part.student_first_choice,
            student2_part.student_second_choice,
            student2_part.student_third_choice,
            student2_part.student_fourth_choice,
            student2_part.student_fifth_choice,
            student2_part.student_sixth_choice,
        ],
        C.STUDENT_3_ROLE: [
            student3_part.student_first_choice,
            student3_part.student_second_choice,
            student3_part.student_third_choice,
            student3_part.student_fourth_choice,
            student3_part.student_fifth_choice,
            student3_part.student_sixth_choice,
        ],
        C.STUDENT_4_ROLE: [
            student4_part.student_first_choice,
            student4_part.student_second_choice,
            student4_part.student_third_choice,
            student4_part.student_fourth_choice,
            student4_part.student_fifth_choice,
            student4_part.student_sixth_choice,
        ],
        C.STUDENT_5_ROLE: [
            student5_part.student_first_choice,
            student5_part.student_second_choice,
            student5_part.student_third_choice,
            student5_part.student_fourth_choice,
            student5_part.student_fifth_choice,
            student5_part.student_sixth_choice,
        ],
        C.STUDENT_6_ROLE: [
            student6_part.student_first_choice,
            student6_part.student_second_choice,
            student6_part.student_third_choice,
            student6_part.student_fourth_choice,
            student6_part.student_fifth_choice,
            student6_part.student_sixth_choice,
        ],
    }

    print("****student_choices************", student_choices)

    # [DAの中で使う]
    global student_choices1
    student_choices1 = copy.deepcopy(student_choices)

    # [学生のマッチング相手の初期値(誰ともマッチしていない状態)]
    global start_studentStatus
    start_studentStatus = {S: None for S in C.student}

    # [学校のマッチング相手の初期値(誰ともマッチしていない状態)]
    global start_teacherStatus
    start_teacherStatus = {T: [] for T in C.teacher}

    totyu_studentStatus = copy.deepcopy(start_studentStatus)

    totyu_teacherStatus = copy.deepcopy(start_teacherStatus)

    student_choices1 = copy.deepcopy(student_choices)

    # DAマッチング
    da_algorithm(
        group,
        student_choices,
        totyu_studentStatus,
        totyu_teacherStatus,
        student_choices1,
    )

    # 結果を格納
    for p in group.get_players():
        print("p.role", p.role)
        if p.role == C.STUDENT_1_ROLE:
            p.partner = group.student1Status
        elif p.role == C.STUDENT_2_ROLE:
            p.partner = group.student2Status
        elif p.role == C.STUDENT_3_ROLE:
            p.partner = group.student3Status
        elif p.role == C.STUDENT_4_ROLE:
            p.partner = group.student4Status
        elif p.role == C.STUDENT_5_ROLE:
            p.partner = group.student5Status
        elif p.role == C.STUDENT_6_ROLE:
            p.partner = group.student6Status
        # 提出した順位でのランキング
        tmp_list = student_choices[p.role]
        p.submitted_partner_index = tmp_list.index(p.partner) + 1
        # 真の希望順位でのランキング：真の希望順位でpayoffは支払い
        tmp_list = C.student_true_choices[p.role]
        print(p.partner, tmp_list)
        p.partner_index = tmp_list.index(p.partner) + 1
        p.payoff = C.payoff_list[p.partner_index]


def input_check(player: Player):
    if player.role == "student1":
        player.input_role_flg = 1
    elif player.role == "student2":
        player.input_role_flg = 2
    elif player.role == "student3":
        player.input_role_flg = 3
    elif player.role == "student4":
        player.input_role_flg = 4
    elif player.role == "student5":
        player.input_role_flg = 5
    elif player.role == "student6":
        player.input_role_flg = 6

    if player.student_first_choice == "":
        player.flg_non_input = 1
        if player.input_role_flg == 1:
            player.student_first_choice = C.student_true_choices["student1"][0]
            player.student_second_choice = C.student_true_choices["student1"][1]
            player.student_third_choice = C.student_true_choices["student1"][2]
            player.student_fourth_choice = C.student_true_choices["student1"][3]
            player.student_fifth_choice = C.student_true_choices["student1"][4]
            player.student_sixth_choice = C.student_true_choices["student1"][5]
        if player.input_role_flg == 2:
            player.student_first_choice = C.student_true_choices["student2"][0]
            player.student_second_choice = C.student_true_choices["student2"][1]
            player.student_third_choice = C.student_true_choices["student2"][2]
            player.student_fourth_choice = C.student_true_choices["student2"][3]
            player.student_fifth_choice = C.student_true_choices["student2"][4]
            player.student_sixth_choice = C.student_true_choices["student2"][5]
        if player.input_role_flg == 3:
            player.student_first_choice = C.student_true_choices["student3"][0]
            player.student_second_choice = C.student_true_choices["student3"][1]
            player.student_third_choice = C.student_true_choices["student3"][2]
            player.student_fourth_choice = C.student_true_choices["student3"][3]
            player.student_fifth_choice = C.student_true_choices["student3"][4]
            player.student_sixth_choice = C.student_true_choices["student3"][5]
        if player.input_role_flg == 4:
            player.student_first_choice = C.student_true_choices["student4"][0]
            player.student_second_choice = C.student_true_choices["student4"][1]
            player.student_third_choice = C.student_true_choices["student4"][2]
            player.student_fourth_choice = C.student_true_choices["student4"][3]
            player.student_fifth_choice = C.student_true_choices["student4"][4]
            player.student_sixth_choice = C.student_true_choices["student4"][5]
        if player.input_role_flg == 5:
            player.student_first_choice = C.student_true_choices["student5"][0]
            player.student_second_choice = C.student_true_choices["student5"][1]
            player.student_third_choice = C.student_true_choices["student5"][2]
            player.student_fourth_choice = C.student_true_choices["student5"][3]
            player.student_fifth_choice = C.student_true_choices["student5"][4]
            player.student_sixth_choice = C.student_true_choices["student5"][5]
        if player.input_role_flg == 6:
            player.student_first_choice = C.student_true_choices["student6"][0]
            player.student_second_choice = C.student_true_choices["student6"][1]
            player.student_third_choice = C.student_true_choices["student6"][2]
            player.student_fourth_choice = C.student_true_choices["student6"][3]
            player.student_fifth_choice = C.student_true_choices["student6"][4]
            player.student_sixth_choice = C.student_true_choices["student6"][5]

    tmp = player.role
    if player.student_first_choice == C.student_true_choices[tmp][0]:
        player.true_telling_flg1 = 1
    if player.student_second_choice == C.student_true_choices[tmp][1]:
        player.true_telling_flg2 = 1
    if player.student_third_choice == C.student_true_choices[tmp][2]:
        player.true_telling_flg3 = 1
    if player.student_fourth_choice == C.student_true_choices[tmp][3]:
        player.true_telling_flg4 = 1
    if player.student_fifth_choice == C.student_true_choices[tmp][4]:
        player.true_telling_flg5 = 1
    if player.student_sixth_choice == C.student_true_choices[tmp][5]:
        player.true_telling_flg6 = 1


# Page --------------------------------------------------
class Introduction(Page):
    timeout_seconds = 30


class Students(Page):
    timeout_seconds = 330
    form_model = "player"
    form_fields = [
        "student_first_choice",
        "student_second_choice",
        "student_third_choice",
        "student_fourth_choice",
        "student_fifth_choice",
        "student_sixth_choice",
        "individual_choice_comment",
    ]

    @staticmethod
    # 重複チェック
    def error_message(self, values):
        if values["student_first_choice"] == values["student_second_choice"]:
            return "第一希望と第二希望が重複しています。"
        elif values["student_first_choice"] == values["student_third_choice"]:
            return "第一希望と第三希望が重複しています。"
        elif values["student_first_choice"] == values["student_fourth_choice"]:
            return "第一希望と第四希望が重複しています。"
        elif values["student_first_choice"] == values["student_fifth_choice"]:
            return "第一希望と第五希望が重複しています。"
        elif values["student_first_choice"] == values["student_sixth_choice"]:
            return "第一希望と第六希望が重複しています。"
        elif values["student_second_choice"] == values["student_third_choice"]:
            return "第二希望と第三希望が重複しています。"
        elif values["student_second_choice"] == values["student_fourth_choice"]:
            return "第二希望と第四希望が重複しています。"
        elif values["student_second_choice"] == values["student_fifth_choice"]:
            return "第二希望と第五希望が重複しています。"
        elif values["student_second_choice"] == values["student_sixth_choice"]:
            return "第二希望と第六希望が重複しています。"
        elif values["student_third_choice"] == values["student_fourth_choice"]:
            return "第三希望と第四希望が重複しています。"
        elif values["student_third_choice"] == values["student_fifth_choice"]:
            return "第三希望と第五希望が重複しています。"
        elif values["student_third_choice"] == values["student_sixth_choice"]:
            return "第三希望と第六希望が重複しています。"
        elif values["student_fourth_choice"] == values["student_fifth_choice"]:
            return "第四希望と第五希望が重複しています。"
        elif values["student_fourth_choice"] == values["student_sixth_choice"]:
            return "第四希望と第六希望が重複しています。"
        elif values["student_fifth_choice"] == values["student_sixth_choice"]:
            return "第五希望と第六希望が重複しています。"


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = input_checks


class Results(Page):
    pass


page_sequence = [Introduction, Students, ResultsWaitPage, Results]
