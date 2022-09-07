# -*- coding: utf-8 -*-

import enum

class Actions(enum.Enum):
    # Actions.up.name
    # Actions.down.value
    up = 1
    right = 2
    down = 3
    left = 4
    

class Global():

    __chain = None

    @classmethod
    def 

class Node:

    cur_state = None
    parent_node = None
    prev_action = None
    path_cost = None
    depth = None

    def __init__(self, state: list, parent: "Node", action: "Actions", cost: int, depth: int):
        self.cur_state = state
        self.parent_node = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        


def get_init_state() -> list:
    return [5, 8, 3, 4, 0, 2, 7, 6, 1]

def get_final_state() -> list:
    return [1, 2, 3, 4, 5, 6, 7, 8, 0]

def check_state_equals(state1: list, state2: list) -> bool:
    for i in range(9):
        if(state1[i] != state2[i]):
            return False
    return True

def check_final(cur_state: list) -> bool:
    if(Global.check_state_equals(cur_state, get_final_state()) == False):
        return True
    else:
        return False

def swap(state: list, i: int, jL int): # TODO
    pass

# return new state or None
def shift_state(cur_state: list, where: "Actions") -> list: # TODO
    # 0 1 2
    # 3 4 5 
    # 6 7 8
    i = cur_state.index(0)

    if(where == Actions.up):
        if(i in (0, 1, 2)):
            return None
        else:

    elif(where == Actions.right):
        if(i in (2, 5, 8)):
            return None
    elif(where == Actions.down):
        if(i in (6, 7, 8)):
            return None
    elif(where == Actions.left):
        if(i in (0, 3, 6)):
            return None
    else:
        print("Failed successfully (shift_state)")

def get_next_states(cur_state: list) -> set:
    res = set()
    

def BFS():
    pass

if __name__ == '__main__':
    pass