# บทที่ 9
# การทดสอบซอฟต์แวร์ (สัปดาห์ที่ 9)

> *\"Program testing can be used to show the presence of bugs, but never to show their absence.\"*
> — Edsger W. Dijkstra

---

## 9.0 บทนำ — โค้ดที่ไม่มี test คือโค้ดที่ "อาจจะ" ทำงาน ไม่ใช่โค้ดที่ "ทำงาน"

> *\"สัปดาห์ที่ 7 สอนว่าโค้ดต้องอ่านได้ สัปดาห์นี้สอนว่าโค้ดต้อง **พิสูจน์ได้** ว่าทำงานจริง\"*

หลังสอบกลางภาค เราเข้าสู่ครึ่งหลังของรายวิชา — ครึ่งที่เน้น **คุณภาพ** ของซอฟต์แวร์ที่ส่งมอบ บทที่ 9 เริ่มต้นด้วยการทดสอบ เพราะไม่มีอะไรอื่นจะพิสูจน์ว่าโค้ดทำงานจริง ถ้าไม่มีการทดสอบ

ทำไม "ทำงานจริง" ถึงสำคัญ? เพราะความเสียหายจาก bug ที่ "ไม่รู้ตัว" มหาศาล — Knight Capital 440 ล้านดอลลาร์, Boeing 346 คน, NHS 10 พันล้านปอนด์ (อ้างจากบทก่อนหน้า) ไม่ใช่ bug ที่ "ไม่มีใครเขียน test" แต่เป็น bug ที่ "เขียน test แต่ครอบคลุมไม่ถึง" หรือ "ไม่ได้เขียน test เลย" — เพราะถ้าเขียน test ครอบคลุมจริง bug ส่วนใหญ่จะถูกจับได้ก่อน production

### เรื่องจริงที่สอนเรื่อง "ทดสอบจริง"

**1) Knight Capital (2012) — test ไม่ครอบคลุม edge case**

Knight Capital มี test suite ที่ "ผ่าน" ทั้งหมด — แต่ flag ที่ "ตาย" มา 8 ปี ไม่ได้อยู่ใน test case ใด เลย ผ่านไป deploy จริง — ขาดทุน 440 ล้านดอลลาร์ใน 45 นาที บทเรียน: **test ที่ "pass" ไม่ได้แปลว่า "ครอบคลุม"** — ต้องคิดว่า test นี้ครอบคลุม edge case อะไรบ้าง (ดู 9.4)

**2) Therac-25 (1985–1987) — unit test ไม่จับ race condition**

ทีม Therac-25 เขียน unit test ทดสอบแต่ละฟังก์ชัน — ทุก function ผ่าน — แต่ race condition ระหว่าง thread ตอน run พร้อมกัน ไม่มี test ไหนจับได้ เพราะ test รันฟังก์ชันทีละตัว ไม่เคยรันพร้อมกัน ผู้ป่วย 6 คนเสียชีวิต บทเรียน: **unit test อย่างเดียวไม่พอ** ต้องมี integration test + system test ด้วย (ดู 9.3 Testing Pyramid)

**3) Apple "goto fail" (2014) — test ที่ผ่านแต่ไม่ได้ทดสอบ logic หลัก**

Apple มี unit test สำหรับ SSL/TLS ที่ "pass" ทั้งหมด — แต่ test ไม่ได้ครอบคลุม "ถ้า function return error จะต้องไม่ดำเนินการต่อ" — bug `goto fail;` ทำให้ SSL verification ถูก skip ผู้เชี่ยวชาญ google เห็นโค้ดภายในไม่กี่ชั่วโมง แต่ test ที่ Apple มี ไม่เคยจับได้ บทเรียน: **test ต้องครอบคลุม behavior ไม่ใช่แค่ function call** (ดู 9.4)

**4) NASA Mars Climate Orbiter (1999) — integration test ที่ขาดหาย**

