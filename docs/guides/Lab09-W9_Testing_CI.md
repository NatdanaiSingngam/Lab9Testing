# ใบงานปฏิบัติการ Lab 9
# Testing Pyramid + Test Doubles + TDD + Coverage

> **รายวิชา**: แนวคิดวิศวกรรมซอฟต์แวร์ · **รหัสวิชา**: 225311
> **สัปดาห์ที่ 9 · ภาคเรียนที่ 1 ปีการศึกษา 2569** 
> **เวลา**: 2 ชั่วโมง (ห้องปฏิบัติการ) · **คะแนน**: 3.5% ของคะแนนรวม
> **อาจารย์ผู้สอน**: ธรรมรัตน์ ธรรมา · สาขาวิทยาการคอมพิวเตอร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา
> **ส่งงานผ่าน**: GitHub Pull Request (tests/) + GitHub Actions CI · reflect.md จาก Post-quiz 9
>
> **📖 คู่มือละเอียด**: ดู `labs/guides/Lab09-Detailed-Guide.md` — อธิบายทีละขั้นพร้อมภาพ + วิธีแก้ปัญหา
> **📝 ตัวอย่าง Post-quiz 9**: ดู `labs/guides/Post-quiz-9-Example.md` — ตัวอย่าง B1/B2/B3 ที่ดี (พร้อม `reflect.md` ใน Solution)

---

## 1. วัตถุประสงค์เชิงพฤติกรรม (Behavioral Objectives)

เมื่อทำ Lab นี้เสร็จ นิสิตสามารถ

1. **แยกแยะ** Unit / Integration / System Test ตาม Testing Pyramid (70/20/10) และอธิบาย trade-off แต่ละระดับ
2. **เลือกใช้** Test Doubles (Stub / Mock / Fake) ได้เหมาะสมกับบริบท
3. **ประยุกต์ TDD** (Red-Green-Refactor) กับฟังก์ชันจริงในโปรเจกต์ — เริ่มจาก test → production code → refactor
4. **วัด Coverage** (line + branch) และตีความอย่างมีความหมาย — ไม่ใช่ "100% = ดี"
5. **รัน Static Analysis** (lint + type check) เป็นส่วนหนึ่งของ CI
6. **เปิดเผย** การใช้ AI ใน `AI_USAGE.md` (test generation + review)

**สอดคล้องกับ Learning Outcomes**: LO2, LO5, LO6

**อ้างอิงเนื้อหาบทเรียน**: บทที่ 9 — การทดสอบซอฟต์แวร์ (9.2 ทำไมต้อง Test · 9.3 Pyramid · 9.4 Test Doubles · 9.5 TDD · 9.6 Coverage/Static)

---

## 2. เนื้อหาที่ต้องอ่านก่อนทำ Lab (Pre-lab Reading)

กรุณาอ่านเนื้อหาก่อนเข้าห้องปฏิบัติการ (อ่านจาก slide deck ของบทที่ 9 หรือ PDF ตำรา):

- **[PP] Tip 67** — A Test Is the First User of Your Code
- **[PP] Tip 68** — Build End-to-End, Not Top-Down or Bottom-Up
- **[PP] Tip 69** — Design to Test
- **[PP] Tip 93** — Test State Coverage, Not Code Coverage
- **[ESP] Ch.9** — Software Testing · Testing Pyramid
- **[SE] Ch.8** — Software Testing (Test Doubles)
- **ทีมของคุณ's source code** — มี function ≥ 1 ตัวที่ test ได้ (เช่น `calculate_discount`, `apply_promo`, `validate_email`)

**คำถามนำก่อนทำ Lab** (ให้คิดมาก่อนเข้าคาบ):
- *function ไหนในโปรเจกต์ที่ "ทดสอบง่าย" และเป็น core business logic?*
- *โค้ดส่วนไหนต้องพึ่ง DB / API ภายนอก — จะใช้ Test Double แบบใด?*

---

## 3. เครื่องมือและบัญชีที่ต้องเตรียม (Materials & Tools)

