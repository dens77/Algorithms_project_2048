import logic
from game2dboard import Board

# Initialize the game board
board = Board(4, 4)
board.cell_size = 100
board.title = "2048 Game"
board.margin = 10
board.cell_spacing = 5  # Adjusted for better visual spacing

# Initialize the game matrix, game_over flag, score, and scores list
mat = logic.start_game()
game_over = False
score = 0
scores = []


def draw_board():
    """Draw the current game board on the UI."""
    for i in range(4):
        for j in range(4):
            value = mat[i][j]
            if value == 0:
                board[i][j] = 'empty.png'  # Path to the empty tile image
            else:
                board[i][j] = f'{value}.png'  # Path to numbered tile images
    board.title = f"2048 Game - Score: {score}"  # Update board title with the score


def display_scoreboard(scores):
    """Display the top scores."""
    print("\nScoreboard:")
    for idx, sc in enumerate(scores):
        print(f"{idx + 1}. {sc}")
    print()


def key_press(key):
    """Handle key presses for game actions."""
    global mat, game_over, score, scores
    key = key.lower()

    if game_over:
        if key == 'r':
            mat = logic.start_game()
            game_over = False
            score = 0  # Reset score on restart
            draw_board()
            print("Game restarted! Continue playing.")
        elif key == 'e':
            board.close()
        else:
            print("Press 'r' to restart or 'e' to exit.")
        return

    if key == 'w':
        mat, changed, move_score = logic.move_up(mat)
    elif key == 's':
        mat, changed, move_score = logic.move_down(mat)
    elif key == 'a':
        mat, changed, move_score = logic.move_left(mat)
    elif key == 'd':
        mat, changed, move_score = logic.move_right(mat)
    else:
        return  # Ignore other keys

    if changed:
        score += move_score  # Update the score with points from the move
        logic.add_new_2(mat)
        draw_board()
        status = logic.search_for_2048_bfs(mat)  
        if status == 'WON':
            print("Congratulations! You won!")
            scores.append(score)
            logic.insertion_sort(scores) 
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True
        elif status == 'LOST':
            print("Game Over!")
            scores.append(score)
            logic.insertion_sort(scores)
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True
    else:
        status = logic.search_for_2048_bfs(mat)
        if status == 'LOST':
            print("Game Over!")
            scores.append(score)
            logic.insertion_sort(scores)
            display_scoreboard(scores)
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True


# Initial draw
draw_board()
board.on_key_press = key_press
board.show()
