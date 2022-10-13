from otree.api import *

doc = """
Quiz with explanation. Re-display the previous page's form as read-only, with answers/explanation.
"""


class Constants(BaseConstants):
    name_in_url = 'quiz_with_explanation'
    players_per_group = None
    num_rounds = 1
    form_template = __name__ + '/form.html'
    progress_template = __name__ + '/progress.html'
    true_false_choices = [(1, 'True'), (0, 'False')]
    quiz_payoff = 0.5  # each correct answer worths 0.5USD
    error_message = "Error message: You are not supposed to change your selection of choice at result page. The change of selection" \
                    " won't change your earning from quiz. If you see this error message, please change your answer back " \
                    "to your original one."


def get_quiz_data():
    return [
        dict(
            name='Q1',
            solution=True,
            explanation="in this experiment you will be in a group consisting of eight players, you and seven others.",
        ),
        dict(
            name='Q2',
            solution=True,
            explanation="At the beginning of this task each group of 8 will be divided into 4 pairs. "
                        "Neither of you will ever know who the other person in your pair is, "
                        "and the person you are paired with will be determined randomly "
                        "(and therefore typically change) in every period.",
        ),
        dict(
            name='Q3',
            solution=True,
            explanation="At the beginning of this task the computer randomly assigns each person a role, A or B, "
                        "and you will learn whether you are A or B. You will remain in the same role throughout the experiment.",
        ),
        dict(
            name='Q4',
            solution=False,
            explanation="In every period A’s earnings will be determined by their own decisions "
                        "and that of the decisions of all B participants in the group.",
        ),
        dict(
            name='Q5',
            solution=3,
            explanation="The table in the instructions shows that choosing higher effort is more costly."
                        " In particular, an effort level of 5 has an associated cost of effort 25.",
        ),
        dict(
            name='Q6',
            solution=2,
            explanation="The relationship between the effort chosen by the B’s in the group and A’s earnings is such "
                        "that: if the sum of the effort levels chosen by all 4 B’s in the group is equal to or greater "
                        "than 28, the effort threshold is met. In this case the total revenue earned by A’s is shown "
                        "in column 3 above. However, if group effort threshold is not met, A’s earnings are reduced by "
                        "half for all effort choices of B, as shown in column 4.",
        ),
        dict(
            name='Q7',
            solution=False,
            explanation="In stage 3, B’s effort level is revealed to the A in their pair. "
                        "A can then decide on the Actual Transfer they want to make to the B in their pair.",
        ),
        dict(
            name='Q8',
            solution=False,
            # "&nbsp; adds space, &bull; is bullet point
            explanation="At the end of the period the results screen will display the following information to "
                        "participants A and B in the same pair:<br>"
                        "&nbsp; &nbsp; &bull;The wage offered by A<br>"
                        "&nbsp; &nbsp; &bull;The effort level chosen by B<br>"
                        "&nbsp; &nbsp; &bull;The actual transfer chosen by A<br>"
                        "&nbsp; &nbsp; &bull;The total effort chosen by the other three B’s<br>"
                        "&nbsp; &nbsp; &bull;Whether the group effort threshold was met<br>"
                        "&nbsp; &nbsp; &bull;Earnings for the period for A and B, from the choices made",
        ),
        dict(
            name='Q9',
            solution=1,
            explanation="two of the periods will be randomly drawn and participants will be paid for their choices "
                        "in one period and for their guesses in the other period.",
        ),
    ]