NASA ส่งยานไปดาวอังคาร มูลค่า 327 ล้านดอลลาร์ — พังเพราะ software ฝั่งหนึ่งใช้หน่วยเมตริก อีกฝั่งใช้หน่วยอังกฤษ ทั้งสองทีมเขียน unit test ของตัวเอง ผ่านหมด — แต่ไม่มี **integration test** ที่รันทั้งสองระบบเข้าด้วยกัน บทเรียน: **unit test อย่างเดียวไม่พอ** ต้องมี integration test (ดู 9.3)

**5) Google "Testing on the Toilet" — culture ของการ test**

Google มี culture ที่ทุกคน test — มีการ์ตูนเรื่อง "Testing on the Toilet" ติดในห้องน้ำ เตือนให้คนเขียน test ทุกครั้งที่เขียนโค้ด ผลลัพธ์: Google มี codebase หลายพันล้านบรรทัด แต่ deploy production ได้หลายพันครั้งต่อวัน เพราะ test suite ครอบคลุมทุกการเปลี่ยนแปลง บทเรียน: **testing เป็น culture ไม่ใช่ task** (ดู 9.6)

> **Pattern**: ทั้งห้าเคสสอนเรื่องเดียวกัน — **test ที่ดีต้องครอบคลุม ไม่ใช่แค่ผ่าน** · **test ต้องหลายระดับ** (unit + integration + system) · **testing เป็น culture ไม่ใช่ event**

