from otree.api import *
import random

doc = """
simultaneously played Prisoner's Dilemma game and Public Goods game
"""


# A function to find at which round each supergame ends
def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new


# function to calculate how many blocks are needed in total
def numblock(lst, a):
    block = []
    for ele in lst:
        if ele % a == 0:
            block.append(int(ele / a))
        else:
            block.append(int(ele // a + 1))
    return block


# function to find a list of rounds that are pay relevant
def find_pay_rounds(sg_lst, sg_start):
    rounds = []
    for m in range(len(sg_lst)):
        pay_periods = [a + 1 for a in list(range(sg_lst[m]))]
        pay_rounds = [b + sg_start[m] for b in pay_periods]
        rounds.extend(pay_rounds)
    return rounds


class C(BaseConstants):
    NAME_IN_URL = 'BS'
    pgg_contribute_template = 'Game/pgg_contribute.html'
    pgg_results_template = 'Game/pgg_results.html'
    pd_choice_template = 'Game/pd_choice.html'
    pd_results_template = 'Game/pd_results.html'
    pd_earnings_template = 'Game/pd_earning_summary.html'
    block_dierolls_template = 'Game/block_dierolls.html'
    pd_summary_template = 'Game/pd_match_history.html'
    pgg_summary_template = 'Game/pgg_match_history.html'
    pgg_calculator_template = "Game/pgg_calculator.html"
    pgg_earnings_template = 'Game/pgg_earning_summary.html'
    PLAYERS_PER_GROUP = 4
    DELTA = 0.75  # discount factor equals to 0.75
    BLOCK_SIZE = int(1 / (1 - DELTA))

    # for app building
    # COUNT_ROUNDS_PER_SG = [5, 1]
    # COUNT_ROUNDS_PER_SG = [5, 1, 4, 1, 2]
    # COUNT_ROUNDS_PER_SG = [1, 4, 4, 1, 2, 5, 8, 5, 3, 9]
    # Dal Bo&Frechette one sequence
    COUNT_ROUNDS_PER_SG = [1, 4, 4, 1, 2, 5, 8, 5, 3, 9, 7, 1, 8, 2, 1, 3, 4, 3, 10, 4]

    NUM_SG = len(COUNT_ROUNDS_PER_SG)
    # print('number of matches,', NUM_SG)
    # find how many blocks are needed for each supergame
    BLOCKS_PER_SG = numblock(COUNT_ROUNDS_PER_SG, BLOCK_SIZE)
    # print('BLOCKS_PER_SG isis', BLOCKS_PER_SG)
    # find out how many rounds players have to go through
    # PLAYED_ROUNDS_PER_SG= [i*BLOCK_SIZE for i in BLOCKS_PER_SG]
    PLAYED_ROUNDS_PER_SG = [i * 4 for i in BLOCKS_PER_SG]
    SG_ENDS = cumsum(PLAYED_ROUNDS_PER_SG)
    # print('PLAYED_ROUND_END is', SG_ENDS)
    PLAYED_ROUND_STARTS = [0] + SG_ENDS[:-1]
    # print('PLAY_STARTS is', PLAYED_ROUND_STARTS)
    PAY_ROUNDS = find_pay_rounds(COUNT_ROUNDS_PER_SG, PLAYED_ROUND_STARTS)
    # print('PAY_ROUNDS are', PAY_ROUNDS)
    PAY_ROUNDS_ENDS = [sum(x) for x in zip(COUNT_ROUNDS_PER_SG, PLAYED_ROUND_STARTS)]
    # print('PAY_ROUND_ENDS are', PAY_ROUNDS_ENDS)
    NUM_ROUNDS = sum(PLAYED_ROUNDS_PER_SG)

    # Nested groups parameters
    super_group_size = 4
    observer_num = 0
    group_size = 2

    ## Easy PD payoff matrix
    # payoff if 1 player defects and the other cooperates
    ez_betray_payoff = 50
    # payoff if 1 player cooperates and the other defects
    ez_betrayed_payoff = 12

    # payoff if both players cooperate or both defect
    ez_both_cooperate_payoff = 48
    ez_both_defect_payoff = 25

    ## Difficult PD payoff matrix
    # payoff if 1 player defects and the other cooperates
    dt_betray_payoff = 50
    # payoff if 1 player cooperates and the other defects
    dt_betrayed_payoff = 12

    # payoff if both players cooperate or both defect
    dt_both_cooperate_payoff = 32
    dt_both_defect_payoff = 25

    ## PGG Parameters
    ENDOWMENT = 25
    MPCR = 0.4
    MULTIPLIER = super_group_size * MPCR


class Subsession(BaseSubsession):
    # current # of supergame
    sg = models.IntegerField()
    # the period in current supergame
    period = models.IntegerField()
    # whether a round is the last period of a supergame
    is_sg_last_period = models.BooleanField()
    # block = models.IntegerField()
    bk = models.IntegerField()
    # whether a round is the last period of a block
    is_bk_last_period = models.BooleanField()
    is_pay_relevant = models.BooleanField()
    dieroll = models.IntegerField(min=1, max=100)
    treatment = models.StringField()


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    individual_share = models.FloatField()


class Player(BasePlayer):
    pair_id = models.IntegerField(initial=0)
    contribution = models.IntegerField(
        min=0,
        max=C.ENDOWMENT,
        label="Token(s) you choose to move to the Group Account:"
    )
    # record ss's payoff from PGG
    pgg_earning = models.FloatField()
    pgg_sg_earning = models.FloatField()
    pd_decision = models.BooleanField(
        choices=[[True, 'Action Y'], [False, 'Action Z']],
        label="""This player's decision""",
        widget=widgets.RadioSelect
    )
    # record ss's payoff from PD
    pd_earning = models.IntegerField()
    pd_sg_earning = models.IntegerField()
    dieroll = models.IntegerField(min=1, max=100)
    calculator_history= models.StringField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    # Importing modules needed
    from random import randint, shuffle, choices
    # Get Constants attributes once for all

    # Set pairs IDs to identify who is matched with whom
    pair_ids = [n for n in range(1, C.super_group_size // C.group_size + 1)] * C.group_size
    # print('pair ids:', pair_ids)
    subsession.session.vars['sim'] = subsession.session.config['sim']
    subsession.session.vars['pd_only'] = subsession.session.config['pd_only']
    subsession.session.vars['num_match'] = C.NUM_SG
    if subsession.round_number == 1:
        sg = 1
        period = 1
        bk = 1
        # loop over all subsessions
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.sg = sg
            ss.period = period
            ss.bk = bk
            # Whether a round is the last round of a supergame
            # 'in' gives you a bool. for example: 5 in [1, 5, 6] # => True
            is_sg_last_period = ss.round_number in C.SG_ENDS
            ss.is_sg_last_period = is_sg_last_period
            if is_sg_last_period:
                sg += 1
                period = 1
            else:
                period += 1
            # whether a round is the last round of a block
            if ss.round_number % C.BLOCK_SIZE == 0:
                is_bk_last_period = 1
            else:
                is_bk_last_period = 0
            ss.is_bk_last_period = is_bk_last_period

            if is_bk_last_period:
                bk += 1
                # if is_sg_last_period:
                #     bk = 1
            # whether a round is pay relevant
            is_pay_relevant = ss.round_number in C.PAY_ROUNDS
            ss.is_pay_relevant = is_pay_relevant

            continuation_chance = int(round(C.DELTA * 100))
            dieroll_continue = random.randint(1, continuation_chance)
            dieroll_end = random.randint(continuation_chance + 1, 100)
            is_pay_round_end = ss.round_number in C.PAY_ROUNDS_ENDS
            if ss.is_pay_relevant and not is_pay_round_end:
                ss.dieroll = random.randint(1, continuation_chance)
            elif is_pay_round_end:
                ss.dieroll = random.randint(continuation_chance + 1, 100)
            else:
                ss.dieroll = random.randint(1, 100)

    ##------------------------Code for nested group; i.e PD opponent is a member of PGG---------------##
    if subsession.session.config['same_group'] == 1:
        if subsession.period == 1:
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
            # print('new pair ids:', pair_ids)
        else:
            # Set group matrix in oTree based on the matrix of the previous round
            subsession.group_like_round(subsession.round_number - 1)
            super_groups = subsession.get_groups()
            for g in super_groups:
                players = g.get_players()
                for p in players:
                    prev_p = p.in_round(p.round_number - 1)
                    p.pair_id = prev_p.pair_id
    ##---------------------------------------------------------nested_group_codes ends--------------------------##
    else:
        ##--------------------------------different groups design-------------------------------##
        if subsession.period == 1:
            # Get all players in the session and in the current round
            ps = subsession.get_players()
            # Apply in-place permutation
            shuffle(ps)
            # regroup players in the first period of each supergame
            subsession.group_randomly()
            for p in ps:
                p.pair_id = p.id_in_group
        # If the current round is not the first round of a super game, copy group and pair IDs
        else:
            # Set group matrix in oTree based on the matrix of the previous round
            subsession.group_like_round(subsession.round_number - 1)
            ps = subsession.get_players()
            # Apply in-place permutation
            for p in ps:
                p.pair_id = p.id_in_group

    if subsession.session.config['sim'] == 1:
        if subsession.session.config['easy'] == 1:
            subsession.treatment = 'sim_easy'
        else:
            subsession.treatment = 'sim_difficult'
    else:
        if subsession.session.config['pd_only'] == 1:
            if subsession.session.config['easy'] == 1:
                subsession.treatment = 'pd_easy'
            else:
                subsession.treatment = 'pd_difficult'
        else:
            subsession.treatment = 'pgg'


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

def set_pgg_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = round(group.total_contribution * C.MPCR, 2)
    for p in players:
        p.pgg_earning = C.ENDOWMENT - p.contribution + group.individual_share


def set_payoffs(subsession: Subsession):
    groups = subsession.get_groups()
    players = subsession.get_players()
    ##TODO get groups
    if subsession.session.config['sim'] == 1:
        for g in groups:
            set_pgg_payoffs(g)
        for p in players:
            set_pd_payoff(p)
    else:
        if subsession.session.config['pd_only'] == 1:
            for p in players:
                p.pgg_earning = 0
                set_pd_payoff(p)
        else:
            for g in groups:
                set_pgg_payoffs(g)
            for p in players:
                p.pd_earning = 0


# PD functions
# Get opponent player id ---------------this works for nested group design---------------#
# def other_player(player: Player):
#     return [p for p in player.get_others_in_group() if p.pair_id == player.pair_id][0]
# -----------------------------------ends------------------------------------------#


# Get opponent id----------------this works for simultaneous two groups design---------------#
def other_player(player: Player):
    return [p for p in player.get_others_in_subsession() if p.pair_id == player.pair_id][0]


def set_pd_payoff(player: Player):
    if player.session.config['easy'] == 1:
        # if PD in this session is the Easy PD
        both_cooperate_payoff = C.ez_both_cooperate_payoff
        betrayed_payoff = C.ez_betrayed_payoff
        betray_payoff = C.ez_betray_payoff
        both_defect_payoff = C.ez_both_defect_payoff
    else:
        # if PD in this session is the Difficult PD
        both_cooperate_payoff = C.dt_both_cooperate_payoff
        betrayed_payoff = C.dt_betrayed_payoff
        betray_payoff = C.dt_betray_payoff
        both_defect_payoff = C.dt_both_defect_payoff
    payoff_matrix = {
        (False, True): betray_payoff,
        (True, True): both_cooperate_payoff,
        (False, False): both_defect_payoff,
        (True, False): betrayed_payoff,
    }
    other = other_player(player)
    player.pd_earning = payoff_matrix[(player.pd_decision, other.pd_decision)]
    # print("me", player)
    # print("other", other)


# #roll a die for the whole session
def get_block_history(player: Player):
    block_first_round = player.round_number - C.BLOCK_SIZE + 1
    block = player.in_rounds(block_first_round, player.round_number)
    block_history = []
    for b in block:
        block_round = dict(round_number=b.subsession.period, dieroll=b.subsession.dieroll,
                           pgg_earning=b.pgg_earning, pd_earning=b.pd_earning,
                           pay_end=b.subsession.round_number in C.PAY_ROUNDS_ENDS, )
        block_history.append(block_round)
    return block_history


# PAGES

class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1
class NewSupergame(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1

    def vars_for_template(player: Player):
        return dict(two_game=player.session.config['sim'],
                    pd_only=player.session.config['pd_only'] )


class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution', 'pd_decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['sim'] == 1

    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['easy'] == 1:
            # if PD in this session is the Easy PD
            both_cooperate_payoff = C.ez_both_cooperate_payoff
            betrayed_payoff = C.ez_betrayed_payoff
            betray_payoff = C.ez_betray_payoff
            both_defect_payoff = C.ez_both_defect_payoff
        else:
            # if PD in this session is the Difficult PD
            both_cooperate_payoff = C.dt_both_cooperate_payoff
            betrayed_payoff = C.dt_betrayed_payoff
            betray_payoff = C.dt_betray_payoff
            both_defect_payoff = C.dt_both_defect_payoff
        return dict(
            # cycle_round_number=player.round_number - player.session.vars['super_games_start_rounds'][
            #     player.subsession.curr_super_game - 1] + 1,
            cycle_round_number=player.subsession.period,
            both_cooperate_payoff=both_cooperate_payoff,
            betrayed_payoff=betrayed_payoff,
            betray_payoff=betray_payoff,
            both_defect_payoff=both_defect_payoff,
            # pgg_selected_match=player.subsession.session.vars['pgg_payment_match'],
            # pd_selected_match=player.subsession.session.vars['pd_payment_match']
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(Endowment=C.ENDOWMENT,
                    MPCR=C.MPCR)


class DecisionSingle(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.subsession.session.config['pd_only'] == 1:
            return ['pd_decision']
        else:
            return ['contribution']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config['sim'] == 0

    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['easy'] == 1:
            # if PD in this session is the Easy PD
            both_cooperate_payoff = C.ez_both_cooperate_payoff
            betrayed_payoff = C.ez_betrayed_payoff
            betray_payoff = C.ez_betray_payoff
            both_defect_payoff = C.ez_both_defect_payoff
        else:
            # if PD in this session is the Difficult PD
            both_cooperate_payoff = C.dt_both_cooperate_payoff
            betrayed_payoff = C.dt_betrayed_payoff
            betray_payoff = C.dt_betray_payoff
            both_defect_payoff = C.dt_both_defect_payoff
        return dict(
            # cycle_round_number=player.round_number - player.session.vars['super_games_start_rounds'][
            #     player.subsession.curr_super_game - 1] + 1,
            cycle_round_number=player.subsession.period,
            both_cooperate_payoff=both_cooperate_payoff,
            betrayed_payoff=betrayed_payoff,
            betray_payoff=betray_payoff,
            both_defect_payoff=both_defect_payoff,
            # pgg_selected_match=player.subsession.session.vars['pgg_payment_match'],
            # pd_selected_match=player.subsession.session.vars['pd_payment_match'],
            pd_only=player.session.config['pd_only']
        )
    @staticmethod
    def js_vars(player: Player):
        return dict(Endowment=C.ENDOWMENT,
                    MPCR=C.MPCR)

class ResultsWaitPage(WaitPage):
    # add the following line of code to wait all players in a subsession

    wait_for_all_groups = True
    after_all_players_arrive = set_payoffs


class RoundResults(Page):

    # @staticmethod
    # def is_displayed(player: Player):
    #     return player.session.config['sim'] == 1

    @staticmethod
    def vars_for_template(player: Player):
        me = player
        opponent = other_player(player)
        session = player.session
        if session.config['sim'] == 1:
            if session.config['easy'] == 1:
                # if PD in this session is the Easy PD
                both_cooperate_payoff = C.ez_both_cooperate_payoff
                betrayed_payoff = C.ez_betrayed_payoff
                betray_payoff = C.ez_betray_payoff
                both_defect_payoff = C.ez_both_defect_payoff
            else:
                # if PD in this session is the Difficult PD
                both_cooperate_payoff = C.dt_both_cooperate_payoff
                betrayed_payoff = C.dt_betrayed_payoff
                betray_payoff = C.dt_betray_payoff
                both_defect_payoff = C.dt_both_defect_payoff
            return {
                'cycle_round_number': player.subsession.period,
                'pgg_private': C.ENDOWMENT - player.contribution,
                # PD relevant variables
                'both_cooperate_payoff': both_cooperate_payoff,
                'betrayed_payoff': betrayed_payoff,
                'betray_payoff': betray_payoff,
                'both_defect_payoff': both_defect_payoff,
                'my_decision': me.field_display('pd_decision'),
                'opponent_decision': opponent.field_display('pd_decision'),
                'same_choice': me.pd_decision == opponent.pd_decision,
                'both_cooperate': me.pd_decision == True and opponent.pd_decision == True,
                'both_defect': me.pd_decision == False and opponent.pd_decision == False,
                'i_cooperate_he_defects': me.pd_decision == True and opponent.pd_decision == False,
                'i_defect_he_cooperates': me.pd_decision == False and opponent.pd_decision == True,
                'pd_only': player.session.config['pd_only'],
                'two_game': player.session.config['sim'],
                'block_end': player.subsession.is_bk_last_period,
                'opponent': opponent
            }
        else:
            if session.config['pd_only'] == 1:
                if session.config['easy'] == 1:
                    # if PD in this session is the Easy PD
                    both_cooperate_payoff = C.ez_both_cooperate_payoff
                    betrayed_payoff = C.ez_betrayed_payoff
                    betray_payoff = C.ez_betray_payoff
                    both_defect_payoff = C.ez_both_defect_payoff
                else:
                    # if PD in this session is the Difficult PD
                    both_cooperate_payoff = C.dt_both_cooperate_payoff
                    betrayed_payoff = C.dt_betrayed_payoff
                    betray_payoff = C.dt_betray_payoff
                    both_defect_payoff = C.dt_both_defect_payoff

                return {
                    'cycle_round_number': player.subsession.period,
                    # PD relevant variables
                    'both_cooperate_payoff': both_cooperate_payoff,
                    'betrayed_payoff': betrayed_payoff,
                    'betray_payoff': betray_payoff,
                    'both_defect_payoff': both_defect_payoff,
                    'my_decision': me.field_display('pd_decision'),
                    'opponent_decision': opponent.field_display('pd_decision'),
                    'same_choice': me.pd_decision == opponent.pd_decision,
                    'both_cooperate': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Y",
                    'both_defect': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Z",
                    'i_cooperate_he_defects': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Z",
                    'i_defect_he_cooperates': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Y",
                    'pd_only': player.session.config['pd_only'],
                    'two_game': player.session.config['sim'],
                    'block_end': player.subsession.is_bk_last_period
                }
            else:
                return {
                    'cycle_round_number': player.subsession.period,
                    'pgg_private': C.ENDOWMENT - player.contribution,
                    'pd_only': player.session.config['pd_only'],
                    'two_game': player.session.config['sim'],
                    'block_end': player.subsession.is_bk_last_period
                }


# class RoundResultsSingle(Page):
#     # @staticmethod
#     # def is_displayed(player: Player):
#     #     return player.session.config['sim'] == 0
#
#     @staticmethod
#     def vars_for_template(player: Player):
#         if player.session.config['pd_only'] == 1:
#             me = player
#             opponent = other_player(player)
#             if player.session.config['easy'] == 1:
#                 # if PD in this session is the Easy PD
#                 both_cooperate_payoff = C.ez_both_cooperate_payoff
#                 betrayed_payoff = C.ez_betrayed_payoff
#                 betray_payoff = C.ez_betray_payoff
#                 both_defect_payoff = C.ez_both_defect_payoff
#             else:
#                 # if PD in this session is the Difficult PD
#                 both_cooperate_payoff = C.dt_both_cooperate_payoff
#                 betrayed_payoff = C.dt_betrayed_payoff
#                 betray_payoff = C.dt_betray_payoff
#                 both_defect_payoff = C.dt_both_defect_payoff
#             return {
#                 'cycle_round_number': player.subsession.period,
#                 # PD relevant variables
#                 'both_cooperate_payoff': both_cooperate_payoff,
#                 'betrayed_payoff': betrayed_payoff,
#                 'betray_payoff': betray_payoff,
#                 'both_defect_payoff': both_defect_payoff,
#                 'my_decision': me.field_display('pd_decision'),
#                 'opponent_decision': opponent.field_display('pd_decision'),
#                 'same_choice': me.pd_decision == opponent.pd_decision,
#                 'both_cooperate': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Y",
#                 'both_defect': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Z",
#                 'i_cooperate_he_defects': me.pd_decision == "Action Y" and opponent.pd_decision == "Action Z",
#                 'i_defect_he_cooperates': me.pd_decision == "Action Z" and opponent.pd_decision == "Action Y",
#                 'pd_only': player.session.config['pd_only']
#             }
#         else:
#             return {
#                 'cycle_round_number': player.subsession.period,
#                 'pgg_private': C.ENDOWMENT - player.contribution,
#                 'pd_only': player.session.config['pd_only'],
#             }


class BlockEnd(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.is_bk_last_period == 1

    @staticmethod
    def vars_for_template(player: Player):
        continuation_chance = int(round(C.DELTA * 100))
        sg = player.subsession.sg
        player_in_end_round = player.in_round(C.PAY_ROUNDS_ENDS[sg - 1])
        end_period = player_in_end_round.subsession.period
        return dict(continuation_chance=continuation_chance,
                    die_threshold_plus_one=continuation_chance + 1,
                    block_history=get_block_history(player),
                    end_period=end_period,
                    two_game=player.session.config['sim'],
                    pd_only=player.session.config['pd_only']
                    )


class MatchSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.is_sg_last_period == 1

    @staticmethod
    def vars_for_template(player: Player):
        sg = player.subsession.sg
        player_in_end_round = player.in_round(C.PAY_ROUNDS_ENDS[sg - 1])
        end_period = player_in_end_round.subsession.period
        start_round = C.PLAYED_ROUND_STARTS[sg - 1]
        sg_end_round = C.SG_ENDS[sg-1]
        sg_duration = C.COUNT_ROUNDS_PER_SG[sg - 1]
        # player_in_pay_rounds = player.in_rounds(start_round + 1, start_round + sg_duration)
        player_in_sg_prev_rounds=player.in_rounds(start_round+1, sg_end_round)
        pgg_tot_earning = 0
        pd_tot_earning = 0
        pd_history = []
        pgg_history = []
        for p in player_in_sg_prev_rounds:
            pd_other = other_player(p)
            if p.subsession.is_pay_relevant:
                pgg_tot_earning += p.pgg_earning
                pd_tot_earning += p.pd_earning
            if p.session.config['sim'] == 1:
                pd_round_result = dict(round_number=p.subsession.period,
                                       pd_decision=p.field_display('pd_decision'),
                                       pd_other_decision=pd_other.field_display('pd_decision'),
                                       pd_earning=p.pd_earning,
                                       is_pay_relevant= p.subsession.is_pay_relevant)
                pgg_round_result = dict(round_number=p.subsession.period,
                                        pgg_private=C.ENDOWMENT - p.contribution,
                                        pgg_total_contribution=p.group.total_contribution,
                                        pgg_earning=p.pgg_earning,
                                        is_pay_relevant= p.subsession.is_pay_relevant)
            else:
                if p.session.config['pd_only'] == 1:
                    pd_round_result = dict(round_number=p.subsession.period,
                                           pd_decision=p.field_display('pd_decision'),
                                           pd_other_decision=pd_other.field_display('pd_decision'),
                                           pd_earning=p.pd_earning,
                                           is_pay_relevant= p.subsession.is_pay_relevant)
                    pgg_round_result = dict(round_number=p.subsession.period,
                                            pgg_private=0,
                                            pgg_total_contribution=0,
                                            pgg_earning=p.pgg_earning,
                                            is_pay_relevant= p.subsession.is_pay_relevant)
                else:
                    pd_round_result = dict(round_number=p.subsession.period,
                                           pd_decision=0,
                                           pd_other_decision=0,
                                           pd_earning=p.pd_earning,
                                           is_pay_relevant= p.subsession.is_pay_relevant)
                    pgg_round_result = dict(round_number=p.subsession.period,
                                            pgg_private=C.ENDOWMENT - p.contribution,
                                            pgg_total_contribution=p.group.total_contribution,
                                            pgg_earning=p.pgg_earning,
                                            is_pay_relevant= p.subsession.is_pay_relevant)
            pd_history.append(pd_round_result)
            pgg_history.append(pgg_round_result)
        player.pgg_sg_earning = round(pgg_tot_earning, 1)
        player.pd_sg_earning = pd_tot_earning
        return dict(pgg_sg_earning=player.pgg_sg_earning,
                    pd_sg_earning=player.pd_sg_earning,
                    end_period=end_period,
                    block_history=get_block_history(player),
                    two_game=player.session.config['sim'],
                    pd_only=player.session.config['pd_only'],
                    pd_history=pd_history,
                    pgg_history=pgg_history,
                    )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        participant = player.participant
        exchange_rate = player.session.config['real_world_currency_per_point']
        # if it's the last round of this task
        if player.round_number == C.NUM_ROUNDS:
            pgg_earnings = 0
            pd_earnings = 0
            sg_history = []
            for sg in range(len(C.SG_ENDS)):
                player_in_end_round_of_sg = player.in_round(C.SG_ENDS[sg])
                pgg_earnings += player_in_end_round_of_sg.pgg_sg_earning
                pd_earnings += player_in_end_round_of_sg.pd_sg_earning
                sg_results = dict(match=sg + 1, pgg_sg_earnings=player_in_end_round_of_sg.pgg_sg_earning,
                                  pd_sg_earnings=player_in_end_round_of_sg.pd_sg_earning)
                sg_history.append(sg_results)
            player.participant.task1_history = sg_history
            participant.pgg_earning = pgg_earnings
            participant.pd_earning = pd_earnings

            # player.payoff = participant.pgg_earning + participant.pd_earning


class FinalPayment(Page):

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        pgg_payment = cu(player.participant.pgg_earning).to_real_world_currency(player.session)
        pd_payment = cu(player.participant.pd_earning).to_real_world_currency(player.session)
        player.participant.payoff = player.participant.pgg_earning + player.participant.pd_earning
        num_sg =player.subsession.session.vars['num_match']
        # convert points to dollar
        return dict(
            participation_fee=player.session.config['participation_fee'],
            conversion_rate=player.session.config['real_world_currency_per_point'],
            two_game=player.session.config['sim'],
            pd_only=player.session.config['pd_only'],
            sg_history=player.participant.task1_history,
            task1_earnings=player.participant.pd_earning + player.participant.pgg_earning,
            task1_payment=pgg_payment + pd_payment,
            half_match=num_sg/2,
            half_match_plus_one=num_sg/2+1
        )


page_sequence = [Instructions,
                 NewSupergame,
                 Decision,
                 DecisionSingle,
                 ResultsWaitPage,
                 RoundResults,
                 BlockEnd,
                 MatchSummary]
                 # FinalPayment]