| รายการ | รายละเอียด |
|---|---|
| **GitHub Account** | บัญชีส่วนตัว (ใช้ account เดียวกับ Lab 1–8) |
| **Team Repository** | มี source code + Dockerfile (จาก Sprint 2 + Lab 6) |
| **GitHub Actions** | ฟรีสำหรับ public repo · CI workflow ใน `.github/workflows/` |
| **Testing Framework** | Python: pytest + pytest-cov · Node.js: Jest · อื่น ๆ ตาม stack |
| **Static Analysis** | Python: ruff + mypy · Node.js: eslint + tsc |
| **AI Tool** | Copilot/ChatGPT/Claude — ใช้ generate test cases อย่างมีวินัย |
| **Post-quiz 9** | `reflect.md` จากคาบบรรยาย (Coverage report + TDD plan + Testing culture) |

---

## 4. สิ่งที่ต้องส่ง (Deliverables)

ส่งผ่าน **GitHub Pull Request + GitHub Actions** ภายในสิ้นสุด Lab (2 ชม.):

### 4.0 ตัวอย่างที่เห็นภาพ — Campus Eats (อ่านก่อนทำ Lab)

> **ตัวอย่างนี้คือสิ่งที่นิสิตต้องส่งในรูปแบบเดียวกัน — ดูแล้วทำตามได้ทันที**

**ฟังก์ชันจริงในโปรเจกต์:**

```python
# src/calc.py — ฟังก์ชันที่ทีม Campus Eats ใช้จริง
def calculate_discount(total: int, tier: str, promo_code: str | None) -> int:
    """คำนวณส่วนลด — tier: vip/member/first, promo_code: ถ้ามีและยาว ≥ 6 จะได้ 20%"""
    VIP_RATE, MEMBER_RATE, PROMO_RATE = 0.15, 0.10, 0.20
    PROMO_MIN_LEN = 6
    rate = {"vip": VIP_RATE, "member": MEMBER_RATE}.get(tier, 0.0)
    if promo_code and len(promo_code) >= PROMO_MIN_LEN:
        rate = max(rate, PROMO_RATE)
    return int(total * rate)

def calculate_total(amount: int, tax_rate: float) -> float:
    return amount * (1 + tax_rate)
```

**Unit Test แบบเห็นภาพ (AAA + Boundary):**

```python
# tests/test_unit.py — 5 tests ครอบคลุม Pyramid ระดับ Unit
def test_vip_gets_15_percent():
    # Arrange — เตรียม
    total, tier, code = 1000, "vip", None
    # Act — ทำ
    result = calculate_discount(total, tier, code)
    # Assert — ตรวจ
    assert result == 150  # 1000 * 0.15

def test_promo_overrides_member():
    assert calculate_discount(1000, "member", "PROMO88") == 200  # 20% > 10%

def test_boundary_promo_len_5_no_discount():
    assert calculate_discount(1000, "first", "ABCDE") == 0  # ยาว 5 < 6 ไม่ได้

def test_boundary_promo_len_6_gets_discount():
    assert calculate_discount(1000, "first", "ABCDEF") == 200  # ยาว 6 ได้

def test_zero_total():
    assert calculate_discount(0, "vip", "PROMO88") == 0
```

**Test Doubles แบบเห็นภาพ (Stub vs Mock vs Fake):**

```python
# Stub — ควบคุม response
def get_user_stub(user_id): return {"name": "Test", "tier": "vip"}
def test_with_stub():
    user = get_user_stub(1)
    assert calculate_discount(1000, user["tier"], None) == 150

# Mock — ตรวจสอบว่าถูกเรียก
def test_send_email_mock(mocker):
    mock = mocker.Mock()
    send_welcome_email("a@b.com", email_service=mock)
    mock.send.assert_called_once_with(to="a@b.com", subject="Welcome")

# Fake — in-memory DB แทนของจริง
class FakeDB:
    def __init__(self): self.users = {}
    def save(self, u): self.users[u.id] = u
    def get(self, uid): return self.users.get(uid)
```

**TDD แบบเห็นภาพ (3 commits):**

```
commit 1 [RED]    test: add calculate_total test — FAIL
commit 2 [GREEN]  feat: minimal calculate_total — PASS
commit 3 [REFACTOR] refactor: simplify to amount * (1 + rate) — PASS
```

