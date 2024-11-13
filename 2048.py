# 2048.py

import logic
from game2dboard import Board
import time

# Initialize the game board
board = Board(4, 4)
board.cell_size = 100
board.title = "2048 Game"
board.margin = 10
board.cell_spacing = 5  # Adjusted for better visual spacing

# Initialize the game matrix
mat = logic.start_game()

def draw_board():
    for i in range(4):
        for j in range(4):
            value = mat[i][j]
            if value == 0:
                board[i][j] = 'empty.png'
            else:
                board[i][j] = f'{value}.png'

def key_press(key):
    global mat
    key = key.lower()
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
        # Use search_for_2048 instead of get_current_state
        status = logic.search_for_2048(mat)
        if status == 'WON':
            print("Congratulations! You won!")
            time.sleep(3)  # Wait for 3 seconds
            board.close()
        elif status == 'LOST':
            print('LOST')
            print("Game Over!")
            time.sleep(3)  # Wait for 3 seconds
            board.close()
    else:
        # Check if there are no moves left
        status = logic.search_for_2048(mat)
        if status == 'LOST':
            print("Game Over!")
            time.sleep(3)  # Wait for 3 seconds
            board.close()


# Initial draw
draw_board()
board.on_key_press = key_press  # Assign the key press handler
board.show()
