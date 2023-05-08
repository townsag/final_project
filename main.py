import math
import time
import io

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Container, Window, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea

from rich.console import Console
import numpy as np
from pyfiglet import Figlet
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from board_functions import *

empty_cell = "              \n              \n              \n" \
             "              \n              \n"

color_lookup: dict[int, str] = {
    0: "grey93",
    2: "dark_violet",
    4: "blue_violet",
    8: "blue1",
    16: "dodger_blue1",
    32: "pale_turquoise1",
    64: "green4",
    128: "chartreuse1",
    256: "yellow1",
    512: "dark_orange",
    1024: "red1",
    2048: "orchid1"
}

symbol_lookup: dict[int, str] = dict()
board: ndarray[int, ...] = np.zeros((4, 4), dtype=int)
score: int
console: Console


def main():
    global symbol_lookup
    # initialize the symbol lookup
    f = Figlet(font='slant')
    # f = Figlet(font='avatar')
    # f = Figlet(font='starwars')
    symbol_lookup = dict()
    symbol_lookup[0] = empty_cell
    for i in range(1, 12):
        symbol_lookup[int(math.pow(2, i))] = \
            f.renderText(str(int(math.pow(2, i))))

    global board
    board = add_value(board)

    global score
    score = 0

    global console
    console = Console()

    welcome_text = f.renderText("Welcome") + "\n\n press any of WASD to begin\n"
    exit_text = f.renderText("Game Over")
    text_area = TextArea(text=welcome_text, wrap_lines=False)
    root_container = VSplit([text_area])
    layout = Layout(root_container)

    def update_board(key: str):
        key_to_direction_index = {"w": 0, "d": 1, "s": 2, "a": 3}
        key_to_direction_str = {"w": "up", "d": "right", "s": "down", "a": "left"}
        global board
        global score
        if is_valid_move(board, key_to_direction_index[key]):
            board, score = make_move(board, score, key_to_direction_index[key])
            board = add_value(board)
            print_board(board, score)
        else:
            print_board(board, score, message=f"{key_to_direction_str[key]} is not a valid move")

    bindings = KeyBindings()

    @bindings.add("w")
    @bindings.add("d")
    @bindings.add("s")
    @bindings.add("a")
    def _(event):
        update_board(event.key_sequence[0].key)
        global board
        if not has_valid_move(board):
            print_board(board, score,
                        message="\nNo more moves\nGame Over :(\nPress q to "
                                "exit")
            # global score
            nonlocal exit_text
            nonlocal text_area
            text_area.text = "\n" + exit_text + f"\n\n final score: {score}\n"
            event.app.exit()

    @bindings.add("q")
    def exit_(event):
        global score
        nonlocal exit_text
        nonlocal text_area
        text_area.text = "\n" + exit_text + f"\n\n final score: {score}\n"
        event.app.exit()

    @bindings.add("e")
    def cheat_code_(event):
        global board
        global score
        board = np.array([[1024, 512, 256, 128],
                          [8, 16, 32, 64],
                          [2, 0, 0, 0],
                          [0, 0, 0, 0]])
        print_board(board, score)

    # Create the application instance with the layout and key bindings.
    app = Application(layout=layout, key_bindings=bindings)

    # Run the application.
    app.run()


def print_board(board: ndarray[int, ...], score: int, message=None) -> str:
    global symbol_lookup
    global color_lookup

    caption = f"Your score: {str(score)}"
    if message is not None:
        caption += ", " + message

    table = Table(
        title=f"Play 2048\nWASD to move, q to quit",
        caption=caption,
        style="bright_white",
        caption_style="bright_white",
        box=box.ROUNDED,
        padding=0,
        show_header=False,
        show_footer=False,
        show_lines=True,
        width=116
    )

    for i in range(4):
        table.add_column(width=29)

    for i in range(board.shape[0]):
        cells = []
        for j in range(board.shape[1]):
            cell_text = None
            cell_text = Text(symbol_lookup[board[i, j]], justify="center")
            cell_text.stylize(color_lookup[board[i, j]])
            cells.append(cell_text)
        table.add_row(*cells)

    global console
    console.clear()
    console.print(table)


if __name__ == "__main__":
    main()
