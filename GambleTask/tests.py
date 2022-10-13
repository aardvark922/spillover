from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import random


class PlayerBot(Bot):

    def play_round(self):
        yield Instructions
        yield (Stimuli, {'gambles': random.randint(1, 5)})