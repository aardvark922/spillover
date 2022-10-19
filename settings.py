from os import environ

SESSION_CONFIGS = [
    dict(
        name='main_task',
        app_sequence=['Game'],
        num_demo_participants=4,
        easy=1,
        sim=1,
        pd_only=0,
        doc="""
        This is the oTree program for treatment with both games"""

    ),
    dict(
        name='main_task_pd_easy',
        app_sequence=['Game'],
        num_demo_participants=4,
        easy=1,
        sim=0,
        pd_only=1,
        doc="""
        This is the oTree program for treatment with easy PD game only"""
    ),
    dict(
        name='main_task_pd_difficult',
        app_sequence=['Game'],
        num_demo_participants=4,
        easy=0,
        sim=0,
        pd_only=1,
        doc="""
    This is the oTree program for treatment with easy PD game only"""
    ),
    dict(
        name='main_task_pgg',
        app_sequence=['Game'],
        num_demo_participants=4,
        easy=1,
        sim=0,
        pd_only=0,
        doc="""
    This is the oTree program for treatment with PD game only"""
    ),
    dict(
        name='Block_Random_Termination',
        app_sequence=['block_random_termination'],
        num_demo_participants=1,

    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.20, participation_fee=5.00, doc="",use_browser_bots=True
)
# use_browser_bots=True
PARTICIPANT_FIELDS = ['quiz_num_correct', 'quiz_earning', 'progress', 'selected_match_pgg', 'selected_match_pd',
                      'pgg_earning', 'pd_earning', 'chosen_gamble', 'random_num_gamble', 'gamble_earning',
                      'selected_round_SVO', 'role_SVO', 'SVO_earning']
SESSION_FIELDS = ['pgg_payment_match', 'pd_payment_match']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2174616233167'
