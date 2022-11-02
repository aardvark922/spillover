from otree.api import *

author = 'Your name here'
doc = """
Simple Demographic Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(min=18, max=100, label=r"What is your age in years?")  # age in years
    gender = models.IntegerField(
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other/Prefer not to say'],
        ],
        label="What is your gender?",
    )
    field_of_study = models.IntegerField(
        choices=[
            [1, 'Management/Business'],
            [2, 'Economics'],
            [3, 'Humanities'],
            [4, 'Liberal Arts'],
            [5, 'Education'],
            [6, 'Engineering'],
            [7, 'Science'],
            [8, 'Social Sciences'],
            [9, 'Agriculture'],
            [10, 'Pharmacy'],
            [11, 'Nursing'],
            [12, 'Other'],
        ],
        label="What is your main field of study?",
    )
    country = models.IntegerField(
        choices=[
            [1, 'USA'],
            [2, 'Canada'],
            [3, 'Mexico'],
            [4, 'Central/South America'],
            [5, 'Australia/New Zealand'],
            [6, 'Other Pacific Nation'],
            [7, 'China'],
            [8, 'Hong Kong'],
            [9, 'Taiwan'],
            [10, 'East Asia'],
            [11, 'South East Asia'],
            [12, 'South Asia'],
            [13, 'Other Asia'],
            [14, 'Europe'],
            [15, 'Africa'],
        ],
        label="Where were you born?",
    )
    length_in_US = models.IntegerField(
        choices=[
            [1, 'N/A'],
            [2, 'More than 5 years'],
            [3, '2-5 years'],
            [4, '1-2 years'],
            [5, 'Less than 1 year'],
        ],
        label="If you were not born in the US, how long have you lived in the US?",
    )
    race = models.IntegerField(
        choices=[
            [1, 'Asian'],
            [2, 'Black'],
            [3, 'Caucasian'],
            [4, 'Hispanic'],
            [5, 'Other'],
        ],
        label="What do you consider your primary racial identity?",
    )
    gpa = models.IntegerField(
        choices=[
            [1, 'Between 3.50 and 4.00'],
            [2, 'Between 3.00 and 3.49'],
            [3, 'Between 2.50 and 2.99'],
            [4, 'Below 2.00'],
            [5, 'N/A as this is my first semester at University'],
        ],
        label="What is your cumulative GPA at the University?",
    )
    years_at_uni = models.IntegerField(
        choices=[
            [1, '1st year'],
            [2, '2nd year'],
            [3, '3rd year'],
            [4, '4th year or above'],
            [5, 'Graduate Student'],
        ],
        label="Are you an undergraduate student (which year?) or a graduate student?",
    )
    num_exper = models.IntegerField(
        min=0,
        max=100,
        label='How many economics experiments have you participated in before this one?',
    )

    understandingSelect = models.StringField(
        choices=['Clear', 'Somewhat Clear', 'Somewhat Confusing',
                 'Confusing'],
        label='Clarity of Part 1 Instructions:', blank=True,
    )
    explainedText = models.LongStringField(
        label='What could have been explained better?', blank=True, )

    strategy0 = models.LongStringField(
        blank=True,
        label='What was your strategy during the experiment? (Please be specific)',
    )
    strategy1 = models.LongStringField(
        blank=True,
        label='Were your strategies in the first few matches different from the strategies '
              'in the last few matches? If so, in what ways were they different? (Please be specific)',
    )
    strategy2 = models.LongStringField(
        blank=True,
        label='Were your strategies in Blue game influenced by your experience in the Green game (or the other way '
              'around)?  (Please be specific)',
    )
    strategy3 = models.LongStringField(
        blank=True,
        label='Where you surprised by any of the decisions by the participants you were matched with? '
                     '(Please be specific)',
    )
    review = models.LongStringField(
        blank=True,
        label='If you have any comments about this experiment, please enter below.'
    )


# FUNCTIONS
def vars_for_admin_report(subsession: Subsession):
    labels = []
    payoffs = []
    for p in subsession.get_players():
        labels.append(p.participant.label)
        payoffs.append(p.participant.vars['payoffs'])
    return dict(labels=labels, payoffs=payoffs)


# PAGES
class Demographics(Page):
    form_model = 'player'

    def get_form_fields(player: Player):
        if player.session.config['sim'] == 1:
            return ['age',
                    'gender',
                    'field_of_study',
                    'country',
                    'length_in_US',
                    'race',
                    'gpa',
                    'years_at_uni',
                    'num_exper',
                    'understandingSelect',
                    'explainedText',
                    'strategy0',
                    'strategy1',
                    'strategy2',
                    'strategy3',
                    'review']
        else:
            return ['age',
                    'gender',
                    'field_of_study',
                    'country',
                    'length_in_US',
                    'race',
                    'gpa',
                    'years_at_uni',
                    'num_exper',
                    'understandingSelect',
                    'explainedText',
                    'strategy0',
                    'strategy1',
                    'strategy3',
                    'review']

    ## this doesn't work...
    # def length_in_US_choices(self):
    #     if self.player.country == 1:
    #         choices = [[1, "N/A"]]
    #     else:
    #         choices = [[2, 'More than 5 years'],
    #             [3, '2-5 years'],
    #             [4, '1-2 years'],
    #             [5, 'Less than 1 year'],]
    #     return choices
    @staticmethod
    def error_message(player: Player, values):
        # print('values is', values)
        if values["country"] == 1 and values['length_in_US'] != 1:
            return 'If you were born in the US, you must answer \'N/A\' for the question: \'If you were not born in the US, how long have you lived in the US?\''
        if values["country"] != 1 and values['length_in_US'] == 1:
            return 'If you were not born in the US, you cannot answer \'N/A\' for the question: \'If you were not born in the US, how long have you lived in the US?\''


page_sequence = [Demographics]
