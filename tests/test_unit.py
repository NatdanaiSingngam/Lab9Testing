"""Unit Tests — TODO: เติม 5 tests (AAA + Boundary)"""
from src.calc import calculate_discount


def test_vip_gets_15_percent():
    total, tier, code = 1000, "vip", None
    assert calculate_discount(total, tier, code) == 150


def test_member_gets_10_percent():
    assert calculate_discount(1000, "member", None) == 100


def test_first_no_discount_without_promo():
    assert calculate_discount(1000, "first", None) == 0


def test_boundary_promo_len_5_no_discount():
    assert calculate_discount(1000, "first", "ABCDE") == 0


def test_boundary_promo_len_6_gets_discount():
    assert calculate_discount(1000, "first", "ABCDEF") == 200


def test_promo_overrides_member():
    assert calculate_discount(1000, "member", "ABCDEF") == 200


def test_zero_total():
    assert calculate_discount(0, "vip", None) == 0
