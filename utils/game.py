from .size import *
from .utils import *
from models import player

PLAYER_COUNT = 4

FRICTION = 3 
MAX_PLAYER_SPEED = PLAYER_RADIUS
MAX_KICK_POWER = 60 


# RULES
ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER = 4
ALLOWED_PLAYERS_AROUND_BALL_NUMBER = 2
ALLOWED_PLAYERS_AROUND_BALL_RADIUS = 54 # 3 * (PLAYER_RADIUS + BALL_RADIUS)
BALL_CROWDED_BAN_CYCLES = 25
PENALTY_ARIA_BAN_CYCLES = 20


RED_PLAYERS_INITIAL_VALUES = []
BLUE_PLAYERS_INITIAL_VALUES = []


RED_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': -428,
    'y': 0,
    'name': "Player0 ",
    'radius': PLAYER_RADIUS,
    'role':'goalkeeper'
})
RED_PLAYERS_INITIAL_VALUES.append({
    'number': 1,
    'x': -324,
    'y': 216,
    'name': "Player1 ",
    'radius': PLAYER_RADIUS,
    'role':'defender'
})
'''
RED_PLAYERS_INITIAL_VALUES.append({
    'number': 2,
    'x': -250,
    'y': -217,
    'name': "Player2 ",
    'radius': PLAYER_RADIUS,
    'role':'defender'
})
'''
RED_PLAYERS_INITIAL_VALUES.append({
    'number': 2,
    'x': -167,
    'y': 216,
    'name': "Player3 ",
    'radius': PLAYER_RADIUS,
    'role':'forward'
})
RED_PLAYERS_INITIAL_VALUES.append({
    'number': 3,
    'x': -83,
    'y': -217,
    'name': "Player4 ",
    'radius': PLAYER_RADIUS,
    'role':'forward'
})




BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': 428,
    'y': 0,
    'name': "Player0 ",
    'radius': PLAYER_RADIUS,
    'role':'goalkeeper'
})
BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 1,
    'x': 334,
    'y': -216,
    'name': "Player1 ",
    'radius': PLAYER_RADIUS,
    'role':'defender'
})
BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 2,
    'x': 250,
    'y': 217,
    'name': "Player2 ",
    'radius': PLAYER_RADIUS,
    'role':'defender'
})
BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 3,
    'x': 167,
    'y': -216,
    'name': "Player3 ",
    'radius': PLAYER_RADIUS,
    'role':'forward'
})
'''
BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 4,
    'x': 83,
    'y': 217,
    'name': "Player4 ",
    'radius': PLAYER_RADIUS,
    'role':'forward'
})
'''



# RED_PLAYERS_INITIAL_VALUES.append({
#     'number': 0,
#     'x': -FOOTBALL_PITCH_LENGTH // 2 + 3 * GOAL_DEPTH,
#     'y': 0,
#     'name': "Player{}".format(0),
#     'radius': PLAYER_RADIUS,
#     'role':'goalkeeper'
# })

# BLUE_PLAYERS_INITIAL_VALUES.append({
#     'number': 0,
#     'x': FOOTBALL_PITCH_LENGTH // 2 - 3 * GOAL_DEPTH,
#     'y': 0,
#     'name': "Player{}".format(0),
#     'radius': PLAYER_RADIUS,
#     'role':'goalkeeper'
# })

# for i in range(1, PLAYER_COUNT):
#     x = (FOOTBALL_PITCH_LENGTH // 2 // (PLAYER_COUNT // 2) + 1) * (PLAYER_COUNT - i - 1) // 2
#     y = FOOTBALL_PITCH_WIDTH // 3 if i % 2 == 1 else -FOOTBALL_PITCH_WIDTH // 3
#     RED_PLAYERS_INITIAL_VALUES.append({
#         'number': i,
#         'x':-x,
#         'y': y,
#         'name': "Player{}".format(i),
#         'radius': PLAYER_RADIUS,
#         'role':'defender'
#     })
#     BLUE_PLAYERS_INITIAL_VALUES.append({
#         'number': i,
#         'x': x,
#         'y': -y,
#         'name': "Player{}".format(i),
#         'radius': PLAYER_RADIUS,
#         'role':'defender'
#     })



SHOULD_PRINT_DECISIONS_ERROR = True