def get_quiz_data_additional():
    return [
            dict(
                name='Q2_fixed',
                solution=False,
                explanation="At the beginning of this task each group of 8 will be divided into 4 pairs. "
                            "Neither of you will ever know who the other person in your pair is, "
                            "but the person you are paired with will remain the same in every period.",
            ),
            dict(
                name='Q6_24',
                solution=2,
                explanation="The relationship between the effort chosen by the B’s in the group and A’s earnings is such "
                            "that: if the sum of the effort levels chosen by all 4 B’s in the group is equal to or greater "
                            "than 24, the effort threshold is met. In this case the total revenue earned by A’s is shown "
                            "in column 3 above. However, if group effort threshold is not met, A’s earnings are reduced by "
                            "half for all effort choices of B, as shown in column 4.",
            )


    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1_response = models.BooleanField(
        label="True/False: You are in a group with eight total players.",
        choices=Constants.true_false_choices)
    Q1_correct = models.BooleanField()
    Q2_response = models.BooleanField(label="True/False: You will typically be paired with a "
                                            "different person from this group every period.",
                                      choices=Constants.true_false_choices)
    Q2_correct = models.BooleanField()
    Q3_response = models.BooleanField(label="True/False: Your Role of participant A or B will "
                                            "remain the same throughout Task 1.",
                                      choices=Constants.true_false_choices)
    Q3_correct = models.BooleanField()
    Q4_response = models.BooleanField(
        label="True/False: A’s earnings will only depend on their own choices and the "
              "choice made by the B they are paired with.",
        choices=Constants.true_false_choices)
    Q4_correct = models.BooleanField()
    Q5_response = models.IntegerField(
        label="Suppose B chooses an effort level of 5. Which of the following is correct?",
        choices=[
            [1, "a. B incurs a cost of effort of 64"],
            [2, "b. B incurs a cost of effort of 5 "],
            [3, "c. B incurs a cost of effort of 25"],
            [4, "d. B incurs a cost of effort of 16 "]
        ],
        widget=widgets.RadioSelect
    )
    Q5_correct = models.BooleanField()
    Q6_response = models.IntegerField(
        label="Suppose B chooses an effort level of 8 and the total effort summed across all the 4 B’s "
              "in their group is 24. Which of the following is correct?",
        choices=[
            [1, "a. A’s Total Revenue is 129"],
            [2, "b. A’s Total Revenue is 64"],
            [3, "c. A’s Total Revenue is 75 "],
            [4, "d. B incurs a cost of effort of 81 "]
        ],
        widget=widgets.RadioSelect
    )
    Q6_24_response = models.IntegerField(
        label="Suppose B chooses an effort level of 8 and the total effort summed across all the 4 B’s "
              "in their group is 22. Which of the following is correct?",
        choices=[
            [1, "a. A’s Total Revenue is 129"],
            [2, "b. A’s Total Revenue is 64"],
            [3, "c. A’s Total Revenue is 75 "],
            [4, "d. B incurs a cost of effort of 81 "]
        ],
        widget=widgets.RadioSelect
    )
    Q6_correct = models.BooleanField()
    Q7_response = models.BooleanField(
        label="True/False: Suppose A suggests a Possible Transfer of 15 experimental dollars to the "
              "B in their pair, then B is guaranteed to receive this transfer of 15 experimental dollars.",
        choices=Constants.true_false_choices)
    Q7_correct = models.BooleanField()
    Q8_response = models.BooleanField(
        label="True/False: A can never observe B’s effort choice.",
        choices=Constants.true_false_choices)
    Q8_correct = models.BooleanField()
    Q9_response = models.IntegerField(
        label="Your Payment for Task 1 will be determined in the following manner: "
              "Two periods will be randomly drawn and for those periods: Which of the following statements is correct?",
        choices=[1, 2, 3, 4
                 ],
        widget=widgets.RadioSelect
    )
    Q9_correct = models.BooleanField()
    # q1d = models.IntegerField(widget=widgets.RadioSelect,
    #                           label="Question 1",
    #                           choices=[1, 2, 3, 4]
    #                           )

    num_correct = models.IntegerField(initial=0)


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        participant = player.participant
        participant.progress = 1


def get_quiz_results(player: Player):
    exchange_rate = player.session.config['real_world_currency_per_point']
    correct_answers = player.num_correct
    # store number of correct answers in participant field
    player.participant.quiz_num_correct = correct_answers
    dollar_payoff = correct_answers * Constants.quiz_payoff
    player.payoff = dollar_payoff / exchange_rate
    player.participant.quiz_earning = player.payoff
    results = dict(correct_answers=correct_answers, quiz_earning=player.payoff, dollar_payoff=dollar_payoff)
    return results


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Q1(Page):
    form_model = 'player'
    form_fields = ['Q1_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False, Q1=fields[0],
                    fixed=player.session.config['fixed_matching'],
                    threshold=player.session.config['threshold']
                    )

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q1_response == fields[0]['solution']:
            player.Q1_correct = True
            player.num_correct += 1
        else:
            player.Q1_correct = False


class Q1Result(Page):
    form_model = 'player'
    form_fields = ['Q1_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=True, Q1=fields[0])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q2(Page):
    form_model = 'player'
    form_fields = ['Q2_response']

    # Only show this question to ss if they are in random matching treatment
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['fixed_matching'] == 0

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q2_response == fields[1]['solution']:
            player.Q2_correct = True
            player.num_correct += 1
        else:
            player.Q2_correct = False


class Q2Result(Page):
    form_model = 'player'
    form_fields = ['Q2_response']

    # Only show this question to ss if they are in random matching treatment
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['fixed_matching'] == 0

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q2=fields[1])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q2_Fixed(Page):
    form_model = 'player'
    form_fields = ['Q2_response']

    # Only show this question to ss if they are in random matching treatment
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['fixed_matching'] == 1

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data_additional()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data_additional()
        if player.Q2_response == fields[0]['solution']:
            player.Q2_correct = True
            player.num_correct += 1
        else:
            player.Q2_correct = False


class Q2Result_Fixed(Page):
    form_model = 'player'
    form_fields = ['Q2_response']

    # Only show this question to ss if they are in random matching treatment
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['fixed_matching'] == 1

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data_additional()
        return dict(show_solutions=True, Q2=fields[0])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q3(Page):
    form_model = 'player'
    form_fields = ['Q3_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q3_response == fields[2]['solution']:
            player.Q3_correct = True
            player.num_correct += 1
        else:
            player.Q3_correct = False


class Q3Result(Page):
    form_model = 'player'
    form_fields = ['Q3_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q3=fields[2])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q4(Page):
    form_model = 'player'
    form_fields = ['Q4_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q4_response == fields[3]['solution']:
            player.Q4_correct = True
            player.num_correct += 1
        else:
            player.Q4_correct = False


class Q4Result(Page):
    form_model = 'player'
    form_fields = ['Q4_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q4=fields[3])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q5(Page):
    form_model = 'player'
    form_fields = ['Q5_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q5_response == fields[4]['solution']:
            player.Q5_correct = True
            player.num_correct += 1
        else:
            player.Q5_correct = False


class Q5Result(Page):
    form_model = 'player'
    form_fields = ['Q5_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q5=fields[4])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q6(Page):
    form_model = 'player'
    form_fields = ['Q6_response']
    #show this Q6 is threshold is 28
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['threshold'] == 28

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q6_response == fields[5]['solution']:
            player.Q6_correct = True
            player.num_correct += 1
        else:
            player.Q6_correct = False


class Q6Result(Page):
    form_model = 'player'
    form_fields = ['Q6_response']
    #show this Q6 is threshold is 28
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['threshold'] == 28


    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q6=fields[5])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1

class Q6_24(Page):
    form_model = 'player'
    form_fields = ['Q6_24_response']

    # show this Q6 is threshold is 24
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['threshold'] == 24

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data_additional()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data_additional()
        if player.Q6_24_response == fields[1]['solution']:
            player.Q6_correct = True
            player.num_correct += 1
        else:
            player.Q6_correct = False


class Q6Result_24(Page):
    form_model = 'player'
    form_fields = ['Q6_24_response']

    # show this Q6 is threshold is 24
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['threshold'] == 24

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data_additional()
        return dict(show_solutions=True, Q6=fields[1])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q7(Page):
    form_model = 'player'
    form_fields = ['Q7_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q7_response == fields[6]['solution']:
            player.Q7_correct = True
            player.num_correct += 1
        else:
            player.Q7_correct = False


class Q7Result(Page):
    form_model = 'player'
    form_fields = ['Q7_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q7=fields[6])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q8(Page):
    form_model = 'player'
    form_fields = ['Q8_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False)

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q8_response == fields[7]['solution']:
            player.Q8_correct = True
            player.num_correct += 1
        else:
            player.Q8_correct = False


class Q8Result(Page):
    form_model = 'player'
    form_fields = ['Q8_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q8=fields[7])

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.progress += 1


class Q9(Page):
    form_model = 'player'
    form_fields = ['Q9_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(fields=fields, show_solutions=False,
                    Q9_1="a. Your earnings will be determined by choices (A: wage, actual transfer; B: effort, actual transfer) "
                         "for one drawn period <b>and</b> your guesses for the other drawn period.",
                    Q9_2="b. Your earnings will be determined <b>only</b> by your guesses.",
                    Q9_3="c. Your earnings will be determined <b>only</b> by the choices made (A: wage, actual transfer; "
                         "B: effort, actual transfer).",
                    Q9_4="d. Your earnings will be determined by choices made <b>or</b> your guesses, randomly determined."
                    )

    @staticmethod
    def before_next_page(player, timeout_happened):
        fields = get_quiz_data()
        if player.Q9_response == fields[8]['solution']:
            player.Q9_correct = True
            player.num_correct += 1
        else:
            player.Q9_correct = False


class Q9Result(Page):
    form_model = 'player'
    form_fields = ['Q9_response']

    @staticmethod
    def vars_for_template(player: Player):
        fields = get_quiz_data()
        return dict(show_solutions=True, Q9=fields[8],
                    Q9_1="a. Your earnings will be determined by choices (A: wage, actual transfer; B: effort, actual transfer) "
                         "for one drawn period <b>and</b> your guesses for the other drawn period.",
                    Q9_2="b. Your earnings will be determined <b>only</b> by your guesses.",
                    Q9_3="c. Your earnings will be determined <b>only</b> by the choices made (A: wage, actual transfer; "
                         "B: effort, actual transfer).",
                    Q9_4="d. Your earnings will be determined by choices made <b>or</b> your guesses, randomly determined."
                    )

    @staticmethod
    def error_message(player: Player, values):
        # show error message if subject attempt to change their answer
        for field in values:
            if getattr(player, field) != values[field]:
                return Constants.error_message

    @staticmethod
    def before_next_page(player, timeout_happened):
        exchange_rate = player.session.config['real_world_currency_per_point']
        correct_answers = player.num_correct
        # store number of correct answers in participant field
        player.participant.quiz_num_correct = correct_answers
        dollar_payoff = correct_answers * Constants.quiz_payoff
        player.payoff = dollar_payoff / exchange_rate
        player.participant.quiz_earning = dollar_payoff


class WaitQuiz(WaitPage):
    body_text = "Waiting for other participants to finish their quiz questions... Task 1 will start once everyone completes the quiz."
    wait_for_all_groups = True  # Wait everyone to finish quiz questions

    @staticmethod
    def vars_for_template(player: Player):
        return dict(correct_answers = player.num_correct)


page_sequence = [Instructions,
                 Q1, Q1Result,
                 Q2, Q2Result,
                 Q2_Fixed, Q2Result_Fixed,
                 Q3, Q3Result,
                 Q4, Q4Result,
                 Q5, Q5Result,
                 Q6, Q6Result,
                 Q6_24, Q6Result_24,
                 Q7, Q7Result,
                 Q8, Q8Result,
                 Q9, Q9Result,
                 WaitQuiz]
