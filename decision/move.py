import exception
from utils import utils,game,size
from .decision import Decision
import math
from models import Point


class MoveDecision(Decision):
    def __init__(self, runner, player_number, player_color, destination, direction, speed, has_ball):
        super().__init__(runner, player_number, player_color)
        self.destination = destination
        self.direction = direction
        self.speed = speed
        self.has_ball = has_ball

    def validate(self):
        super().validate()
        if not 0 <= self.speed <= game.MAX_PLAYER_SPEED:
            raise exception.DecisionException('Wrong move speed')
        if not -size.FOOTBALL_PITCH_LENGTH // 2 < self.destination.x < size.FOOTBALL_PITCH_LENGTH // 2 or \
                not -size.FOOTBALL_PITCH_WIDTH // 2 < self.destination.y < size.FOOTBALL_PITCH_WIDTH // 2:
            raise exception.DecisionException('Cannot move out of screen')
        
    def perform(self):
        #self.player.move(self.destination,self.direction, self.speed) #计算与目的地的距离与角度差
        movement,alpha = self.pfa(self.has_ball)
        # self.player.x += int(movement * math.cos(alpha))
        # self.player.y += int(movement * math.sin(alpha))
        # self.player.direction = alpha
        # self.player.speed = movement

        # if the owner of the ball is the player
        if self.runner.ball.owner == self.player:
            if self.has_ball:
                # which color and player has the ball
                print("player color:",self.player.color, "player number:",self.player.number, "has the ball")
                self.runner.ball.movable = True
                # the location of the player
                self.runner.ball.move_with_ball(self.player)
            else :
                self.runner.ball.movable = False
                
        if movement < self.speed: #一步到位
            self.player.x = self.destination.x
            self.player.y = self.destination.y
            self.player.direction = alpha
        else: #正常走一tick,pfa就是修改了speed和alpha,
            self.player.x += movement * math.cos(alpha)
            self.player.y += movement * math.sin(alpha)
            self.player.direction = alpha
            self.player.speed = movement
            
        
     
    def get_enemy_positions(self):
        # 根据当前球员的颜色确定敌方球队
        enemy_members = self.runner.blue_players if self.player.color == 'red' else self.runner.red_players
        enemy_positions = [(player.x, player.y) for player in enemy_members]
        return enemy_positions
    
    def get_teammates_positions(self):
        # 获取队友列表，并排除当前玩家
        if self.player.color == 'red':
            teammates = [player for player in self.runner.red_players if player != self.player]
        else:
            teammates = [player for player in self.runner.blue_players if player != self.player]
        teammates_positions = [(player.x, player.y) for player in teammates]
        return teammates_positions
    
    def pfa(self,has_ball):
        enemy_team_position = self.get_enemy_positions()
        teammate_position = self.get_teammates_positions()
        attract_force = self.calculate_attract_force()
        if has_ball:
            repulse_forces_enemy = [self.calculate_repulse_force(enemy_pos_tuple,150,5) for enemy_pos_tuple in enemy_team_position]
        else:
            repulse_forces_enemy = [self.calculate_repulse_force(enemy_pos_tuple,100,3) for enemy_pos_tuple in enemy_team_position]
        repulse_forces_teammates = [self.calculate_repulse_force(teammates_pos_tuple,100,2.5) for teammates_pos_tuple in teammate_position]
        repulse_forces = repulse_forces_enemy + repulse_forces_teammates
        total_force = self.combine_forces(attract_force, repulse_forces)
        alpha = math.atan2(total_force[1], total_force[0])# 计算总力的方向
        speed = min(self.speed, math.sqrt(total_force[0]**2 + total_force[1]**2))# 计算移动距离，这里假设speed是一个基于力大小的动态值
        return speed, alpha

    def calculate_attract_force(self):
        # 根据球员与目的地之间的距离计算吸引力
        distance_to_destination = utils.distance(self.player, self.destination)
        direction_to_destination = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
        attract_force = (math.cos(direction_to_destination) * distance_to_destination, math.sin(direction_to_destination) * distance_to_destination)
        return attract_force
    
    def calculate_repulse_force(self, others_pos_tuple,repulse_force_intensity_factor,repulse_distance_threshold_factor):
        # repulse_force_intensity_factor 是斥力强度，敌人设为40，队友设为30
        others_pos = Point(others_pos_tuple[0], others_pos_tuple[1])
        # 计算当前球员与敌方球员之间的距离
        distance_to_others = utils.distance(self.player, others_pos)
        # 计算指向其他球员的方向
        direction_to_others = math.atan2((others_pos.y - self.player.y), (others_pos.x - self.player.x))
        # 根据距离计算排斥力的强度（这里需要您根据实际情况调整计算方式）
        # print('看看有没有斥力',1 - (distance_to_others / self.player.radius * 2))
        repulse_strength = repulse_force_intensity_factor * max(0, 1 - (distance_to_others / (self.player.radius * repulse_distance_threshold_factor)))  
        # repulse_distance_threshold比较大，则括号内越小，则一减它越大，也就是感应范围越大，所以，enemy设为2，teammates设为1.2
        repulse_forces = (-math.cos(direction_to_others) * repulse_strength, -math.sin(direction_to_others) * repulse_strength)
        return repulse_forces

    def combine_forces(self, attract_force, repulse_forces):
        # 合成吸引力和排斥力
        total_force_x = attract_force[0] + sum(force[0] for force in repulse_forces)
        total_force_y = attract_force[1] + sum(force[1] for force in repulse_forces)
        return (total_force_x, total_force_y)
