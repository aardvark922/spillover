from otree.api import *


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

def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new
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
    print('PLAYED_ROUND_END is',PLAYED_ROUNDS_PER_SG)
    SG_ENDS = cumsum(PLAYED_ROUNDS_PER_SG)
    print('SG_ENDS is', SG_ENDS)
    NUM_ROUNDS = sum(PLAYED_ROUNDS_PER_SG)




class Subsession(BaseSubsession):
    # current number of supergame
    sg = models.IntegerField()
    # the period in current supergame
    period = models.IntegerField()
    is_last_period = models.BooleanField()
    block = models.IntegerField()
    bk = models.IntegerField()
    is_bk_last_period = models.BooleanField()
    is_pay_relevant = models.BooleanField()


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        sg = 1
        period = 1
        bk=1
        # loop over all subsessions
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.sg = sg
            ss.period = period
            # 'in' gives you a bool. for example: 5 in [1, 5, 6] # => True
            is_last_period = ss.round_number in C.SG_ENDS
            ss.is_last_period = is_last_period
            if ss.round_number%C.BLOCK_SIZE == 0:
                is_bk_last_period=1
            else:
                is_bk_last_period=0
            ss.is_bk_last_period = is_bk_last_period
            if is_bk_last_period:
                bk+=1
            if is_last_period:
                sg += 1
                period = 1
                bk=1
            else:
                period += 1

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
