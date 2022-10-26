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
        # convert points to dollar
        return dict(pgg_payment=cu(pp.pgg_earning).to_real_world_currency(player.session),
                    pd_payment=cu(pp.pd_earning).to_real_world_currency(player.session),
                    selected_round_SVO=pp.selected_round_SVO,
                    SVO_role=pp.role_SVO,
                    SVO_payment=pp.SVO_earning,
                    # SVO_payment=float(player.participant.SVO_earning),
                    participation_fee=player.session.config['participation_fee'],
                    quiz_earning=pp.quiz_earning,
                    quiz_num_correct=pp.quiz_num_correct,
                    payment=pp.quiz_earning +
                            cu(pp.pgg_earning).to_real_world_currency(player.session) +
                            cu(pp.pd_earning).to_real_world_currency(player.session)
                            + pp.gamble_earning +
                            pp.SVO_earning + player.session.config['participation_fee'],
                    conversion_rate=player.session.config['real_world_currency_per_point'],
                    two_game=player.session.vars['sim'],
                    pd_only=player.session.vars['pd_only'],
                    )


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinalPayment]
