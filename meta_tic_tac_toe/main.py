"""Meta Tic Tac Toe game logic.

This module implements the core mechanics of Meta Tic Tac Toe (also
known as Ultimate Tic Tac Toe). The game consists of nine 3x3 boards
arranged in a 3x3 grid. Players take turns placing X and O marks.
The square chosen dictates the board for the opponent's next move.
Winning a small board yields that board for the player. The first
player to win three small boards in a row (horizontally, vertically or
diagonally) wins the match.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Player = str  # either "X" or "O"


@dataclass
class SmallBoard:
    """Represents a single 3x3 Tic Tac Toe board."""

    cells: List[List[Optional[Player]]] = field(
        default_factory=lambda: [[None] * 3 for _ in range(3)]
    )
    winner: Optional[Player] = None
    is_full: bool = False

    def play(self, row: int, col: int, player: Player) -> None:
        """Place a mark for *player* at *row*, *col* if possible."""
        if self.winner or self.is_full:
            raise ValueError("Board already finished")
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Cell out of range")
        if self.cells[row][col] is not None:
            raise ValueError("Cell already occupied")

        self.cells[row][col] = player
        self._update_state(player)

    def _update_state(self, player: Player) -> None:
        lines = [
            self.cells[0],
            self.cells[1],
            self.cells[2],
            [self.cells[r][0] for r in range(3)],
            [self.cells[r][1] for r in range(3)],
            [self.cells[r][2] for r in range(3)],
            [self.cells[i][i] for i in range(3)],
            [self.cells[i][2 - i] for i in range(3)],
        ]
        if any(all(cell == player for cell in line) for line in lines):
            self.winner = player
        self.is_full = all(cell is not None for row in self.cells for cell in row)


@dataclass
class MetaBoard:
    """A board containing nine :class:`SmallBoard` instances."""

    boards: List[List[SmallBoard]] = field(
        default_factory=lambda: [[SmallBoard() for _ in range(3)] for _ in range(3)]
    )
    overall_winner: Optional[Player] = None
    last_move: Optional[Tuple[int, int, int, int]] = None  # board_row, board_col, cell_row, cell_col

    def play(self, br: int, bc: int, cr: int, cc: int, player: Player) -> None:
        """Make a move on board (br, bc) at cell (cr, cc)."""
        if self.overall_winner:
            raise ValueError("Game already finished")
        if self.last_move is not None:
            expected_br, expected_bc = self.last_move[2], self.last_move[3]
            target_board = self.boards[expected_br][expected_bc]
            if not target_board.is_full and (br != expected_br or bc != expected_bc):
                raise ValueError(
                    f"Must play on directed board ({expected_br}, {expected_bc})"
                )
        if not (0 <= br < 3 and 0 <= bc < 3):
            raise ValueError("Board coordinates out of range")

        board = self.boards[br][bc]
        board.play(cr, cc, player)
        self.last_move = (br, bc, cr, cc)
        self._update_overall_state(player, br, bc)

    def _update_overall_state(self, player: Player, br: int, bc: int) -> None:
        if self.boards[br][bc].winner != player:
            return

        winners = [[b.winner for b in row] for row in self.boards]
        lines = [
            winners[0],
            winners[1],
            winners[2],
            [winners[r][0] for r in range(3)],
            [winners[r][1] for r in range(3)],
            [winners[r][2] for r in range(3)],
            [winners[i][i] for i in range(3)],
            [winners[i][2 - i] for i in range(3)],
        ]
        if any(all(cell == player for cell in line) for line in lines):
            self.overall_winner = player

    def allowed_board(self) -> Optional[Tuple[int, int]]:
        """Return the coordinates of the board the next player must play on.

        If the directed board is full or None, the player can choose any
        unfinished board (returns None).
        """
        if self.last_move is None:
            return None
        br, bc = self.last_move[2], self.last_move[3]
        if self.boards[br][bc].is_full:
            return None
        return br, bc


@dataclass
class Game:
    """Manages player turns and enforces move validity."""

    next_player: Player = "X"
    board: MetaBoard = field(default_factory=MetaBoard)

    def play(self, br: int, bc: int, cr: int, cc: int) -> None:
        player = self.next_player
        self.board.play(br, bc, cr, cc, player)
        self.next_player = "O" if player == "X" else "X"


__all__ = ["SmallBoard", "MetaBoard", "Game"]
