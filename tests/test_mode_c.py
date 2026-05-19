import pytest
import time
from pages.roulette_page import RoulettePage


class TestModeC:
    # ▶ TC-C-01: 커스텀 확률 모드 정상 적용 테스트
    def test_tc_c_01_custom_probability(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-C-01: 커스텀 모드 확률 적용 테스트 시작")

        # Appium ID: radio_mode_c
        page.select_mode(page.RADIO_MODE_C)
        menus = ["SSR", "SR", "R"]
        probs = ["1", "19", "80"]

        # 기본 두개의 항목에 한개의 항목을 더 추가하여 3개의 항목으로 만들기
        page.add_items(1)
        page.input_menus(menus)
        page.input_probabilities(probs)

        # Appium ID: btn_spin_enabled
        page.spin_roulette()
        # 팝업의 텍스트를 읽어와 raw_winner_text로 넣기
        raw_winner_text = page.get_result_and_close_popup()

        # 아직 결과를 모르기 때문에 None으로 설정
        winner_menu = None
        for menu in menus:
            # menus의 항목들을 하나씩 비교하며 raw_winner_text의 항목과 일치하는 항목이 있는지 체크
            if menu in raw_winner_text:
                # 일치하는 항목이 있다면 winner_menu 항목에 넣기
                winner_menu = menu
                break

        print(f"['{winner_menu}' 선정 확인 (설정 확률: SSR 1%, SR 19%, R 80%)]")
        # winner_menu None이 아닌지 기대값(assert) 체크
        assert winner_menu is not None, f"❌ TC-C-01 FAIL: 선정된 데이터 없음."

    # ▶ TC-C-02: 확률 입력 형식 제한(n.nn%) 검증
    def test_tc_c_02_prob_format_limit(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-C-02: 확률 입력 형식 제한(n.nn%) 검증 시작")

        # Appium ID: radio_mode_c
        page.select_mode(page.RADIO_MODE_C)
        invalid_prob = "12.345" # 비정상 포멧
        expected_prob = "12.34" # 정상 기대값

        print(f"[확률 텍스트박스에 '{invalid_prob}' 입력 시도.]")
        page.input_probabilities([invalid_prob])
        time.sleep(1)

        print(f"[실제 화면에 '{expected_prob}'가 입력되고 '{invalid_prob}'는 입력 방어되었는지 확인 시도]")

        if page.platform == "ios":
            # iOS 전용 데이터 읽기 로직
            # RoulettePage의 get_prob_text 함수의 iOS 로직을 사용하여 확률 텍스트 박스의 현재 값 읽어와 actual_prob에 넣기
            actual_prob = page.get_prob_text(0)
            # 실제 입력값(actual_prob)에 비정상 포멧(invalid_prob)이 없는지(not in) 기대값(assert) 체크
            assert invalid_prob not in actual_prob, f"❌ TC-C-02 FAIL(iOS): 소수점 셋째 자리({invalid_prob})가 입력됨."
            # 실제 입력값(actual_prob)애 정상 기대값(expected_prob)이 있는지 기대값(assert) 체크
            assert expected_prob in actual_prob, f"❌ TC-C-02 FAIL(iOS): 기대값({expected_prob})을 찾을 수 없음."
        else:
            # AOS 전용 데이터 읽기 로직
            # Appium 로직 page_source를 활용하여 화면 전체를 XML로 추출하여 source에 넣기
            source = driver.page_source
            # 추출한 값(source)에 비정상 포멧(invalid_prob)이 없는지 기대값(assert) 체크
            assert invalid_prob not in source, f"❌ TC-C-02 FAIL(AOS): 소수점 셋째 자리({invalid_prob})가 입력됨."
            # 추출한 값(source)에 정상 기대값(expected_prob)아 있는자 기대값(assert) 체크
            assert expected_prob in source, f"❌ TC-C-02 FAIL(AOS): 기대값({expected_prob})을 찾을 수 없음."

        print("✅ TC-C-02 PASS: 소수점 셋째자리 이상 입력 방어 작동 확인")

    # ▶ TC-C-E01: 확률 합산 오류(99.99% / 100.01%) 스핀 방어 검증
    def test_tc_c_e01_prob_sum_validation(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-C-E01: 확률 합산 오류(99.99% / 100.01%) 스핀 방어 검증")

        # Appium ID: radio_mode_c
        page.select_mode(page.RADIO_MODE_C)
        page.add_items(1)

        # 1. 99.99% 상황 테스트
        print("[총합 99.99% 입력 시도중]")
        page.input_probabilities(["33.33", "33.33", "33.33"])
        # RoulettePage의 is_spin_button_enabled 함수를 통해 스핀 버튼의 활성화 여부를 체크하고 결과를 is_enabled_99에 넣기
        is_enabled_99 = page.is_spin_button_enabled()
        # 스핀 버튼이 활성화 되지 않았는지(False) 기대값(assert) 체크
        assert is_enabled_99 == False, "❌ TC-C-E01 FAIL: 총합이 100%가 아님에도 Spin 버튼이 활성화됨.(99.99%)"

        # 2. 100.01% 상황 테스트
        print("[총합 100.01% 입력 시도중]")
        page.input_probabilities(["33.34", "33.34", "33.33"])
        is_enabled_100_01 = page.is_spin_button_enabled()
        assert is_enabled_100_01 == False, "❌ TC-C-E01 FAIL: 총합이 100%가 아님에도 Spin 버튼이 활성화됨.(100.01%)"

        print("✅ TC-C-E01 PASS: 총합이 100.00%가 아닌 경우 스핀 버튼 비활성화 확인")

    # ▶ TC-C-E02: 0% 확률 선정 제외 로직 검증
    def test_tc_c_e02_zero_percent_prob(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-C-E02: 0% 확률 선정 제외 로직 검증")

        # Appium ID: radio_mode_c
        page.select_mode(page.RADIO_MODE_C)
        page.add_items(1)
        page.input_menus(["확률100", "확률0_A", "확률0_B"])
        page.input_probabilities(["100", "0", "0"])

        # Appium ID: btn_spin_enabled
        page.spin_roulette()
        # 룰렛을 돌리고 결과 텍스트를 raw_winner_text에 넣기
        raw_winner_text = page.get_result_and_close_popup()

        # 결과 텍스트가 '확률100'인지 기대값(assert) 체크
        assert "확률100" in raw_winner_text, f"❌ TC-C-E02 FAIL: 0% 확률 항목이 선정됨. (결과: {raw_winner_text})"
        print("✅ TC-C-E02 PASS: 0% 확률 선정 불가 확인")

    # ▶ TC-C-E03: 확률 필드 특수문자 입력 방어 검증
    def test_tc_c_e03_invalid_string_input(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-C-E03: 확률 필드 특수문자 입력 방어 검증")

        # Appium ID: radio_mode_c
        page.select_mode(page.RADIO_MODE_C)
        # 비정상 텍스트인 특수문자를 invalid_text 변수로 선언
        invalid_text = "!@#$"

        print(f"[확률 텍스트박스에 특수문자 '{invalid_text}' 입력 시도.]")
        page.input_probabilities([invalid_text])
        time.sleep(1)

        # 확률 텍스트박스에 현재 입력된 텍스트 불러오기
        if page.platform == "ios":
            # iOS전용 데이터 읽기 로직
            # RoulettePage의 is_get_prob_text의 iOS 함수를 통해 확률 텍스트박스의 현재 값을 읽어 actual_prob에 넣기
            actual_prob = page.get_prob_text(0)
            # 실제 입력값(actual_prob)이 특수문자가 아닌지 기대값(assert) 체크
            assert invalid_text not in actual_prob, "❌ TC-C-E03 FAIL(iOS): 특수문자가 입력됨."
        else:
            # AOS전용 데이터 읽기 로직
            # Appium 로직 page_source를 활용하여 화면 전체를 XML로 추출하여 source에 넣기
            source = driver.page_source
            # 추출한 값(source)에 비정상 포멧(invalid_text)이 없는지 기대값(assert) 체크
            assert invalid_text not in source, "❌ TC-C-E03 FAIL(AOS): 특수문자가 입력됨."

        print("✅ TC-C-E03 PASS: 특수문자 입력 방어 확인.")