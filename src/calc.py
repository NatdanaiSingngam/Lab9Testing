"""Campus Eats — TODO: เติมฟังก์ชันคำนวณส่วนลด + รวมยอด"""

VIP_RATE = 0.15
MEMBER_RATE = 0.10
PROMO_RATE = 0.20
PROMO_MIN_LEN = 6

def calculate_discount(total: int, tier: str, promo_code: str | None) -> int:
    """TODO: คำนวณส่วนลด

    - tier: vip/member/first
    - promo_code ยาว ≥ 6 ได้ 20% (ทับ tier ที่น้อยกว่า)
    - return int(total * rate)
    """
    rate = 0.0
    if promo_code and len(promo_code) >= PROMO_MIN_LEN:
        rate = PROMO_RATE
    elif tier == "vip":
        rate = VIP_RATE
    elif tier == "member":
        rate = MEMBER_RATE
    
    return int(total * rate)


def calculate_total(amount: int, tax_rate: float) -> float:
    """TODO: รวมยอด + ภาษี"""
    return amount * (1 + tax_rate)
