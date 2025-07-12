import pygame
import sys
import os
import copy

pygame.init()


BOARD_SIZE = 640
WIDTH = BOARD_SIZE
HEIGHT = BOARD_SIZE + 100
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS


LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_SELECTED = (255, 255, 0, 100)
POSSIBLE_MOVE = (130, 151, 105)
CAPTURE_MOVE = (169, 162, 58)
LAST_MOVE = (205, 210, 106)
BG_COLOR = (48, 46, 43)
TEXT_COLOR = (255, 255, 255)


board = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("        "),
    list("        "),
    list("        "),
    list("        "),
    list("PPPPPPPP"),
    list("RNBQKBNR")
]

captured_white = []
captured_black = []
last_move = None
user_wins = 0
computer_wins = 0


IMAGES = {}
image_folder = os.path.join(os.path.dirname(__file__), "images")
piece_to_file = {
    'P': 'Chess_plt60.png', 'p': 'Chess_pdt60.png',
    'R': 'Chess_rlt60.png', 'r': 'Chess_rdt60.png',
    'N': 'Chess_nlt60.png', 'n': 'Chess_ndt60.png',
    'B': 'Chess_blt60.png', 'b': 'Chess_bdt60.png',
    'Q': 'Chess_qlt60.png', 'q': 'Chess_qdt60.png',
    'K': 'Chess_klt60.png', 'k': 'Chess_kdt60.png',
}

