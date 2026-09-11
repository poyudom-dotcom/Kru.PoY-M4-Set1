import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อสำหรับ Kru.PoY-M4-Set1 (ข้อละ 4 เคส = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: คำนวณพื้นที่สามเหลี่ยม (0.5 * b * h)
    "Examination_1.py": [
        (["10", "5"], "25.0"),
        (["3.5", "2.0"], "3.5"),
        (["0", "5"], "0.0"),
        (["100", "200"], "10000.0")
    ],
    # ข้อ 2: ตรวจสอบเลขคู่ หรือ เลขคี่ (Even / Odd)
    "Examination_2.py": [
        (["4"], "Even"),
        (["7"], "Odd"),
        (["0"], "Even"),
        (["-3"], "Odd")
    ],
    # ข้อ 3: ตรวจสอบผลการสอบ (>=50 Pass, <50 Fail)
    "Examination_3.py": [
        (["85"], "Pass"),
        (["50"], "Pass"),
        (["49"], "Fail"),
        (["0"], "Fail")
    ],
    # ข้อ 4: ตัดเกรด 5 ระดับ (>=80:A, >=70:B, >=60:C, >=50:D, <50:F)
    "Examination_4.py": [
        (["85"], "A"),
        (["72"], "B"),
        (["60"], "C"),
        (["45"], "F")
    ],
    # ข้อ 5: คำนวณราคาตั๋วสวนสนุก (<12 จ่าย 50, 12-59 จ่าย 100, >=60 เข้าฟรี 0)
    "Examination_5.py": [
        (["8"], "50"),
        (["25"], "100"),
        (["65"], "0"),
        (["12"], "100")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(base_name):
        return base_name
    elif os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name.replace(".py", "")):
        return base_name.replace(".py", "")
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งข้อความและทศนิยม"""
    if actual is None:
        return False
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean.lower() == expected_clean.lower():
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # คะแนนยืดหยุ่น (1 เคส = 1 คะแนน)
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม (Set 1)

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
