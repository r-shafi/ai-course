def dls(graph, start, goal, limit, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]
    if start == goal:
        return path
    if limit <= 0:
        return None
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dls(graph, neighbor, goal, limit -
                         1, visited, path + [neighbor])
            if result:
                return result
    return None


def deepening_search(graph, start, goal):
    depth = 0
    while True:
        result = dls(graph, start, goal, depth)
        if result:
            return result
        depth += 1


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
print(deepening_search(graph, 'A', 'F'))
