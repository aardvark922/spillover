from otree.api import *
import random

doc = """
Implement Block Random Termination
"""
def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new

def numblock(lst,a):
    block=[]
    for ele in lst:
        if ele%a ==0:
            block.append(int(ele/a))
        else:
            block.append(int(ele//a+1))
    return block

def find_pay_rounds(sg_lst,sg_start):
    rounds=[]
    for m in range(len(sg_lst)):
        pay_periods= [a+1 for a in list(range(sg_lst[m]))]
        pay_rounds= [b+sg_start[m] for b in pay_periods]
        rounds.extend(pay_rounds)
    return rounds

class C(BaseConstants):
    NAME_IN_URL = 'block_random_termination'
    PLAYERS_PER_GROUP = None

    DELTA = 0.75  # discount factor equals to 0.75
    BLOCK_SIZE = 1/(1-DELTA)
    # first supergame lasts 2 rounds, second supergame lasts 3 rounds, etc...
    #These are the payoff relevants rounds
    COUNT_ROUNDS_PER_SG = [2, 3, 4, 5]
    # number of supergames to be played
    NUM_SG= len(COUNT_ROUNDS_PER_SG)
    #Get what the round each supergame ends
    # SG_ENDS = cumsum(COUNT_ROUNDS_PER_SG)

    #find how many blocks are needed for each supergame
    BLOCKS_PER_SG= numblock(COUNT_ROUNDS_PER_SG,BLOCK_SIZE)
    print('BLOCKS_PER_SG is',BLOCKS_PER_SG)
    #find out how many rounds players have to go through
    # PLAYED_ROUNDS_PER_SG= [i*BLOCK_SIZE for i in BLOCKS_PER_SG]
    PLAYED_ROUNDS_PER_SG= [i*4 for i in BLOCKS_PER_SG]
    SG_ENDS=cumsum(PLAYED_ROUNDS_PER_SG)
    print('PLAYED_ROUND_END is',SG_ENDS)
    PLAYED_ROUND_STARTS= [0]+SG_ENDS[:-1]
    print('PLAY_STARTS is', PLAYED_ROUND_STARTS)
    PAY_ROUNDS = find_pay_rounds(COUNT_ROUNDS_PER_SG,PLAYED_ROUND_STARTS)
    print('PAY_ROUNDS are', PAY_ROUNDS)
    PAY_ROUNDS_ENDS=[sum(x) for x in zip(COUNT_ROUNDS_PER_SG,PLAYED_ROUND_STARTS)]
    print('PAY_ROUND_ENDS are', PAY_ROUNDS_ENDS)
    NUM_ROUNDS = sum(PLAYED_ROUNDS_PER_SG)


class Subsession(BaseSubsession):
    # current # of supergame
    sg = models.IntegerField()
    # the period in current supergame
    period = models.IntegerField()
    #whether a round is the last period of a supergame
    is_sg_last_period = models.BooleanField()
    # block = models.IntegerField()
    bk = models.IntegerField()
    #whether a round is the last period of a block
    is_bk_last_period = models.BooleanField()
    is_pay_relevant = models.BooleanField()
    dieroll = models.IntegerField(min=1, max=100)


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        sg = 1
        period = 1
        bk = 1
        # loop over all subsessions
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.sg = sg
            ss.period = period
            ss.bk = bk
            #Whether a round is the last round of a supergame
            # 'in' gives you a bool. for example: 5 in [1, 5, 6] # => True
            is_sg_last_period = ss.round_number in C.SG_ENDS
            ss.is_sg_last_period = is_sg_last_period
            if is_sg_last_period:
                sg += 1
                period = 1
            else:
                period += 1
            #whether a round is the last round of a block
            if ss.round_number%C.BLOCK_SIZE == 0:
                is_bk_last_period=1
            else:
                is_bk_last_period=0
            ss.is_bk_last_period = is_bk_last_period

            if is_bk_last_period:
                bk += 1
                # if is_sg_last_period:
                #     bk = 1
            #whether a round is pay relevant
            is_pay_relevant=ss.round_number in C.PAY_ROUNDS
            ss.is_pay_relevant=is_pay_relevant

            continuation_chance = int(round(C.DELTA * 100))
            dieroll_continue = random.randint(1, continuation_chance)
            dieroll_end = random.randint(continuation_chance + 1, 100)
            if ss.is_pay_relevant:
                if ss in C.PAY_ROUNDS_ENDS:  ##only end at last pay round!
                    ss.dieroll = dieroll_end
                else:
                    ss.dieroll = dieroll_continue
            else:
                ss.dieroll=dieroll_end


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    pass


class NewSupergame(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1

class BlockEnd(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.is_bk_last_period == 1

    def vars_for_template(player: Player):
        continuation_chance = int(round(C.delta * 100))
        #TODO: pull out a history of dierolls in this block gettattr()?
        # player.subsession.dieroll
        # previous_rounds_in_block=
        return dict(dieroll=player.dieroll, continuation_chance=continuation_chance,
                        die_threshold_plus_one=continuation_chance + 1,
                        cycle_round_number=player.round_number - player.session.vars['super_games_start_rounds'][
                            player.subsession.curr_super_game - 1] + 1
                        )



class Play(Page):
    pass


page_sequence = [NewSupergame, Play, BlockEnd]