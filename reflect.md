# Post-quiz 9 — Reflection (updated Lab 9 criteria)

**ชื่อ:** นายณัฐดนัย สิงห์งาม — **ทีม:** sec2-team4 — **Sprint:** 9

## B1. Unit Test plan

เลือก `calculate_discount(total, tier, promo_code)` เป็น business logic ที่ทดสอบได้โดยไม่ต้องพึ่งบริการภายนอก แบ่งกรณีเป็น tier `vip`, `member`, `first`; promo ไม่ถึง 6 ตัวและตั้งแต่ 6 ตัว; promo ที่ทับส่วนลดของ tier; และยอดรวม 0 จุด boundary สำคัญคือความยาว promo 5 กับ 6 ตัว ซึ่งมี unit tests แยกกัน ผลล่าสุด `src/calc.py` ครอบคลุม statements และ branches 100%

## B2. TDD plan and result

ใช้ FizzBuzz kata: เริ่มจาก test สำหรับ 3 ที่ fail เพราะยังไม่มี `fizzbuzz`; เขียน implementation ขั้นต่ำให้ pass; เพิ่มกรณี 1, 5, 15, 7 ให้ fail แล้วขยาย implementation; จากนั้นแยก helper `is_multiple` โดย test ทั้ง 5 ยัง pass ประวัติ commits บน `feature/lab9-testing` แสดง Red, Green และ Refactor แยกกัน

## B3. Property-Based Test

ใช้ Hypothesis ตรวจอัตราส่วนลด VIP, promo ยาวอย่างน้อย 6 ตัวที่ต้องได้ 20% ในทุก tier, promo สั้นที่ไม่ควรลดราคา `first`, และ FizzBuzz สำหรับพหุคูณของ 15 ขณะจงใจเปลี่ยน `>= 6` เป็น `> 6` Hypothesis พบกรณีล้มเหลวและ shrink เหลือ `total=5`, `promo_code='000000'`, `tier='vip'` หลังแก้กลับ test ผ่านทั้งหมด