**Coverage Report แบบเห็นภาพ:**

```
Name              Stmts  Miss Branch BrPart  Cover
---------------------------------------------------
src/calc.py           12      0      4      0   100%
src/email_service.py   8      2      2      1    75%  ← ต้องเพิ่ม test ตรง error handling
---------------------------------------------------
TOTAL                 20      2      6      1    90%
```

> **โฟลเดอร์ตัวอย่างที่รันได้:** 
> - Starter (ให้นิสิตทำ): `labs/examples/lab09-sample-starter/` — มี TODO ให้เติม
> - Solution (เฉลย): `labs/examples/lab09-sample-solution/` — รันได้ทันที `pytest --cov` 13 passed 94%

### 4.1 ไฟล์ที่ต้องมี

| ไฟล์ | เนื้อหา | เกณฑ์ |
|---|---|---|
| `tests/test_unit.py` (หรือเทียบเท่า) | Unit Test ≥ 5 tests — ครอบคลุม happy path + edge cases + boundary | tests pass · AAA pattern |
| `tests/test_doubles.py` | Test Doubles ≥ 1 ตัว — Stub หรือ Mock หรือ Fake ที่isolate external dependency | verify behavior ชัดเจน |
| `tests/test_tdd.py` + `src/<module>.py` | TDD — Red-Green-Refactor commit history ชัดเจน | 3 commits แยก (Red/Green/Refactor) |
| `.github/workflows/test.yml` | GitHub Actions CI — รัน lint + test + coverage ทุก PR | green badge · block merge on fail |
| `docs/coverage-report.md` | Coverage report (line + branch) + วิเคราะห์ว่าส่วนไหนต่ำและทำไม | มีตัวเลข + วิเคราะห์ |
| `reflect.md` (root) | Post-quiz 9 (merge จาก feature branch) | 3 reflection (B1–B3) |
| `AI_USAGE.md` (root) | อัปเดต: tools + prompts + ส่วนที่รับจาก AI | ครบทั้ง 3 sections |

### 4.2 PR Workflow

- Branch: `feature/lab9-testing`
- ต้อง merge `reflect.md` (Post-quiz 9) เข้ามาพร้อม
- ต้องมี **GitHub Actions badge** ใน PR description (green = pass)
- ผ่าน review + merge เข้า main

---

## 5. ขั้นตอนการปฏิบัติ (Step-by-Step)

> **ก่อนเริ่ม Lab 9** — ตรวจสอบว่านิสิตได้ทำ Post-quiz จากคาบบรรยายแล้ว (จาก §9.7 ในบทเรียน)
> - ถ้ายังไม่ได้ทำ → ให้ทำ Post-quiz 3 ข้อ (Coverage + TDD + Testing culture) ใน 15 นาทีแรกของ Lab
> - **Coverage report (B1)** จะถูกใช้เป็น starter สำหรับ Step 4 — **TDD plan (B2)** จะใช้กับ Step 2 — **Testing culture (B3)** จะใช้สะท้อนหลัง Lab

### Step 1: Testing Pyramid Workshop — จำแนก Test ที่มีอยู่ (20 นาที)

1. Branch `feature/lab9-testing`
2. เปิด `tests/` ของทีม — ลิสต์ test ที่มีอยู่ทั้งหมด
3. จำแนกแต่ละ test ว่าเป็น **Unit / Integration / E2E** ตาม Pyramid:

| ระดับ | สัดส่วนแนะนำ | ความเร็ว | ตัวอย่างในโปรเจกต์ |
|---|---|---|---|
| Unit | 70% | < 1 ms | `calculate_discount()` |
| Integration | 20% | 100 ms – 1 s | API → Service → DB |
| E2E | 10% | วินาที–นาที | browser login → checkout |

4. ประเมิน: ทีมมีสัดส่วนใกล้ 70/20/10 หรือไม่ — ถ้า E2E เยอะเกิน → วางแผนเพิ่ม Unit
5. Commit: `docs: classify existing tests by pyramid level`

