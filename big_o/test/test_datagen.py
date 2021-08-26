from big_o import datagen


def test_n_():
    assert datagen.n_(0) == 0
    assert datagen.n_(3) == 3


def test_range_n():
    result = datagen.range_n(5, start=4)
    expected = [4, 5, 6, 7, 8]
    assert result == expected


def test_integers():
    n = 912
    result = datagen.integers(n, min_=3, max_=12)
    assert len(result) == n
    assert min(result) >= 3
    assert max(result) <= 12


def test_large_integers():
    n = 912
    result = datagen.large_integers(n)
    assert len(result) == n
    assert max(result) > 1000000


def test_strings():
    chars = ['O', 'M', 'G']
    result = datagen.strings(13, chars=chars)
    assert isinstance(result, str)
    assert len(result) == 13
    assert len(set(result).difference(set(chars))) == 0
