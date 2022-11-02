# hello world!

from __future__ import division
import math
from functools import reduce

class ExactNumber:
  pass

class ExactNumber:
  MAX_BITS_FLOAT = 64 - 1 # minus for security
  LIMIT_FLOATABLE = MAX_BITS_FLOAT * math.log(2) / math.log(10)
  
  def __init__(self, x: str | int | float | dict = 0):
    self.digits = {0:0}
    self._update_boundaries()

    if isinstance(x, str | int | float):
      self.digits = ExactNumber.nb2dict_digits(x)
      self._update_boundaries()
    elif isinstance(x, dict):
      if ExactNumber.is_dict_correct(x):
        for k in sorted(x.keys()):
          v = x[k]
          if v != 0:
            self[k] += v
      else:
        raise ValueError(f"Dict given {x} has wrong format!")
    else:
      raise ValueError(f"Could not create number from given argument {x}")
  
  def __repr__(self, prec=64) -> str:
    # bound = min(prec, abs(self.dmax - self.dmin)) + 1
    # digs = [str(self[k]) + ("." if k == 0 else "") for k in range(self.dmax, self.dmax - bound)]
    # return reduce(lambda a, b : a + b, digs)
    return "<EN " + str(float(self)) + ">"

  def digit(self, idx: int) -> int:
    """Returns corresponding digit at given position
    """
    if isinstance(idx, int):
      return self.digits.get(idx, 0)
    else:
      raise ValueError(f"'{idx}' has wrong type '{type(idx)}': must be `int`")
  
  def __getitem__(self, idx: int) -> int:
    """Returns corresponding digit at given position
    """
    if isinstance(idx, int):
      return self.digits.get(idx, 0)
    else:
      raise ValueError(f"'{idx}' has wrong type '{type(idx)}': must be `int`")
  
  def __setitem__(self, idx: int, val: int | float):
    """Sets the corresponding digit at given position"""
    """TO IMPLEMENT: if user sets digit at 2 with value 12.34
    well, it is simply equivalent to this correct dict: {3:1, 2:2, 1:3, 0:4}, and we add this dict to the digits dict
    so if user wants to set this value, it updates the """
    if isinstance(idx, int):
      if isinstance(val, int | float):
        if (-10 < val < 10) and isinstance(val, int):
          self.digits[idx] = val
        else:
          self.digits[idx] = 0
          codic = {(k + idx): v for k, v in ExactNumber.nb2dict_digits(val).items()} # this gives the corresponding good formatted dict of the given value at index!!
          self.digits = {k: codic.get(k, 0) + self.digits.get(k, 0) for k in set(self.digits.keys()) | set(codic.keys())}
        self._remove_zeros()
        keys = sorted(self.digits)
        isneg = self.digits.get(keys[-1]) < 0
        sig = (-1)**isneg
        k = keys[0]
        while True:
          if self[k] == 0 and k > self.dmax:
            break
          d = self[k]
          if d != 0:
            divi = sig * (d // (sig * 10))
            self.digits[k] %= sig * 10
            if divi != 0:
              self.digits[k+1] = self.digits.get(k+1, 0) + divi
          k += 1
        self._remove_zeros()
      else:
        raise ValueError(f"'{val}' has wrong type '{type(val)}': must be `int`")
    else:
      raise ValueError(f"'{idx}' has wrong type '{type(idx)}': must be `int`")

  def _update_boundaries(self) -> None:
    keys = self.digits.keys()
    self.dmin, self.dmax = min(keys), max(keys)
  
  def _remove_zeros(self) -> None:
    for k in list(self.digits.keys()):
      if self.digits[k] == 0:
        del self.digits[k]
    self._update_boundaries()
  
  def is_negative(self) -> bool:
    return self.digit(self.dmax) < 0
  
  @staticmethod
  def is_dict_correct(d: dict[int, int]) -> bool:
    """`True` if given dict is `dict[int, int]`, aka can store digits"""
    for k, v in d.items():
      correct = isinstance(k, int) and isinstance(v, int)
      if not correct:
        return False
    else:
      return True

  def iterator_digits(self, other):
    # generator on all relevant digits for both numbers
    for el in set(self.digits.keys()).union(set(other.digits.keys())):
      yield el

  def comparison(self, other: ExactNumber) -> int:
    """Compares each digits of both numbers and returns their difference if not equal
    """
    if isinstance(other, ExactNumber):
      for i in sorted(self.iterator_digits(other), reverse=True):
        delta = self.digit(i) - other.digit(i)
        if delta:
          return delta
      else:
        return 0
    else:
      raise ValueError(f"{other} not a {type(ExactNumber)}")

  def __lt__(self, other: ExactNumber) -> bool: # <
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) < 0

  def __le__(self, other: ExactNumber) -> bool: # <=
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) <= 0

  def __gt__(self, other: ExactNumber) -> bool: # >
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) > 0

  def __ge__(self, other: ExactNumber) -> bool: # >=
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) >= 0

  def __eq__(self, other: ExactNumber) -> bool: # ==
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) == 0

  def __ne__(self, other: ExactNumber) -> bool: # !=
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return self.comparison(o) != 0

  def __add__(self, other: ExactNumber) -> ExactNumber: # +
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return ExactNumber({k: self[k] + o[k] for k in self.iterator_digits(o)})

  def __sub__(self, other: ExactNumber) -> ExactNumber: # -
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    return ExactNumber({k: self[k] - o[k] for k in self.iterator_digits(o)})
  
  def __neg__(self) -> ExactNumber: # -()
    return ExactNumber({k: -v for k, v in self.digits.items()})
  
  def __abs__(self) -> ExactNumber: # abs()
    if self.is_negative():
      return -self
    else:
      return self
  
  def __lshift__(self, n: int) -> ExactNumber: # <<
    """Shifts the decimal point to the right, equivalent to multiplying by 10**n"""
    return ExactNumber({k + int(n): v for k, v in self.digits.items()})
  
  def __rshift__(self, n: int) -> ExactNumber: # >>
    """Shifts the decimal point to the left, equivalent to dividing by 10**n"""
    return ExactNumber({k - int(n): v for k, v in self.digits.items()})

  def __mul__(self, other: ExactNumber) -> ExactNumber: # *
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    di = {}
    for ka, va in self.digits.items():
      for kb, vb in o.digits.items():
        idx = ka + kb
        di[idx] = di.get(idx, 0) +  va * vb
    return ExactNumber(di)

  def __div__(self, other: ExactNumber, prec: int=64): # /
    o = other if isinstance(other, ExactNumber) else ExactNumber(other)
    a = abs(self)
    b = abs(o)
    
    # TODO: handling if `b > a`!
    correction = ExactNumber(1)
    expo = 1
    if b > a:
      expo = math.ceil(a.log10_approx() - b.log10_approx()) # finding N so that `10**N >= a/b`
      a =<< expo
      
    quot = ExactNumber._binary_method(a, b)
    rest = self - quot*b
    digits = quot.digits
    for i in range(-1, -prec, -1):
      r10 = rest * 10
      q = int(ExactNumber._binary_method(r10, b)) # q < 10 !
      digits[i] = q
      rest = r10 - q*b
      if rest == 0:
        break
    
    pn = ExactNumber(digits) >> expo
    return -pn if (self.is_negative() ^ o.is_negative()) else pn
  
  def _halve(self) -> ExactNumber:
    "Computes and returns the half of the number"
    digits = {}
    ret = 0
    for i in range(self.dmax, self.dmin - 1, -1):
      d = self.digit(i)
      digits[i] = d // 2 + ret
      ret = 0 if d % 2 == 0 else 5
    if ret != 0:
      digits[self.dmin-1] = ret
    return ExactNumber(digits)

  @staticmethod
  def nb2dict_digits(x: float | int | str):
    digits = dict()

    if isinstance(x, float):
      if x == 0:
        return {0:0}
      x = str(x)
    
    if isinstance(x, str):
      isneg = x[0] == "-"
      try:
        float(x)
      except ValueError:
        ValueError(f"{x} could not be interpreted as a number")
      m = (-1)**isneg
      if isneg: # trim negative sign
        x = x[1:]
      x = x.lower()
      if "e" in x: # scientific notation
        num, zeros = x.split("e")
        digits = ExactNumber.nb2dict_digits(num) # we generate the corresponding number
        return {k + int(zeros): v for k, v in digits.items()} # and we shift the decimals by the number of zeros
      else:
        dig, *dec = x.split(".")
        dec = dec[0] if len(dec) != 0 else ""
        for i, d in enumerate(dig[::-1]):
          if (v := int(d)) != 0:
            digits[i] = v * m
        for i, d in enumerate(dec):
          j = -(i + 1)
          if (v := int(d)) != 0:
            digits[j] = v * m
        return digits if digits != {} else {0:0}
    elif isinstance(x, int):
      if x == 0:
        return {0:0}
      m = (-1)**(x < 0)
      if m < 0:
        x = abs(x)
      i = 0
      while x > 0:
        digits[i] = (x % 10)*m
        x //= 10
        i += 1
      return digits
    else:
      raise ValueError(f"{x} has wrong type {type(x)}. (should be int | float | str)")
  
  def __float__(self) -> float:
    # careful: may lose information!
    r = 0
    for k, v in sorted(self.digits.items(), reverse=True):
      rr = v * 10**k
      if r == r + rr:
        break
      r += rr
    return float(r)
  
  def __int__(self) -> int:
    return sum(v * 10**k for k, v in self.digits.items() if k >= 0) + (1 if self.digit(-1) >= 5 else 0)
  
  def lossless_float(self) -> float:
    if self.dmax - self.dmin < ExactNumber.LIMIT_FLOATABLE:
      return float(self)
    else:
      raise RuntimeError("Too much information to convert number as float!")
  
  def scientific_approx(self) -> tuple[float, int]:
    """Returns the scientific notation (approximative) of the number
    
    Example:
    >>> print(ExactNumber(12345e8).scientific_approx())
    >>> (1.2345, 8)
    >>> print(ExactNumber('0.0000456').scientific_approx())
    >>> (4.56, -5)
    """
    return float(self << -self.dmax), self.dmax
  
  def log10_approx(self) -> float:
    """Returns a float approximation of the natural logarithm"""
    f, e = self.scientific_approx()
    return math.log10(f) + e

  def __hash__(self) -> int:
    return hash(self.digits)
  
  @staticmethod
  def _binary_method(a: ExactNumber, b: ExactNumber) -> ExactNumber:
    """Binary method for division calculation a/b, returns the quotient

    https://fr.wikipedia.org/wiki/Division_euclidienne#M%C3%A9thode_binaire
    """
    conda = a >= 0
    condb = b > 0
    if not (conda and condb):
      raise ArithmeticError(
        f"Could not do binary method on both {a} and {b}: "
        f"{a} should be >= 0   " if conda else ""
        f"{b} should be > 0    " if condb else ""
      )
     
    if b > a:
      raise ArithmeticError
    
    one = ExactNumber(1)
    if a == b:
      return one
    elif b == one:
      return a
    
    n = math.floor((a.log10_approx() - b.log10_approx()) / math.log10(2)) # approximation of the 2**n
    alpha = ExactNumber(2**n)
    beta = ExactNumber(2**(n+1))
    for _ in range(0, n):
      mid = (alpha + beta)._halve()
      pr = mid * b
      seta, setb = (mid, beta) if (pr <= a) else (alpha, mid)
      alpha = seta
      beta = setb
      if pr == a:
        break
    return alpha
