from otree.api import *


doc = """
Your app description
"""
#A function to find at which round each supergame ends
def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new

#function to calculate how many blocks are needed in total
def numblock(lst, a):
    block = []
    for ele in lst:
        if ele % a == 0:
            block.append(int(ele / a))
        else:
            block.append(int(ele // a + 1))
    return block

#function to find a list of rounds that are pay relevant
def find_pay_rounds(sg_lst, sg_start):
    rounds = []
    for m in range(len(sg_lst)):
        pay_periods = [a + 1 for a in list(range(sg_lst[m]))]
        pay_rounds = [b + sg_start[m] for b in pay_periods]
        rounds.extend(pay_rounds)
    return rounds

class C(BaseConstants):
    NAME_IN_URL = 'PD'
    pd_choice_template = 'Game/pd_choice.html'
    pd_results_template = 'Game/pd_results.html'
    PLAYERS_PER_GROUP = None
    block_dierolls_template = 'Game/block_dierolls.html'
    PLAYERS_PER_GROUP = None
    DELTA = 0.75  # discount factor equals to 0.75
    BLOCK_SIZE = int(1 / (1 - DELTA))

    # supergame_duration = [10, 3, 21, 10, 12]
    # for app building
    COUNT_ROUNDS_PER_SG = [2, 1, 1, 1, 5]
    # Dal Bo&Frechette one sequence
    # COUNT_ROUNDS_PER_SG = [1, 4, 4, 1, 2, 5, 8, 5, 3, 9, 7, 1, 8, 2, 1, 3, 4, 3, 10, 4]

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


class Subsession(BaseSubsession):
    pass


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
