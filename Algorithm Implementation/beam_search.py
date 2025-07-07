def beam_search(graph, start, goal, heuristic, beam_width):
    queue = [(heuristic[start], start, [start])]

    while queue:
        candidates = []

        for _, current_node, path in queue:
            if current_node == goal:
                return path

            for neighbor in graph[current_node]:
                new_path = path + [neighbor]
                candidates.append((heuristic[neighbor], neighbor, new_path))

        candidates.sort()

        queue = candidates[:beam_width]

    return None


graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

heuristic = {'A': 6, 'B': 4, 'C': 4, 'D': 3, 'E': 2, 'F': 0}

print(beam_search(graph, 'A', 'F', heuristic, 2))
