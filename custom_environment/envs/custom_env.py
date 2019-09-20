import numpy as np
import gym
import pygame
from gym import error, spaces, utils
from gym.utils import seeding

try:
    import hfo_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install HFO dependencies with 'pip install gym[soccer].)'".
                                       format(e))

import logging
logger = logging.getLogger(__name__)


class CustomEnv(gym.Env):
    """A multitask 2-D environment for testing algorithms developed 10x10
    [[-1. -1. -1. 10. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. 10.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]
    [-1. -1. -1. -1. -1. -1. -1. -1. -1. -1.]]

    Agent Location will be at location (0,9)

    Goal Locations are (0,3) and (6,9)

    Actions are discrete and deterministc:
    - 0: move south
    - 1: move north
    - 2: move east
    - 3: move west

    Rewards:
    There is a reward of -1 for each action
    Additional reward of +10 for landing in goal state

    Rendering:
    - blue for goal 1
    - red for goal 2
    -white for non goal states

    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.x_bound = 10
        self.y_bound = 10
        self.state = np.negative(np.ones((self.x_bound, self.y_bound)))
        self.agent_state = [9, 0]
        self.agent_reward = 0
        self.agent_done = False
        self.goal_states = [[0, 3], [6, 9]]
        for x, y in self.goal_states:
            self.state[x, y] = 10

    def south(self, state):
        new_state = [state[0] - 1, state[1]]
        new_state = self.normalise(new_state)
        return new_state

    def north(self, state):
        new_state = [state[0] + 1, state[1]]
        new_state = self.normalise(new_state)
        return new_state

    def east(self, state):
        new_state = [state[0], state[1] + 1]
        new_state = self.normalise(new_state)
        return new_state

    def west(self, state):
        new_state = [state[0], state[1] - 1]
        new_state = self.normalise(new_state)
        return new_state

    def normalise(self,state):
        if state[0] > self.x_bound - 1:
            state = [state[0] - 1, state[1]]
        elif state[0] < 0:
            state = [state[0] + 1, state[1]]

        if state[1] > self. y_bound - 1:
            state = [state[0], state[1] - 1]
        elif state[1] < 0:
            state = [state[0], state[1] + 1]
        return state

    def step(self, action):
        switch = {
            0: self.south,
            1: self.north,
            2: self.east,
            3: self.west
        }
        func = switch.get(action, lambda: "Invalid action")
        self.agent_state = func(self.agent_state)
        self.agent_reward = self.reward(self.agent_state)
        if self.agent_reward == 10:
            self.agent_done = True
        return self.agent_state, self.agent_reward, self.agent_done

    def reset(self):
        self.agent_state = [9, 0]
        self.agent_reward = 0
        self.agent_done = False
        return self.agent_state, self.agent_reward

    def reward(self, state):
        for x, y in self.goal_states:
            if state[0] == x:
                if state[1] == y:
                    return 10
                else:
                    return -1
            else:
                return -1

    def render(self, mode='human', close=False):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        WIDTH = 20
        HEIGHT = 20
        MARGIN = 5
        pygame.init()
        screen_size = (255, 255)
        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()
        screen.fill(BLACK)
        for row in range(10):
            for column in range(10):
                color = WHITE
                if row == self.agent_state[0]:
                    if column == self.agent_state[1]:
                        color == RED
                if self.state[row, column] == 10:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        clock.tick(60)
        pygame.display.flip()
        pygame.quit()

    def close(self):
        pass