### Step 2: TDD — Red-Green-Refactor กับฟังก์ชันจริง (30 นาที)

6. เลือก **1 function** จาก codebase ที่ยังไม่มี test หรือ test ไม่ครอบคลุม (ตาม Post-quiz B2)
7. **🔴 Red** — เขียน test ที่ fail ก่อน:

   ```python
   def test_calculate_total_with_tax():
       assert calculate_total(100, 0.07) == 107.0  # FAIL — function ยังไม่มี
   ```

8. **🟢 Green** — เขียน production code น้อยที่สุดให้ผ่าน:

   ```python
   def calculate_total(amount, tax_rate):
       return amount + (amount * tax_rate)
   ```

9. **🔵 Refactor** — ปรับปรุง code โดยไม่เปลี่ยน behavior (test ยัง pass):

   ```python
   def calculate_total(amount, tax_rate):
       return amount * (1 + tax_rate)
   ```

10. Commit แยก 3 commits: `test: add calculate_total test [RED]` → `feat: minimal calculate_total [GREEN]` → `refactor: simplify calculate_total`
11. **สะท้อน:** ถ้า test เขียนยาก → design ไม่ดี — ควร refactor ให้ test ง่ายขึ้น (PP Tip 69)

### Step 3: Test Doubles — Stub / Mock / Fake (30 นาที)

12. เลือก function ที่พึ่ง external dependency (DB / API / email service) — เช่น `send_welcome_email(user)` หรือ `fetch_promotion(user_id)`
13. เลือก Test Double ที่เหมาะสม:

| Double | เมื่อใช้ | ตัวอย่าง |
|---|---|---|
| **Stub** | control response ของ dependency | `get_user_stub()` return ค่าตายตัว |
| **Mock** | verify ว่า dependency ถูกเรียกตามคาด | `mock_email.verify_called_with(...)` |
| **Fake** | ต้องการ stateful object แบบง่าย | `FakeDatabase` in-memory |

14. เขียน test ที่ใช้ Double — ตัวอย่าง Mock:

   ```python
   def test_send_welcome_email_calls_service(mocker):
       mock_email = mocker.Mock()
       send_welcome_email("user@test.com", email_service=mock_email)
       mock_email.send.assert_called_once_with(to="user@test.com", subject="Welcome")
   ```

15. **ข้อควรระวัง:** อย่าใช้ Mock มากเกิน — จะทำให้ test ผูกกับ implementation (brittle)
16. Commit: `test: add mock for email service (test doubles)`

### Step 4: Coverage + Static Analysis (20 นาที)

17. รัน coverage:

   ```bash
   pytest --cov=src --cov-branch --cov-report=term-missing
   ```

18. บันทึกผลลง `docs/coverage-report.md`:

   ```markdown
   ## Coverage Report — Lab 9
   - Overall: 72% line, 65% branch
   - ต่ำสุด: src/payment.py — 45% (ยังไม่มี test สำหรับ error handling)
   - แผน: เพิ่ม test สำหรับ payment failure ใน Sprint ถัดไป
   ```

19. รัน static analysis:

   ```bash
   ruff check src/   # lint
   mypy src/         # type check (ถ้ามี)
   ```

