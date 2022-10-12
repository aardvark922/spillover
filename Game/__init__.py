from otree.api import *

doc = """
indefinitely repeated public goods game with 4 playes
"""


class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    pgg_contribute_template = 'Game/pgg_contribute.html'
    pgg_results_template = 'Game/pgg_results.html'
    pd_choice_template = 'Game/pd_choice.html'
    pd_results_template = 'Game/pd_results.html'
    PLAYERS_PER_GROUP = None
    num_super_games = 5
    delta = 0.75  # discount factor equals to 0.75
    # supergame_duration = [10, 3, 21, 10, 12]
    # for app building
    supergame_duration = [2, 1, 3, 2, 3]
    NUM_ROUNDS = sum(supergame_duration)
    last_round = sum(supergame_duration)  # sum(super_game_duration)

    # Nested groups parameters
    super_group_size = 4
    observer_num = 0
    group_size = 2

    ## parameters for Easy PD matrix
    # payoff if 1 player defects and the other cooperates""",
    ez_betray_payoff = 50
    ez_betrayed_payoff = 12

    # payoff if both players cooperate or both defect
    ez_both_cooperate_payoff = 48
    ez_both_defect_payoff = 25

    ## parameters for Difficult PD matrix
    # payoff if 1 player defects and the other cooperates""",
    dt_betray_payoff = 50
    dt_betrayed_payoff = 12

    # payoff if both players cooperate or both defect
    dt_both_cooperate_payoff = 32  # TODO: needs to be calculated
    dt_both_defect_payoff = 25

    # PGG Parameters

    ENDOWMENT = 25
    MPCR = 0.4
    MULTIPLIER = super_group_size * MPCR


class Subsession(BaseSubsession):
    curr_super_game = models.IntegerField(initial=0)
    last_round = models.IntegerField()


class Group(BaseGroup):
    total_contribution = models.FloatField()
    individual_share = models.FloatField()


class Player(BasePlayer):
    pair_id = models.IntegerField(initial=0)
    contribution = models.IntegerField(
        min=0,
        max=C.ENDOWMENT,
        label="Token you choose to move to the Group Account:"
    )
    # record ss's payoff from PGG
    pgg_earning = models.FloatField()
    pd_decision = models.StringField(
        initial='NA',
        choices=[['Action Y', 'Action Y'], ['Action Z', 'Action Z']],
        label="""This player's decision""",
        widget=widgets.RadioSelect
    )
    # record ss's payoff from PD
    pd_earning = models.FloatField()
    dieroll = models.IntegerField(min=1, max=100)


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
        # TODO pair_ID 0 needs to be fixed!
        print('new pair ids:', pair_ids)
    else:
        # Set group matrix in oTree based on the matrix of the previous round
        subsession.group_like_round(subsession.round_number - 1)
        super_groups = subsession.get_groups()
        for g in super_groups:
            players = g.get_players()
            for p in players:
                prev_p = p.in_round(p.round_number - 1)
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


# in one function set pgg and pd payoffs
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = round(group.total_contribution * C.MPCR, 2)
    for p in players:
        p.pgg_earning = C.ENDOWMENT - p.contribution + group.individual_share
        set_pd_payoff(p)


# PD functions
# Get opponent player id
def other_player(player: Player):
    return [p for p in player.get_others_in_group() if p.pair_id == player.pair_id][0]


def set_pd_payoff(player: Player):
    if player.session.config['easy'] == 1:
        # if PD in this session is the Easy PD
        both_cooperate_payoff = C.ez_both_cooperate_payoff
        betrayed_payoff = C.ez_betrayed_payoff
        betray_payoff = C.ez_betrayed_payoff
        both_defect_payoff = C.ez_both_defect_payoff
    else:
        # if PD in this session is the Difficult PD
        both_cooperate_payoff = C.dt_both_cooperate_payoff
        betrayed_payoff = C.dt_betrayed_payoff
        betray_payoff = C.dt_betrayed_payoff
        both_defect_payoff = C.dt_both_defect_payoff
    payoff_matrix = {
        'Action Y':
            {
                'Action Y': both_cooperate_payoff,
                'Action Z': betrayed_payoff
            },
        'Action Z':
            {
                'Action Y': betray_payoff,
                'Action Z': both_defect_payoff
            }
    }
    for p in player.group.get_players():
        p.pd_earning = payoff_matrix[p.pd_decision][other_player(p).pd_decision]


# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution','pd_decision']

    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['easy'] == 1:
            # if PD in this session is the Easy PD
            both_cooperate_payoff = C.ez_both_cooperate_payoff
            betrayed_payoff = C.ez_betrayed_payoff
            betray_payoff = C.ez_betrayed_payoff
            both_defect_payoff = C.ez_both_defect_payoff
        else:
            # if PD in this session is the Difficult PD
            both_cooperate_payoff = C.dt_both_cooperate_payoff
            betrayed_payoff = C.dt_betrayed_payoff
            betray_payoff = C.dt_betrayed_payoff
            both_defect_payoff = C.dt_both_defect_payoff
        return dict(
            cycle_round_number=player.round_number - player.session.vars['super_games_start_rounds'][
                player.subsession.curr_super_game - 1] + 1,
            both_cooperate_payoff=both_cooperate_payoff,
            betrayed_payoff=betrayed_payoff,
            betray_payoff=betray_payoff,
            both_defect_payoff=both_defect_payoff
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        me = player
        opponent = other_player(player)
        if player.session.config['easy'] == 1:
            # if PD in this session is the Easy PD
            both_cooperate_payoff = C.ez_both_cooperate_payoff
            betrayed_payoff = C.ez_betrayed_payoff
            betray_payoff = C.ez_betrayed_payoff
            both_defect_payoff = C.ez_both_defect_payoff
        else:
            # if PD in this session is the Difficult PD
            both_cooperate_payoff = C.dt_both_cooperate_payoff
            betrayed_payoff = C.dt_betrayed_payoff
            betray_payoff = C.dt_betrayed_payoff
            both_defect_payoff = C.dt_both_defect_payoff
        return {
            'cycle_round_number': player.round_number - player.session.vars['super_games_start_rounds'][
                player.subsession.curr_super_game - 1] + 1,
            'pgg_private': C.ENDOWMENT - player.contribution,
            #PD relevant variables
            'both_cooperate_payoff': both_cooperate_payoff,
            'betrayed_payoff': betrayed_payoff,
            'betray_payoff': betray_payoff,
            'both_defect_payoff': both_defect_payoff,
            'my_decision': me.pd_decision,
            'opponent_decision': opponent.pd_decision,
            'same_choice': me.pd_decision == opponent.pd_decision,
            'both_cooperate': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Y",
            'both_defect': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Z",
            'i_cooperate_he_defects': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Z",
            'i_defect_he_cooperates': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Y",
        }


page_sequence = [Decision, ResultsWaitPage, Results]
