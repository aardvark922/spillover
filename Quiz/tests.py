from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random


class PlayerBot(Bot):

    def play_round(self):
        config=self.player.session.config
        yield Instructions
        if config['sim'] == 1:
            # yield (Q1, {'Q1_response': random.randint(0, 1)})
            yield (Q1, {'Q1_response': 0})
            yield (Q1Result)
        if config['sim']==1:
            # yield (Q2, {'Q2_response': random.randint(0, 1)})
            yield (Q2, {'Q2_response': 1})
            yield (Q2Result)
        elif config['sim']==0 and config['pd_only']==0:
            yield (Q2_Pgg, {'Q2_pgg_response': 1})
            yield (Q2Result_Pgg)
        else:
            yield (Q2_Pd, {'Q2_pd_response': random.randint(0, 1)})
            yield (Q2Result_Pd)
        # yield (Q3, {'Q3_response': random.randint(0, 1)})
        yield (Q3, {'Q3_response': 1})
        yield (Q3Result)
        if config['sim'] == 1:
            # yield (Q4, {'Q4_response': random.randint(0, 1)})
            yield (Q4, {'Q4_response': 1})
            yield (Q4Result)
        yield (Q5, {'Q5_response': 2})
        yield (Q5Result)
        if config['sim']==1 or config['pd_only']==0:
            yield (Q6, {'Q6_response': 3})
            yield (Q6Result)
        # if self.player.session.config['threshold'] == 28:
        #
        # else:
        #     yield (Q6_24, {'Q6_24_response': random.randint(1, 4)})
        #     yield (Q6Result_24)
        if config['sim']==1 or config['pd_only']==1:
            yield (Q7, {'Q7_response': 2})
            yield (Q7Result)
        # yield (Q8, {'Q8_response': random.randint(0, 1)})
        # yield (Q8Result)
        # yield (Q9, {'Q9_response': random.randint(1, 4)})
        # yield (Q9Result)

