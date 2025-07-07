def best_first(graph, start, goal, heuristic):
    visited = set()
    queue = [(heuristic[start], start, [start])]
    while queue:
        _, node, path = queue.pop(0)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            neighbors = [(heuristic[neighbor], neighbor, path + [neighbor])
                         for neighbor in graph[node]]
            queue.extend(neighbors)
            queue.sort()
    return None


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}
heuristic = {'A': 6, 'B': 4, 'C': 4, 'D': 3, 'E': 2, 'F': 0}
print(best_first(graph, 'A', 'F', heuristic))
