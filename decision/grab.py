import random
import exception
import utils
from .decision import Decision
import math
import time
class GrabDecision(Decision):
    def __init__(self, runner, player_number, player_color,direction):
        super().__init__(runner, player_number, player_color)
        # self.direction = direction
    

    def perform(self):
        self._grab_ball()

    def _grab_ball(self):
        grab_radius = 24  # The radius of the player's grabbing range
        min_distance = float('inf')  # 初始化最小距离为正无穷大
        closest_player = None
        
        # if the player who tries to grab is the closest to the ball and the distance is less than the grab_radius
        for player in self.runner.players:
            distance = utils.distance(player, self.runner.ball)
            if distance <= grab_radius and distance < min_distance:
                min_distance = distance
                closest_player = player
        
        # if closest player exists and the owner of the ball is not the closest player
        if closest_player == self.player:
            self.runner.ball.owner = closest_player
            self.runner.ball.direction = closest_player.direction
            self.runner.ball.grab(closest_player)
        # if self.runner.ball.owner exists, print the color and number of the owner
            print("Ball grabbed by", self.runner.ball.owner.color, self.runner.ball.owner.number)
        # if closest_player:
        #     # sleep 1 second
        #     self.runner.ball.owner = closest_player
        #     # Here you should also set the ball's position relative to the player
        #     # This might need information about from which direction the ball was grabbed, which could be tracked.
        #     ball_direction = math.radians(closest_player.direction)
            
        #     # Call the ball's grab method and set the ball's owner and grab_direction
        #     # self.runner.ball.grab(closest_player)
        #     print("Ball grabbed by", closest_player.color, closest_player.number)


            