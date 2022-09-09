# -*- coding: utf-8 -*-

import enum

class Actions(enum.Enum):
    # Actions.up.name
    # Actions.up.value
    up = 1
    right = 2
    down = 3
    left = 4
    

class Nodes_handler():

    #__chain = None
    __all_nodes = None

    @classmethod
    def init(cls):
        init_node = Node(get_init_state(), None, None, 0, 0)
        #cls.__chain = init_node
        cls.__all_nodes = {0: [init_node]}

    @classmethod
    def expand_chain(cls, lvl_i: int, node: "Node"):
        #prev_node = node.parent_node
        deep = node.depth
        if(lvl_i not in cls.__all_nodes):
            cls.__all_nodes[deep] = [node]
        else:
            cls.__all_nodes[deep].append(node)

    @classmethod
    def get_nodes_on_lvl(cls, lvl: int) -> list:
        return list(cls.__all_nodes[lvl])

    @classmethod
    def print_state(cls, state: list):
        gi = 0
        for i in range(3):
            for j in range(3):
                print(state[gi], end=" ")
                gi+=1
            print("")
    
    @classmethod
    def print_node(cls, node: "Node"):
        parent_id = None
        if(node.parent_node != None):
            parent_id = node.parent_node.node_id
        print(f"id = {node.node_id}, parent_id = {parent_id}, \ndepth = {node.depth}, cost = {node.cost}, state: ")
        cls.print_state(node.cur_state)
        print("")
        

class Node:

    cur_state = None
    parent_node = None
    prev_action = None
    path_cost = None
    depth = None
    node_id = None

    #@classvar
    static_node_id = 0

    def __init__(self, state: list, parent: "Node", action: "Actions", cost: int, depth: int):
        self.cur_state = state
        self.parent_node = parent
        self.action = action
        self.cost = cost
        self.depth = depth

        self.node_id = Node.static_node_id
        Node.static_node_id += 1
        

def get_init_state() -> list:
    return [4, 3, 5, 8, 6, 7, 2, 1, 0]

def get_final_state() -> list:
    return [1, 2, 3, 4, 5, 6, 7, 8, 0]
'''
# 5 8 3
# 4 0 2
# 7 6 1
def get_init_state() -> list:
    return [5, 8, 3, 4, 0, 2, 7, 6, 1]

# 1 2 3
# 4 5 6
# 7 8 0
def get_final_state() -> list:
    return [1, 2, 3, 4, 5, 6, 7, 8, 0]
'''

def check_state_equals(state1: list, state2: list) -> bool:
    for i in range(9):
        if(state1[i] != state2[i]):
            return False
    return True

def check_final(cur_state: list) -> bool:
    if(check_state_equals(cur_state, get_final_state()) == True):
        return True
    else:
        return False

def cals_state_hash(state: list) -> int:
    hash = 7
    for i in state:
        hash = 31*hash + i
    return hash

def state_swap(state: list, i: int, j: int) -> list:
    res = list(state)
    res[i], res[j] = res[j], res[i]
    return res

# return new state or None
def shift_state(cur_state: list, where: "Actions") -> list:
    # 0 1 2
    # 3 4 5 
    # 6 7 8
    i = cur_state.index(0)

    if(where == Actions.up):
        if(i in (0, 1, 2)):
            return None
        else:
            return state_swap(cur_state, i, i-3)
    elif(where == Actions.right):
        if(i in (2, 5, 8)):
            return None
        else:
            return state_swap(cur_state, i, i+1)
    elif(where == Actions.down):
        if(i in (6, 7, 8)):
            return None
        else:
            return state_swap(cur_state, i, i+3)
    elif(where == Actions.left):
        if(i in (0, 3, 6)):
            return None
        else:
            return state_swap(cur_state, i, i-1)
    else:
        print("Failed successfully (shift_state)")

def get_next_states(cur_state: list) -> list:
    res = []
    for action_i in Actions:
        res.append(    shift_state(cur_state, action_i)    )
    res = list(filter(lambda x: x != None, res)) # Убрать все None`ы
    return res
    

def BFS():
    cur_lvl = 0
    hashes = set()
    while(True):
        nodes_prev_lvl = Nodes_handler.get_nodes_on_lvl(cur_lvl)
        cur_lvl+=1
        #print(f"cur_depth = {cur_lvl}")

        for node_i in nodes_prev_lvl:
            #print("\n\n\n\ncur_node:")
            #Nodes_handler.print_node(node_i)

            new_states = get_next_states(node_i.cur_state)

            new_nodes = []

            #print("\nits children:")
            for new_state_i in new_states:
                new_state_hash_i = cals_state_hash(new_state_i)
                if(new_state_hash_i in hashes):
                    continue
                new_node = Node(new_state_i, node_i, None, cur_lvl, cur_lvl) # Поиск в ширину - это частный случай поиска по критерию стоимости, когда стоимость равна глубине.
                new_nodes.append(new_node)
                hashes.add(new_state_hash_i)
                Nodes_handler.expand_chain(cur_lvl, new_node)
            
                #Nodes_handler.print_node(new_node)
            
            for new_node_i in new_nodes:
                if(check_final(new_node_i.cur_state) == True):
                    Nodes_handler.print_node(new_node_i)
                    exit()
        #input()

if __name__ == '__main__':
    Nodes_handler.init()

    BFS()