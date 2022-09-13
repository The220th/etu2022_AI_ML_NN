# -*- coding: utf-8 -*-

import enum
import heapq
import psutil
import os
from time import process_time

'''
============================== Variable section begin ==============================
'''    



GRAPH_VISIALISATION = True

GRAPH_VISIALISATION_FILE_NAME = "result_graph"

# False  -  H1
# True   -  H2
H1_H2 = False

# Если True, то каждый шаг придётся нажимать enter
DEBUG = False


global_final_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# Вариант 1
# 5 8 3
# 4 0 2
# 7 6 1
def get_init_state() -> list:
    return [5, 8, 3, 4, 0, 2, 7, 6, 1]

# Вариант 1
# 1 2 3
# 4 5 6
# 7 8 0
def get_final_state() -> list:
    return list(global_final_state)


# O(1)
def heuristics(node: "Node") -> int:
    if(H1_H2 == False):
        cur_value = node.cost + h1(node.cur_state)
    else:
        cur_value = node.cost + h2(node.cur_state)
    return cur_value

'''
============================== Variable section end ==============================
'''



class Actions(enum.Enum):
    # Actions.up.name
    # Actions.up.value
    up = 1
    right = 2
    down = 3
    left = 4




class Nodes_handler():

    __all_nodes = None
    __hashes = None

    @classmethod
    def init(cls):
        cls.__all_nodes = []
        cls.__hashes = {}

    '''
    Если состояние нода повторяется, то не добавится.
    '''
    @classmethod
    def expand_chain(cls, node: "Node"):
        if(cls.check_if_state_consist(node.cur_state) == True):
            return
        cls.__all_nodes.append(node)
        cls.__hashes[cals_state_hash(node.cur_state)] = node

    @classmethod
    def get_all_nodes(cls) -> list:
        return cls.__all_nodes

    # O(1)
    @classmethod
    def check_if_state_consist(cls, state: list) -> bool:
        state_hash = cals_state_hash(state)
        if(state_hash in cls.__hashes):
            return True
        else:
            return False

    # O(1)
    @classmethod
    def get_node_by_state(cls, state: list):
        state_hash = cals_state_hash(state)
        return cls.__hashes[state_hash]

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
        node_prev_action = None
        if(node.prev_action != None):
            node_prev_action = node.prev_action.name
        print(f"id = {node.node_id}, parent_id = {parent_id}, action = {node_prev_action}, \ncost = {node.cost}, state: ")
        cls.print_state(node.cur_state)
        print("")

    @classmethod
    def print_chain(cls, node_final: "Node"):
        chain = []
        cur_node = node_final
        while(cur_node.parent_node != None):
            chain.append(cur_node)
            cur_node = cur_node.parent_node
        chain.append(cur_node)
        for node_i in chain:
            cls.print_node(node_i)
            print("\t^\n\t|\n")

class Node:

    cur_state = None
    parent_node = None
    prev_action = None
    cost = None # g
    node_id = None

    #@classvar
    static_node_id = 0

    def __init__(self, state: list, parent: "Node", action: "Actions", cost: int):
        self.cur_state = state
        self.parent_node = parent
        self.prev_action = action
        self.cost = cost

        self.node_id = Node.static_node_id
        Node.static_node_id += 1

    @classmethod
    def get_node_amount(cls) -> int:
        return cls.static_node_id + 1
        


# O(1)
def check_state_equals(state1: list, state2: list) -> bool:
    for i in range(9):
        if(state1[i] != state2[i]):
            return False
    return True

# O(1)
def check_final(cur_state: list) -> bool:
    if(check_state_equals(cur_state, global_final_state) == True):
        return True
    else:
        return False

# O(1)
def cals_state_hash(state: list) -> int:
    hash = 7
    for i in state:
        hash = 31*hash + i
    return hash

def node_to_str(node: "Node") -> str:
    res = f"id={node.node_id}, \ncost = {node.cost}\n"
    state = node.cur_state
    gi = 0
    for i in range(3):
        for j in range(3):
            if(state[gi] == 0):
                res += "- "
            else:
                res += f"{state[gi]} "
            gi+=1
        res += "\n"
    return res


def build_graph(node_id_of_result: int = -1):
    # https://github.com/pydot/pydot
    # https://stackoverflow.com/questions/7670280/tree-plotting-in-python

    print(f"Generating grapth \"{GRAPH_VISIALISATION_FILE_NAME}\" in dot-format and svg-format. Please wait... ")
    import pydot

    graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="white")
    all_nodes = Nodes_handler.get_all_nodes()
    for node_i in all_nodes:
        if(node_i.node_id == node_id_of_result):
            # https://graphviz.org/docs/attrs/fillcolor/
            # https://stackoverflow.com/questions/17252630/why-doesnt-fillcolor-work-with-graphviz
            graph.add_node(pydot.Node(f"node{node_i.node_id}", label=f"{node_to_str(node_i)}", fillcolor="red", style="filled"))
        else:
            graph.add_node(pydot.Node(f"node{node_i.node_id}", label=f"{node_to_str(node_i)}"))
    
    edges = set()
    for node_i in all_nodes:
        if(node_i.parent_node != None):
            edge_name = f"{node_i.node_id}-{node_i.parent_node.node_id}"
            if(edge_name not in edges):
                edges.add(edge_name)
                graph.add_edge(pydot.Edge(f"node{node_i.node_id}", f"node{node_i.parent_node.node_id}", color="black"))
    
    graph.write_raw(f"{GRAPH_VISIALISATION_FILE_NAME}.dot")
    graph.write_svg(f"{GRAPH_VISIALISATION_FILE_NAME}.svg")


