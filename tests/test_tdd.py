"""TDD — TODO: Red-Green-Refactor กับ calculate_total"""
from src.calc import calculate_total


def test_calculate_total_with_tax():
    assert calculate_total(100, 0.07) == 107.0


def test_calculate_total_no_tax():
    assert calculate_total(100, 0.0) == 100.0


def test_calculate_total_zero_amount():
    assert calculate_total(0, 0.07) == 0.0


# TDD History (ทำ 3 commits แยก):
# commit 1 [RED]    test: add calculate_total test — FAIL
# commit 2 [GREEN]  feat: minimal calculate_total — PASS
# commit 3 [REFACTOR] refactor: simplify — PASS
