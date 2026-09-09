# Post-quiz 9 — Reflection

**ชื่อ:** นายณัฐดนัย สิงห์งาม — **ทีม:** sec2-team4 — **Sprint:** 9

## B1. Apply — Coverage Report

รัน `pytest --cov=src --cov-branch` ได้ Overall 95% line / 100% branch
ต่ำสุดคือ `src/email_service.py` ที่ 67% (ไม่มี test ในส่วน error handling หรือบรรทัดที่ 6-7)
จะเพิ่ม `test_send_email_failure` ใน Sprint ถัดไป เพื่อทดสอบกรณีส่งอีเมลไม่สำเร็จ

## B2. Connect — TDD

เลือก `calculate_total(amount, tax_rate)` — ถ้าเขียน test ก่อน
จะพบว่าเราต้องคิดถึงกรณีเช่น `tax_rate=0.0` หรือ `amount=0` ทำให้ตัดสินใจง่ายขึ้นว่า logic ควรรองรับ edge case อย่างไร
ดีขึ้น: ฟังก์ชันมีเป้าหมายทำงานชัดเจน ครอบคลุม edge case ได้ตั้งแต่ต้น
แย่ลง: ต้องเสียเวลาเขียน test ในช่วงแรก และต้องทำตามขั้นตอน Red-Green-Refactor ทำให้ใช้เวลาเริ่มงานนานกว่าเดิม

## B3. Reflect — Testing Culture

Sprint หน้าทีมจะตั้งกฎว่า ทุก PR ต้องมีการรัน CI (GitHub Actions) และมี Unit Test อย่างน้อย 1 ตัวก่อน merge 
โดยตั้ง Branch Protection ที่ main ให้ต้องผ่าน `lint` และ `test` — เริ่มจากฟังก์ชันที่ถูกแก้ไขทั้งหมดใน Sprint ถัดไป
