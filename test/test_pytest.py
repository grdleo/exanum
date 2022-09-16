# hello world!!!

from functools import reduce
import pytest
from exanum import ExactNumber as EN
from random import random, randint

def rdnb(len=8) -> str:
    r = lambda a, b : str(a) + str(randint(0, 9))
    s = reduce(r, range(len))
    fpt = randint(1, len - 1)
    s = s[:fpt] + ("." if randint(0, 1) else "") + s[fpt:]
    s = "-" + s if randint(0, 1) else s
    return s

def test_nb2dict():
    assert EN.nb2dict_digits(412.29) == {2:4,1:1,0:2,-1:2,-2:9}

def test_initialisation():
    assert EN(0).digits == {0:0}
    assert EN(123.45).digits == {2:1, 1:2, 0:3, -1:4, -2:5}
    assert EN("0098.1010000").digits == {0:8, 1:9, -1:1, -3:1}

    zeros = 2048
    x = EN("1." + "0"*zeros + "1")
    assert x.digits == {0:1, -zeros-1:1}
    assert x.digit(0) == 1
    assert x.digit(1) == 0
    assert x.digit(-1) == 0
    assert x.digit(-zeros-1) == 1

    assert EN({-1:9, -2:9, -3:10}) == {0:1}

def test_random_comparison():
    for _ in range(0, 100):
        a, b = rdnb(len=128), rdnb(len=128)
        na, nb = EN(a), EN(b)
        a, b = float(a), float(b)
        assert (na > nb) == (a > b)
        assert (na >= nb) == (a >= b)
        assert (na < nb) == (a < b)
        assert (na <= nb) == (a <= b)
        assert (na == nb) == (a == b)

def test_items():
    a = EN("123")
    a[1] += 412.29
    assert a.digits == {3:4, 2:2, 1:4, 0:5, -1:9}
    a[2] += -701
    assert a.digits == {-1:-1, 0:-4, 1:-5, 2:-8, 3:-5, 4:-6}
    a[2] = 12
    assert a.digits == {-1:-1, 0:-4, 1:-5, 2:-8, 3:-3, 4:-6}

def test_addition():
    zeros = 4096
    x = EN("1." + "0"*zeros + "123")
    assert x == EN(f"0.123e-{zeros}") + EN(1.)
    assert EN("1.007") + EN("0.009") == EN("1.016")
    assert EN("0.999") + EN("0.001") == EN("1")
    assert EN("1.123") - 0.456 == 0.667
    assert EN("12.9347") - 44.99311 == -32.05841
    assert EN(-4) + EN(-6) == -10

def test_random_addition():
    for _ in range(0, 100):
        a, b = rdnb(len=128), rdnb(len=128)
        fsum = float(a) + float(b)
        float(EN(a) + EN(b)) == pytest.approx(fsum)

@pytest.mark.parametrize("a, b", [
    (1, 1),
    (12, 345),
    (-4, 9.6),
    (12.345, 6.789),
    (8495309230825798446026, 87589734902190975034659823)
])
def test_mult(a, b):
    assert EN(a) * EN(b) == a * b

def test_random_mult():
    for _ in range(0, 100):
        a, b = rdnb(len=32), rdnb(len=32)
        prod = EN(a) * EN(b)
        fprod = float(a) * float(b)
        assert float(prod) == pytest.approx(fprod, 1e-12)

@pytest.mark.parametrize("a", [
    1,
    2,
    4,
    16,
    67.7283,
    12.34,
    -89.1111,
    893460396,
    12345678909876543456789512345678987253859834698436626476589346879682369586205876349856934
])
def test_half(a):
    assert float(EN(a)._halve()) == pytest.approx(a * 0.5, 1e-12)

@pytest.mark.parametrize("a, b", [
    (1, 1),
    (12, 1),
    (12, 5),
    (12, 12),
    (23, 4),
    (76, 55),
    (65, 43),
    (99, 21),
    (909, 451),
    (765, 128),
    (9467, 34),
    (62932, 1234),
    (91748, 12675),
    (987654321098, 2345),
    (8734986349689645934, 12479865285656)
])
def test_quotient(a, b):
    q = a // b
    assert EN._binary_method(EN(a), EN(b)) == q

@pytest.mark.parametrize("nb", [
    1,
    123,
    0.007823,
    8273560001443,
    9.00000043,
    -12.34
])
def test_scientific(nb):
    scistr = f"{nb:.32e}".split("e")
    f, e = float(scistr[0]), int(scistr[1])
    ff, ee = EN(nb).scientific_approx()
    assert f == pytest.approx(ff, 1e-9)
    assert e == ee

