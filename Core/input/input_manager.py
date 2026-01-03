import pygame
from Core.actions import Action, ActionType, Direction

class InputManager:
    KEYMAP = {
        pygame.K_w: Direction.JUMP_UP,
        pygame.K_s: Direction.JUMP_DOWN,
        pygame.K_a: Direction.JUMP_LEFT,
        pygame.K_d: Direction.JUMP_RIGHT,
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
    }

    def get_actions(self, events):
        actions = []

        for event in events:
            if event.type == pygame.KEYDOWN:
                is_shift = event.mod & pygame.KMOD_SHIFT
                
                if is_shift and event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    direction = None
                    if event.key == pygame.K_w: direction = Direction.UP
                    elif event.key == pygame.K_s: direction = Direction.DOWN
                    elif event.key == pygame.K_a: direction = Direction.LEFT
                    elif event.key == pygame.K_d: direction = Direction.RIGHT
                    
                    if direction:
                        actions.append(Action(ActionType.PLACE_BOMB, direction))
                        continue

                if event.key in self.KEYMAP:
                    direction = self.KEYMAP[event.key]
                    actions.append(Action(ActionType.MOVE, direction))

        return actions
