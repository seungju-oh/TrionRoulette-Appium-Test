import pytest
import time
from pages.roulette_page import RoulettePage


class TestPreset:
    # ▶ TC-P-01: 프리셋 저장 및 불러오기 무결성 검증
    def test_tc_p_01_save_and_load_integrity(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-P-01: 프리셋 저장 및 불러오기 무결성 검증 시작")

        # 1. 초기 데이터 세팅 (모드 C)
        page.select_mode(page.RADIO_MODE_C)
        # 기본 두개 항목에서 하나를 더 추가하여 3개의 항목으로 만들기
        page.add_items(1)
        original_menus = ["프리셋1", "프리셋2", "프리셋3"]
        original_probs = ["20", "30", "50"]

        page.input_menus(original_menus)
        page.input_probabilities(original_probs)

        # 2. 프리셋 저장
        preset_name = "QA_TEST_AUTO"
        # 선언한 프리셋 이름(QA_TEST_AUTO)으로 RoulettePage의 save_preset 함수를 써서 저장
        page.save_preset(preset_name)

        # 3. 항목 오염 (모드 A로 변경 및 쓰레기 데이터 추가)
        print("\n[항목 데이터 오염 시도 (모드 A 변경 및 항목 추가)]")
        # 다른 모드(A) 선택
        page.select_mode(page.RADIO_MODE_A)
        # 3개의 항목 상태에서 두개를 더 추가하여 5개의 항목으로 만들기
        page.add_items(2)
        page.input_menus(["오염1", "오염2", "오염3", "오염4", "오염5"])

        # 4. 프리셋 다시 불러오기
        # RoulettePage의 load_preset 함수를 써서 저장한 프리셋 불러오기
        page.load_preset(preset_name)
        # 확률 프리셋도 불러와졌는지 확인하기 위해 모드C로 화면 전환
        page.select_mode(page.RADIO_MODE_C)

        print("[복구된 UI 렌더링 대기]")
        time.sleep(2)

        # 5. 데이터 무결성 검증
        print("[복구된 데이터 무결성 검증 시도]")
        # RoulettePage의 get_item_count 함수를 써서 현재 항목 개수를 계산한 뒤 actual_count에 저장
        actual_count = page.get_item_count()
        # 프리셋 저장 항목수인 3개 항목인지 기대값(assert) 체크
        assert actual_count == 3, f"❌TC-P-01 FAIL: 항목 개수 복구 실패. 기대: 3, 실제: {actual_count}"

        # 항목, 확률 텍스트박스의 현재 입력된 텍스트 읽어오기
        if page.platform == "ios":
            # iOS전용 텍스트 읽기 로직
            for i in range(3):
                # RoulettePage의 get_item_text 함수를 사용하여 항목의 총 갯수(3)만큼 반복하며 체크하여 actual_text에 넣기
                actual_text = page.get_item_text(i)
                # 결과 값(actual_text)에 원래 항목들(original_menus)이 있는지 차례대로(i) 확인하며 기대값(assert) 체크
                assert original_menus[i] in actual_text, f"❌TC-P-01 FAIL: 텍스트 복구 실패. 기대: {original_menus[i]}, 실제: {actual_text}"

                actual_prob = page.get_prob_text(i)
                # 결과 확률(actual_prob)에 원래 항목들(original_probs)이 있는지 차례대로(i) 확인하며 기대값(assert) 체크
                assert original_probs[i] in actual_prob, f"❌TC-P-01 FAIL: 확률 복구 실패. 기대: {original_probs[i]}, 실제: {actual_prob}"
        else:
            # AOS전용 텍스트 읽기 로직
            # Appium 로직 page_source를 활용하여 화면 전체를 XML로 추출하여 source에 넣기
            source = driver.page_source
            for i in range(3):
                # 추출된 source에 원래 항목들(original_menus, original_probs)이 있는지 차례대로(i) 확인하며 기대값(assert) 체크
                assert original_menus[i] in source, f"❌TC-P-01 FAIL: 텍스트 복구 실패(AOS). 기대값({original_menus[i]})이 존재하지 않음."
                assert original_probs[i] in source, f"❌TC-P-01 FAIL: 확률 복구 실패(AOS). 기대값({original_probs[i]})이 존재하지 않음."

        print("✅ TC-P-01 PASS: 프리셋 데이터 복구 확인")

    # ▶ TC-P-02: 기존 프리셋 덮어쓰기 검증
    def test_tc_p_02_overwrite_preset(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-P-02: 기존 프리셋 덮어쓰기 기능 검증 시작")

        preset_name = "QA_TEST_AUTO"

        # 1. 새로운 데이터 세팅 (모드 A)
        page.select_mode(page.RADIO_MODE_A)
        page.add_items(2)  # 기존 3개에서 4개로 증가
        new_menus = ["프리셋A", "프리셋B", "프리셋C", "프리셋D"]
        page.input_menus(new_menus)

        # 2. 동일한 이름으로 저장 시도 (덮어쓰기 팝업 처리 로직 동작)
        print(f"\n[기존 이름('{preset_name}')으로 덮어쓰기 시도]")
        # "QA_TEST_AUTO" 이름으로 프리셋 저장
        page.save_preset(preset_name)

        # 3. 화면 오염
        page.input_menus(["오염1", "오염2", "오염3", "오염4"])

        # 4. 프리셋 불러오기
        page.load_preset(preset_name)
        time.sleep(2)

        # 5. 덮어써진 데이터가 맞게 불러와지는지 검증
        print("[덮어쓰기된 데이터 검증 시도]")
        # RoulettePage의 get_item_count 함수를 이용하여 항목 개수를 계산하여 actual_count에 대입
        actual_count = page.get_item_count()
        # 계산된 항목 수(actual_count)가 원래 항목 개수인 4개로 일치하는지 기대값(assert) 체크
        assert actual_count == 4, f"❌TC-P-02 FAIL: 덮어쓰기 복구 실패. 기대 개수: 4, 실제: {actual_count}"

        # 항목 텍스트박스 내용 읽어오기
        if page.platform == "ios":
            # iOS전용 텍스트 읽기
            for i in range(4):
                # RoulettePage의 get_item_text 함수를 사용하여 항목의 총 갯수(4)만큼 반복하며 체크하여 actual_text에 넣기
                actual_text = page.get_item_text(i)
                # 결과 값(actual_text)에 원래 항목들(new_menus)이 있는지 차례대로(i) 확인하며 기대값(assert) 체크
                assert new_menus[i] in actual_text, f"❌TC-P-02 FAIL: 덮어쓰기 텍스트 불일치(iOS). 기대: {new_menus[i]}, 실제: {actual_text}"
        else:
            # AOS전용 텍스트 읽기
            # Appium 로직 page_source를 활용하여 화면 전체를 XML로 추출하여 source에 넣기
            source = driver.page_source
            for i in range(4):
                # 추출된 source에 원래 항목들(new_menus)이 있는지 차례대로(i) 확인하며 기대값(assert) 체크
                assert new_menus[i] in source, f"❌TC-P-02 FAIL: 덮어쓰기 텍스트 불일치(AOS). 기대값({new_menus[i]})을 찾을 수 없음."

        print("✅ TC-P-02 PASS: 기존 프리셋 덮어쓰기 기능 동작 확인")