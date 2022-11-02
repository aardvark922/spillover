from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class FinalPayment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        pp=player.participant
        pgg_payment = cu(player.participant.pgg_earning).to_real_world_currency(player.session)
        pd_payment = cu(player.participant.pd_earning).to_real_world_currency(player.session)
        player.participant.payoff = player.participant.pgg_earning + player.participant.pd_earning
        num_sg =player.subsession.session.vars['num_match']
        # convert points to dollar
        return dict(pgg_payment=cu(pp.pgg_earning).to_real_world_currency(player.session),
                    pd_payment=cu(pp.pd_earning).to_real_world_currency(player.session),
                    participation_fee=player.session.config['participation_fee'],
                    quiz_earning=pp.quiz_earning,
                    quiz_num_correct=pp.quiz_num_correct,
                    payment=pp.quiz_earning +
                            cu(pp.pgg_earning).to_real_world_currency(player.session) +
                            cu(pp.pd_earning).to_real_world_currency(player.session)
                            + pp.gamble_earning  + player.session.config['participation_fee'],
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
