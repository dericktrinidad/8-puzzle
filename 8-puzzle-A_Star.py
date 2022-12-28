from __future__ import division
from __future__ import print_function

import math
import time
import queue as Q

max_depth = 0
nodes_expanded = 0

## The 8 Puzzle Class
class PuzzleState(object):

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        empty_pos = self.blank_index
        board_state = list(self.config)

        if 0 <= empty_pos <= 2:
            return None
        board_state[empty_pos], board_state[empty_pos-3] = board_state[empty_pos-3], board_state[empty_pos]
        return PuzzleState(board_state, self.n, self, 'Up', self.cost  + 1)

    def move_down(self):
        empty_pos = self.blank_index

        board_state = list(self.config)

        if 6 <= empty_pos <= 8:
            return None
        board_state[empty_pos], board_state[empty_pos + 3] = board_state[empty_pos + 3], board_state[empty_pos]

        return PuzzleState(board_state, self.n, self, 'Down', self.cost  + 1)

    def move_left(self):
        empty_pos = self.blank_index
        board_state = list(self.config)
        
        if empty_pos in {0, 3, 6}:
            return None

        board_state[empty_pos], board_state[empty_pos - 1] = board_state[empty_pos - 1], board_state[empty_pos]
        
        return PuzzleState(board_state, self.n, self, 'Left', self.cost  + 1)

    def move_right(self):
        empty_pos = self.blank_index
        board_state = list(self.config)

        if empty_pos in {2, 5, 8}:
            return None
        
        board_state[empty_pos], board_state[empty_pos + 1] = board_state[empty_pos + 1], board_state[empty_pos]
        
        return PuzzleState(board_state, self.n, self, 'Right', self.cost  + 1)

    def expand(self):
        if len(self.children) != 0:
            return self.children
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        self.children = [state for state in children if state is not None]
        
        return self.children
    def __lt__(self, other):
        return self.cost < other.cost
    def __eq__(self, other):
        return self.cost == other.cost
    def __str__(self):
        return str(self.config)
    __repr__ = __str__


def writeOutput(nodes_expanded, goal_path, run_time, depth):

    file = open('./output.txt', 'w')

    file.write("path_to_goal: " + str(goal_path) + "\n")
    file.write("cost_of_path:" + str(len(goal_path)) + "\n")
    file.write("nodes_expanded: "+ str(nodes_expanded) + "\n")
    file.write("search_depth:" + str(len(goal_path)) + "\n")
    file.write("max_search_depth:" + str(depth) + "\n")
    file.write("running_time: %.3f" % run_time + "\n")
    file.close()

    print("path_to_goal: " + str(goal_path))
    print("cost_of_path: " + str(len(goal_path)))
    print("nodes_expanded: " + str(nodes_expanded))
    print("search_depth: " + str(len(goal_path)))
    print("max_search_depth:" + str(depth))
    print("running_time: %.3f" % run_time)
    return 

def record_goal_path(goal_state):
    actions = []
    while goal_state.parent:
        actions.append(goal_state.action)
        goal_state = goal_state.parent
    return actions[::-1]


def A_star_search(initial_state):
    global nodes_expanded, max_depth

    frontier = Q.PriorityQueue()
    initial_state.cost = calculate_total_cost(initial_state)
    frontier.put(initial_state)

    explored = set()
    frontier_set = set()

    while frontier:

        state = frontier.get()
        explored.add(str(state.config))

        if test_goal(state.config):
            max_depth = len(record_goal_path(state))
            nodes_expanded = len(explored) - 1

            return state

        state.expand()
        neighbors = state.children

        nodes_expanded += len(neighbors)
        for n in neighbors:

            n.cost += calculate_total_cost(n)

            str_n = str(n)
            if str_n not in (explored and frontier_set):
                frontier.put(n)
                frontier_set.add(str_n)
            elif str_n in frontier_set:
                lowest_cost_queue = frontier.get()
                if n.cost < lowest_cost_queue.cost:
                    frontier.put(n)
                else:
                    frontier.put(lowest_cost_queue)
    return False

def calculate_total_cost(state):
    cost = 0
    for pos,value in enumerate(state.config):
        if value == 0: continue
        cost += calculate_manhattan_dist(pos, value, state.n)
    return cost 

def calculate_manhattan_dist(idx, value, n):
    init_row, init_col = int(idx / n), idx % n
    goal_row, goal_col = int(value / n), value % n

    man_distance = abs(init_row - goal_row) + abs(init_col - goal_col)

    return man_distance

def test_goal(puzzle_state):
    goal = '[0, 1, 2, 3, 4, 5, 6, 7, 8]'
    if str(puzzle_state) == goal:
        return True

def main():
    begin_state = [0,8,7,6,5,4,3,2,1]
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()
    goal = A_star_search(hard_state)
    end_time = time.time()
    run_time = end_time - start_time
    writeOutput(nodes_expanded, record_goal_path(goal), run_time, max_depth)
    print("Program completed in %.3f second(s)" % (end_time - start_time))

if __name__ == '__main__':
    main()
