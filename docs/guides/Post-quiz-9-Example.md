# ตัวอย่าง Post-quiz 9 — Section B Reflection (เฉลยตัวอย่าง)

> **สำหรับนิสิต** — นี่คือตัวอย่างคำตอบที่ดีสำหรับ Post-quiz 9 §9.7 Section B
> **ห้ามคัดลอกตรงๆ** — ให้เขียนจากโปรเจกต์ของทีมตัวเอง — ตัวอย่างนี้ใช้ Campus Eats เป็นต้นแบบ

---

## B1. Apply — Coverage Report (2–3 ประโยค)

**คำถาม:** รัน coverage ของโปรเจกต์ตัวเอง — coverage เท่าไหร่ — ส่วนไหนต่ำที่สุด จะเพิ่ม coverage ส่วนนั้นได้อย่างไร

**ตัวอย่างคำตอบที่ดี:**

> รัน `pytest --cov=src --cov-branch` ได้ **Overall 68% line / 55% branch** — ต่ำสุดคือ `src/payment.py` ที่ 42% (ส่วน `handle_payment_error` ไม่มี test เลย) — จะเพิ่มโดยเขียน test สำหรับ `test_payment_failure_returns_retry` และ `test_payment_timeout_raises` ใน Sprint ถัดไป พร้อมเพิ่ม branch test สำหรับ `if promo_code is None` ที่ยังไม่ครอบคลุม

**ทำไมดี:**
- มีตัวเลขจริง (68% / 55% / 42%)
- ระบุไฟล์และ function ที่ต่ำ (`payment.py` / `handle_payment_error`)
- มีแผนชัดว่าจะเพิ่ม test อะไร (2 tests + branch)

**ตัวอย่างที่ไม่ดี:**
> ❌ "Coverage ต่ำ จะพยายามเพิ่ม" — ไม่มีตัวเลข ไม่รู้ว่าต่ำตรงไหน

---

## B2. Connect — TDD (3–4 ประโยค)

**คำถาม:** เลือก 1 function ในโปรเจกต์: ถ้าเขียน test ก่อน code จะ design เปลี่ยนไหม — อะไรดีขึ้น อะไรแย่ลง

**ตัวอย่างคำตอบที่ดี:**

> เลือก `calculate_discount(total, tier, promo_code)` — ถ้าเขียน test ก่อน จะพบว่า `promo_code` ควรเป็น `str | None` ไม่ใช่ `str` เปล่าๆ และควรแยก `PROMO_MIN_LEN` เป็น constant เพื่อให้ test เขียน boundary (5 vs 6) ได้ง่าย — **ดีขึ้น:** API ชัดขึ้นเพราะต้องคิด input/output ก่อน, **ดีขึ้น:** แยก pure logic ออกจาก DB ทำให้ test เร็ว — **แย่ลง:** ใช้เวลาเขียน test เพิ่ม 15 นาทีในช่วงแรก แต่ลดเวลา debug ทีหลัง

**ทำไมดี:**
- เลือก function จริงในโปรเจกต์
- อธิบายว่า design เปลี่ยนอย่างไร (type + constant + แยก logic)
- บอกทั้งดีขึ้นและแย่ลง

**ตัวอย่างที่ไม่ดี:**
> ❌ "TDD ทำให้ code ดีขึ้น" — ไม่บอกว่า function ไหน ไม่บอกว่าเปลี่ยนอย่างไร

---

## B3. Reflect — Testing Culture (1 ประโยค)

**คำถาม:** ใน Sprint หน้า ทีมจะปรับปรุง testing culture อย่างไร 1 อย่าง

**ตัวอย่างคำตอบที่ดี:**

> Sprint หน้าทีมจะตั้งกฎว่า **ทุก PR ต้องมี test อย่างน้อย 1 ตัวและต้องผ่าน CI ก่อน merge** — โดยตั้ง Branch Protection (Require status checks) ที่ `main` เพื่อบังคับ — เริ่มจาก `calculate_discount` ใน Sprint 9 แล้วขยายไปทุก feature ใหม่

**ทำไมดี:**
- ระบุ 1 อย่างชัด (`ทุก PR ต้องมี test + CI`)
- มีวิธีบังคับ (Branch Protection)
- เริ่มจากจุดเล็กแล้วขยาย

**ตัวอย่างที่ไม่ดี:**
> ❌ "จะเขียน test ให้มากขึ้น" — ไม่บอกว่าทำอย่างไร ไม่บอกว่าเริ่มตรงไหน

---

## ไฟล์ `reflect.md` ที่ส่งจริง (ตัวอย่างเต็ม)

```markdown
# Post-quiz 9 — Reflection

**ชื่อ:** สมชาย ใจดี — **ทีม:** Campus Eats — **Sprint:** 9

## B1. Apply — Coverage Report

รัน `pytest --cov=src --cov-branch` ได้ Overall 68% line / 55% branch
ต่ำสุดคือ `src/payment.py` ที่ 42% (handle_payment_error ไม่มี test)
จะเพิ่ม test_payment_failure_returns_retry และ test_payment_timeout_raises
พร้อม branch test สำหรับ if promo_code is None ใน Sprint ถัดไป

## B2. Connect — TDD

เลือก calculate_discount(total, tier, promo_code) — ถ้าเขียน test ก่อน
จะพบว่า promo_code ควรเป็น str | None และควรแยก PROMO_MIN_LEN เป็น constant
เพื่อให้ test boundary (5 vs 6) ได้ง่าย — ดีขึ้น: API ชัด, แยก pure logic ทำให้ test เร็ว
แย่ลง: ใช้เวลาเพิ่ม 15 นาทีช่วงแรก แต่ลด debug ทีหลัง

## B3. Reflect — Testing Culture

Sprint หน้าทีมจะตั้งกฎว่า ทุก PR ต้องมี test ≥1 ตัวและผ่าน CI ก่อน merge
โดยตั้ง Branch Protection ที่ main — เริ่มจาก calculate_discount แล้วขยายไปทุก feature
```

---

## เกณฑ์ที่อาจารย์ตรวจ (Section B ไม่นับคะแนน แต่ต้องมีคุณภาพ)

| ข้อ | ตรวจอะไร | ผ่าน | ไม่ผ่าน |
|---|---|---|---|
| **B1** | มีตัวเลข coverage + ระบุไฟล์ต่ำ + แผนเพิ่ม | มีครบ 3 อย่าง | ไม่มีตัวเลข / ไม่ระบุไฟล์ |
| **B2** | เลือก function จริง + บอกว่า design เปลี่ยน + ดี/แย่ | ครบ | ตอบลอยๆ |
| **B3** | ระบุ 1 อย่างที่ทำได้จริง + มีวิธีบังคับ | ชัด + ทำได้ | "จะพยายามมากขึ้น" |

---

*ตัวอย่างนี้จัดทำโดย: ธรรมรัตน์ ธรรมา · สัปดาห์ที่ 9 · สอดคล้องกับบทที่ 9 §9.7 และ Lab09*
