import pytest

from naval_warfare.models import Board2D


@pytest.mark.parametrize("length,width", [(1, 1), (2, 3), (3, 2)])
def test_should_create_a_2d_board_with_the_given_length_and_width(length: int, width: int):
    board = Board2D(length, width)

    assert board.length == length
    assert board.width == width
