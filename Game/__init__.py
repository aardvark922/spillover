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
    NUM_ROUNDS = sum(supergame_duration)
    last_round = sum(supergame_duration)  # sum(super_game_duration)

    # Nested groups parameters
    super_group_size = 4
    observer_num = 0
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
    curr_super_game = models.IntegerField(initial=0)
    last_round = models.IntegerField()


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    pair_id = models.IntegerField(initial=0)
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
def creating_session(subsession: Subsession):
    # Importing modules needed
    from random import randint, shuffle, choices
    # Get Constants attributes once for all

    # Set pairs IDs to identify who is matched with whom
    pair_ids = [n for n in range(1, C.super_group_size // C.group_size + 1)] * C.group_size
    print('pair ids:', pair_ids)

    super_games_duration = C.supergame_duration.copy()

    subsession.session.vars['super_games_duration'] = super_games_duration
    print('supergame duration:', super_games_duration)

    subsession.session.vars['super_games_end_rounds'] = [sum(super_games_duration[:i + 1]) for i in
                                                         range(len(super_games_duration))]

    subsession.session.vars['last_round'] = subsession.session.vars['super_games_end_rounds'][
        C.num_super_games - 1]
    subsession.last_round = C.last_round
    print('supergames end at rounds:', subsession.session.vars['super_games_end_rounds'])
    print('the last round of the experiment is:', subsession.session.vars['last_round'])

    subsession.session.vars['super_games_start_rounds'] = [sum(([1] + super_games_duration)[:i + 1]) for i in
                                                           range(len(super_games_duration))]
    print('supergames start at rounds:', subsession.session.vars['super_games_start_rounds'])

    curr_round = subsession.round_number
    for i, start in enumerate(subsession.session.vars['super_games_start_rounds']):
        if curr_round == start:
            subsession.curr_super_game = i + 1
            break
        else:
            # print(curr_round)
            subsession.curr_super_game = subsession.in_round(curr_round - 1).curr_super_game

    if subsession.round_number in subsession.session.vars['super_games_start_rounds']:
        # Get all players in the session and in the current round
        ps = subsession.get_players()
        # Apply in-place permutation
        shuffle(ps)
        # Set list of list, where each sublist is a supergroup
        super_groups = [ps[n:n + C.super_group_size] for n in range(0, len(ps), C.super_group_size)]
        # print('current round number:', subsession.round_number)
        # print('super groups:',super_groups)
        # Set group matrix in oTree based on the supergroups
        subsession.set_group_matrix(super_groups)
        # Call the set_pairs function
        set_pairs(subsession, pair_ids)
        #TODO pair_ID 0 needs to be fixed!
        print('new pair ids:', pair_ids)
    else:
        super_groups=subsession.get_groups()
        for g in super_groups:
            players = g.get_players()
            for p in players:
                prev_p= p.in_round(p.round_number-1)
                p.pair_id = prev_p.pair_id



# Within each supergroup, randomly assign a paird ID, excluding the last player who will be an observer
def set_pairs(subsession: Subsession, pair_ids: list):
    from random import shuffle
    # Get the supergroups for this round
    super_groups = subsession.get_groups()
    for g in super_groups:
        players = g.get_players()
        shuffle(pair_ids)
        for n, p in enumerate(players[:len(players)]):
            p.pair_id = pair_ids[n]

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