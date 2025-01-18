import random
import time
from threading import Thread,Lock

import pygame as pg

import exception
import models
import utils
from decision import get_decisions
from red import play as red_play
from blue import play as blue_play
import math



def red_fire(*args, **kwargs):
    global red_responses
    red_responses = red_play(*args, **kwargs)

def blue_fire(*args, **kwargs):
    global blue_responses
    blue_responses = blue_play(*args, **kwargs)


class Runner:
    def __init__(self, config):
        pg.init()
        self.config = config
        self.screen = pg.display.set_mode((utils.SCREEN_LENGTH, utils.SCREEN_WIDTH))
        self.ball = models.Ball()
        self._init_players()
        self.scoreboard = models.Scoreboard()
        self._show_and_increase_cycle_number()
        self.red_lock = Lock()  # 创建红队的锁
        self.blue_lock = Lock()  # 创建蓝队的锁

    def run(self):
        global actions
        global red_responses, blue_responses
        end = False
        pause = False
        while not end:
            # sleep 1 second
            print("-----------------")
            # events: pause and quit
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        pause = not pause
                        print('pause')
                    if event.key == pg.K_ESCAPE:
                        end = True
                if event.type == pg.QUIT:
                    end = True
            if pause:
                continue
            if self.scoreboard.cycle_number > self.config.max_cycle:
                continue
            red_responses = None
            blue_responses = None

            red_thread = Thread(
                target=red_fire,
                args=self._get_args_for_red_team(),
            )
            blue_thread = Thread(
                target=blue_fire,
                args=self._get_args_for_blue_team(),
            )
            blue_thread.start()
            red_thread.start()
            for _ in range(self.config.delay_count):
                time.sleep(self.config.delay_amount)
                with self.red_lock:  # 加锁
                    with self.blue_lock:  # 加锁
                        if red_responses is not None and blue_responses is not None:
                            break
            if not isinstance(red_responses, list):
                red_responses = []
            if not isinstance(blue_responses, list):
                blue_responses = []

            self.perform_decisions(red_responses, blue_responses)
            self.decrement_ban_cycles()
            players = self.blue_players+self.red_players
            self.ball.move(players)
            self.check_if_scored()
            self.check_if_overlapp(5)
            
            
            # self.check_if_the_bus_is_parked()
            # self.check_if_ball_is_crowded()
            self.adjust_overlapping_players()  # Adjust overlapping players to prevent freezing
            self.adjust_ball_player_overlap()
            self._show_and_increase_cycle_number()
            if self.scoreboard.cycle_number > self.config.max_cycle:
                if self.config.additional_delay:
                    time.sleep(4)
                end = True

    @staticmethod
    def handle_decision_perform_with_exception(decision):
        try:
            decision.validate()
            decision.perform()
        except exception.DecisionException as de:
            if utils.SHOULD_PRINT_DECISIONS_ERROR:
                print(de)
                
    def adjust_ball_player_overlap(self):
        for player in self.red_players + self.blue_players:
            if utils.distance(player, self.ball) < player.radius + self.ball.radius:
                # プレイヤーとボールが重なった場合、ボールをプレイヤーから遠ざける
                angle = math.atan2(self.ball.y - player.y, self.ball.x - player.x)
                overlap_distance = player.radius + self.ball.radius - utils.distance(player, self.ball)
                self.ball.x += math.cos(angle) * overlap_distance
                self.ball.y += math.sin(angle) * overlap_distance
                # # ボールの速度と方向を更新（反発するように）
                # if self.ball.owner is player:
                #     self.ball.speed = min(max(self.ball.speed, 5), 10)  # 一定の速度を保証
                #     self.ball.direction = math.degrees(angle)

    def perform_decisions(self, red_responses, blue_responses):
        red_decisions, blue_decisions = get_decisions(self, red_responses, blue_responses)

        while red_decisions and blue_decisions:
            # Randomly choose the order of execution
            order = random.sample([red_decisions, blue_decisions], k=2)
            for decisions in order:
                if decisions:
                    decision = decisions.pop(0)
                    self.handle_decision_perform_with_exception(decision)

        # Execute remaining decisions if any team is empty
        for red_decision in red_decisions: #可以在这里检查一下，如果是kick则有几率上冻结，还有另一种，如果产生重叠，则一方回躺下，
            self.handle_decision_perform_with_exception(red_decision)
        for blue_decision in blue_decisions:
            self.handle_decision_perform_with_exception(blue_decision)
        # for test_decision in test_decisions:
        #     self.handle_decision_perform_with_exception(test_decision)

        self.decrement_ban_cycles()
    

    
    def decrement_ban_cycles(self):
        for player in self.red_players + self.blue_players:
            if player.ban_cycles > 0:
                player.ban_cycles -= 1

                
    def check_if_overlapp(self,ban_cycles):
        new_distance = 2 * utils.PLAYER_RADIUS + 4
        players = self.blue_players+self.red_players
        for i,player_a in enumerate(players):
            for j, player_b in enumerate(players):
                if i != j:  # 确保不与自身比较
                    # 计算两个玩家之间的距离
                    dx = abs(player_a.x - player_b.x)
                    dy = abs(player_a.y - player_b.y)
                    dx = dx if dx != 0 else 0.01
                    dy = dy if dy != 0 else 0.01
                    distance = (dx ** 2 + dy ** 2) ** 0.5


                    # 如果距离小于或等于2 radius，则视为重叠
                    if distance <= 2 * utils.PLAYER_RADIUS:
                        #两步，第一，把二者先弹开，第二，把二者冻住
                        unit_dx = dx / distance
                        unit_dy = dy / distance
                        # 设置新位置
                        new_x = player_a.x + unit_dx * new_distance if player_a.x < player_b.x else player_a.x - unit_dx * new_distance
                        new_y = player_a.y + unit_dy * new_distance if player_a.y < player_b.y else player_a.y - unit_dy * new_distance
                        # 更新player_b的位置
                        # print('设置新位置了,首先,原来的a,X:',player_a.x,'Y:',player_a.y,', b,X',player_b.x,'Y:',player_b.y,'新距离',new_x,new_y)
                        player_b.x, player_b.y = new_x, new_y

                        self.freeze_player(player_a,ban_cycles,0.3)
                        self.freeze_player(player_b,ban_cycles,0.3)

    def freeze_player(self, player, ban_cycles, probability):
        if random.random() < probability:  
            if player==self.ball.owner:#球没了
                self.ball.owner = None 
                self.ball.speed = 16
                self.ball.direction = random.random()*360
            player.ban_cycles = ban_cycles

    def check_if_scored(self):
        if self.ball.x - self.ball.radius  <= -utils.FOOTBALL_PITCH_LENGTH // 2 and \
                (-utils.GOAL_WIDTH // 2 <= self.ball.y <= utils.GOAL_WIDTH // 2):
            self.scoreboard.blue_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = None
            self.ball.speed = 0
            self.red_players[utils.PLAYER_COUNT - 1].x, self.red_players[utils.PLAYER_COUNT - 1].y = self.ball.x-24, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)
        if self.ball.x + self.ball.radius>= utils.FOOTBALL_PITCH_LENGTH // 2 and \
                (-utils.GOAL_WIDTH // 2 <= self.ball.y <= utils.GOAL_WIDTH // 2):
            self.scoreboard.red_score += 1
            self._init_players()
            self.ball.x, self.ball.y = (0, 0)
            self.ball.direction = None
            self.ball.owner = None
            self.ball.speed = 0
            self.blue_players[utils.PLAYER_COUNT - 1].x, self.blue_players[utils.PLAYER_COUNT - 1].y = self.ball.x+24, self.ball.y
            if self.config.additional_delay:
                time.sleep(1)
                
    def end(self):
        result_file = open('result.txt', 'w')
        result_file.write(f"{self.scoreboard.red_score} {self.scoreboard.blue_score}")
        print('end')

    def _init_players(self):
        red_players = []
        blue_players = []
        
        for red_player in utils.RED_PLAYERS_INITIAL_VALUES:
            red_players.append(models.Player(
                color='red',
                **red_player,
            ))
        for blue_player in utils.BLUE_PLAYERS_INITIAL_VALUES:
            blue_players.append(models.Player(
                color='blue',
                **blue_player,
            ))
        self.red_players = red_players
        self.blue_players = blue_players
        self.players = red_players + blue_players
        
    def _get_args_for_red_team(self):
        red_players_info = []
        blue_players_info = []
        for red_player in self.red_players:
            red_players_info.append(red_player.info)
        for blue_player in self.blue_players:
            blue_players_info.append(blue_player.info)
        ball_info = self.ball.info
        return red_players_info, blue_players_info, ball_info

    def _get_args_for_blue_team(self):
        red_players_info = []
        blue_players_info = []
        for red_player in self.red_players:
            red_players_info.append(red_player.info)
        for blue_player in self.blue_players:
            blue_players_info.append(blue_player.info)
        ball_info = self.ball.info
        return red_players_info, blue_players_info, ball_info

    def _show_and_increase_cycle_number(self):
        if self.config.graphical_output:
            self.screen.fill(utils.GRASS_COLOR)
            self._draw_margins()
            self._draw_football_pitch()
            self._draw_team_names()
            # Draw players and their direction with team-specific colors
            for red_player in self.red_players:
                red_player.draw(self.screen)
                self.draw_player_direction(red_player, 'red')
            for blue_player in self.blue_players:
                blue_player.draw(self.screen)
                self.draw_player_direction(blue_player, 'blue')
            self.ball.draw(self.screen)
            self.scoreboard.draw(self.screen)
            pg.display.update()
        self.scoreboard.cycle_number += 1

    def _draw_football_pitch(self):
        # DRAW GOALS
        # 红队球门坐上角
        red_goal_pygame_x = utils.HORIZONTAL_MARGIN + utils.BORDER_STRIP_WIDTH - utils.GOAL_DEPTH
        # red_goal_pygame_x = utils.HORIZONTAL_MARGIN - utils.GOAL_DEPTH
        red_goal_pygame_y = utils.SCREEN_WIDTH // 2 - utils.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            utils.GOAL_COLOR['red'],
            (red_goal_pygame_x, red_goal_pygame_y, utils.GOAL_DEPTH, utils.GOAL_WIDTH),
            0,
        )
        # 蓝队球门坐上角
        blue_goal_pygame_x = utils.SCREEN_LENGTH - utils.HORIZONTAL_MARGIN - utils.BORDER_STRIP_WIDTH
        # blue_goal_pygame_x = utils.SCREEN_LENGTH - utils.HORIZONTAL_MARGIN
        blue_goal_pygame_y = utils.SCREEN_WIDTH // 2 - utils.GOAL_WIDTH // 2
        pg.draw.rect(
            self.screen,
            utils.GOAL_COLOR['blue'],
            (blue_goal_pygame_x, blue_goal_pygame_y, utils.GOAL_DEPTH, utils.GOAL_WIDTH),
            0,
        )
        # DRAW LEFT GOAL AREA (RED GOAL AREA)
        left_goal_area_pygame_x = utils.HORIZONTAL_MARGIN + utils.BORDER_STRIP_WIDTH
        # left_goal_area_pygame_x = utils.HORIZONTAL_MARGIN
        left_goal_area_pygame_y = (utils.SCREEN_WIDTH // 2) - (utils.GOAL_AREA_WIDTH // 2)
        pg.draw.rect(
            self.screen,
            utils.LINE_COLOR,
            (left_goal_area_pygame_x, left_goal_area_pygame_y, utils.GOAL_AREA_LENGTH, utils.GOAL_AREA_WIDTH),
            utils.LINE_THICKNESS
        )

        # DRAW RIGHT GOAL AREA (BLUE GOAL AREA)
        right_goal_area_pygame_x = utils.SCREEN_LENGTH - utils.BORDER_STRIP_WIDTH - utils.HORIZONTAL_MARGIN - utils.GOAL_AREA_LENGTH
        # right_goal_area_pygame_x = utils.SCREEN_LENGTH - utils.HORIZONTAL_MARGIN - utils.GOAL_AREA_LENGTH
        right_goal_area_pygame_y = (utils.SCREEN_WIDTH // 2) - (utils.GOAL_AREA_WIDTH // 2)
        pg.draw.rect(
            self.screen,
            utils.LINE_COLOR,
            (right_goal_area_pygame_x, right_goal_area_pygame_y, utils.GOAL_AREA_LENGTH, utils.GOAL_AREA_WIDTH),
            utils.LINE_THICKNESS
        )
        # 禁区
        # DRAW PENALTY AREA
            # LEFT
        left_x1 = utils.HORIZONTAL_MARGIN + utils.BORDER_STRIP_WIDTH
        left_x2 = utils.HORIZONTAL_MARGIN + utils.BORDER_STRIP_WIDTH + utils.PENALTY_AREA_LENGTH
        left_y1 = utils.SCREEN_WIDTH // 2 - utils.PENALTY_AREA_WIDTH // 2
        left_y2 = utils.SCREEN_WIDTH // 2 + utils.PENALTY_AREA_WIDTH // 2
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x1, left_y1),
            (left_x2, left_y1),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x2, left_y1),
            (left_x2, left_y2),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (left_x1, left_y2),
            (left_x2, left_y2),
            utils.LINE_THICKNESS,
        )
            # RIGHT
        right_x1 = utils.SCREEN_LENGTH - utils.BORDER_STRIP_WIDTH - utils.HORIZONTAL_MARGIN
        right_x2 = right_x1 - utils.PENALTY_AREA_LENGTH
        right_y1 = left_y1
        right_y2 = left_y2
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x1, right_y1),
            (right_x2, right_y1),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x2, right_y1),
            (right_x2, right_y2),
            utils.LINE_THICKNESS,
        )
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (right_x1, right_y2),
            (right_x2, right_y2),
            utils.LINE_THICKNESS,
        )

        # DRAW PITCH BOUNDARY
        boundary_x_left = utils.HORIZONTAL_MARGIN + utils.BORDER_STRIP_WIDTH
        boundary_x_right = utils.SCREEN_LENGTH - utils.HORIZONTAL_MARGIN - utils.BORDER_STRIP_WIDTH
        boundary_y_top = utils.VERTICAL_MARGIN + utils.BORDER_STRIP_WIDTH
        boundary_y_bottom = utils.SCREEN_WIDTH - utils.VERTICAL_MARGIN - utils.BORDER_STRIP_WIDTH

            # 顶部边界线
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (boundary_x_left, boundary_y_top),
            (boundary_x_right, boundary_y_top),
            utils.LINE_THICKNESS,
        )

        # 底部边界线
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (boundary_x_left, boundary_y_bottom),
            (boundary_x_right, boundary_y_bottom),
            utils.LINE_THICKNESS,
        )

        # 左侧边界线
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (boundary_x_left, boundary_y_top),
            (boundary_x_left, boundary_y_bottom),
            utils.LINE_THICKNESS,
        )

        # 右侧边界线
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (boundary_x_right, boundary_y_top),
            (boundary_x_right, boundary_y_bottom),
            utils.LINE_THICKNESS,
        )


        # DRAW CENTER POINT
        pg.draw.circle(
            self.screen,
            utils.LINE_COLOR,
            utils.convert_coordinate_cartesian_to_pygame(0, 0),
            utils.CENTER_POINT_RADIUS,
            0,
        )
        # DRAW CENTER CIRCLE
        pg.draw.circle(
            self.screen,
            utils.LINE_COLOR,
            utils.convert_coordinate_cartesian_to_pygame(0, 0),
            utils.CENTER_CIRCLE_RADIUS,
            utils.LINE_THICKNESS,
        )
        # DRAW CENTER LINE
        pg.draw.line(
            self.screen,
            utils.LINE_COLOR,
            (utils.SCREEN_LENGTH // 2 - utils.LINE_THICKNESS // 2, utils.VERTICAL_MARGIN),
            (utils.SCREEN_LENGTH // 2 - utils.LINE_THICKNESS // 2, utils.SCREEN_WIDTH - utils.VERTICAL_MARGIN),
            utils.LINE_THICKNESS,
        )
        


    def _draw_team_names(self):
        utils.write_text_on_pygame_screen(
            self.screen,
            30,
            utils.SCOREBOARD_RED_SCORE_COLOR,
            self.config.team1_name,
            -utils.SCREEN_LENGTH // 4,
            utils.SCREEN_WIDTH // 2 - 5,
        )
        utils.write_text_on_pygame_screen(
            self.screen,
            30,
            utils.SCOREBOARD_BLUE_SCORE_COLOR,
            self.config.team2_name,
            utils.SCREEN_LENGTH // 4,
            utils.SCREEN_WIDTH // 2 - 5,
        )

    def _draw_margins(self):
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, utils.SCREEN_LENGTH, utils.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, utils.SCREEN_WIDTH - utils.VERTICAL_MARGIN, utils.SCREEN_LENGTH, utils.VERTICAL_MARGIN)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (0, 0, utils.HORIZONTAL_MARGIN, utils.SCREEN_WIDTH)
        )
        pg.draw.rect(
            self.screen,
            (255, 255, 255),
            (utils.SCREEN_LENGTH - utils.HORIZONTAL_MARGIN, 0, utils.HORIZONTAL_MARGIN, utils.SCREEN_WIDTH)
        )

    def draw_player_direction(self, player, team_color):
        # Assuming player.direction is the direction in radians
        line_length = 30  # Length of the direction line
        end_x = player.x + line_length * math.cos(player.direction)
        end_y = player.y + line_length * math.sin(player.direction)
        
        # Convert player and end point positions if necessary
        player_pos = utils.convert_coordinate_cartesian_to_pygame(player.x, player.y)
        end_pos = utils.convert_coordinate_cartesian_to_pygame(end_x, end_y)
        
        # Determine color based on the team
        color = (255, 0, 0) if team_color == 'red' else (0, 0, 255)
        
        # Draw the line
        pg.draw.line(self.screen, color, player_pos, end_pos, 2)
        
    
    def adjust_overlapping_players(self):
        for player in self.red_players + self.blue_players:
            for other_player in self.red_players + self.blue_players:
                if player != other_player and self.is_overlapping(player, other_player):
                    self.separate_players(player, other_player)

    def is_overlapping(self, player1, player2):
        distance = utils.distance(player1, player2)
        return distance < (player1.radius + player2.radius)  # Assuming players have a 'radius' attribute

    def separate_players(self, player1, player2):
        # Adjust players' positions slightly to no longer overlap
        angle = math.atan2(player2.y - player1.y, player2.x - player1.x)
        displacement = 1  # Adjust as needed for your game's scale
        player1.x -= math.cos(angle) * displacement
        player1.y -= math.sin(angle) * displacement
        player2.x += math.cos(angle) * displacement
        player2.y += math.sin(angle) * displacement
