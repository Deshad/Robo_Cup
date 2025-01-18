from .grab import GrabDecision
from .kick import KickDecision
from .move import MoveDecision
from models import Point

def get_decisions(runner, red_responses, blue_responses):
    red_decisions = []
    blue_decisions = []
    for red_response in red_responses:
        red_response['player_color'] = 'red'
        red_decisions.append(_decision_factory(runner, red_response))
    for blue_response in blue_responses:
        blue_response['player_color'] = 'blue'
        if 'direction' in blue_response:
            blue_response['direction'] = blue_response['direction']
        if 'destination' in blue_response:
            blue_response['destination'] = {
                'x': blue_response['destination']['x'],
                'y': blue_response['destination']['y'],
            }
        blue_decisions.append(_decision_factory(runner, blue_response))
    return _unique_decisions(red_decisions), _unique_decisions(blue_decisions)

def _decision_factory(runner, decision):
    if decision['type'] == 'move':
        return MoveDecision(
            runner=runner,
            player_number=decision['player_number'],
            player_color=decision['player_color'],
            destination=Point(decision['destination']['x'], decision['destination']['y']),
            direction=decision['direction'] % 360,
            speed=decision['speed'],
            has_ball=decision['has_ball'],
        )
    if decision['type'] == 'kick':
        return KickDecision(
            runner=runner,
            player_number=decision['player_number'],
            player_color=decision['player_color'],
            direction=decision['direction'] % 360,
            power=decision['power'],
        )
    if decision['type'] == 'grab':
        if 'direction' in decision:
            return GrabDecision(
                runner=runner,
                player_number=decision['player_number'],
                player_color=decision['player_color'],
                direction=decision['direction'] % 360
            )
        else:
            return GrabDecision(
                runner=runner,
                player_number=decision['player_number'],
                player_color=decision['player_color'],
                direction=0
            )
    # if decision['type'] == 'collision':
    #     return Collision(
    #         runner=runner,
    #         player_number=decision['player_number'],
    #         player_color=decision['player_color'],
    #         direction=decision['direction'] % 360,
    #         #speed=decision['speed'],
    #     )

def _unique_decisions(decisions):
    uniqued_decisions = []
    for decision in decisions:
        flag = True
        for uniqued_decision in uniqued_decisions:
            if type(decision) is type(uniqued_decision) and decision.player == uniqued_decision.player:
                flag = False
        if flag:
            uniqued_decisions.append(decision)
    return uniqued_decisions
