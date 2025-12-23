import pytest

from calc import calculate, evaluate


@pytest.mark.parametrize("op,a,b,expected", [
    ('^', 2, 3, 8),
    ('^^', 6, 3, 5),
    ('sigma', 1, 5, 15),
    ('&', 6, 3, 2),
    ('|', 6, 3, 7),
    ('pow', 2, 10, 1024),
    ('xor', 10, 3, 9),
    ('sum', 5, 3, 12),
])
def test_calculate(op, a, b, expected):
    assert calculate(op, a, b) == expected


def test_evaluate_simple():
    val, env = evaluate('2 + 3')
    assert val == 5


def test_evaluate_assign_and_use():
    val, env = evaluate('x = 10\nx * 2')
    assert val == 20
    assert env['x'] == 10
