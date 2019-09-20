import arcade
from board import CellStatus, Board

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * 8 + MARGIN + 30
SCREEN_HEIGHT = (HEIGHT + MARGIN) * 8 + MARGIN + 30
SCREEN_TITLE = "Battleship"

class BoardWindow(arcade.Window):
    '''
    Window for the main game phase (displaying boards and shooting shots)
    '''

    def __init__(self, width, height, title, board: Board):
        super().__init__(width, height, title)
        self.shape_list = None
        self.board = board

        arcade.set_background_color(arcade.color.BLACK)
        self.recreate_grid()

    def recreate_grid(self):
        self.shape_list = arcade.ShapeElementList()
        grid = self.board.get_board_view()[0]
        for row in range(8):
            for column in range(8):
                if grid[row][column] == CellStatus.EMPTY:
                    color = arcade.color.WHITE
                elif grid[row][column] == CellStatus.MISS:
                    color = arcade.color.GRAY
                elif grid[row][column] == CellStatus.HIT:
                    color = arcade.color.RED

                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                current_rect = arcade.create_rectangle_filled(x + 30, y, WIDTH, HEIGHT, color)
                self.shape_list.append(current_rect)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        numbers.reverse()
        for i in range(8):
            arcade.draw_text(letters[i], (i * 80) + 70, SCREEN_WIDTH - 20, arcade.color.WHITE)
            arcade.draw_text(numbers[i], 15, (i * 80) + 70, arcade.color.WHITE)

        self.shape_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change the x/y screen coordinates to grid coordinates
        column = (x - 30) // (WIDTH + MARGIN)
        row = (y) // (HEIGHT + MARGIN)

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < 8 and column < 8:
            self.board.attacked(row, column)

        self.recreate_grid()