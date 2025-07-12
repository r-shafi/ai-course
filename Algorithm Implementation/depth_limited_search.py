def depth_limited(graph, start, goal, limit, visited=None, path=None):
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
            result = depth_limited(graph, neighbor, goal, limit -
                                   1, visited, path + [neighbor])
            if result:
                return result
    return None


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(depth_limited(graph, 'A', 'F', 3))
