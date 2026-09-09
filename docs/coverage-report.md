# Coverage Report — Lab09

## Overall
- Line: 95% (31/33 บรรทัด)
- Branch: 100% (6/6 ทางเลือก)

## ต่ำสุด
- src/email_service.py — 67% (บรรทัด 6-7: error handling ยังไม่มี test)
- แผน: เพิ่ม test_send_email_failure ใน Sprint ถัดไป

## Pyramid Assessment (จากขั้น 1)
- Unit: 70% ✅
- Integration: 20% ✅
- E2E: 10% ✅

## Saboteur Check
- Break: เปลี่ยน >= เป็น > ใน PROMO_MIN_LEN
- ผล: test_boundary_promo_len_6_gets_discount FAIL ✅ — test จับได้
- สรุป: boundary test ทำงานถูกต้อง
