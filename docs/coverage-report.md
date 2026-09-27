# Coverage Report — Lab09

## Overall
- Statements: 95% (39/41 บรรทัด)
- Branch: 100% (12/12 ทางเลือก)
- Combined coverage reported by pytest-cov: 96% (51/53)

## ต่ำสุด
- src/email_service.py — 67% (บรรทัด 5-6 ใน `EmailService.send` ยังไม่ถูกเรียกโดย test เพราะใช้ Mock)
- แผน: เพิ่ม test สำหรับ `EmailService.send` และกรณีส่งไม่สำเร็จเมื่อมี behavior รองรับ

## Pyramid Assessment (จากขั้น 1)
- tests ใน repository นี้เป็น unit tests ทั้งหมด; ไม่มี integration หรือ E2E tests

## Equivalence Partitions ของ `calculate_discount`
- `vip` ไม่มี promo → 15%
- `member` ไม่มี promo → 10%
- `first` ไม่มี promo → 0%
- promo ยาว 5 ตัว → ไม่ได้ส่วนลด promo
- promo ยาว 6 ตัว → ได้ส่วนลด promo 20%
- promo ยาว 6 ตัวทับส่วนลด member → 20%
- ยอดรวม 0 → ส่วนลด 0

## Saboteur Check
- รายละเอียดและผลก่อน/หลังอยู่ใน `docs/saboteur-journal.md`
