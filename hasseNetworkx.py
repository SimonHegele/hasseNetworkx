def exists_path(Graph, u, v, start=False):
    '''
    If there exits a path from u to v in G with length > 1: Return True
    Else                                                  : Return False 
    '''
    # Trivial case 1: Reached v
    if u == v and not start:
        return True
    successors = [successor for successor in Graph.neighbors(u) if not ((successor == v) and start)]
    # Trivial case 2: u has no successors 
    if len(successors) == 0:
        return False
    # Recursion
    successors_on_path = [exists_path(Graph, successor, v, start=False) for successor in successors]
    return (True in successors_on_path)

def transitivity_elimination(Graph):
    ''' 
    Removes edges that are implied by transitivity of the partial order
    '''
    edges_to_remove = []
    for edge in Graph.edges():
        if exists_path(Graph, edge[0], edge[1], start=True):
            edges_to_remove.append(edge)
    Graph.remove_edges_from(edges_to_remove)
    return Graph

def layer(positions, i):
    '''
    Returns the positions of nodes at layer i in a dictionary
    '''
    return {position[0]: position[1] for position in positions.items() if  position[1][1]==i}

def y_positioning(Graph, positions, n = 0):
    current_layer = layer(positions, n)
    final_layer = True
    for u in current_layer:
        for v in current_layer:
            if (u,v) in Graph.edges() and positions[v][1]==n:
                final_layer = False
                positions[v] = (positions[v][0],positions[v][1]+1)
    if final_layer:
        return positions
    else:
        return y_positioning(Graph, positions, n = n+1)

def x_positioning(Graph, positions):
    number_of_layers       = max([position[1] for position in positions.values()])
    max_nodes_in_one_layer = max([len([1 for position in positions.items() if position[1][1]==n]) for n in range(number_of_layers)])
    print(max_nodes_in_one_layer)
    for i in range(number_of_layers):
        current_layer = {position[0]: position[1] for position in positions.items() if  position[1][1]==i}
    return positions

def number_of_layers(positions):
    return max([position[1][1] for position in positions.items()])

def max_layer_size(positions):
    return max([len(layer(positions, i)) for i in range(number_of_layers(positions))])
    
def x_positioning(Graph, positions):
    n = number_of_layers(positions) # height
    w = max_layer_size(positions)   # width
    for i in range(n+1):
        current_layer = layer(positions, i)
        for j, node in enumerate(current_layer):
            positions[node] = (1+(j+1)*w/(len(current_layer)+1), positions[node][1])
    return positions

def layout(Graph):
    '''
    Returns a dictionary with positions for the nodes of the graph
    '''
    positions = {node: (0,0) for node in Graph.nodes()}
    positions = y_positioning(Graph, positions, n = 0)
    positions = x_positioning(Graph, positions)
    return positions