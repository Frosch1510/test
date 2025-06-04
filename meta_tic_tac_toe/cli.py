"""Simple terminal interface for Meta Tic Tac Toe."""
from __future__ import annotations

import sys

from .main import Game


SYMBOLS = {None: ".", "X": "X", "O": "O"}


def print_board(game: Game) -> None:
    board = game.board
    rows = []
    for br in range(3):
        sub_rows = ["" for _ in range(3)]
        for bc in range(3):
            sb = board.boards[br][bc].cells
            for r in range(3):
                sub_rows[r] += " ".join(SYMBOLS[c] for c in sb[r]) + "   "
        rows.extend(sub_rows)
        rows.append("")
    sys.stdout.write("\n".join(rows) + "\n")


def prompt_move(game: Game) -> None:
    player = game.next_player
    allowed = game.board.allowed_board()
    if allowed is None:
        print(f"Player {player}, choose board row,col and cell row,col (e.g. 0 2 1 1):")
    else:
        br, bc = allowed
        print(
            f"Player {player}, you must play on board ({br}, {bc}). "
            "Enter cell row and column (e.g. 0 2):"
        )
    while True:
        try:
            tokens = input().strip().split()
            if allowed is None:
                if len(tokens) != 4:
                    raise ValueError
                br, bc, cr, cc = map(int, tokens)
            else:
                if len(tokens) != 2:
                    raise ValueError
                cr, cc = map(int, tokens)
                br, bc = allowed
            game.play(br, bc, cr, cc)
            break
        except Exception as exc:  # catch ValueError and others
            print(f"Invalid move: {exc}. Try again:")


def main() -> None:
    game = Game()
    while not game.board.overall_winner:
        print_board(game)
        prompt_move(game)
    print_board(game)
    print(f"Winner: {game.board.overall_winner}")


if __name__ == "__main__":
    main()