> *แหล่งอ้างอิงที่ตรวจสอบได้:*
> - Knight Capital: [Bloomberg, 2 Aug 2012](https://www.bloomberg.com/news/articles/2012-08-02/knight-capital-s-trading-fiasco-cost-440-million-in-45-minutes)
> - Therac-25: [Leveson & Turner, CACM 1993](https://cacm.acm.org/research/the-therac-25-incident/)
> - Apple goto fail: [Adam Langley, 2014](https://www.imperialviolet.org/2014/02/22/applebug.html)
> - Mars Climate Orbiter: [NASA, 1999](https://mars.jpl.nasa.gov/msp98/news/mco990930.html)
> - Google Testing: [Whittaker et al., 2012](https://testing.googleblog.com/)

### Mindset Shift

| เดิม | ใหม่ |
|---|---|
| Test = งานของ QA ทีมเดียว | Test = งานของทุกคนที่เขียนโค้ด (9.2) |
| เขียน test หลังโค้ดเสร็จ | เขียน test ก่อนโค้ด — TDD (9.5) |
| Test ผ่าน = พอแล้ว | Test ครอบคลุม = พอ (9.4 Coverage) |
| Unit test อย่างเดียวพอ | ต้องมีหลายระดับ — Testing Pyramid (9.3) |
| "Code coverage 100% = test ดี" | Coverage สูง ≠ test ดี — ต้องคิด behavior (9.4) |
| Bug = ความผิดของ programmer | Bug = โอกาสเรียนรู้กระบวนการ (9.7) |

### Roadmap ของคาบนี้

**9.1 แผนบริหารการสอน** — Post-quiz Pattern · **9.2 ทำไมต้อง Test (10 นาที)** — 5 เหตุผล + ROI · **9.3 Testing Pyramid (15 นาที)** — Unit + Integration + System · **9.4 Test Doubles (15 นาที)** — Stub + Mock + Fake · **9.5 TDD (20 นาที)** — Red-Green-Refactor · **9.6 Coverage + Static Analysis (10 นาที)** — วัดแต่ไม่จบ · **9.7 Post-quiz (15 นาที)** — 5 MCQ + 3 reflection (1.5%)

บทที่ 10 (Continuous Integration + Deployment) จะต่อยอดเรื่อง test อัตโนมัติเข้ากับ pipeline Lab 9 คือเขียน test ให้ครอบคลุม Lab 1–8 ที่ทีมส่งมา

**Prerequisites:** Lab 1–8 ที่ส่งแล้ว · Sprint Retrospective (บท 8) · Project codebase

**Self-check:** (1) ถ้าเพื่อนในทีมเขียน test แค่ happy path — เมื่อส่งงานจะเกิดอะไร (ตอบ: bug หลุดเข้า production เพราะ edge case ไม่ได้ทดสอบ) (2) ถ้า code coverage 100% แต่ไม่มี integration test — ระบบ Mars Climate Orbiter แบบนี้ไหม (ตอบ: ใช่ — unit test ผ่านแต่ระบบพังเพราะ integration ล้ม) (3) ถ้าทีมเขียน test แต่ไม่มีใครอ่าน — test มีประโยชน์ไหม (ตอบ: ไม่มาก — test ที่ไม่มีคนดูแล = dead test)

> **คำเตือนจากน้องวิจัย**: ถ้า test เป็นเรื่องของ "ทีม QA" ฝ่ายเดียว — เหมือนมีแมวจับหนูตัวเดียวในบ้านที่มีหนู 100 ตัว ต้องมีแมวทุกตัวช่วยกัน — ทุกคนเขียน test 🐾

---

## 9.1 แผนบริหารการสอนประจำบท

**ระยะเวลา**: 2 ชั่วโมง (บรรยาย) + 2 ชั่วโมง (ปฏิบัติการ) · **สัปดาห์ที่ 9**

### วัตถุประสงค์เชิงพฤติกรรม

เมื่อจบบทนี้ นิสิตสามารถ

1. อธิบายเหตุผลและ ROI ของการทดสอบ
2. แยกแยะ Unit / Integration / System Test
3. เลือกใช้ Test Doubles ที่เหมาะสม
4. เขียน test ตาม TDD (Red-Green-Refactor)
5. วัด Coverage อย่างมีความหมาย

### โครงสร้างการสอน (Post-quiz Pattern)

| เวลา | กิจกรรม | สื่อ |
|---|---|---|
| 0:15–0:25 | **9.2** ทำไมต้อง Test (10 นาที) | 5 เคส + ROI |
| 0:25–0:40 | **9.3** Testing Pyramid (15 นาที) | วาด pyramid |
| 0:40–0:55 | **9.4** Test Doubles (15 นาที) | ตัวอย่าง Stub + Mock |
| 0:55–1:15 | **9.5** TDD (20 นาที) | Live coding demo |
| 1:15–1:25 | **9.6** Coverage + Static (10 นาที) | Coverage report |
| 1:25–1:45 | **Workshop** เขียน test จริง (20 นาที) | Lab 9 setup |
| 1:45–2:00 | **Post-quiz** (5 MCQ + 3 reflection, 1.5%) | commit `reflect.md` |

### การวัดผล

| ส่วน | คะแนน |
|---|:---:|
| Post-quiz | 1.5% |
| Lab 9 (Test Coverage) | 3.5% |
| รวม | 5% |

---

## 9.2 ทำไมต้องทดสอบ

### 9.2.1 5 เหตุผลที่ต้อง Test

1. **ลดความเสียหายใน production** — bug ใน production แพงกว่า bug ตอน dev 10–100 เท่า
2. **ทำให้ refactor ได้อย่างปลอดภัย** — มี test ครอบคลุม = กล้าเปลี่ยน
3. **เป็นเอกสารที่ดีที่สุดของโค้ด** — test อธิบายว่าโค้ดทำอะไร
4. **ช่วยออกแบบ** — เขียน test ยาก = ออกแบบไม่ดี
5. **ลดเวลา debug** — เมื่อ test fail รู้ทันทีว่า bug อยู่ตรงไหน

### 9.2.2 ROI ของ Testing

Microsoft Research (2009) — "Better Testing = Lower Defect Rate" พบว่า:

- ทีมที่มี test coverage สูง ใช้เวลา fix bug น้อยกว่า 60%
- TDD ลด defect 40–90% (varies by study)
- แต่ TDD ใช้เวลาเขียน test + production code มากกว่า 15–35% ในตอนแรก
- **ระยะยาว** TDD ประหยัดเวลามากกว่า เพราะลด debug time

### 9.2.3 Testing Mindset

> *Test ที่ดีคือ test ที่ **ทำให้คุณกล้าเปลี่ยน** ไม่ใช่ test ที่ทำให้คุณกลัวจะเปลี่ยน*

ถ้า test ทำให้คุณกลัวจะ refactor — test นั้นไม่ดี เพราะมันผูกกับ implementation มากเกินไป (brittle test)

---

## 9.3 Testing Pyramid

Mike Cohn (2009) เสนนะ **Testing Pyramid** — แบ่ง test เป็น 3 ระดับ:

```
        /\
       /  \      E2E / UI Tests (น้อย, ช้า, แพง)
      /----\
     /      \    Integration Tests (ปานกลาง)
    /--------\
   /          \  Unit Tests (มาก, เร็ว, ถูก)
  /____________\
```

### 9.3.1 Unit Test

**ทดสอบ**: ฟังก์ชัน/เมธอดเดียว แยกจากส่วนอื่น  
**ความเร็ว**: เร็วมาก (< 1 ms ต่อ test)  
**ขอบเขต**: แคบมาก  
**ตัวอย่าง**: `calculate_discount(price, rate) → 90.0`

```python
def test_calculate_discount_with_10_percent():
    assert calculate_discount(100, 0.10) == 90.0
```

### 9.3.2 Integration Test

**ทดสอบ**: หลาย component ทำงานร่วมกัน  
**ความเร็ว**: ปานกลาง (100 ms – 1 s ต่อ test)  
**ขอบเขต**: กว้างกว่า  
**ตัวอย่าง**: API → Service → DB → Response

### 9.3.3 System / E2E Test

**ทดสอบ**: ระบบทั้งหมด รวม UI, API, DB, external services  
**ความเร็ว**: ช้า (วินาที – นาทีต่อ test)  
**ขอบเขต**: กว้างที่สุด  
**ตัวอย่าง**: เปิด browser, login, คลิก, ตรวจผล

### 9.3.4 กฎ 70-20-10

แนะนำให้เขียน test ในสัดส่วน:
- **70%** Unit Test
- **20%** Integration Test
- **10%** E2E Test

**เหตุผล**: Unit test เร็ว ถูก ดูแลง่าย · E2E test ช้า แพง ดูแลยาก (brittle)

---

## 9.4 Test Doubles

เมื่อ unit test ต้องทดสอบ logic ที่ต้องพึ่ง external system (DB, API, file) — เราใช้ **Test Doubles** ทดแทน

### 9.4.1 ประเภท (Gerard Meszaros, 2007)

| ประเภท | คำอธิบาย | เมื่อใช้ |
|---|---|---|
| **Dummy** | object ที่ส่งผ่าน แต่ไม่ถูกใช้ | เติม parameter list |
| **Stub** | object ที่ return ค่าตายตัว | เมื่อต้องการ control response |
| **Mock** | object ที่ verify ว่าถูกเรียกตามที่คาดหวัง | เมื่อต้องการ verify behavior |
| **Fake** | object ที่มี implementation จริงแต่เรียบง่าย | เช่น in-memory database |
| **Spy** | object ที่บันทึกการเรียก | ตรวจสอบหลังการ call |

### 9.4.2 ตัวอย่าง

```python
# Stub — return ค่าตามที่กำหนด
def get_user_stub(user_id):
    return {"name": "Test User", "email": "test@test.com"}

# Mock — verify ว่าถูกเรียก
mock_email_service.verify_called_with(
    to="user@test.com",
    subject="Welcome"
)

# Fake — in-memory implementation
class FakeDatabase:
    def __init__(self):
        self.users = {}
    
    def save(self, user):
        self.users[user.id] = user
```

### 9.4.3 เลือกใช้อย่างไร

**Stub** เมื่อ: ทดสอบว่า logic ทำงานถูกเมื่อได้รับ input  
**Mock** เมื่อ: ทดสอบว่า logic เรียก external service ตามที่คาดหวัง  
**Fake** เมื่อ: ต้องการ stateful object (เช่น in-memory DB) แทนของจริง

**ข้อควรระวัง**: อย่าใช้ Mock มากเกินไป — จะทำให้ test ผูกกับ implementation เปลี่ยน implementation = test พัง

---

## 9.5 Test-Driven Development (TDD)

### 9.5.1 Red-Green-Refactor

Kent Beck (2003) เสนอ TDD เป็น 3 ขั้น:

1. **🔴 Red** — เขียน test ที่ fail ก่อน (test สำหรับ behavior ที่ยังไม่มี)
2. **🟢 Green** — เขียน production code น้อยที่สุดที่ทำให้ test ผ่าน
3. **🔵 Refactor** — ปรับปรุง code โดยไม่เปลี่ยน behavior (test ยัง pass)

ทำซ้ำในรอบสั้น ๆ (5–10 นาทีต่อ cycle) — เมื่อจบ Sprint จะมี test ครอบคลุม + production code ที่ทำงาน

### 9.5.2 ตัวอย่าง

**🔴 Red**:
```python
def test_calculate_total_with_tax():
    assert calculate_total(100, 0.07) == 107.0  # FAIL — function not defined
```

**🟢 Green**:
```python
def calculate_total(amount, tax_rate):
    return amount + (amount * tax_rate)  # ผ่าน
```

**🔵 Refactor**:
```python
def calculate_total(amount, tax_rate):
    return amount * (1 + tax_rate)  # กระชับขึ้น
```

### 9.5.3 TDD ทำให้ Design ดีขึ้น

> *ถ้า test เขียนยาก — design ไม่ดี*

ถ้าต้อง mock 5 object ก่อน test function — function นั้นผูกกับของอื่นมากเกินไป ควร refactor

### 9.5.4 Limitations

TDD ไม่ได้จับทุก bug:
- Bug ที่ต้องดู design — จับได้ยากด้วย test
- Bug ที่เกิดจาก integration — ต้อง integration test
- Bug ที่ user ไม่ชอบ — ต้อง user testing

**TDD คือ เครื่องมือ** ไม่ใช่ **คำตอบสุดท้าย**

---

## 9.6 Coverage และ Static Analysis

### 9.6.1 Code Coverage

**Code Coverage** คือ % ของบรรทัดโค้ดที่ถูกทดสอบ

```bash
pytest --cov=myapp
# myapp/module.py    85%   12-15, 23
```

**ความเข้าใจผิด**: "100% coverage = ไม่มี bug" — **ผิด** Coverage 100% หมายความว่า "ทุกบรรทัดถูก run" ไม่ได้หมายความว่า "ทุก behavior ถูกต้อง"

### 9.6.2 Branch Coverage

ครอบคลุม "ทุกทางเลือก" ไม่ใช่แค่ "ทุกบรรทัด":

```python
if user.is_admin:        # branch 1: True
    show_admin_panel()
else:                    # branch 2: False
    show_user_panel()
```

Line coverage = 100% เมื่อ test ทั้ง 2 case · แต่ถ้า test แค่ case แรก = line coverage 100% แต่ branch coverage 50%

### 9.6.3 แนวทาง Coverage

- **70%+** เป็นเป้าหมายที่ดี
- **90%+** สำหรับ critical code (payment, security)
- **100%** อาจไม่คุ้ม — test infrastructure code อาจไม่จำเป็น

### 9.6.4 Static Analysis

**Static Analysis** คือการวิเคราะห์โค้ดโดยไม่รัน (lint):

```bash
pylint myapp/
mypy myapp/
```

ช่วยจับ:
- Bug ที่ compiler ไม่จับ (เช่น undefined variable)
- Code smell (long function, duplicate code)
- Security issue (SQL injection pattern)

---

## 9.7 Post-quiz (ท้ายคาบ 1:45–2:00, 1.5%)

### Section A: เลือกคำตอบที่ถูกต้องที่สุด (5 ข้อ × 0.3 = 1.5 คะแนน)

**A1.** Mike Cohn Testing Pyramid แนะนำสัดส่วน test อย่างไร
- A) 90% Unit, 5% Integration, 5% E2E
- B) 70% Unit, 20% Integration, 10% E2E
- C) 33% เท่ากันทุกระดับ
- D) 50% Unit, 30% Integration, 20% E2E

**A2.** Test Double ประเภทใดที่ "verify ว่าถูกเรียกตามที่คาดหวัง"
- A) Stub
- B) Fake
- C) Mock
- D) Dummy

