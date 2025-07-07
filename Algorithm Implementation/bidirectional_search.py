from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F']
}


def bidirectional(graph, start, goal):
    forward = deque([(start, [start])])
    backward = deque([(goal, [goal])])

    forward_visited = {start: [start]}
    backward_visited = {goal: [goal]}

    while forward and backward:
        if forward:
            node, path = forward.popleft()
            if node in backward_visited:
                backward_path = backward_visited[node]
                return path + backward_path[-2::-1]

            for neighbor in graph[node]:
                if neighbor not in forward_visited:
                    forward_visited[neighbor] = path + [neighbor]
                    forward.append((neighbor, path + [neighbor]))

        if backward:
            node, path = backward.popleft()
            if node in forward_visited:
                forward_path = forward_visited[node]
                return forward_path + path[-2::-1]

            for neighbor in graph[node]:
                if neighbor not in backward_visited:
                    backward_visited[neighbor] = path + [neighbor]
                    backward.append((neighbor, path + [neighbor]))

    return None


print(bidirectional(graph, 'A', 'F'))