# O(1)
def state_swap(state: list, i: int, j: int) -> list:
    res = list(state)
    res[i], res[j] = res[j], res[i]
    return res

# O(1)
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

# O(1)
def get_next_states(cur_state: list) -> dict:
    res = {}
    for action_i in Actions:
        cur_state_i = shift_state(cur_state, action_i)
        if(cur_state_i != None):
            res[action_i] = cur_state_i
    #res = list(filter(lambda x: x != None, res)) # Убрать все None`ы
    return res

# O(1)
def h1(state: list) -> int:
    state_final = global_final_state
    res = 0
    for i in range(9):
        if(state_final[i] != state[i]):
            res+=1
    return res

# O(1)
def h2(state: list) -> int:
    state_final = global_final_state
    res = 0
    for i in range(9):
        state_x, state_y = i // 3, i % 3
        where = state_final.index(state[i])
        final_x, final_y = where // 3, where % 3
        res += abs(final_x-state_x) + abs(final_y-state_y)
    return res

# O(1)
def get_neighbors(with_node: "Node") -> list:
    new_states_dict = get_next_states(with_node.cur_state)
    neighbors = []
    for new_state_move_i in new_states_dict:
        new_state_i = new_states_dict[new_state_move_i]
        if(Nodes_handler.check_if_state_consist(new_state_i) == True):
            neighbors.append(Nodes_handler.get_node_by_state(new_state_i))
        else:
            new_node = Node(new_state_i, with_node, new_state_move_i, with_node.cost+1)
            neighbors.append(new_node)
            Nodes_handler.expand_chain(new_node)
    return neighbors
        

def A_star():
    node_by_hash = {}
    open_list = set()
    open_list_q = []   #     https://docs.python.org/3/library/heapq.html
    close_list = set()

    cursor = Node(get_init_state(), None, None, 0)
    Nodes_handler.expand_chain(cursor)
    close_list.add(cursor.node_id)

    neighbors = get_neighbors(cursor)
    for neighbor_i in neighbors:
        open_list.add(neighbor_i.node_id)
        neighbor_i_h = heuristics(neighbor_i)
        heapq.heappush(open_list_q, (neighbor_i_h, neighbor_i.node_id, neighbor_i))
    
    iteration_count = 0
    step_i = 0
    while(True):

        heap_lowest = heapq.heappop(open_list_q)
        cursor = heap_lowest[2]
        open_list.remove(cursor.node_id)
        close_list.add(cursor.node_id)
        if(DEBUG):
            print(f"Current lenght of open list  = {len(open_list)}")
            print(f"Current lenght of close list = {len(close_list)}")
            print(f"Cursor was selected because it had the minimum value of the f={heap_lowest[0]}")
            print("Looking at node (cursor): ")
            Nodes_handler.print_node(cursor)

        iteration_count+=1
        if(check_final(cursor.cur_state) == True):
            if(DEBUG):
                print("!!! Answer finded !!!")
                Nodes_handler.print_node(cursor)

            TIME_STOP = process_time()

            Nodes_handler.print_chain(cursor)
            print(f"Total turned out to be nodes: {Node.get_node_amount()}")
            print(f"Cost (depth): {cursor.cost}")
            print(f"Iteration count: {iteration_count}")
            print(f"Processor time user: {(TIME_STOP-TIME_START)*1000} miliseconds")
            print(f"Memory (rss) used: {psutil.Process(os.getpid()).memory_info().rss} bytes")
            if(GRAPH_VISIALISATION):
                build_graph(cursor.node_id)
            exit()

        neighbors = get_neighbors(cursor)

        if(DEBUG):
            print("Neighbors of cursor: ")
            for neighbor_i in neighbors:
                if(neighbor_i.node_id in close_list):
                    print("This neighbor is located in a closed list and will not be considered")
                elif(neighbor_i.node_id in open_list):
                    print("This neighbor is located in the open list and g will be recalculated for it, if necessary")
                else:
                    print("This neighbor is new and has not been considered before. It will be added to the open list")
                Nodes_handler.print_node(neighbor_i)
                print(f"It has f = {heuristics(neighbor_i)}")

        for neighbor_i in neighbors:
            if(neighbor_i.node_id in open_list):
                old_g = neighbor_i.cost
                new_g = cursor.cost + 1
                if(new_g < old_g):
                    neighbor_i.cost = new_g
                    neighbor_i.parent_node = cursor
            else:
                if(neighbor_i.node_id not in close_list):
                    open_list.add(neighbor_i.node_id)
                    neighbor_i_h = heuristics(neighbor_i)
                    heapq.heappush(open_list_q, (neighbor_i_h, neighbor_i.node_id, neighbor_i))

        if(DEBUG):
            print(f"Current step: {step_i}. Press Enter... ")
            input()
            print("\n\n\n")
        step_i += 1
        

TIME_START = None

if __name__ == '__main__':
    Nodes_handler.init()

    TIME_START = process_time()

    A_star()