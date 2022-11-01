from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random


class PlayerBot(Bot):

    def play_round(self):
        yield Instructions
        yield (Q1, {'Q1_response': random.randint(0, 1)})
        yield (Q1Result)
        yield (Q2, {'Q2_response': random.randint(0, 1)})
        yield (Q2Result)
        # if self.player.session.config['fixed_matching'] == 0:
        #
        # else:
        #     yield (Q2_Fixed, {'Q2_response': random.randint(0, 1)})
        #     yield (Q2Result_Fixed)
        yield (Q3, {'Q3_response': random.randint(0, 1)})
        yield (Q3Result)
        yield (Q4, {'Q4_response': random.randint(0, 1)})
        yield (Q4Result)
        yield (Q5, {'Q5_response': random.randint(1, 4)})
        yield (Q5Result)
        yield (Q6, {'Q6_response': random.randint(1, 4)})
        yield (Q6Result)
        # if self.player.session.config['threshold'] == 28:
        #
        # else:
        #     yield (Q6_24, {'Q6_24_response': random.randint(1, 4)})
        #     yield (Q6Result_24)
        yield (Q7, {'Q7_response': random.randint(0, 1)})
        yield (Q7Result)
        # yield (Q8, {'Q8_response': random.randint(0, 1)})
        # yield (Q8Result)
        # yield (Q9, {'Q9_response': random.randint(1, 4)})
        # yield (Q9Result)

