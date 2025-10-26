from collections import deque, defaultdict
import itertools

graph = {
    'S': {'A': 9, 'E': 8, 'I': 7, 'M': 3},
    'A': {'B': 2, 'N': 6},
    'B': {'C': 6, 'G': 3, 'E': 4},
    'C': {'D': 2, 'H': 4},
    'D': {'T': 7},
    'E': {'F': 6},
    'F': {'G': 1, 'K': 3, 'C': 6},
    'G': {'H': 6, 'L': 8},
    'H': {'T': 2},
    'I': {'J': 2, 'F': 2},
    'J': {'K': 5, 'G': 4, 'O': 6},
    'K': {'L': 1, 'P': 5},
    'L': {'T': 7},
    'M': {'J': 2, 'N': 4},
    'N': {'K': 1, 'O': 3},
    'O': {'P': 4, 'D': 6},
    'P': {'T': 6},
    'T': {}
}

def bfs_capacity_path(graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()

        for v in graph[u]:
            if v not in visited and graph[u][v] > 0:  # Check for positive capacity
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False

def ford_fulkerson(graph, source, sink):
    parent = {}
    max_flow = 0

    while bfs_capacity_path(graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink

        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            print (path_flow)
            print (parent)
            s = parent[s]
            
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            if v not in graph:
                graph[v] = {}
            if u not in graph[v]:
                graph[v][u] = 0
            graph[v][u] += path_flow
            v = parent[v]

       

    return max_flow

def cut_capacity(graph, S_set):
    """Compute total capacity of edges crossing from S_set to T_set."""
    total = 0
    for u in S_set:
        for v, cap in graph[u].items():
            if v not in S_set:  # edge goes across the cut
                total += cap
    return total


def brute_force_min_cut(graph, source, sink):
    nodes = list(graph.keys())
    nodes.remove(source)
    nodes.remove(sink)

    min_cut_value = float('inf')
    min_cut_partition = None

    # Try all subsets that include the source
    for r in range(len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            S_set = {source, *subset}
            if sink in S_set:
                continue  # invalid cut, sink must be on the other side

            cut_value = cut_capacity(graph, S_set)
            if cut_value < min_cut_value:
                min_cut_value = cut_value
                min_cut_partition = S_set

    return min_cut_value, min_cut_partition


if __name__ == "__main__":
    source = 'S'
    sink = 'T'
    min_cut = brute_force_min_cut(graph, source, sink)
    print(f"The minimum cut value is {min_cut[0]} with partition {min_cut[1]}")
    max_flow_value = ford_fulkerson(graph, source, sink)
    print(f"The maximum possible flow from {source} to {sink} is {max_flow_value}")