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
        #convert points to dollar
        return dict(selected_round_SVO=player.participant.selected_round_SVO,
                    SVO_role =player.participant.role_SVO,
                    SVO_payment=player.participant.SVO_earning,
                    # SVO_payment=float(player.participant.SVO_earning),
                    choice_payment=cu(player.participant.choice_earning).to_real_world_currency(player.session),
                    choice_earning= cu(player.participant.choice_earning),
                    guess_payment= player.participant.guess_earning,
                    gamble_payment= player.participant.gamble_earning,
                    participation_fee=player.session.config['participation_fee'],
                    quiz_earning=player.participant.quiz_earning,
                    quiz_num_correct= player.participant.quiz_num_correct,
                    payment= player.participant.quiz_earning+
                             cu(player.participant.choice_earning).to_real_world_currency(player.session)+
                             player.participant.guess_earning+player.participant.gamble_earning+
                             player.participant.SVO_earning+player.session.config['participation_fee'],
                    conversion_rate=player.session.config['real_world_currency_per_point']
                    )



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [FinalPayment]
