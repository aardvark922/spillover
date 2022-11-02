from otree.api import *

doc = """
Choice list (Holt/Laury, risk preferences, price list, equivalence test, etc)
"""


class C(BaseConstants):
    NAME_IN_URL = 'choice_list'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TABLE_TEMPLATE = __name__ + '/table.html'
    TABLE_INSTRUCTION_TEMPLATE = __name__ + '/table_instruction.html'
    probability = 50


def read_csv():
    import csv
    import random

    f = open(__name__ + '/stimuli.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))

    # random.shuffle(rows)
    return rows


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        stimuli = read_csv()
        for stim in stimuli:
            # In python, ** unpacks a dict.
            Trial.create(player=p, **stim)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # chose_lottery = models.BooleanField()
    # won_lottery = models.BooleanField()
    gambles = models.IntegerField()
    random_number = models.IntegerField()
    # gamble_payoff = models.CurrencyField()


class Trial(ExtraModel):
    player = models.Link(Player)
    gamble = models.IntegerField()
    lottery_high = models.IntegerField()
    lottery_low = models.FloatField()
    probability_percent = models.IntegerField()
    # chose_lottery = models.BooleanField()
    is_selected = models.BooleanField(initial=False)

#Functions
#
# def gambel_table(gamble):
#     return dict(zip(gambles,trials))
# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        exchange_rate = player.session.config['real_world_currency_per_point']
        return dict(trials=Trial.filter(player=player), is_results=False,
                    probability_low=C.probability+1,
                    # guess_payment=player.participant.guess_earning,
                    # choice_earning=player.participant.choice_earning,
                    # task2poinits= participant.choice_earning + participant.guess_earning/exchange_rate
                    )

class Stimuli(Page):
    form_model = 'player'
    form_fields = ['gambles']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player), is_results=False)
    #TODO: template filter
    # @register.filter(name='zip')
    # def zip_lists(a, b):
    #     return zip(a, b)

    @staticmethod
    def live_method(player: Player, data):
        # In this case, Trial.filter() will return a list with just 1 item.
        # so we use python 'iterable unpacking' to assign that single item
        # to the variable 'trial'.
        [trial] = Trial.filter(player=player, id=data['trial_id'])
        # trial.chose_lottery = data['chose_lottery']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        exchange_rate= player.session.config['real_world_currency_per_point']

        # if your page has a timeout, you would need to adjust this code.
        trials = Trial.filter(player=player)
        #get the info of selected gamble
        selected_trial = trials[player.gambles-1]
        player.participant.chosen_gamble=player.gambles
        selected_trial.is_selected = True
        # player.chose_lottery = selected_trial.chose_lottery

        player.random_number = random.randrange(1,100,1)
        player.participant.random_num_gamble = player.random_number

        #participant won the gamble(get payoff from middle column) if 50> random number
        if player.random_number < C.probability:
            player.participant.gamble_earning = selected_trial.lottery_high
        else:
            player.participant.gamble_earning = selected_trial.lottery_low
        player.payoff = player.participant.gamble_earning/exchange_rate
        pp = player.participant
        pp.payoff = pp.quiz_earning/exchange_rate + pp.pgg_earning + pp.pd_earning + pp.gamble_earning/exchange_rate

class WaitGambleTask(WaitPage):
    body_text = "Waiting for other participants to finish their Part 2... The next part will start once everyone completes Part 2."
    wait_for_all_groups = True  # Wait everyone to finish quiz questions

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        trials = Trial.filter(player=player, is_selected=True)
        return dict(trials=trials, is_results=True,
                    chosen_gamble=player.participant.chosen_gamble,
                    random_number=player.participant.random_num_gamble,
                    earning=player.participant.gamble_earning
                    )


page_sequence = [Instructions,Stimuli,WaitGambleTask]
                 # Results