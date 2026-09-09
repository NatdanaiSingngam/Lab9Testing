# Lab09 Starter — ให้นิสิตเติมเอง

โฟลเดอร์นี้คือ **Starter** — มีโครงว่าง + TODO ให้นิสิตเติมเอง
เฉลยดูที่ `../lab09-sample-solution/`

## วิธีทำ

```bash
pip install -r requirements.txt
pytest -v              # ตอนแรกจะ FAIL (เพราะยัง TODO)
# เติมโค้ดตาม TODO ใน src/ และ tests/ แล้วรันใหม่จนเขียว
pytest --cov=src --cov-branch -v
```

## สิ่งที่ต้องเติม (ดู TODO ในไฟล์)

1. `src/calc.py` — เติม `calculate_discount` + `calculate_total`
2. `tests/test_unit.py` — เติม 5 Unit Tests (AAA + Boundary)
3. `tests/test_doubles.py` — เติม Stub / Mock / Fake
4. `tests/test_tdd.py` — เติม TDD 3 tests
