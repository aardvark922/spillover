from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire(Page):

    form_model = 'player'
    form_fields = ['understandingSelect',
                   'explainedText',
                   'strategy0Text',
                   'strategy1Text',
                   'strategy2Text',
                   'strategy3Text',
                   'strategy4Text',
                   ]

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [

    Questionnaire

]
