from otree.api import *

doc = """
indefinitely repeated public goods game with 4 playes
"""


class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    pgg_contribute_template = 'Game/pgg_contribute.html'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(25)
    MPCR = 0.4
    MULTIPLIER = PLAYERS_PER_GROUP * MPCR


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    PD_decision = models.StringField(
        initial='NA',
        choices=[['Action Y', 'Action Y'], ['Action Z', 'Action Z']],
        label="""This player's decision""",
        widget=widgets.RadioSelect
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
            group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Decision, ResultsWaitPage, Results]
