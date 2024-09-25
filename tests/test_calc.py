from dagger_test import add


def test_add():
    x, y = 1, 2
    truth = 3

    assert add(x, y) == truth
