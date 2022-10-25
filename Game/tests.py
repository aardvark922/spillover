from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.player.session.config['sim']==1:
            if self.player.subsession.period == 1:
                yield NewSupergame
            # yield Decision, dict(contribution= random.randint(1, 25),
            #                      pd_decision= random.randint(0, 1))
            #
            yield Decision, dict(contribution= random.randint(1, 25),
                                 pd_decision= random.randint(0, 1))
            yield RoundResults
            if self.player.subsession.is_bk_last_period == 1:
                yield BlockEnd
        else:
            if self.player.session.config['pd_only']==1:
                if self.player.subsession.period == 1:
                    yield NewSupergame
                # yield Decision, dict(contribution= random.randint(1, 25),
                #                      pd_decision= random.randint(0, 1))
                #
                yield DecisionSingle, dict(pd_decision= random.randint(0, 1))
                yield RoundResultsSingle
                if self.player.subsession.is_bk_last_period == 1:
                    yield BlockEnd
            else:
                if self.player.subsession.period == 1:
                    yield NewSupergame
                # yield Decision, dict(contribution= random.randint(1, 25),
                #                      pd_decision= random.randint(0, 1))
                #
                yield DecisionSingle, dict(contribution= random.randint(1, 25))
                yield RoundResultsSingle
                if self.player.subsession.is_bk_last_period == 1:
                    yield BlockEnd