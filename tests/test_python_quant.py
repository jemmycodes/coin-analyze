from python_quant import func


def test_func_adds_one():
    assert func(3) == 4


def test_func_handles_negative_numbers():
    assert func(-1) == 0
