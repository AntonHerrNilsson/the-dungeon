import bisect

class Problem:
    
    def __init__(self, initial_state):
        self.initial_state = initial_state
    
    def actions(self, state):
        raise NotImplementedError
    
    def result(self, state, action):
        raise NotImplementedError
    
    def goal_test(self, state):
        raise NotImplementedError
    
    def step_cost(self, from_state, action, to_state):
        return 1

class Node:
    
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        
def expand_node(parent, problem):
    new_nodes = []
    for action in problem.actions(parent.state):
        state = problem.result(parent.state, action)
        path_cost = (parent.path_cost 
                    + problem.step_cost(parent.state, action, state))
        new_nodes.append(Node(state, parent, action, path_cost))
    return new_nodes

def get_solution(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return list(reversed(actions))

def astar_search(problem):
    frontier = [Node(state=problem.initial_state,
                     parent=None, action=None, path_cost=0)]
    frontier[0].estimated_cost = problem.heuristic(problem.initial_state)
    explored = set()
    while frontier:
        current_node = frontier.pop(0)
        if problem.goal_test(current_node.state):
            return get_solution(current_node)
        explored.add(current_node.state)
        new_nodes = expand_node(current_node, problem)
        for node in new_nodes:
            try:
                ind = [f.state for f in frontier].index(node.state)
                if frontier[ind].path_cost > node.path_cost:
                    frontier.pop(ind)
            except ValueError:
                pass
            if node.state not in explored and node.state not in [f.state for f in frontier]:
                node.estimated_cost = node.path_cost + problem.heuristic(node.state)
                ind = bisect.bisect([n.estimated_cost for n in frontier], node.estimated_cost)
                frontier.insert(ind, node)
    return None
        
        
        
        
