# -*- coding: utf-8 -*-

import enum
import pydot

class Actions(enum.Enum):
    # Actions.up.name
    # Actions.up.value
    up = 1
    right = 2
    down = 3
    left = 4
    

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


# pip install --upgrade pip
# pip install pydot









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
    def get_all_nodes(cls) -> list:
        res = []
        for k in cls.__all_nodes:
            res += cls.__all_nodes[k]
        return res

    @classmethod
    def get_nodes_on_lvl(cls, lvl: int) -> list:
        return list(cls.__all_nodes[lvl])

    @classmethod
    def get_lowest_lvl(cls) -> int:
        return max(cls.__all_nodes.keys())

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
        print(f"id = {node.node_id}, parent_id = {parent_id}, action = {node_prev_action}, \ndepth = {node.depth}, cost = {node.cost}, state: ")
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
    path_cost = None
    depth = None
    node_id = None

    #@classvar
    static_node_id = 0

    def __init__(self, state: list, parent: "Node", action: "Actions", cost: int, depth: int):
        self.cur_state = state
        self.parent_node = parent
        self.prev_action = action
        self.cost = cost
        self.depth = depth

        self.node_id = Node.static_node_id
        Node.static_node_id += 1
        


# O(1)
def check_state_equals(state1: list, state2: list) -> bool:
    for i in range(9):
        if(state1[i] != state2[i]):
            return False
    return True

# O(1)
def check_final(cur_state: list) -> bool:
    if(check_state_equals(cur_state, get_final_state()) == True):
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
    res = f"id={node.node_id}, state: \n"
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

'''
depth 18 ~ 7-8 GB RAM
depth 22 ~ 10-12 GB RAM
enjoy=)
'''
def build_graph(node_id_of_result: int = -1):
    # https://github.com/pydot/pydot
    # https://stackoverflow.com/questions/7670280/tree-plotting-in-python

    print("Generating grapth \"result_graph.svg\" in svg-format. Please wait... ")

    graph = pydot.Dot("my_graph", graph_type="graph", bgcolor="white")
    all_nodes = Nodes_handler.get_all_nodes()
    for node_i in all_nodes:
        if(node_i.node_id == node_id_of_result):
            # https://graphviz.org/docs/attrs/fillcolor/
            # https://stackoverflow.com/questions/17252630/why-doesnt-fillcolor-work-with-graphviz
            graph.add_node(pydot.Node(f"node{node_i.node_id}", label=f"{node_to_str(node_i)}", fillcolor="red", style="filled"))
        else:
            graph.add_node(pydot.Node(f"node{node_i.node_id}", label=f"{node_to_str(node_i)}"))
    
    lowest_lvl = Nodes_handler.get_lowest_lvl()
    for i_h in range(lowest_lvl+1):
        i = lowest_lvl-i_h
        lowest_nodes = Nodes_handler.get_nodes_on_lvl(i)

        for node_i in lowest_nodes:
            if(node_i.parent_node != None):
                graph.add_edge(pydot.Edge(f"node{node_i.node_id}", f"node{node_i.parent_node.node_id}", color="black"))
    
    #graph.write_png("1.png")
    graph.write_svg("result_graph.svg")


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
    

# O( SUM[C^i, i=0..N] ) = , N - глубина результата, C - какая-то константа
# = O ( 1/2*(C^(N+1) - 1) ) = O(C^N)
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

            new_states_dict = get_next_states(node_i.cur_state)

            new_nodes = []

            #print("\nits children:")
            for new_state_move_i in new_states_dict:
                new_state_i = new_states_dict[new_state_move_i]
                new_state_hash_i = cals_state_hash(new_state_i)
                if(new_state_hash_i in hashes):
                    continue
                new_node = Node(new_state_i, node_i, new_state_move_i, cur_lvl, cur_lvl) # Поиск в ширину - это частный случай поиска по критерию стоимости, когда стоимость равна глубине.
                new_nodes.append(new_node)
                hashes.add(new_state_hash_i)
                Nodes_handler.expand_chain(cur_lvl, new_node)
            
                #Nodes_handler.print_node(new_node)
            
            for new_node_i in new_nodes:
                if(check_final(new_node_i.cur_state) == True):
                    #Nodes_handler.print_node(new_node_i)
                    Nodes_handler.print_chain(new_node_i)
                    #build_graph(new_node_i.node_id)
                    exit()
        #input()

def DFS(start: "Node", hashes: set, visited_id: list, lvl: int):
    if(hashes == None):
        import sys
        #print(sys.getrecursionlimit())
        sys.setrecursionlimit(1500000)
        hashes = set()
        visited_id = set()
    visited_id.add(start.node_id)
    
    new_states_dict = get_next_states(start.cur_state)
    neighbors = []
    for new_state_move_i in new_states_dict:
        new_state_i = new_states_dict[new_state_move_i]
        new_state_hash_i = cals_state_hash(new_state_i)
        if(new_state_hash_i in hashes):
            continue
        new_node = Node(new_state_i, start, new_state_move_i, lvl+1, lvl+1) # Стоимость равна глубине?
        neighbors.append(new_node)
        hashes.add(new_state_hash_i)
        Nodes_handler.expand_chain(lvl+1, new_node)

    for new_node_i in neighbors:
        if(check_final(new_node_i.cur_state) == True):
            #Nodes_handler.print_node(new_node_i)
            Nodes_handler.print_chain(new_node_i)
            #build_graph(new_node_i.node_id)
            exit()
    for next_node in neighbors:
        if(next_node.node_id not in visited_id):
            DFS(next_node, hashes, visited_id, lvl+1)
    

if __name__ == '__main__':
    Nodes_handler.init()

    #BFS()
    DFS(Nodes_handler.get_nodes_on_lvl(0)[0], None, None, 0)