for piece, filename in piece_to_file.items():
    path = os.path.join(image_folder, filename)
    try:
        image = pygame.image.load(path)
        IMAGES[piece] = pygame.transform.scale(
            image, (SQUARE_SIZE, SQUARE_SIZE))
    except pygame.error:
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
        surface.fill(color)
        font = pygame.font.Font(None, 36)
        text = font.render(piece.upper(), True, (255, 0, 0)
                           if piece.isupper() else (255, 255, 255))
        text_rect = text.get_rect(center=(SQUARE_SIZE//2, SQUARE_SIZE//2))
        surface.blit(text, text_rect)
        IMAGES[piece] = surface


def draw_board(win, selected_square, possible_moves):
    """Draw the chess board"""
    for row in range(ROWS):
        for col in range(COLS):
            is_light = (row + col) % 2 == 0
            color = LIGHT_SQUARE if is_light else DARK_SQUARE
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(win, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            if last_move and ((row, col) == last_move[0] or (row, col) == last_move[1]):
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                highlight_surface.set_alpha(100)
                highlight_surface.fill(LAST_MOVE)
                win.blit(highlight_surface, (x, y))

            if selected_square == (row, col):
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                highlight_surface.set_alpha(120)
                highlight_surface.fill(HIGHLIGHT_SELECTED)
                win.blit(highlight_surface, (x, y))

    for move in possible_moves:
        (_, _), (to_row, to_col) = move
        is_capture = board[to_row][to_col] != ' '
        center_x = to_col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = to_row * SQUARE_SIZE + SQUARE_SIZE // 2

        if is_capture:
            pygame.draw.circle(win, CAPTURE_MOVE, (center_x,
                               center_y), SQUARE_SIZE // 3, 4)
        else:
            pygame.draw.circle(win, POSSIBLE_MOVE,
                               (center_x, center_y), SQUARE_SIZE // 8)


def draw_pieces(win):
    """Draw pieces on the board"""
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != ' ':
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                win.blit(IMAGES[piece], (x, y))


def draw_bottom_info(win):
    """Draw scores and captured pieces below the board"""
    font = pygame.font.Font(None, 24)
    piece_size = 24

    score_y = BOARD_SIZE + 10
    user_text = font.render(f"User: {user_wins}", True, TEXT_COLOR)
    computer_text = font.render(f"Computer: {computer_wins}", True, TEXT_COLOR)

    user_rect = user_text.get_rect(center=(WIDTH // 4, score_y))
    computer_rect = computer_text.get_rect(center=(3 * WIDTH // 4, score_y))

    win.blit(user_text, user_rect)
    win.blit(computer_text, computer_rect)

    captured_y = BOARD_SIZE + 40

    x = 10
    for piece in captured_black:
        if x + piece_size > WIDTH // 2 - 10:
            break
        scaled_piece = pygame.transform.scale(
            IMAGES[piece], (piece_size, piece_size))
        win.blit(scaled_piece, (x, captured_y))
        x += piece_size + 2

    x = WIDTH // 2 + 10
    for piece in captured_white:
        if x + piece_size > WIDTH - 10:
            break
        scaled_piece = pygame.transform.scale(
            IMAGES[piece], (piece_size, piece_size))
        win.blit(scaled_piece, (x, captured_y))
        x += piece_size + 2


def is_valid_position(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def get_piece_moves(board, r, c):
    piece = board[r][c]
    if piece == ' ':
        return []

    moves = []

    if piece.upper() == 'P':
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1

        new_row = r + direction
        if is_valid_position(new_row, c) and board[new_row][c] == ' ':
            moves.append(((r, c), (new_row, c)))

            if r == start_row and board[new_row + direction][c] == ' ':
                moves.append(((r, c), (new_row + direction, c)))

        for dc in [-1, 1]:
            new_row, new_col = r + direction, c + dc
            if is_valid_position(new_row, new_col):
                target = board[new_row][new_col]
                if target != ' ' and piece.isupper() != target.isupper():
                    moves.append(((r, c), (new_row, new_col)))

    elif piece.upper() == 'N':
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            new_row, new_col = r + dr, c + dc
            if is_valid_position(new_row, new_col):
                target = board[new_row][new_col]
                if target == ' ' or piece.isupper() != target.isupper():
                    moves.append(((r, c), (new_row, new_col)))

    elif piece.upper() in ['R', 'B', 'Q']:
        directions = []
        if piece.upper() == 'R':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece.upper() == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.upper() == 'Q':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = r + dr * i, c + dc * i
                if not is_valid_position(new_row, new_col):
                    break
                target = board[new_row][new_col]
                if target == ' ':
                    moves.append(((r, c), (new_row, new_col)))
                elif piece.isupper() != target.isupper():
                    moves.append(((r, c), (new_row, new_col)))
                    break
                else:
                    break

    elif piece.upper() == 'K':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = r + dr, c + dc
            if is_valid_position(new_row, new_col):
                target = board[new_row][new_col]
                if target == ' ' or piece.isupper() != target.isupper():
                    moves.append(((r, c), (new_row, new_col)))

    return moves


def get_all_moves(board, white=True):
    """Get all possible moves for the given color"""
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == ' ':
                continue
            if white and piece.isupper():
                moves.extend(get_piece_moves(board, r, c))
            elif not white and piece.islower():
                moves.extend(get_piece_moves(board, r, c))
    return moves


def find_king(board, white=True):
    """Find the position of the king"""
    king = 'K' if white else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                return (r, c)
    return None


def is_square_attacked(board, row, col, by_white=True):
    """Check if a square is attacked by the given color"""
    attacking_moves = get_all_moves(board, white=by_white)
    for move in attacking_moves:
        (_, _), (target_row, target_col) = move
        if target_row == row and target_col == col:
            return True
    return False


def is_in_check(board, white=True):
    """Check if the king is in check"""
    king_pos = find_king(board, white)
    if king_pos is None:
        return False
    king_row, king_col = king_pos
    return is_square_attacked(board, king_row, king_col, by_white=not white)


def is_legal_move(board, move):
    """Check if a move is legal (doesn't put own king in check)"""
    (from_row, from_col), (to_row, to_col) = move
    piece = board[from_row][from_col]
    if piece == ' ':
        return False

    temp_board = copy.deepcopy(board)
    temp_board[to_row][to_col] = temp_board[from_row][from_col]
    temp_board[from_row][from_col] = ' '

    white_piece = piece.isupper()
    return not is_in_check(temp_board, white=white_piece)


def get_legal_moves(board, white=True):
    """Get all legal moves for the given color"""
    all_moves = get_all_moves(board, white)
    legal_moves = []
    for move in all_moves:
        if is_legal_move(board, move):
            legal_moves.append(move)
    return legal_moves


def is_checkmate(board, white=True):
    """Check if the given color is in checkmate"""
    if not is_in_check(board, white):
        return False
    legal_moves = get_legal_moves(board, white)
    return len(legal_moves) == 0


def is_stalemate(board, white=True):
    """Check if the given color is in stalemate"""
    if is_in_check(board, white):
        return False
    legal_moves = get_legal_moves(board, white)
    return len(legal_moves) == 0


def make_move(board, move):
    new_board = copy.deepcopy(board)
    (r1, c1), (r2, c2) = move
    captured_piece = new_board[r2][c2]
    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = ' '
    return new_board, captured_piece


def evaluate(board):
    piece_values = {'P': 1, 'p': -1, 'N': 3, 'n': -3, 'B': 3, 'b': -3,
                    'R': 5, 'r': -5, 'Q': 9, 'q': -9, 'K': 1000, 'k': -1000}
    score = 0
    for row in board:
        for piece in row:
            if piece in piece_values:
                score += piece_values[piece]
    return score


def minimax(board, depth, maximizing):
    """Simple minimax AI"""
    if depth == 0:
        return evaluate(board), None

    moves = get_legal_moves(board, white=maximizing)
    if not moves:
        if is_in_check(board, white=maximizing):
            return -10000 if maximizing else 10000, None
        else:
            return 0, None

    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            new_board, _ = make_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board, _ = make_move(board, move)
            eval_score, _ = minimax(new_board, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def get_square_from_mouse(mouse_pos):
    """Convert mouse position to board coordinates"""
    x, y = mouse_pos
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col)
    return None


def reset_game():
    global board, captured_white, captured_black, last_move
    board = [
        list("rnbqkbnr"),
        list("pppppppp"),
        list("        "),
        list("        "),
        list("        "),
        list("        "),
        list("PPPPPPPP"),
        list("RNBQKBNR")
    ]
    captured_white = []
    captured_black = []
    last_move = None


def main():
    global board, captured_white, captured_black, last_move, user_wins, computer_wins

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()

    selected = None
    possible_moves = []
    white_turn = True
    ai_thinking = False
    game_over = False

    running = True
    while running:
        clock.tick(60)

        if is_checkmate(board, white_turn):
            if not game_over:
                if white_turn:
                    computer_wins += 1
                else:
                    user_wins += 1
                game_over = True
        elif is_stalemate(board, white_turn):
            game_over = True

        win.fill(BG_COLOR)
        draw_board(win, selected, possible_moves)
        draw_pieces(win)
        draw_bottom_info(win)

        if game_over:
            font = pygame.font.Font(None, 48)
            if is_checkmate(board, white_turn):
                winner = "Computer" if white_turn else "User"
                text = font.render(f"{winner} Wins!", True, TEXT_COLOR)
            else:
                text = font.render("Draw!", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WIDTH // 2, BOARD_SIZE // 2))
            win.blit(text, text_rect)

            small_font = pygame.font.Font(None, 24)
            restart_text = small_font.render(
                "Press SPACE to play again", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(
                center=(WIDTH // 2, BOARD_SIZE // 2 + 40))
            win.blit(restart_text, restart_rect)

        pygame.display.flip()

        if not white_turn and not ai_thinking and not game_over:
            ai_thinking = True
            legal_moves = get_legal_moves(board, white=False)
            if legal_moves:
                _, ai_move = minimax(board, 2, False)
                if ai_move and ai_move in legal_moves:
                    new_board, captured_piece = make_move(board, ai_move)
                    board = new_board
                    last_move = ai_move

                    if captured_piece != ' ':
                        if captured_piece.isupper():
                            captured_white.append(captured_piece)
                        else:
                            captured_black.append(captured_piece)

                    white_turn = True
            ai_thinking = False
            selected = None
            possible_moves = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and white_turn and not ai_thinking and not game_over:
                square = get_square_from_mouse(pygame.mouse.get_pos())
                if square is None:
                    continue

                row, col = square

                if selected:
                    move = (selected, (row, col))
                    if move in possible_moves:
                        new_board, captured_piece = make_move(board, move)
                        board = new_board
                        last_move = move

                        if captured_piece != ' ':
                            if captured_piece.isupper():
                                captured_white.append(captured_piece)
                            else:
                                captured_black.append(captured_piece)

                        white_turn = False
                        selected = None
                        possible_moves = []
                    else:
                        piece = board[row][col]
                        if piece != ' ' and piece.isupper():
                            selected = (row, col)
                            piece_moves = get_piece_moves(board, row, col)
                            possible_moves = [
                                move for move in piece_moves if is_legal_move(board, move)]
                        else:
                            selected = None
                            possible_moves = []
                else:
                    piece = board[row][col]
                    if piece != ' ' and piece.isupper():
                        selected = (row, col)
                        piece_moves = get_piece_moves(board, row, col)
                        possible_moves = [
                            move for move in piece_moves if is_legal_move(board, move)]

            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    selected = None
                    possible_moves = []
                    white_turn = True
                    game_over = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
