from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random


class PlayerBot(Bot):

    def play_round(self):
        cnty = random.randint(1, 15)
        if cnty == 1:
            lius = 1
        else:
            lius = random.randint(2, 5)
        yield (Demographics, {'age': random.randint(18, 50),
                              'gender': random.randint(1, 2),
                              'field_of_study': random.randint(1, 12),
                              'country': cnty,
                              'length_in_US': lius,
                              'race': random.randint(1, 5),
                              'gpa': random.randint(1, 5),
                              'years_at_uni': random.randint(1, 5),
                              'num_exper': random.randint(0, 20)
                              }
               )
