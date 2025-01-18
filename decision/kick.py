import random
import exception
import utils
from .decision import Decision


class KickDecision(Decision):
    def __init__(self, runner, player_number, player_color, direction, power):
        super().__init__(runner, player_number, player_color)
        self.player_number = player_number
        self.player_color = player_color
        self.direction = direction
        self.power = power

    def validate(self):
        super().validate()
        if not 0 <= self.power <= utils.MAX_KICK_POWER:
            raise exception.DecisionException('Wrong kick power')
        if self.runner.ball.owner is None:
            raise exception.DecisionException('The player is not the owner of the ball') 
        if self.runner.ball.owner.number != self.player_number:
            raise exception.DecisionException('The player is not the owner of the ball') 
    def perform(self):
        self.runner.ball.owner = None
        self.runner.ball.direction = self.direction
        self.runner.ball.speed = self.power
        self.runner.ball.movable = True
        print("Ball kicked by", self.player.color, self.player.number)
        if random.random() < 1: #虽然这样不太合理，但它简答
            self.player.ban_cycles = 4
