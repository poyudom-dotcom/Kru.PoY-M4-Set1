import os
import subprocess

# ==========================================
# ชุดข้อมูลทดสอบสำหรับข้อสอบ ม.4 ชุดที่ 1
# ==========================================
TEST_CASES = {
    "Examination_1": [
        {"input": "5\n10\n", "expected": "50"},
        {"input": "7\n3\n", "expected": "21"}
    ],
    "Examination_2": [
        {"input": "85\n", "expected": "A"},
        {"input": "65\n", "expected": "C"},
        {"input": "42\n", "expected": "F"}
    ],
    "Examination_3": [
        {"input": "5\n", "expected": "15"},
        {"input": "10\n", "expected": "55"}
    ],
    "Examination_4": [
        {"input": "10\n25\n15\n", "expected": "25"},
        {"input": "99\n50\n12\n", "expected": "99"}
    ],
    "Examination_5": [
        {"input": "1500\n", "expected": "1400"},
        {"input": "800\n", "expected": "800"}
    ]
}

def is_equal(actual, expected):
    """
    ตรวจสอบความถูกต้องแบบยืดหยุ่น:
    1. ตัดช่องว่าง/ขึ้นบรรทัดใหม่เกิน (.strip())
    2. ไม่ซีเรียสตัวพิมพ์เล็ก-ใหญ่ (.lower())
    3. ตรวจเช็กตัวเลขทศนิยม (เช่น 50.0 เท่ากับ 50)
    """
    clean_actual = actual.strip().lower()
    clean_expected = expected.strip().lower()
    
    # เช็กข้อความตรงๆ
    if clean_actual == clean_expected:
        return True
        
    # เผื่อคำตอบเป็นตัวเลขทศนิยม
    try:
        if float(clean_actual) == float(clean_expected):
            return True
    except ValueError:
        pass
        
    return False

def run_tests():
    all_passed = True
    
    for file_name, cases in TEST_CASES.items():
        py_file = f"{file_name}.py"
        if not os.path.exists(py_file):
            continue

        print(f"\n--- Testing {py_file} ---")
        for i, case in enumerate(cases, 1):
            try:
                process = subprocess.Popen(
                    ["python", py_file],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5  # กันนักเรียนเขียนโค้ดติด Loop ไม่สิ้นสุด
                )
                stdout, stderr = process.communicate(input=case["input"])
                
                if is_equal(stdout, case["expected"]):
                    print(f"  Test Case {i}: PASSED ✅")
                else:
                    got_clean = stdout.strip()
                    print(f"  Test Case {i}: FAILED ❌ (Got: '{got_clean}', Expected: '{case['expected']}')")
                    all_passed = False
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"  Test Case {i}: FAILED ❌ (Timeout - โค้ดติด Infinite Loop)")
                all_passed = False
            except Exception as e:
                print(f"  Test Case {i}: ERROR ❌ ({str(e)})")
                all_passed = False

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    run_tests()
