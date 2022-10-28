from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np

author = 'Yaroslav Rosokha'

doc = """
Post-experimental Questionnaire.
"""


class Constants(BaseConstants):
    name_in_url = 'TeamsQueue_08_FeedbackQuestions'
    players_per_group = None
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    # Questionnaire
    understandingSelect = models.StringField(
        choices=['Clear', 'Somewhat Clear', 'Somewhat Confusing',
                 'Confusing'],
        verbose_name='Clarity of Instructions:', blank=True,
        widget=widgets.RadioSelectHorizontal)

    explainedText = models.StringField(
        verbose_name='What could have been explained better?', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))

    strategy0Text = models.StringField(
        verbose_name='What was your strategy during the experiment? (Please be specific)', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))

    strategy1Text = models.StringField(
        verbose_name='Were your strategies in the first few matches different from the strategies '
                     'in the last few matches? If so, in what ways were they different?? (Please be specific)', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))

    strategy2Text = models.StringField(
        verbose_name='Was you strategy different depending on whether you faced Task A or Task B? (Please be '
                     'specific)', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))

    strategy3Text = models.StringField(
        verbose_name='Was your strategy different depending on number of tasks in the queue? For example/ what '
                     'strategy did you use when the queue had one task vs when the queue was full? (Please be '
                     'specific)', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))

    strategy4Text = models.StringField(
        verbose_name='Where you surprised by any of the decisions by the participants you were paired with? '
                     '(Please be specific)', blank=True,
        widget=widgets.Textarea(attrs={'rows': "10", 'cols': "50", 'style': 'height:150px;'}))