**A3.** TDD มี 3 ขั้นคือ
- A) Plan-Code-Test
- B) Red-Green-Refactor
- C) Write-Test-Debug
- D) Build-Run-Fix

**A4.** "Code Coverage 100%" หมายความว่า
- A) ทุกบรรทัดถูก run ใน test
- B) ไม่มี bug
- C) Test ครอบคลุมทุก behavior
- D) Test ผ่านทั้งหมด

**A5.** เหตุผลสำคัญที่สุดที่ต้องเขียน test คือ
- A) เพราะอาจารย์สั่ง
- B) ทำให้ refactor ได้อย่างปลอดภัย — มี test ครอบคลุม = กล้าเปลี่ยน
- C) ทำให้โค้ดช้าลง
- D) ทำให้ลูกค้าชอบ

### เฉลย

- **A1. B** — 70/20/10
- **A2. C** — Mock
- **A3. B** — Red-Green-Refactor
- **A4. A** — ทุกบรรทัดถูก run ใน test
- **A5. B** — Refactor ได้อย่างปลอดภัย

### Section B: Reflection (ไม่นับคะแนน — เขียนหลังทำ Lab09 เสร็จ)

> **เมื่อไหร่ทำ:** หลังทำ Lab09 ทั้ง 5 ขั้นเสร็จแล้ว — เปิด `reflect.md` แล้วเขียนสะท้อนสิ่งที่เพิ่งทำ (ดูตัวอย่างที่ `labs/guides/Post-quiz-9-Example.md` และ `labs/examples/lab09-sample-solution/reflect.md`)

