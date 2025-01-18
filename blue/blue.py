from roles.blue_goalkeeper import BlueGoalKeeper
from roles.blue_defender import BlueDefender
from roles.blue_forward import BlueForward
from roles.blue_flexible import BlueFlexible


def play(red_players, blue_players, ball):
    decisions = []
    
    for player in blue_players:
        if player['role'] == 'goalkeeper':
        # Depending on the role, call the appropriate decision-making function
            goalkeeper = BlueGoalKeeper(color='blue',**player)
            decisions.extend(goalkeeper.decide_action(ball, blue_players))

        elif player['role'] == 'defender' and player['number'] == 1:
            # Defenders make decisions based on ball possession and strategic positioning
            defender = BlueDefender(color='blue',**player)
            decisions.extend(defender.decide_action(ball, blue_players))
        elif player['role'] == 'defender' and player['number'] == 2:
            flexible = BlueFlexible(color='blue',**player)
            decisions.extend(flexible.decide_action(ball,blue_players))
        elif player['role'] == 'forward':
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            forward = BlueForward(color='blue',**player)
            decisions.extend(forward.decide_action(ball, blue_players,red_players))
        else:
            print(f"Unrecognized player role for player {player['number']}")

    return decisions