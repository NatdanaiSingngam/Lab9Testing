# AI Usage — Lab 9

## Tools

- OpenAI Codex assisted with repository review, FizzBuzz implementation, tests, CI updates, and documentation.

## Prompts in this session

1. "ตรวจสอบว่าไฟล์ที่มีทำตามเนื้อหาต่อไปนี้ครบหรือไม่ แล้วลิสรายการที่ยังไม่ได้ทำมา" followed by the updated Lab 9 brief.
2. "ดำเนินการได้เลย"

These were the two prompts about the Lab 9 work after the earlier request to clone the repository. The rubric requests at least three prompts about test generation, gap identification, and quality review; no third Lab 9 prompt is claimed here.

## AI output accepted directly

- `src/fizzbuzz.py` and `tests/test_fizzbuzz.py`, developed in recorded Red, Green, and Refactor commits.
- `tests/test_property.py` with four Hypothesis properties.
- CI dependency and coverage threshold changes, plus the saboteur and coverage documentation.

The generated tests were checked by running pytest, Ruff, and a temporary boundary mutation. Review by the student is still required under the course AI policy.
