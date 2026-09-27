"""Properties of the discount rules across generated inputs."""

from hypothesis import given
from hypothesis import strategies as st

from src.calc import calculate_discount
from src.fizzbuzz import fizzbuzz


@given(st.integers(min_value=0, max_value=100_000))
def test_vip_discount_is_fifteen_percent_without_promo(total):
    assert calculate_discount(total, "vip", None) == int(total * 0.15)


@given(
    st.integers(min_value=0, max_value=100_000),
    st.text(min_size=6, max_size=20),
    st.sampled_from(["vip", "member", "first"]),
)
def test_qualifying_promo_overrides_every_tier(total, promo_code, tier):
    assert calculate_discount(total, tier, promo_code) == int(total * 0.20)


@given(
    st.integers(min_value=0, max_value=100_000),
    st.text(max_size=5),
)
def test_short_promo_does_not_discount_first_tier(total, promo_code):
    assert calculate_discount(total, "first", promo_code) == 0


@given(st.integers(min_value=1, max_value=10_000))
def test_fizzbuzz_classifies_multiples_of_fifteen(multiplier):
    assert fizzbuzz(multiplier * 15) == "FizzBuzz"
