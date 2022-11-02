from os import environ

SESSION_CONFIGS = [
    dict(
        name='main_task_sim_easy',
        app_sequence=['Game'],
        num_demo_participants=8,
        easy=1,
        sim=1,
        pd_only=0,
        same_group=0,
        doc="""
        This is the oTree program for treatment with both games"""

    ),
    dict(
        name='treatment_sim_easy',
        app_sequence=['Quiz','Game','GambleTask','Demographics','Payment'],
        num_demo_participants=8,
        easy=1,
        sim=1,
        pd_only=0,
        same_group=0,
        doc="""program for simultaneous treatment with easy pd"""

    ),
    # dict(
    #     name='gamble_task',
    #     app_sequence=['GambleTask'],
    #     num_demo_participants=1
    # ),
    # dict(
    #     name='demographics',
    #     app_sequence=['Demographics'],
    #     num_demo_participants=1,
    #     sim=0,
    # ),
    # dict(
    #     name='quiz_sim_easy',
    #     app_sequence=['Quiz'],
    #     num_demo_participants=1,
    #     easy=1,
    #     sim=1,
    #     pd_only=0,
    #     same_group=0,
    # ),
    # dict(
    #     name='quiz_pgg',
    #     app_sequence=['Quiz'],
    #     num_demo_participants=1,
    #     easy=0,
    #     sim=0,
    #     pd_only=0,
    #     same_group=0,
    # # ),
    # dict(
    #     name='quiz_pd',
    #     app_sequence=['Quiz'],
    #     num_demo_participants=1,
    #     easy=0,
    #     sim=0,
    #     pd_only=1,
    #     same_group=0,
    # ),
    dict(
        name='main_task_pd_easy',
        app_sequence=['Game'],
        num_demo_participants=8,
        easy=1,
        sim=0,
        pd_only=1,
        same_group=0,
        doc="""
        This is the oTree program for treatment with easy PD game only"""
    ),
    dict(
        name='main_task_pd_difficult',
        app_sequence=['Game'],
        num_demo_participants=8,
        easy=0,
        sim=0,
        pd_only=1,
        same_group=0,
        doc="""
    This is the oTree program for treatment with easy PD game only"""
    ),
    dict(
        name='main_task_pgg',
        app_sequence=['Game'],
        num_demo_participants=8,
        easy=1,
        sim=0,
        pd_only=0,
        same_group=0,
        doc="""
    This is the oTree program for treatment with PD game only"""
    ),
    # dict(
    #     name='Block_Random_Termination',
    #     app_sequence=['block_random_termination'],
    #     num_demo_participants=1,
    #
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.0025, participation_fee=0.00, doc=""
)
# use_browser_bots=True
PARTICIPANT_FIELDS = ['quiz_num_correct', 'quiz_earning', 'progress',
                      'pgg_earning', 'pd_earning', 'task1_history','chosen_gamble', 'random_num_gamble', 'gamble_earning',
                      'selected_round_SVO', 'role_SVO', 'SVO_earning']
#'selected_match_pgg', 'selected_match_pd',
SESSION_FIELDS = ['pd_only','sim','num_match']
#'pgg_payment_match', 'pd_payment_match',
# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='SO1',
        display_name='Spillover_Session1',
        participant_label_file='_rooms/lab.txt',
        # use_secure_urls=True
    ),
    dict(
        name='SO2',
        display_name='Spillover_Session2',
        participant_label_file='_rooms/lab.txt',
        # use_secure_urls=True
    )
]
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2174616233167'
