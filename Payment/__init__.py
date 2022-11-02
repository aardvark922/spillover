from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    pgg_earnings_template = 'Game/pgg_earning_summary.html'
    pd_earnings_template = 'Game/pd_earning_summary.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class FinalPayment(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        pp = player.participant
        pp.payoff = pp.quiz_earning + pp.pgg_earning + pp.pd_earning + pp.gamble_earning
    @staticmethod
    def vars_for_template(player: Player):
        import math
        pp=player.participant
        pgg_payment = cu(player.participant.pgg_earning).to_real_world_currency(player.session)
        pd_payment = cu(player.participant.pd_earning).to_real_world_currency(player.session)
        # pp.payoff = pp.quiz_earning + pp.pgg_earning + pp.pd_earning + pp.gamble_earning
        num_sg =player.subsession.session.vars['num_match']
        # convert points to dollar
        return dict(pgg_payment=cu(pp.pgg_earning).to_real_world_currency(player.session),
                    pd_payment=cu(pp.pd_earning).to_real_world_currency(player.session),
                    participation_fee=player.session.config['participation_fee'],
                    quiz_earning=pp.quiz_earning,
                    quiz_num_correct=pp.quiz_num_correct,
                    gamble_payment=player.participant.gamble_earning,
                    # payment=pp.quiz_earning +
                    #         cu(pp.pgg_earning).to_real_world_currency(player.session) +
                    #         cu(pp.pd_earning).to_real_world_currency(player.session)
                    #         + pp.gamble_earning  + player.session.config['participation_fee'],
                    payment=math.ceil(player.participant.payoff_plus_participation_fee() * 4) / 4,
                    conversion_rate=1/player.session.config['real_world_currency_per_point'],
                    two_game=player.session.config['sim'],
                    pd_only=player.session.config['pd_only'],
                    sg_history=player.participant.task1_history,
                    task1_earnings=player.participant.pd_earning + player.participant.pgg_earning,
                    task1_payment=pgg_payment + pd_payment,
                    half_match=num_sg / 2,
                    half_match_plus_one=num_sg / 2 + 1
                    )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinalPayment]
