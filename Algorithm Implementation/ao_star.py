def ao_star(graph, start, goal, heuristic, costs):
    def solve(node):
        if node == goal:
            return 0, [node]

        if node in visited:
            return float('inf'), []

        visited.add(node)

        min_cost = float('inf')
        best_path = []

        for neighbor in graph[node]:
            cost, path = solve(neighbor)

            total_cost = cost + costs[(node, neighbor)] + heuristic[neighbor]

            if total_cost < min_cost:
                min_cost = total_cost
                best_path = [node] + path

        visited.remove(node)

        return min_cost, best_path

    visited = set()

    _, path = solve(start)

    return path


graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

heuristic = {'A': 6, 'B': 4, 'C': 4, 'D': 3, 'E': 2, 'F': 0}

costs = {
    ('A', 'B'): 1, ('A', 'C'): 1,
    ('B', 'D'): 1, ('B', 'E'): 1,
    ('C', 'F'): 1, ('E', 'F'): 1
}

print(ao_star(graph, 'A', 'F', heuristic, costs))
