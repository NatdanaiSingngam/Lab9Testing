# คู่มือทำแล็บ Lab09 แบบละเอียด (สำหรับผู้เริ่มต้น — ไม่มีพื้นฐานมาก่อน)
# Testing Pyramid + Test Doubles + TDD + Coverage

> **สำหรับนิสิตที่ยังไม่เคยเขียน test มาก่อน** — คู่มือนี้อธิบายทุกคำศัพท์ ทุกคำสั่ง ทีละบรรทัด ทำตามได้เลยแม้ไม่เคยใช้ `pytest` หรือ `git` มาก่อน

---

## สารบัญ

0. [คำศัพท์ที่ต้องรู้ก่อน (5 นาที)](#0-คำศัพท์ที่ต้องรู้ก่อน)
1. [ทำไมต้องทำแล็บนี้](#1-ทำไมต้องทำแล็บนี้)
2. [เตรียมเครื่องทีละขั้น (Windows)](#2-เตรียมเครื่องทีละขั้น)
3. [ภาพรวม 5 ขั้น — ทำอะไรบ้างใน 2 ชั่วโมง](#3-ภาพรวม-5-ขั้น)
4. [ขั้น 1: Testing Pyramid — แยก test 3 ระดับ](#ขั้น-1)
5. [ขั้น 2: TDD — เขียน test ก่อน แล้วค่อยเขียนโค้ด](#ขั้น-2)
6. [ขั้น 3: Test Doubles — ตัวปลอมแทนของจริง](#ขั้น-3)
7. [ขั้น 4: Coverage + Lint — วัดว่า test พอไหม](#ขั้น-4)
8. [ขั้น 5: Saboteur — แกล้งทำโค้ดพังดูว่า test จับได้ไหม](#ขั้น-5)
9. [ส่งงาน](#9-ส่งงาน)
10. [แก้ปัญหาเมื่อติด (รวม PowerShell)](#10-แก้ปัญหาเมื่อติด)
11. [ตัวอย่างที่รันได้ (Starter/Solution)](#11-ตัวอย่างที่รันได้)

---

## 0. คำศัพท์ที่ต้องรู้ก่อน

> ถ้ารู้แล้วข้ามไปข้อ 1 ได้เลย

| คำศัพท์ | คืออะไร (อธิบายแบบบ้านๆ) | ตัวอย่าง |
|---|---|---|
| **Test** | โปรแกรมเล็กๆ ที่ตรวจว่าโปรแกรมใหญ่ทำงานถูกไหม | `assert calculate_discount(1000, "vip", None) == 150` |
| **Unit Test** | test ฟังก์ชันเดียว ไม่ยุ่งกับของอื่น | test `calculate_discount` อย่างเดียว |
| **Integration Test** | test หลายชิ้นต่อกัน | test "กดปุ่มสั่งอาหาร → บันทึก DB" |
| **E2E Test** | test เหมือนผู้ใช้จริง เปิดแอปแล้วคลิก | เปิด browser → login → สั่งอาหาร |
| **pytest** | โปรแกรมรัน test ของ Python | พิมพ์ `pytest` แล้วมันรันทุก `test_*.py` |
| **Mock/Stub/Fake** | **ตัวปลอม** แทนของจริง (DB/Email) เพื่อให้ test เร็ว | ไม่ต้องต่อ DB จริง ใช้ `FakeDB` แทน |
| **TDD** | เขียน test ก่อน แล้วค่อยเขียนโค้ดให้ผ่าน | เขียน `test_calculate_total` ก่อน แล้วค่อยเขียน `calculate_total` |
| **Coverage** | % ของโค้ดที่ถูก test รันผ่าน | 94% = มี 6% ที่ยังไม่มี test รัน |
| **Lint (ruff)** | โปรแกรมตรวจว่าโค้ดเขียนสวยไหม | `ruff check src/` บอกว่า import ไหนไม่ได้ใช้ |
| **GitHub Actions (CI)** | หุ่นยนต์ใน GitHub ที่รัน test อัตโนมัติทุกครั้งที่ push | push แล้ว Actions รัน `pytest` ให้ ไม่ต้องรันเอง |
| **Branch** | กิ่งของโค้ด — ทำแล็บในกิ่ง `feature/lab9-testing` ไม่ยุ่งกับ `main` | `git checkout -b feature/lab9-testing` |

---

## 1. ทำไมต้องทำแล็บนี้

**เรื่องจริง:**
- **Knight Capital (2012)** — test ไม่ครอบคลุม boundary → ขาดทุน **440 ล้านดอลลาร์ใน 45 นาที** → บริษัทเจ๊ง
- **Therac-25 (1985)** — มีแต่ Unit Test ไม่มี Integration Test → คนไข้เสียชีวิต 6 คน
- **Mars Climate Orbiter (1999)** — test แต่ละทีมผ่านหมด แต่ไม่เคย test รวมกัน → ยาน 125 ล้านดอลลาร์ระเบิด

**บทเรียน:** test ที่ "ผ่าน" ไม่พอ ต้อง **ครอบคลุม** และ **หลายระดับ**

| ถ้าไม่ทำแล็บนี้ | ถ้าทำแล็บนี้ |
|---|---|
| เขียนแต่กรณีปกติ (happy path) → bug แอบอยู่ตรงขอบ (เช่น `promo` ยาว 5 vs 6) | เขียน boundary → bug ถูกจับก่อนถึงผู้ใช้ |
| ต้องต่อ DB จริงทุกครั้งที่ test → ช้า 5 วินาที/test | ใช้ FakeDB → เร็ว 0.01 วินาที/test |
| Coverage 100% แต่ไม่รู้ว่า test ดีไหม | ทำ Saboteur → รู้ว่า test จับ bug ได้จริง |

---

## 2. เตรียมเครื่องทีละขั้น (Windows)

> **ทำครั้งเดียว ใช้ได้ทั้งเทอม**

### 2.1 ติดตั้ง Python (ถ้ายังไม่มี)

1. เปิด https://www.python.org/downloads/ → Download Python 3.12
2. ตอนติดตั้ง ติ๊ก ✅ **Add python.exe to PATH** (สำคัญ!)
3. เสร็จแล้วเปิด **PowerShell** พิมพ์:

```powershell
python --version
# ต้องเห็น Python 3.12.x

pip --version
# ต้องเห็น pip 24.x
```

ถ้าขึ้น `ไม่พบคำสั่ง` → ปิด PowerShell แล้วเปิดใหม่

### 2.2 ติดตั้งเครื่องมือของ Lab09

เปิด PowerShell พิมพ์ทีละบรรทัด (รอจบก่อนพิมพ์บรรทัดถัดไป):

```powershell
pip install pytest pytest-cov ruff
```

ตรวจว่าติดตั้งสำเร็จ:

```powershell
pytest --version
# pytest 8.x.x

ruff --version
# ruff 0.x.x
```

### 2.3 เตรียม Git และ repo

```powershell
git --version
# git version 2.x

# clone repo ของทีม (ถ้ายังไม่ได้ clone)
git clone https://github.com/YOUR_TEAM/campus-eats.git
cd campus-eats

# ตรวจว่าอยู่ใน repo
git status
# On branch main
```

### 2.4 Post-quiz 9 (ต้องทำก่อน Lab)

ในคาบบรรยาย อาจารย์ให้ทำ **Post-quiz §9.7** มี 3 คำถาม reflection:

- **B1** — Coverage report: `pytest --cov` ได้เท่าไหร่ ส่วนไหนต่ำสุด
- **B2** — TDD plan: จะทำ function ไหนด้วย TDD
- **B3** — Testing culture: Sprint หน้าจะปรับอะไร 1 อย่าง

> **ถ้ายังไม่ได้ทำ:** ใช้ 15 นาทีแรกของ Lab ทำก่อน — คำตอบจะถูกใช้ในขั้น 2

**ตัวอย่างคำตอบที่ดี:** ดู `labs/guides/Post-quiz-9-Example.md` และ `labs/examples/lab09-sample-solution/reflect.md`

---

## 3. ภาพรวม 5 ขั้น (2 ชั่วโมง)

| ขั้น | เวลา | ทำอะไร (ภาษาบ้านๆ) | ได้อะไร |
|---|---|---|---|
| 1 | 20 นาที | เปิด `tests/` ดูว่า test เดิมเป็นระดับไหน (Unit/Integration/E2E) | รู้ว่าทีมขาด test แบบไหน |
| 2 | 30 นาที | **TDD** — เขียน test ก่อน แล้วค่อยเขียนโค้ดให้ผ่าน (3 commits) | 1 function ใหม่ + ประวัติ Red-Green-Refactor |
| 3 | 30 นาที | **Test Doubles** — ใช้ตัวปลอมแทน DB/Email | 1 Stub/Mock/Fake |
| 4 | 20 นาที | **Coverage + Lint** — วัดว่า test พอไหม + ตรวจโค้ดสวยไหม + ใส่ CI | report + GitHub Actions เขียว |
| 5 | 10 นาที | **Saboteur** — แกล้งทำโค้ดให้ผิด ดูว่า test จับได้ไหม | พิสูจน์ว่า test ดีจริง |
| **ส่งงาน** | 10 นาที | Push + เปิด PR | merge `reflect.md` |

**โฟลเดอร์ตัวอย่างที่ทำตามได้:** 
- Starter (มี TODO): `labs/examples/lab09-sample-starter/`
- Solution (เฉลย): `labs/examples/lab09-sample-solution/` — รัน `pytest --cov -v` ได้ 13 passed 94%

---

## ขั้น 1: Testing Pyramid — แยก test 3 ระดับ (20 นาที)

### คืออะไร

Pyramid คือ **พีระมิด** — ฐานกว้าง (Unit เยอะ) ยอดแหลม (E2E น้อย) เพราะ Unit เร็ว ถูก ดูแลง่าย ส่วน E2E ช้า แพง พังง่าย

```
        /\
       /  \      E2E 10%  (น้อย ช้า แพง — เปิด browser จริง)
      /----\
     /      \    Integration 20% (ปานกลาง — ต่อ API+DB)
    /--------\
   /          \  Unit 70% (มาก เร็ว ถูก — test ฟังก์ชันเดียว)
```

### ทำอย่างไร (ทีละคลิก)

**1. สร้าง branch ใหม่ (กิ่งใหม่ ไม่ยุ่งกับ main):**

```powershell
git checkout -b feature/lab9-testing
# Switched to a new branch 'feature/lab9-testing'
```

**2. เปิดโฟลเดอร์ `tests/` ดูว่ามีไฟล์อะไรบ้าง:**

```powershell
dir tests
# test_calc.py
# test_api.py
# test_e2e.py  ← ถ้ามี
```

**3. เปิดแต่ละไฟล์แล้วถาม 3 คำถาม:**

| คำถาม | ถ้าตอบ "ใช่" → ระดับ |
|---|---|
| test ฟังก์ชันเดียว ไม่ต้องต่อ DB/API? | **Unit** |
| test ต้องต่อ DB หรือเรียก API? | **Integration** |
| test เปิด browser/app แล้วคลิกเหมือนผู้ใช้? | **E2E** |

**ตัวอย่าง:**

```
tests/test_calc.py::test_vip_discount  → Unit (เรียก calculate_discount อย่างเดียว)
tests/test_api.py::test_create_order   → Integration (เรียก API → บันทึก DB)
tests/test_e2e.py::test_login_flow     → E2E (เปิด browser → พิมพ์รหัส → กด login)
```

**4. นับแล้วเขียนลง `docs/coverage-report.md` (สร้างไฟล์ใหม่ถ้ายังไม่มี):**

```markdown
# Coverage Report — Lab09

## Pyramid Assessment (ขั้น 1)
- Unit: 8 tests (40%) — ต้องเพิ่ม (ควร 70%)
- Integration: 6 tests (30%)
- E2E: 6 tests (30%) — เยอะไป ควรลด
- แผน: เพิ่ม Unit 5 tests ในขั้น 2-3
```

**5. บันทึก:**

```powershell
git add docs/coverage-report.md
git commit -m "docs: classify existing tests by pyramid level"
```

**ดูอย่างไรว่าสำเร็จ:** `git log --oneline` เห็น commit ใหม่ 1 อัน

---

## ขั้น 2: TDD — เขียน test ก่อน แล้วค่อยเขียนโค้ด (30 นาที)

### คืออะไร

**TDD = Test-Driven Development** — เขียน test ก่อน แล้วค่อยเขียนโค้ดให้ test ผ่าน แบ่งเป็น 3 สี:

```
🔴 Red    — เขียน test ที่ FAIL ก่อน (ยังไม่มีโค้ด) — สีแดง = ยังพัง
🟢 Green  — เขียนโค้ดน้อยที่สุดให้ PASS — สีเขียว = ผ่านแล้ว
🔵 Refactor — จัดโค้ดให้สวย โดย test ยังเขียว — ไม่เปลี่ยนผลลัพธ์ แค่สวยขึ้น
```

**ทำไมต้อง Red ก่อน?** — เพื่อพิสูจน์ว่า test จับ bug ได้จริง — ถ้าเขียนโค้ดก่อนแล้ว test ทีหลัง อาจเขียน test ที่ผ่านเพราะบังเอิญ (test ไม่ดีแต่ก็เขียว)

### ทำอย่างไร — ตัวอย่าง Campus Eats `calculate_total`

**เลือก function:** `calculate_total(amount, tax_rate)` — ฟังก์ชันรวมยอด + ภาษี — ยังไม่มีในโปรเจกต์ (ถ้ามีแล้ว เลือก function อื่นที่ยังไม่มี test)

#### 🔴 Red — เขียน test ก่อน (ต้อง FAIL)

**1. สร้างไฟล์ `tests/test_tdd.py` พิมพ์:**

```python
# tests/test_tdd.py
from src.calc import calculate_total  # ยังไม่มี function นี้ — ต้อง FAIL

def test_calculate_total_with_tax():
    assert calculate_total(100, 0.07) == 107.0

def test_calculate_total_no_tax():
    assert calculate_total(100, 0.0) == 100.0
```

**2. รัน — ต้อง FAIL (สีแดง):**

```powershell
pytest tests/test_tdd.py -v
```

**ต้องเห็น:**

```
FAILED tests/test_tdd.py::test_calculate_total_with_tax - ImportError: cannot import name 'calculate_total'
```

> ✅ นี่คือ **Red ที่ถูกต้อง** — FAIL เพราะยังไม่มีโค้ด — ถ้า PASS ตั้งแต่ตอนนี้แปลว่า test ผิด

**3. บันทึก Red:**

```powershell
git add tests/test_tdd.py
git commit -m "test: add calculate_total test [RED]"
```

#### 🟢 Green — เขียนโค้ดน้อยที่สุดให้ผ่าน

**4. เปิด `src/calc.py` เติม:**

```python
# src/calc.py
def calculate_total(amount: int, tax_rate: float) -> float:
    return amount * (1 + tax_rate)
```

> เขียนแค่นี้พอ — อย่าเพิ่งคิดเยอะ — ขอให้ test ผ่านก่อน

**5. รัน — ต้อง PASS (สีเขียว):**

```powershell
pytest tests/test_tdd.py -v
```

**ต้องเห็น:**

```
tests/test_tdd.py::test_calculate_total_with_tax PASSED
tests/test_tdd.py::test_calculate_total_no_tax PASSED
2 passed
```

> ✅ เขียวแล้ว — ดีใจได้ 1 วิ

**6. บันทึก Green:**

```powershell
git add src/calc.py
git commit -m "feat: minimal calculate_total [GREEN]"
```

#### 🔵 Refactor — จัดให้สวย (test ยังต้องเขียว)

**7. จัดโค้ด (ถ้าเดิมเขียน `amount + amount * tax_rate` → จัดเป็น `amount * (1 + tax_rate)`):**

```python
# ไม่เปลี่ยนผลลัพธ์ แค่กระชับขึ้น — ถ้าไม่มีอะไรให้จัด ข้ามขั้นนี้ได้
```

**8. รันอีกครั้ง — ต้องยัง PASS:**

```powershell
pytest tests/test_tdd.py -v
# 2 passed ✅ ยังเขียว — แปลว่า refactor ไม่ได้ทำพัง
```

**9. บันทึก Refactor:**

```powershell
git commit -m "refactor: simplify calculate_total" --allow-empty
# หรือถ้ามีแก้ไฟล์: git add src/calc.py && git commit -m "refactor: simplify calculate_total"
```

### ดูอย่างไรว่าสำเร็จ

พิมพ์:

```powershell
git log --oneline -3
```

**ต้องเห็น 3 บรรทัดแยกกัน:**

```
a1b2c3 refactor: simplify calculate_total
d4e5f6 feat: minimal calculate_total [GREEN]
g7h8i9 test: add calculate_total test [RED]
```

> ❌ ถ้าเห็น commit เดียวรวมทุกอย่าง → อาจารย์หักคะแนน TDD — ต้องแยก 3 commits

---

## ขั้น 3: Test Doubles — ตัวปลอมแทนของจริง (30 นาที)

### คืออะไร (อธิบายแบบบ้านๆ)

สมมติ function `send_welcome_email` ต้อง **ส่งอีเมลจริง** — ถ้า test ต้องส่งอีเมลจริงทุกครั้งจะช้าและต้องมีรหัสผ่าน → ใช้ **ตัวปลอม** แทน

| ตัวปลอม | ทำอะไร | เหมือนอะไรในชีวิตจริง |
|---|---|---|
| **Stub** | ตอบค่าตายตัวตามที่เราสั่ง | หุ่นโชว์เสื้อในร้าน — ยืนนิ่งๆ ให้ดู |
| **Mock** | จำว่าถูกเรียกไหม เรียกด้วยอะไร | กล้องวงจรปิด — บันทึกว่าใครเดินผ่าน |
| **Fake** | ทำงานได้จริงแต่แบบง่ายๆ | เงินปลอมที่ใช้ซ้อมนับ — นับได้แต่ใช้ซื้อของไม่ได้ |

### เลือกอย่างไร

| ถ้าต้องการ... | ใช้ |
|---|---|
| ควบคุมว่า dependency ตอบอะไร | **Stub** |
| ตรวจสอบว่า dependency ถูกเรียกตามคาดไหม | **Mock** |
| เก็บข้อมูลแบบง่ายแทน DB จริง | **Fake** |

### ตัวอย่าง 1: Stub — ตอบค่าตายตัว

```python
# tests/test_doubles.py

# Stub — เราสั่งให้ตอบ tier = "vip" เสมอ
def get_user_stub(user_id: int) -> dict:
    return {"id": user_id, "name": "Test", "tier": "vip"}

def test_with_stub():
    user = get_user_stub(1)  # ไม่ต้องต่อ DB จริง
    from src.calc import calculate_discount
    result = calculate_discount(1000, user["tier"], None)
    assert result == 150  # vip 15%
```

### ตัวอย่าง 2: Mock — ตรวจสอบว่าถูกเรียก

```python
from unittest.mock import Mock
from src.email_service import send_welcome_email

def test_send_email_mock():
    # สร้าง Mock — ตัวปลอมที่จำทุกอย่าง
    mock_service = Mock()
    mock_service.send.return_value = True  # สั่งให้ตอบ True

    # เรียก function ที่ต้อง test — ส่ง Mock เข้าไปแทนของจริง
    result = send_welcome_email("a@b.com", email_service=mock_service)

    assert result is True
    # ตรวจสอบว่า Mock ถูกเรียกตามคาด — นี่คือจุดต่างจาก Stub
    mock_service.send.assert_called_once_with(
        to="a@b.com", subject="Welcome to Campus Eats", body="Hello!"
    )
```

> ถ้า `assert_called_once_with` ผิด → test จะ FAIL บอกว่า "เรียกไม่ตรงที่คาด"

### ตัวอย่าง 3: Fake — DB ปลอมที่เก็บข้อมูลได้

```python
from src.store import FakeDB, User

def test_fake_db():
    db = FakeDB()  # ไม่ต้องต่อ Postgres จริง — เก็บในหน่วยความจำ
    user = User(id=1, name="Mint", tier="member")
    db.save(user)  # บันทึก

    fetched = db.get(1)
    assert fetched.name == "Mint"
    assert db.get(999) is None  # ไม่มี user นี้ → ได้ None
```

### บันทึก

```powershell
git add tests/test_doubles.py
git commit -m "test: add mock for email service (test doubles)"
```

> ⚠️ **อย่า Mock มากเกินไป** — ถ้า test มี Mock 5 ตัว อาจแปลว่า function รับ parameter เยอะเกิน — ควรแยก function ให้เล็กลง

---

## ขั้น 4: Coverage + Lint — วัดว่า test พอไหม (20 นาที)

### 4.1 Coverage คืออะไร

**Coverage = % ของโค้ดที่ถูก test รันผ่าน**

- **Line Coverage** — กี่บรรทัดที่ test รันผ่าน
- **Branch Coverage** — กี่ทางเลือก (`if/else`) ที่ test ครอบคลุม

> **100% ไม่ได้แปลว่าไม่มี bug** — แค่แปลว่า "ทุกบรรทัดถูก run" แต่ไม่ได้แปลว่า "ทุก behavior ถูกตรวจ"

### รัน Coverage

```powershell
pytest --cov=src --cov-branch --cov-report=term-missing -v
```

**ผลที่ควรเห็น (ตัวอย่างเฉลย):**

```
Name                   Stmts  Miss Branch BrPart  Cover
--------------------------------------------------------
src/calc.py               11      0      2      0   100%
src/email_service.py       6      2      0      0    67%  ← ต้องเพิ่ม test ตรงนี้
src/store.py              13      0      0      0   100%
--------------------------------------------------------
TOTAL                     30      2      2      0    94%
```

**อ่านอย่างไร:**

| คอลัมน์ | คืออะไร | ดูตรงไหน |
|---|---|---|
| Stmts | จำนวนบรรทัด | 11 บรรทัด |
| Miss | บรรทัดที่ยังไม่มี test รัน | 0 = ครบ, 2 = ขาด 2 บรรทัด |
| Branch | จำนวนทางเลือก `if/else` | 2 |
| Cover | % ที่ครอบคลุม | 100% ดี, 67% ต้องเพิ่ม |
| Missing | บรรทัดไหนที่ยังไม่ถูก test | `6-7` = บรรทัด 6-7 ยังไม่มี test |

### เขียน `docs/coverage-report.md`

สร้างไฟล์ `docs/coverage-report.md` (สร้างโฟลเดอร์ `docs` ถ้ายังไม่มี: `mkdir docs`) พิมพ์:

```markdown
# Coverage Report — Lab09

## Overall
- Line: 94% (30/32 บรรทัด)
- Branch: 80% (4/5 ทางเลือก)

## ต่ำสุด
- src/email_service.py — 67% (บรรทัด 6-7: error handling ยังไม่มี test)
- แผน: เพิ่ม test_send_email_failure ใน Sprint ถัดไป

## Pyramid Assessment (จากขั้น 1)
- Unit: 70% ✅
- Integration: 20% ✅
- E2E: 10% ✅
```

### 4.2 Lint — ตรวจว่าโค้ดสวยไหม

**Lint = ตรวจว่าโค้ดเขียนตามกติกาไหม** (เช่น import ไม่ได้ใช้, ตัวแปรไม่ได้ใช้)

```powershell
pip install ruff
ruff check src/
```

- ถ้าเห็น `All checks passed!` → สวยแล้ว ✅
- ถ้าเห็น `F401 'os' imported but unused` → ลบ `import os` บรรทัดนั้น

### 4.3 ใส่ CI — ให้หุ่นยนต์ตรวจอัตโนมัติ

**CI = ให้ GitHub รัน `ruff` + `pytest` อัตโนมัติทุกครั้งที่ push**

สร้างไฟล์ `.github/workflows/test.yml` (สร้างโฟลเดอร์ `.github/workflows` ถ้ายังไม่มี):

```yaml
name: Tests
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install ruff
      - run: ruff check src/       # ← รันก่อน test — ถ้า lint fail ไม่ต้องรัน test
  test:
    needs: lint                     # ← รอ lint ผ่านก่อนค่อยรัน test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov=src --cov-branch --cov-fail-under=60
```

**ตั้ง Branch Protection (บังคับให้ต้องเขียวก่อน merge):**

1. เปิด GitHub → repo ของทีม → Settings → Branches → Add rule
2. Branch name pattern: `main`
3. ติ๊ก ✅ **Require status checks to pass before merging**
4. เลือก `lint` และ `test`
5. Save

> ถ้าไม่ตั้ง → CI แค่ "บอก" แต่ไม่ "บังคับ" — PR ยัง merge ได้แม้ test แดง

---

## ขั้น 5: Saboteur — แกล้งทำโค้ดพังดูว่า test จับได้ไหม (10 นาที)

### คืออะไร

**Saboteur = สายลับที่แกล้งทำโค้ดให้ผิด** — แล้วดูว่า test จับได้ไหม — ถ้าจับไม่ได้ = test ไม่ดี

### ทำอย่างไร

**1. แก้โค้ดให้ผิดชั่วคราว:**

เปิด `src/calc.py`:

```python
# จาก:
if promo_code and len(promo_code) >= 6:
# เป็น:
if promo_code and len(promo_code) > 6:  # เปลี่ยน >= เป็น > (ผิด!)
```

**2. รัน test:**

```powershell
pytest -v
```

- ถ้า `test_boundary_promo_len_6_gets_discount` **FAIL** → test จับได้ ✅ ดี
- ถ้า **ทุก test ยัง PASS** → test ไม่ครอบคลุม boundary ❌ ต้องเพิ่ม test

**3. แก้กลับทันที:**

```powershell
git diff src/calc.py
# ดูว่าที่แก้คือบรรทัดไหน

git restore src/calc.py
# แก้กลับ

pytest -v
# ต้องกลับมาเขียวทั้งหมด 13 passed
```

**4. บันทึกใน `docs/coverage-report.md`:**

```markdown
## Saboteur Check
- Break: เปลี่ยน >= เป็น > ใน PROMO_MIN_LEN
- ผล: test_boundary_promo_len_6_gets_discount FAIL ✅ — test จับได้
- สรุป: boundary test ทำงานถูกต้อง
```

---

## 9. ส่งงาน

### Checklist ก่อน Push (ติ๊กให้ครบ)

- [ ] `pytest -v` เขียวทั้งหมด (13 tests)
- [ ] `pytest --cov` ≥ 60% (หรือตามที่ทีมตั้ง)
- [ ] `ruff check src/` ไม่มี error (All checks passed!)
- [ ] `git log --oneline` เห็น 3 commits แยก (Red/Green/Refactor)
- [ ] `docs/coverage-report.md` มีตัวเลข + วิเคราะห์ + Pyramid + Saboteur
- [ ] `reflect.md` merge มาจาก `feature/post-quiz-9` (ดู `labs/guides/Post-quiz-9-Example.md`)

### คำสั่งส่ง

```powershell
git add tests/ src/calc.py docs/coverage-report.md reflect.md
git commit -m "test: lab09 TDD + doubles + coverage"
git push -u origin feature/lab9-testing
```

**เปิด PR ใน GitHub:**

1. เปิด GitHub → repo → Pull requests → New pull request
2. base: `main` ← compare: `feature/lab9-testing`
3. Title: `Lab09: Testing Pyramid + TDD + Doubles`
4. Description: วาง Actions badge + สรุปว่าเพิ่ม test อะไร
5. Create pull request → รอ Actions เขียว ✅ → ขอ review → Merge

---

## 10. แก้ปัญหาเมื่อติด

### PowerShell โดยเฉพาะ (Windows)

| อาการ | สาเหตุ | วิธีแก้ |
|---|---|---|
| `python : The term 'python' is not recognized` | Python ไม่อยู่ใน PATH | ปิด PowerShell แล้วเปิดใหม่ / ติ๊ก Add to PATH ตอนติดตั้ง |
| `pip : The term 'pip' is not recognized` | เหมือนข้างบน | เหมือนข้างบน |
| `ModuleNotFoundError: No module named 'src'` | รัน `python tests/test_unit.py` โดยตรง | **ต้องรัน `pytest` จากโฟลเดอร์ `lab09-sample`** ไม่ใช่ `python tests/test_unit.py` |
| `pytest: command not found` | ยังไม่ติดตั้ง | `pip install pytest pytest-cov` |
| `ruff: command not found` | ยังไม่ติดตั้ง | `pip install ruff` |
| `git : The term 'git' is not recognized` | ยังไม่ติดตั้ง Git | ติดตั้งจาก https://git-scm.com/download/win |

### Lab09 โดยเฉพาะ

| อาการ | สาเหตุ | วิธีแก้ |
|---|---|---|
| `FAILED test_with_stub` | logic `PROMO_MIN_LEN` ผิด | เปิด `src/calc.py` ดูว่า `>= 6` ถูกไหม |
| `coverage 45%` | test น้อย | เพิ่ม boundary tests (ยาว 5 vs 6, total 0) |
| `Mock.assert_called_once FAILED` | argument ไม่ตรง | เช็คว่า `to=`, `subject=` ตรงกับที่ Mock คาดไหม — เปิด `test_doubles.py` เทียบกับ `email_service.py` |
| `Actions แดง` | lint หรือ test fail | คลิกแท็บ **Actions** → คลิก job ที่แดง → ดู log ว่าบรรทัดไหน fail — แก้แล้ว push ใหม่ |
| `Branch protection ไม่ทำงาน` | ยังไม่ตั้ง | Settings → Branches → Require status checks → เลือก `lint` + `test` |
| `git push ถูก reject` | branch เก่า | `git pull --rebase origin main` แล้ว `git push` ใหม่ |

### คำถามที่พบบ่อย

**Q: ต้อง Mock ทุก test ไหม?**
A: ไม่ — Mock เฉพาะเมื่อพึ่งของภายนอก (DB/API/Email) — ถ้าเป็น pure function (เช่น `calculate_discount`) ไม่ต้อง Mock ใช้ Stub ก็พอ

**Q: Coverage ต้อง 100% ไหม?**
A: ไม่ — เป้า Lab09 คือ ≥ 60% — 100% ไม่ได้แปลว่าไม่มี bug (ดู Therac-25 — test ผ่านหมดแต่คนตาย)

**Q: TDD ต้องทำทุก function ไหม?**
A: ทำ 1 function ใน Lab09 พอ — แต่ Sprint ถัดไปควรทำทุก feature ใหม่ด้วย TDD จะได้ไม่ต้องมาแก้ทีหลัง

**Q: รัน `pytest` แล้วขึ้น `13 passed in 0.23s` คืออะไร?**
A: คือ test 13 ตัวผ่านหมดใน 0.23 วินาที — ถ้าเห็น `FAILED` แปลว่ามี test ไม่ผ่าน ต้องแก้

**Q: ทำไมต้อง commit แยก 3 ครั้ง?**
A: เพื่อให้เห็นว่า TDD ทำทีละขั้น — อาจารย์ดู `git log` แล้วรู้ว่าเข้าใจ Red-Green-Refactor — ถ้ารวม commit เดียวจะหักคะแนน

---

## 11. ตัวอย่างที่รันได้

| โฟลเดอร์ | สำหรับใคร | วิธีรัน | ผลที่ควรเห็น |
|---|---|---|---|
| `labs/examples/lab09-sample-starter/` | **นิสิต** (มี TODO) | `pytest -v` → **FAIL** ต้องเติมเอง | `FAILED` ตอนแรก |
| `labs/examples/lab09-sample-solution/` | **เฉลย** | `pytest --cov -v` → **PASS** | `13 passed, 94%` |

```powershell
# ลองรันเฉลย (ต้องอยู่โฟลเดอร์ lab09-sample-solution)
cd labs/examples/lab09-sample-solution
pip install -r requirements.txt
pytest --cov=src --cov-branch -v
```

**ผลที่ควรเห็น:**

```
tests/test_doubles.py::test_with_stub PASSED
tests/test_doubles.py::test_send_email_mock PASSED
tests/test_doubles.py::test_fake_db PASSED
tests/test_tdd.py::test_calculate_total_with_tax PASSED
tests/test_tdd.py::test_calculate_total_no_tax PASSED
tests/test_tdd.py::test_calculate_total_zero_amount PASSED
tests/test_unit.py::test_vip_gets_15_percent PASSED
...
TOTAL 30 2 2 0 94%
13 passed in 0.23s
```

---

## 12. เชื่อมโยงบทเรียน

| แนวคิดใน Lab09 | ใช้ต่อที่ไหนในวิชานี้ |
|---|---|
| Testing Pyramid 70/20/10 | ใช้ตัดสินใจทุก Sprint ว่าจะเขียน test ระดับไหน |
| Test Doubles (Stub/Mock/Fake) | ใช้ isolate DB/API ทุกครั้งที่ test |
| TDD Red-Green-Refactor | ใช้กับทุก feature ใหม่ — เขียน test ก่อนเสมอ |
| Coverage + Branch | ใช้ดูว่า test ครอบคลุมจริงไหม — ไม่ใช่แค่เลข |
| CI fail-fast (lint ก่อน test) | ใช้ทุก PR — ให้หุ่นยนต์ตรวจก่อนคนตรวจ |
| Saboteur | ใช้ก่อน release ทุก Sprint — พิสูจน์ว่า test ดีจริง |

---

*คู่มือนี้จัดทำโดย: ธรรมรัตน์ ธรรมา · สาขาวิทยาการคอมพิวเตอร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา · ภาคเรียนที่ 1 ปีการศึกษา 2569 · สอดคล้องกับบทที่ 9 (Testing) และ Lab09 — เวอร์ชันสำหรับผู้เริ่มต้น ไม่มีพื้นฐานมาก่อน*
