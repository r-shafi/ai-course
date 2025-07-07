def alpha_beta(game_tree, node, is_max, alpha, beta):
    if not game_tree[node]:
        return node

    if is_max:
        best_value = float('-inf')
        for child in game_tree[node]:
            value = alpha_beta(game_tree, child, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if beta <= alpha:
                break

        return best_value

    else:
        best_value = float('inf')
        for child in game_tree[node]:
            value = alpha_beta(game_tree, child, True, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)

            if beta <= alpha:
                break

        return best_value


game_tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [3],
    'E': [5],
    'F': [6],
    'G': [9]
}

print(alpha_beta(game_tree, 'A', True, float('-inf'), float('inf')))
