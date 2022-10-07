from otree.api import *

doc = """
indefinitely repeated public goods game with 4 playes
"""


class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    pgg_contribute_template = 'Game/pgg_contribute.html'
    PLAYERS_PER_GROUP = None
    num_super_games = 5
    delta = 0.90  # discount factor equals to 0.90
    # supergame_duration = [10, 3, 21, 10, 12]
    #for app building
    supergame_duration = [1,2,1,1,2]
    num_rounds = sum(supergame_duration)
    last_round = sum(supergame_duration)  # sum(super_game_duration)

    # Nested groups parameters
    super_group_size = 4
    group_size = 2

    ## parameters for Easy PD matrix
    # payoff if 1 player defects and the other cooperates""",
    ez_betray_payoff = cu(50)
    ez_betrayed_payoff = cu(12)

    # payoff if both players cooperate or both defect
    ez_both_cooperate_payoff = cu(48)
    ez_both_defect_payoff = cu(25)

    ## parameters for Difficult PD matrix
    # payoff if 1 player defects and the other cooperates""",
    dt_betray_payoff = cu(50)
    dt_betrayed_payoff = cu(12)

    # payoff if both players cooperate or both defect
    dt_both_cooperate_payoff = cu(32) #TODO: needs to be calculated
    dt_both_defect_payoff = cu(25)

    #PGG Parameters

    ENDOWMENT = cu(25)
    MPCR = 0.4
    MULTIPLIER = super_group_size * MPCR


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