**B1. Apply — Coverage Report (2–3 ประโยค + ตัวเลข)**

ทำอย่างไร (หลัง Lab ขั้น 4 เสร็จ):
1. เปิด PowerShell ที่โฟลเดอร์โปรเจกต์ (โฟลเดอร์ที่มี `src/` และ `tests/`)
2. พิมพ์: `pytest --cov=src --cov-branch --cov-report=term-missing -v` แล้วกด Enter
3. ดูบรรทัดสุดท้าย — จะเห็นตาราง `TOTAL ... 68%` — นั่นคือ coverage หลังทำ Lab
4. ดูคอลัมน์ `Missing` — บรรทัดไหนที่ยังไม่มี test

เขียนตอบ 3 อย่าง (สะท้อนหลังทำ Lab):
- **ตัวเลข:** หลังทำ Lab ได้ Overall เท่าไหร่ (เช่น 68% line / 55% branch) — เทียบกับก่อนทำ Lab เพิ่มขึ้นไหม
- **ต่ำสุด:** ไฟล์/ฟังก์ชันไหนต่ำสุด (เช่น `src/payment.py:42` → 42% — `handle_payment_error` ไม่มี test)
- **แผน:** หลัง Lab จะเพิ่ม test อะไรต่อ (เช่น `test_payment_failure_returns_retry` + branch `if promo is None`)

