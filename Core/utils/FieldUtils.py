from Core.game_objects.environment.neutral.Emptiness import Emptiness
from Core.game_objects.environment.harmful.Stone import Stone
from Core.game_objects.environment.useful.Diamond import Diamond
from Core.game_objects.characters.Enemy import Enemy
from Core.game_objects.environment.neutral.Sand import Sand
import json
import os
from collections import deque

class FieldUtils:
    
    CLASS_MAP = {
        "Stone": Stone,
        "Diamond": Diamond,
        "Enemy": Enemy,
        "Sand": Sand,
        "Emptiness": Emptiness
    }

    @staticmethod
    def save_field_to_file(field, width, height, filename):
        data = {
            "width": width,
            "height": height,
            "cells": []
        }
        
        for y in range(height):
            row = []
            for x in range(width):
                obj = field[y][x]
                obj_name = "Emptiness"
                from Core.game_objects.characters.Player import Player
                if isinstance(obj, Stone): obj_name = "Stone"
                elif isinstance(obj, Diamond): obj_name = "Diamond"
                elif isinstance(obj, Player): obj_name = "Player"
                elif isinstance(obj, Enemy): obj_name = "Enemy"
                elif isinstance(obj, Sand): obj_name = "Sand"
                row.append(obj_name)
            data["cells"].append(row)
            
        with open(filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_field_from_file(filename):
        if not os.path.exists(filename):
            return None, 0, 0
            
        with open(filename, 'r') as f:
            data = json.load(f)
            
        width = data["width"]
        height = data["height"]
        raw_cells = data["cells"]
        
        field = [[Emptiness() for _ in range(width)] for _ in range(height)]
        
        for y in range(height):
            for x in range(width):
                name = raw_cells[y][x]
                if name in FieldUtils.CLASS_MAP and name != "Emptiness":
                    field[y][x] = FieldUtils.CLASS_MAP[name]()
                elif name == 'Player':
                    from Core.game_objects.characters.Player import Player
                    field[y][x] = Player()
                    
        return field, width, height


    @staticmethod
    def init_field(field_height, field_width):
        field = []
        for i in range(field_height):
            field.append([Emptiness() for _ in range(field_width)])
        return field
    
    @staticmethod
    def can_move(field, nx, ny):
        return 0 <= ny < len(field) and 0 <= nx < len(field[0]) and field[ny][nx].can_player_move_on()
    
    @staticmethod
    def move_object(field, y, x, ny, nx):
        field[ny][nx] = field[y][x]
        field[y][x] = Emptiness()
        
    @staticmethod
    def field_to_boolean_field(field, field_height, field_width):
        bool_field = [[True for _ in range(field_width)] for _ in range(field_height)]
        for y in range(field_height):
            for x in range(field_width):
                if not field[y][x].can_enemy_move_on():
                    bool_field[y][x] = False
        return bool_field
    
    @staticmethod
    def find_farthest_point(map_, height, width, start_x, start_y):
        # distances[y][x] = distance from start, -1 if not visited
        distances = [[-1 for _ in range(width)] for _ in range(height)]

        queue = deque()
        queue.append((start_x, start_y))
        distances[start_y][start_x] = 0

        farthest_x, farthest_y = start_x, start_y
        max_distance = 0

        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        while queue:
            x, y = queue.popleft()
            current_distance = distances[y][x]

            if current_distance > max_distance:
                max_distance = current_distance
                farthest_x, farthest_y = x, y

            for i in range(4):
                new_x = x + dx[i]
                new_y = y + dy[i]

                if 0 <= new_x < width and 0 <= new_y < height:
                    if map_[new_y][new_x] and distances[new_y][new_x] == -1:
                        distances[new_y][new_x] = current_distance + 1
                        queue.append((new_x, new_y))

        return farthest_x, farthest_y

