# forward.py
from utils import get_direction, get_distance,how_to_grab, is_within_angle_to_ball, reposition_around_ball, is_closest_to_ball
from utils import FOOTBALL_PITCH_LENGTH,FOOTBALL_PITCH_WIDTH
import numpy as np
from itertools import combinations
from models import player
import random
import heapq
class RedForward(player.Player):
    
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)
        self.historic_centers = []
        self.cost_map = [[1] * (FOOTBALL_PITCH_LENGTH // 50) for _ in range(FOOTBALL_PITCH_WIDTH // 50)]  # Default cost value

    '''
    def decide_action(self, ball, players,opponent_players):
        decisions = []
        strategic_position = self.calculate_strategic_position(ball, players,opponent_players)
        self.update_cost_map(ball,players,opponent_players)
        if self.in_attacking_area(ball):
            if self.is_closest_to_ball(players, ball):
                if self.owns_ball(ball):
                    pass_decision = self.find_best_receiver(players,opponent_players)
                    if self.in_shoot_area():
                        decisions.append(self.attempt_to_score(ball))
                    elif pass_decision:
                        decisions.append(pass_decision)
                    elif self.opponent_in_randius(opponent_players):
                        decisions.append(self.random_kick_out(opponent_players))
                    elif self.can_be_grab(opponent_players):
                        decisions.append(self.shoot())
                    else:
                        decisions.append(self.move_towards_goal(ball))
                elif ball['owner_color'] != self.color:
                    decisions.append(self.intercept_ball(ball,players,opponent_players))
            elif self.in_strategic_position(ball,players,opponent_players):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))

        elif self.owns_ball(ball):
            print(f"forward{self.color}{self.number}")
            pass_decision = self.find_best_receiver(players,opponent_players)              
            if pass_decision:
                decisions.append(pass_decision)
            elif self.opponent_in_randius(opponent_players):
                decisions.append(self.random_kick_out(opponent_players))
            else:
                decisions.append(self.attempt_to_score(ball))
        
        elif self.in_strategic_position(ball,players,opponent_players):
                decisions.append(self.face_ball_direction(ball))        
        else:
            decisions.append(self.move_to_strategic_position(strategic_position))
            
        return decisions
    '''

    def decide_action(self, ball, players,opponent_players):
        decisions = []
        strategic_position = self.calculate_strategic_position(ball, players,opponent_players)
        self.update_cost_map(ball,players,opponent_players)
        if self.in_attacking_area(ball):
            if ball['owner_color'] == self.color:
                if self.owns_ball(ball):           
                    print("red_forward owns ball")
                    pass_decision = self.find_best_receiver(players,opponent_players)
                    if self.in_shoot_area():
                        print("red_forward in_shoot_area")
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                        if is_within_angle_to_ball(self, ball,  direction):
                            decisions.append(self.attempt_to_score(ball))
                        else:
                            decisions.append(reposition_around_ball(self, ball, direction))
                    elif pass_decision:
                        print("red_forward pass_decision:",pass_decision)
                        if is_within_angle_to_ball(self, ball, pass_decision['direction']):
                            decisions.append(pass_decision)
                        else:
                            decisions.append(reposition_around_ball(self, ball, pass_decision['direction']))
                    elif self.opponent_in_randius(opponent_players):
                        print("red_forward opponent_in_randius")
                        direction = how_to_grab({'x': self.x, 'y': self.y},opponent_players)
                        if is_within_angle_to_ball(self, ball, direction):
                            print("red_forward random_kick_out")
                            decisions.append(self.random_kick_out(opponent_players))
                        else: 
                            decisions.append(reposition_around_ball(self, ball, how_to_grab({'x': self.x, 'y': self.y},opponent_players)))
                    elif self.can_be_grab(opponent_players):
                        print("red_forward can shoot")
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                        if is_within_angle_to_ball(self, ball, direction):
                            decisions.append(self.shoot())
                        else:
                            decisions.append(reposition_around_ball(self, ball, direction))
                    else:
                        print("red_forward move_towards_goal")
                        direction = get_direction({'x': self.x, 'y': self.y}, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                        if is_within_angle_to_ball(self, ball, direction):
                            decisions.append(self.move_towards_goal(ball))
                        else:
                            decisions.append(reposition_around_ball(self, ball, direction))
                elif is_closest_to_ball(self, ball, players):
                    print("red_forward is_closest_to_ball and intercept_ball")
                    decisions.append(self.intercept_ball(ball,players,opponent_players))
                else:
                    decisions.append(self.move_to_strategic_position(strategic_position))
            elif is_closest_to_ball(self, ball, players):
                print("red_forward is_closest_to_ball and intercept_ball")
                decisions.append(self.intercept_ball(ball,players,opponent_players))
            elif self.in_strategic_position(ball,players,opponent_players):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position)) 
        elif self.in_strategic_position(ball,players,opponent_players):
                decisions.append(self.face_ball_direction(ball))        
        else:
            decisions.append(self.move_to_strategic_position(strategic_position))
            
        return decisions

    def in_attacking_area(self,ball):
        if self.color == 'blue':
            x = ball['x']
            x1 = -450
            x2 = 75
        elif self.color == 'red':
            x = ball['x']
            x1 = -75
            x2 = 450
        return x1 < x < x2
    
    def shoot(self):
        # Example action to attempt scoring        
        if self.color == 'red':
            goal_position = {'x': 400, 'y': 0}
        else:
            goal_position = {'x': -400, 'y': 0}
        direction = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {
            'type': 'kick',
            'player_number': self.number,
            'direction': direction,
            'power': 40,  # Power might be adjusted based on distance to goal
        }        

    def move_towards_ball(self,ball):
        # Example action to move towards the ball
        #print(f"Forward {self.number} moving towards the ball at {ball['x']}, {ball['y']}")
        direction = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': ball,
            'direction': direction,
            'speed': 10,  # Speed might be adjusted based on the situation
            'has_ball':False
        }

    def attempt_to_score(self, ball):
        # Example action to attempt scoring        
        if self.color == 'red':
            goal_position = {'x': 450, 'y': 0}
        else:
            goal_position = {'x': -450, 'y': 0}
        direction = get_direction({'x': self.x, 'y': self.y}, goal_position)
        if self.in_shoot_area():
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction,
                'power': 50,  # Power might be adjusted based on distance to goal
            }
        else:
            return self.move_towards_goal(ball)

    
    def in_shoot_area(self):
        if (self.color == 'red' and self.x >= 200) or (self.color == 'blue' and self.x <= -200):
            return True  #需要定义射门区域
        return False

    def calculate_strategic_position(self, ball, players,opponent_players):
        if not self.own_half(ball):
            # Scenario 1: Ball on our attacking half
            if ball['owner_color'] != self.color and not is_closest_to_ball(self, ball, players):
                # Move to a position that covers the farthest goal from the ball
                return self.calculate_offensive_strategic_position(ball, players,opponent_players)
            elif ball['owner_color'] == self.color and ball['owner_number'] != self.number:
                # Scenario when we own the ball or are closest to it
                return self.calculate_offensive_strategic_position(ball, players,opponent_players)
        elif self.owns_ball(ball):
            return self.calculate_offensive_strategic_position(ball,players,opponent_players)
        else:
            return self.calculate_offensive_strategic_position(ball,players,opponent_players)

    def default_strategic_position(self,ball):
        # Return a default strategic position based on the side of the field
        y = 200 if self.number == 3 else -200
        x = 200 
        #两个前锋一人一个默认的战略点，避免打架
        return{'x':x,'y':y}
        #return {'x': (self.x + ball['x'])/2, 'y': (self.y + ball['y'])/2}  # Example value

    # def calculate_defensive_strategic_position(self, ball, players,opponent_players):
    #     # Calculate defensive position based on ball and goal locations
    #     # Implement logic from documentation
    #     #return self.cal_sparse_area(ball,opponent_players)  # Placeholder logic
    #     return self.calculate_a_star_defensive_position(ball,players,opponent_players)

    def calculate_offensive_strategic_position(self, ball, players,opponent_players):
        # Calculate offensive position when in possession but not holding the ball
        # Implement logic from documentation
        #return self.cal_sparse_area(ball,players)  # Placeholder logic  
        return self.calculate_a_star_offensive_position(ball,players,opponent_players)
    def in_strategic_position(self,ball,players,opponent_players):
        # Check if the defender is in a strategic position
        strategic_pos = self.calculate_strategic_position(ball,players,opponent_players)
        if not strategic_pos:
            return True
        strategic_x = strategic_pos['x']
        strategic_y = strategic_pos['y']
        strategic_x_min, strategic_x_max = strategic_x - 10, strategic_x + 10
        strategic_y_min, strategic_y_max = strategic_y - 10, strategic_y + 10  
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max

    # def is_closest_to_ball(self, players, ball):
    #     """Check if this player is the closest to the ball among all forwards."""
    #     own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
    #     flexible = [player for player in players if player['number'] == 3]
    #     forwards = [player for player in players if player['role'] == 'forward']
    #     if ball['x'] < 0:
    #         if get_distance({'x': flexible['x'], 'y': flexible['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
    #             return False
    #     for player in forwards:
    #         if player['number'] != self.number:
    #             if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
    #                 return False
    #     return True

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number and ball['owner_color'] == self.color
    
    def opponent_in_randius(self,opponent_players):
        count = 0
        for player in opponent_players:
            if get_distance(player,{'x':self.x,'y':self.y}) <= 100 and player['role'] != 'goalkeeper':
                count += 1
        if count >= 2:  #感觉一碰到人就立即传球不合理，所以半径人遇到两人以上拦截再传
            return True
        return False
    
    def can_be_grab(self,opponent_players):
        for player in opponent_players:
            if get_distance(player,{'x':self.x,'y':self.y}) <= 50 and player['role'] != 'goalkeeper':
                return True     
        return False
    
    def random_kick_out(self,opponent_players):
        # print(f"{self.color}Forward {self.number}检测到拦截风险大，随机踢出")
        angle = how_to_grab({'x': self.x, 'y': self.y},opponent_players)
        return{      
            'type': 'kick',
            'player_number': self.number,
            'direction': angle,
            'power': 50,  
        }

    
    # def pass_to_teammates(self, players, ball):
    #     most_advanced_teammate = None
    #     max_advance_x = -float('inf')  # Initialize with a very small number

    #     for player in players:
    #         if player['number'] != self.number and player['role'] != 'goalkeeper':
    #             # Check if this player is more advanced towards the opponent's goal
    #             if player['x'] > max_advance_x:
    #                 most_advanced_teammate = player
    #                 max_advance_x = player['x']
        
    #     if most_advanced_teammate:
    #         direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': most_advanced_teammate['x'], 'y': most_advanced_teammate['y']})
    #         return {
    #             'type': 'kick',
    #             'player_number': self.number,
    #             'direction': direction_to_teammate,
    #             'power': 50  # Adjust power as necessary
    #         }
    #     else:
    #         return None
        
    def find_best_receiver(self,players, opponent_players):
        best_receiver = None
        min_opponent_distance = 100
        min_goal_distance = 100
        min_pass_distance = 200

        for player in players:
            if player['role'] != 'goalkeeper':
                
                opponent_distance= min([get_distance(player, opponent) for opponent in opponent_players])
                #print(opponent_distance,"distance")
                goal_distance = get_distance(player, {'x': 450 if self.color == 'red' else -450, 'y': 0})
                team_distance = get_distance(player,{'x':self.x,'y':self.y})
                if opponent_distance > min_opponent_distance or (opponent_distance == min_opponent_distance and goal_distance < min_goal_distance and team_distance > min_pass_distance):
                    best_receiver = player
                    min_opponent_distance = opponent_distance
                    min_goal_distance = goal_distance
        
        if best_receiver is not None and best_receiver['number'] != self.number:
            goal_x = 200 if self.color == 'red' else -200
            goal_y = 0
            direction_to_receiver = get_direction({'x': self.x, 'y': self.y}, {'x': best_receiver['x'], 'y': best_receiver['y']})
            distance_to_receiver = get_distance({'x': self.x, 'y': self.y}, {'x': best_receiver['x'], 'y': best_receiver['y']})
            distance_to_goal = get_distance({'x': self.x, 'y': self.y},{'x':goal_x,'y':goal_y})
            if distance_to_goal <= distance_to_receiver:
                return None   #如果可以进球，那么优先进球而不是传球
            print(f"Forward {self.color}{self.number} ")
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_receiver,
                'power': 50  # Adjust power as necessary
            }
        else:
            return None

    
    def move_towards_goal(self, ball):
        if self.color == 'red':
            goal_position = {'x': 200, 'y': 0}
        else:
            goal_position = {'x': -200, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        print(f"{self.color}Forward {self.number} moving towards the goal")
        return {
            'type': 'move', 
            'player_number': self.number,
            'destination': goal_position, 
            'direction': direction_to_goal, 
            'speed': 7,
            'has_ball':True
        }

    def move_to_strategic_position(self, strategic_pos):
        # Move to a predefined strategic position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 10,
            'has_ball':False
        }
    
    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move', 
            'player_number': self.number, 
            'destination': {'x': self.x, 'y': self.y}, 
            'direction': direction_to_ball, 
            'speed': 0,
            'has_ball':False
        }

    
    # def distance_to_ball(self,ball):
    #     return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})


    def is_most_closet(self,ball,players):
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        for player in players:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True
    
    def intercept_ball(self, ball,players,opponent_players):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        distance_to_ball = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        if distance_to_ball > 24:

            return {
                'type': 'move',
                'player_number': self.number,
                'destination': ball,
                'direction': direction_to_ball,
                'speed': 10,  # This speed can be adjusted based on gameplay needs
                'has_ball':False
            }
        else:
            return self.grab_ball(ball)
    
    def grab_ball(self,ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'grab',
            'player_number': self.number,
            'direction': direction_to_ball,
        }

    
    def own_half(self,ball):
        if self.color == 'red':
            x = ball['x']
            x1 = -450
            x2 = 75
        elif self.color == 'blue':
            x = ball['x']
            x1 = -75
            x2 = 450
        else:
            print("Error in own_half")
        return x1 <= x <= x2
    

    # def calculate_a_star_defensive_position(self, ball, players, opponent_players):
    #     # Implement A* algorithm for defensive position calculation
    #     #self.update_cost_map(players,opponent_players)
    #     start_node = (self.x,self.y)
    #     goal_node = (ball['x'], ball['y'])
    #     visited = set()
    #     if len(self.cost_map) > 0 and len(self.cost_map[0]) > 0:
    #         open_set = []
    #         heapq.heappush(open_set, (0, start_node))

    #     while open_set:
    #         _, current = heapq.heappop(open_set)
    #         #print("Current node:", current)  # 打印当前节点
    #         if current in visited:
    #             continue
    #         visited.add(current)
    #         tolerance = 5  # 容忍范围
    #         if abs(current[0] - goal_node[0]) <= tolerance and abs(current[1] - goal_node[1]) <= tolerance:
    #             # 到达目标节点
    #             #print(f"Forward {self.color} {self.number} reached",current[0],current[1])
    #             return {'x': current[0], 'y': current[1]}  # Defensive position found

    #         for neighbor in self.get_neighbors(current):
    #             if 0 <= abs(neighbor[0] // 50) < len(self.cost_map[0]) and 0 <= abs(neighbor[1] // 50) < len(self.cost_map):
    #                 new_cost = self.cost_map[int(abs(neighbor[1] // 50))][int(abs(neighbor[0] // 50))]
    #                 heapq.heappush(open_set, (new_cost, neighbor))
    #     # Defensive position not found, return default position
    #     #print("Defensive position not found, returning default position")
    #     return self.default_strategic_position(ball)


    def calculate_a_star_offensive_position(self, ball, players,opponent_players):
        # Implement A* algorithm for offensive position calculation
        #这个方法即是前锋的战略点
        if self.owns_ball(ball):
            goal_node = (300 if self.color == 'red' else -300, 0)
        elif ball['owner_color'] == self.color:
            # 定义矩形区域的边界
            x_min, y_min = 100, 0 if self.number == 3 else -200
            x_max, y_max = 300, 200 if self.number == 3 else 0

            # 生成随机坐标点
            random_x = random.uniform(x_min, x_max)
            random_y = random.uniform(y_min, y_max)        
            goal_node = (random_x, random_y)
        else:
            x = (ball['x'] + self.x) / 2
            y = (ball['y'] + self.y) / 2
            goal_node = (abs(x) if ball['x'] < 0 else x,y)
        
        start_node = (self.x, self.y)
        visited = set()
        if self.cost_map and len(self.cost_map) > 0 and len(self.cost_map[0]) > 0:
            open_set = []
            heapq.heappush(open_set, (0, start_node))

        while open_set:
            _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            tolerance = 20  # 容忍范围
            if abs(current[0] - goal_node[0]) <= tolerance and abs(current[1] - goal_node[1]) <= tolerance:
                # 到达目标节点
                #print(f"Forward {self.color} {self.number} reached",current[0],current[1])
                return {'x': current[0], 'y': current[1]}  # Offensive position found

            for neighbor in self.get_neighbors(current):
                if 0 <= abs(neighbor[0] // 50) < len(self.cost_map[0]) and 0 <= abs(neighbor[1] // 50) < len(self.cost_map):
                    new_cost = self.cost_map[int(abs(neighbor[1] // 50))][int(abs(neighbor[0] // 50))]
                    heapq.heappush(open_set, (new_cost, neighbor))

        # Offensive position not found, return default position
        return self.default_strategic_position(ball)
    
    def get_neighbors(self, node):
        x, y = node
        neighbors = []

        # 添加当前节点周围的四个相邻节点，同时检查边界
        if (x + 10) // 50 * 50 <= 450:
            neighbors.append(((x + 10) // 50 * 50, y))  # 右边节点
        if (x - 10) // 50 * 50 >= -450:
            neighbors.append(((x - 10) // 50 * 50, y))  # 左边节点
        if (y + 10) // 50 * 50 <= 450:
            neighbors.append((x, (y + 10) // 50 * 50))  # 下方节点
        if (y - 10) // 50 * 50 >= -450:
            neighbors.append((x, (y - 10) // 50 * 50))  # 上方节点

        return neighbors


    def update_cost_map(self,ball,player_positions, opponent_positions):
        grid_size = 50
        grid_cols = len(self.cost_map[0])
        grid_rows = len(self.cost_map)

        for row in range(grid_rows):
            for col in range(grid_cols):
                row_start, row_end = row - 2, row + 2  # 子矩阵的行索引范围
                col_start, col_end = col - 2, col + 2  # 子矩阵的列索引范围

                # 确保行索引范围有效
                if row_start < 0:
                    row_start = 0
                if row_end > len(self.cost_map):
                    row_end = len(self.cost_map)

                # 确保列索引范围有效
                if col_start < 0:
                    col_start = 0
                if col_end > len(self.cost_map[0]):
                    col_end = len(self.cost_map[0])

                # 计算网格单元格左上角的坐标
                grid_top_left_x = col * grid_size - 450
                grid_top_left_y = 300 - row * grid_size

                # 计算网格单元格右下角的坐标
                grid_bottom_right_x = (col + 1) * grid_size - 450
                grid_bottom_right_y = 300 - (row + 1) * grid_size

                # 检查每个球员的位置是否在当前网格单元格内
                for player_pos in player_positions:
                    if (grid_top_left_x <= player_pos['x'] < grid_bottom_right_x and
                        grid_bottom_right_y <= player_pos['y'] < grid_top_left_y):

                        # 如果球员在网格单元格内，则减少代价
                        if player_pos['number'] == self.number:
                            self.cost_map[row][col] +=  0
                        elif player_pos['number'] == ball['owner_number'] and self.color == ball['owner_color']:
                            #self.cost_map[row][col] +=  200
                            for i in range(row_start, row_end):
                                for j in range(col_start, col_end):
                                    self.cost_map[i][j] += 150
                        else:
                            self.cost_map[row][col] -=  50

                # 检查每个对手的位置是否在当前网格单元格内
                for opponent_pos in opponent_positions:
                    if (grid_top_left_x <= opponent_pos['x'] < grid_bottom_right_x and
                        grid_bottom_right_y <= opponent_pos['y'] < grid_top_left_y):
                        # 如果对手在网格单元格内，则增加代价
                            for i in range(row_start, row_end):
                                for j in range(col_start, col_end):
                                    self.cost_map[i][j] += 100
        #print(self.cost_map)