ตัวอย่างที่ดี / ไม่ดี: ดู `labs/guides/Post-quiz-9-Example.md` หัวข้อ B1

**B2. Connect — TDD (3–4 ประโยค — เขียนหลังทำ Lab ขั้น 2 เสร็จ)**

เลือก **1 function จริง** ที่เพิ่งทำ TDD ใน Lab ขั้น 2 (เช่น `calculate_total`, `calculate_discount`, `validate_email`):

เขียนตอบ 3 อย่าง (สะท้อนหลังทำ):
- **เลือก function ไหน:** ชื่อ + ไฟล์ที่เพิ่งทำ TDD (เช่น `calculate_total` ใน `src/calc.py`)
- **เขียน test ก่อน code แล้ว design เปลี่ยนไหม:** เช่น `promo_code` ควรเป็น `str | None` ไม่ใช่ `str` เปล่าๆ, ควรแยก `PROMO_MIN_LEN` เป็น constant เพื่อให้ test boundary ได้ง่าย
- **ดีขึ้น / แย่ลง (หลังทำจริง):** ดีขึ้น = API ชัด, แยก pure logic ทำให้ test เร็ว / แย่ลง = ใช้เวลาเพิ่ม 15 นาทีช่วงแรกแต่ลด debug ทีหลัง

