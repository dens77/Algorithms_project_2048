import logic
from game2dboard import Board

# Initialize the game board
board = Board(4, 4)
board.cell_size = 100
board.title = "2048 Game"
board.margin = 10
board.cell_spacing = 5  # Adjusted for better visual spacing

# Initialize the game matrix and game_over flag
mat = logic.start_game()
game_over = False


def draw_board():
    """Draw the current game board on the UI."""
    for i in range(4):
        for j in range(4):
            value = mat[i][j]
            if value == 0:
                board[i][j] = 'empty.png'  # Path to the empty tile image
            else:
                board[i][j] = f'{value}.png'  # Path to numbered tile images


def key_press(key):
    """Handle key presses for game actions."""
    global mat, game_over
    key = key.lower()

    if game_over:
        if key == 'r':
            mat = logic.start_game()
            game_over = False
            draw_board()
            print("Game restarted! Continue playing.")
        elif key == 'e':
            board.close()
        else:
            print("Press 'r' to restart or 'e' to exit.")
        return

    if key == 'w':
        mat, changed = logic.move_up(mat)
    elif key == 's':
        mat, changed = logic.move_down(mat)
    elif key == 'a':
        mat, changed = logic.move_left(mat)
    elif key == 'd':
        mat, changed = logic.move_right(mat)
    else:
        return  # Ignore other keys

    if changed:
        logic.add_new_2(mat)
        draw_board()
        status = logic.search_for_2048(mat)  # Use the search_for_2048 function
        if status == 'WON':
            print("Congratulations! You won!")
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True
        elif status == 'LOST':
            print("Game Over!")
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True
    else:
        # Check if there are no moves left
        status = logic.search_for_2048(mat)
        if status == 'LOST':
            print("Game Over!")
            print("Press 'r' to restart or 'e' to exit.")
            game_over = True


# Initial draw
draw_board()
board.on_key_press = key_press
board.show()