20. เพิ่มเข้า CI — อัปเดต `.github/workflows/test.yml` ให้รัน lint ก่อน test (fail fast):

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
         - run: ruff check src/
     test:
       needs: lint
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with: { python-version: '3.12' }
         - run: pip install -r requirements.txt
         - run: pytest --cov=src --cov-branch --cov-fail-under=60
   ```

21. Push → เช็ค Actions tab ต้อง green — ตั้ง Branch protection (Require status checks)
22. Commit: `ci: add lint + coverage to GitHub Actions (fail fast)`

### Step 5: Saboteur Check — Test จับ Bug ได้จริงไหม (10 นาที)

23. สมาชิกคนหนึ่ง **จงใจ break code** (เช่น `>` เป็น `>=` ใน `calculate_discount`)
24. Push → Actions ต้อง **fail** (test จับได้) — ถ้าไม่ fail → test ไม่ครอบคลุม → เพิ่ม test
25. revert break + บันทึกใน `docs/coverage-report.md`
26. Commit: `docs: saboteur check — test detected boundary bug`

---

## 6. เกณฑ์การประเมิน (Rubric)

| เกณฑ์ | น้ำหนัก | A (90–100%) | B (70–89%) | C (50–69%) | F (<50%) |
|---|---|---|---|---|---|
| **Testing Pyramid** (Step 1) | 15% | จำแนกครบ + วิเคราะห์สัดส่วน + แผนปรับ | จำแนกครบ | บางส่วน | ไม่ทำ |
| **TDD discipline** (Step 2) | 30% | Red-Green-Refactor ชัด + 3 commits แยก | ส่วนใหญ่ | บางส่วน | เขียน test ทีหลัง |
| **Test Doubles** (Step 3) | 25% | เลือกถูกประเภท + verify behavior ชัด | ใช้ได้แต่เลือกไม่เหมาะ | มีแต่ไม่ verify | ไม่มี |
| **Coverage + Static** (Step 4) | 20% | report ครบ + วิเคราะห์ + CI fail-fast | report ครบ | บางส่วน | ไม่มี |
| **Saboteur check** (Step 5) | 10% | break → fail → fix ครบ | ทำแต่ไม่บันทึก | ทำบางส่วน | ไม่ทำ |

**คำนวณคะแนน:**
- ได้ครบ 5 เกณฑ์ที่ ≥ C = 3.0%
- ได้ครบ 5 เกณฑ์ที่ ≥ B = 3.5% (full)

**Deliverables ที่ต้องส่ง:**

| # | ไฟล์/หลักฐาน | ตรวจอะไร |
|---|---|---|
| 1 | `tests/test_unit.py` | ≥ 5 tests + boundary + pass |
| 2 | `tests/test_doubles.py` | ≥ 1 double + verify behavior |
| 3 | `tests/test_tdd.py` + commit history | Red-Green-Refactor 3 commits |
| 4 | `.github/workflows/test.yml` | lint + test + coverage + branch protection |
| 5 | `docs/coverage-report.md` | line + branch + วิเคราะห์ |
| 6 | `reflect.md` | 3 reflections (B1–B3) |
| 7 | `AI_USAGE.md` | prompts + ส่วนที่รับจาก AI |

> **หมายเหตุ**: คะแนนเป็น **Completion and Quality** — ต้องได้ครบ 5 เกณฑ์ ≥ C + ทุก test pass + workflow green ถึงจะได้คะแนนเต็ม

---

## 7. นโยบายการใช้ Generative AI (AI Usage Guidance)

| ✅ อนุญาต | ❌ ไม่อนุญาต |
|---|---|
| ใช้ AI generate test cases (จาก AC, edge cases) | **ห้าม** รับ test ที่ AI generate โดยไม่ review |
| ใช้ AI suggest Test Double ที่เหมาะสม | **ห้าม** สร้าง test ที่ "ผ่าน" แต่ไม่ test behavior (เช่น `assert mock.called`) |
| ใช้ AI review test quality + coverage gaps | **ห้าม** ให้ AI generate test + implementation พร้อมกัน (เสี่ยง test ผ่านเพราะผิดทั้งคู่) |
| ใช้ AI อธิบาย coverage report | ห้ามปล่อยให้ AI เขียน test เกิน 50% โดยไม่เข้าใจ |

**ต้องเปิดเผย** ใน `AI_USAGE.md`:
- เครื่องมือ: <Copilot/ChatGPT/Claude/etc.>
- Prompts ที่ใช้ (≥ 3 prompts: generate test cases · suggest doubles · review coverage)
- ส่วนที่รับจาก AI ตรง ๆ (ไม่แก้)

---

## 8. ข้อควรระวัง (Common Pitfalls)

> **❌ Test ที่ผ่านแต่ไม่ test behavior** — `assert mock.method.called` โดยไม่ verify argument ไม่ได้ test logic

> **❌ 100% coverage แต่ bug ยังโผล่** — coverage วัดแค่ "บรรทัดที่ run" ไม่ใช่ "behavior ที่ถูก test" (Tip 93) — Mars Climate Orbiter ก็มี unit test ผ่านทุกตัว

> **❌ Mock มากเกินไป** — test ผูกกับ implementation → เปลี่ยน implementation = test พัง (brittle) — ใช้ Stub/Fake เมื่อเหมาะกว่า

> **❌ TDD เป็นทาส** — เขียน test แค่ให้ coverage ขึ้น ไม่ได้คิดว่า "test = first user" — ตกหลุมพราง TDD zealot

> **❌ GitHub Actions ไม่ block merge** — branch protection ไม่ได้ตั้ง → CI แค่ "informational" ไม่ enforce

> **❌ ไม่ merge reflect.md** — ขาด input จาก Post-quiz 9 (coverage report + TDD plan)

---

## 9. ความท้าทายเพิ่มเติม (Stretch Goals)

สำหรับนิสิตที่ทำเสร็จก่อน — ลองทำเพิ่ม (ไม่บังคับ ไม่คิดคะแนนเพิ่ม):

- **Mutation testing** — `pip install mutmut` → `mutmut run` → ดูว่า test จับ mutant ได้กี่ %
- **Property-based test** — Hypothesis `@given` กับ business rule ที่ซับซ้อน (ส่วนลด 5 ขั้น)
- **Coverage badge** — เพิ่ม Codecov badge ใน README (GitHub Actions + codecov)
- **Testcontainers** — integration test ที่ใช้ Docker container จริง (DB · Redis)
- **Cross-team review** — review test ของทีมอื่น + comment suggestion

---

## 10. การส่งงาน

1. **Pull Request** `feature/lab9-testing` — tests pass + CI green — merge ก่อนหมดเวลา
2. **`tests/test_unit.py`** — ≥ 5 tests
3. **`tests/test_doubles.py`** — ≥ 1 Test Double
4. **`tests/test_tdd.py` + `src/<module>.py`** — TDD 3 commits
5. **`.github/workflows/test.yml`** — lint + test + coverage + branch protection
6. **`docs/coverage-report.md`** — coverage report + วิเคราะห์
7. **`reflect.md`** (Post-quiz 9) — merge พร้อม Lab 9
8. **`AI_USAGE.md`** — อัปเดต

> **Due**: สิ้นสุด Lab ภายใน 2 ชั่วโมง

---

## 11. เชื่อมโยงบทเรียน

แนวคิดที่ใช้ใน Lab 9 นี้จะถูกนำไปใช้ตลอดภาคการศึกษา:

- **Testing Pyramid 70/20/10** → ใช้ตัดสินใจว่า test อะไรควรเขียนเมื่อใด
- **Test Doubles** → ใช้ isolate external dependency ทุก Sprint
- **TDD Red-Green-Refactor** → ใช้ทุก Sprint — เริ่มจาก test
- **Coverage (line + branch)** → วัดแต่ไม่จบ — ต้องคิด behavior
- **Static Analysis** → ใช้ทุก PR — lint ก่อน test (fail fast)
- **GitHub Actions CI** → ใช้ทุก PR — block merge ถ้า test fail
- **Saboteur check** → ใช้ก่อน release ทุก Sprint

---

## 12. บรรณานุกรมประจำ Lab

- Hunt, A., & Thomas, D. (2019). *The Pragmatic Programmer* (2nd ed.). Addison-Wesley. Tips 67–69, 93.
- Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson. Chapter 8.
- Sommerville, I. (2019). *Engineering Software Products*. Pearson. Chapter 9.
- Beck, K. (2003). *Test-Driven Development: By Example*. Addison-Wesley.
- Cohn, M. (2009). *Succeeding with Agile*. Addison-Wesley. Testing Pyramid.
- Meszaros, G. (2007). *xUnit Test Patterns*. Addison-Wesley. Test Doubles.
- เอกสารประกอบการสอน บทที่ 9 — การทดสอบซอฟต์แวร์

---

*ใบงานนี้จัดทำโดย: ธรรมรัตน์ ธรรมา · สาขาวิทยาการคอมพิวเตอร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา · ภาคเรียนที่ 1 ปีการศึกษา 2569*