ตัวอย่างที่ดี / ไม่ดี: ดู `labs/guides/Post-quiz-9-Example.md` หัวข้อ B2

**B3. Reflect — Testing Culture (1–2 ประโยค — เขียนหลังทำ Lab ทั้งหมดเสร็จ)**

หลังทำ Lab09 ทั้ง 5 ขั้นแล้ว ทีมจะปรับปรุง **1 อย่าง** ที่ทำได้จริงใน Sprint หน้า:

เขียนตอบ 2 อย่าง:
- **จะทำอะไร:** 1 อย่างชัด (เช่น `ทุก PR ต้องมี test ≥1 ตัวและต้องผ่าน CI ก่อน merge`)
- **บังคับอย่างไร:** มีวิธีบังคับ (เช่น ตั้ง Branch Protection ที่ `main` → Require status checks `lint` + `test`)

ตัวอย่างที่ดี: `Sprint หน้าทีมจะตั้งกฎว่า ทุก PR ต้องมี test ≥1 ตัวและผ่าน CI ก่อน merge โดยตั้ง Branch Protection ที่ main — เริ่มจาก calculate_discount แล้วขยายไปทุก feature`
ตัวอย่างที่ไม่ดี: `จะเขียน test ให้มากขึ้น` (ไม่บอกว่าทำอย่างไร)

> **เกณฑ์ที่อาจารย์ดู (Section B ไม่นับคะแนน แต่ต้องผ่าน — เขียนหลัง Lab):** B1 ต้องมีตัวเลขหลัง Lab + ระบุไฟล์ต่ำ + แผน / B2 ต้องเลือก function ที่เพิ่งทำ TDD + บอก design เปลี่ยน + ดี/แย่ / B3 ต้องระบุ 1 อย่าง + วิธีบังคับ — ถ้าไม่ครบจะให้แก้ก่อน merge PR

**ตัวอย่าง `reflect.md` ที่ส่งจริง (เขียนหลัง Lab):**

```markdown
# Post-quiz 9 — Reflection (เขียนหลังทำ Lab09)
**ชื่อ:** สมชาย ใจดี — **ทีม:** Campus Eats — **Sprint:** 9

## B1. Apply — Coverage Report (หลังทำ Lab)
รัน pytest --cov หลังทำ Lab ได้ Overall 68% line / 55% branch (ก่อนทำ 45%)
ต่ำสุดคือ src/payment.py ที่ 42% (handle_payment_error ไม่มี test)
หลัง Lab จะเพิ่ม test_payment_failure_returns_retry และ branch if promo is None ใน Sprint ถัดไป

## B2. Connect — TDD (หลังทำขั้น 2)
เลือก calculate_total(amount, tax_rate) ที่เพิ่งทำ TDD — เขียน test ก่อน
จะพบว่า promo_code ควรเป็น str | None และควรแยก PROMO_MIN_LEN เป็น constant
เพื่อให้ test boundary (5 vs 6) ได้ง่าย — ดีขึ้น: API ชัด, แยก pure logic ทำให้ test เร็ว
แย่ลง: ใช้เวลาเพิ่ม 15 นาทีช่วงแรก แต่ลด debug ทีหลัง

## B3. Reflect — Testing Culture (หลังทำ Lab)
หลังทำ Lab09 ทั้ง 5 ขั้น Sprint หน้าทีมจะตั้งกฎว่า ทุก PR ต้องมี test ≥1 ตัวและผ่าน CI ก่อน merge
โดยตั้ง Branch Protection ที่ main — เริ่มจาก calculate_total ที่เพิ่งทำ แล้วขยายไปทุก feature
```

### วิธีส่ง

1. ทำ Lab09 ทั้ง 5 ขั้นให้เสร็จก่อน
2. สร้าง branch `feature/post-quiz-9` (หรือใช้ branch เดียวกับ Lab `feature/lab9-testing`)
3. สร้าง `reflect.md` ที่ root (copy โครงข้างบนแล้วเติมคำตอบหลังทำ Lab)
4. Commit + push + เปิด PR (merge พร้อม Lab 9)

> **ดูตัวอย่างเต็ม:** `labs/guides/Post-quiz-9-Example.md` — มีตัวอย่างที่ดี/ไม่ดี + เกณฑ์ตรวจ

---

## 9.8 สรุปสาระสำคัญ

บทที่ 9 ครอบคลุมการทดสอบ:

- **ทำไมต้อง Test** — ลดความเสียหาย + refactor ได้อย่างปลอดภัย
- **Testing Pyramid** — 70% Unit, 20% Integration, 10% E2E
- **Test Doubles** — Stub + Mock + Fake
- **TDD** — Red-Green-Refactor ทำให้ design ดีขึ้น
- **Coverage** — วัดได้แต่ไม่ใช่คำตอบสุดท้าย

Knight Capital ล้มเพราะ test ไม่ครอบคลุม · Therac-25 ล้มเพราะไม่มี integration test · Mars Climate Orbiter 327 ล้านเพราะขาด integration test · ทั้งหมดสอนเรื่องเดียวกัน — **test ที่ดีต้องครอบคลุมและหลายระดับ**

แนวคิดเหล่านี้จะถูกใช้ในบทที่ 10 (CI/CD) ที่จะรัน test อัตโนมัติทุกครั้งที่ commit Lab 9 คือเขียน test ให้ครอบคลุม Lab 1–8 ของทีม

---

## 9.9 คำถามทบทวน

1. Testing Pyramid — ทำไมต้องมี Unit มากกว่า E2E
2. Test Doubles แต่ละประเภทต่างกันอย่างไร — เมื่อไหร่ใช้อะไร
3. TDD ช่วยเรื่อง design ได้อย่างไร
4. Code Coverage 100% ≠ ไม่มี bug — ยกตัวอย่าง
5. Testing เป็น "งานของ QA" ฝ่ายเดียว — ดีหรือไม่ ทำไม

---

## บรรณานุกรมเพิ่มเติมประจำบท

- Beck, K. (2003). *Test-Driven Development by Example*. Addison-Wesley.
- Meszaros, G. (2007). *xUnit Test Patterns*. Addison-Wesley.
- Fowler, M. (2012). *Patterns of Enterprise Application Architecture*. Addison-Wesley.
- Cohn, M. (2009). *Succeeding with Agile*. Addison-Wesley.
- Martin, R. C. (2008). *Clean Code*. Prentice Hall. Chapter 9.
- Whittaker, J., et al. (2012). *How Google Tests Software*. Addison-Wesley.
- Dijkstra, E. W. (1969). Notes on Structured Programming.

---

*จัดทำโดย: ธรรมรัตน์ ธรรมา · สาขาวิทยาการคอมพิวเตอร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา · ภาคเรียนที่ 1 ปีการศึกษา 2569*
