import pytest
import time
from pages.roulette_page import RoulettePage


class TestModeB:
    # ▶ TC-B-01: 서바이벌 모드 선정 결과 항목 제외(Dim) 로직 검증
    def test_tc_b_01_survival_exclusion(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-B-01: 서바이벌 모드 선정 결과 항목 제외(Dim) 검증 시작")

        # 1. 서바이벌 모드 선택 및 3개 항목 입력
        page.select_mode(page.RADIO_MODE_B)
        page.add_items(1)
        menus = ["테스트1", "테스트2", "테스트3"]
        page.input_menus(menus)

        # 2. 첫 번째 스핀 실행
        page.spin_roulette()
        # RoulettePage의 get_result_and_close_popup 함수를 사용하여 선정 팝업에서 추출된 raw_text를 winner_text에 대입
        winner_text = page.get_result_and_close_popup()

        # 3. 어떤 항목이 선정되었는지 인덱스(순서) 찾기
        winner_index = -1 # 결과를 아직 모르기 때문에 menus의 index가 될 0 이상의 숫자가 아닌 -1로 두기
        for i in range(len(menus)):
            # menus 리스트에서 항목들을 하나하나 꺼내서 팝업에서 추출된 raw_text 안에 해당 텍스트가 있는지 순서대로 확인
            if menus[i] in winner_text:
                winner_index = i # raw_text와 일치하는 메뉴를 찾았으면 해당 메뉴의 인덱스를 winner_index에 저장
                break

        # winner_index가 여전히 -1이 아닌지 기대값(assert) 체크
        assert winner_index != -1, f"❌ TC-B-01 FAIL: 선정 텍스트('{winner_text}')와 일치하는 항목을 찾을 수 없음."
        print(f"  - ['{menus[winner_index]}' 항목 선정 확인]")

        # 4. 검증: 선정된 항목의 텍스트 박스가 잠김(Disabled) 상태로 변했는지 확인
        # RoulettePage의 check_item_enabled 함수를 사용하여 winner_index의 항목이 활성화 상태인지 체크
        is_enabled = page.check_item_enabled(winner_index)
        # winner_index가 여전히 비활성화(False) 상태인지 기대값(assert) 체크
        assert is_enabled == False, f"❌ TC-B-01 FAIL: 선정된 '{menus[winner_index]}' 항목이 비활성화(Dim) 되지 않음."

        print(f"✅ TC-B-01 PASS: 선정된 항목 비활성화 확인")

    # ▶ TC-B-02: 모든 항목 선정 후 자동 초기화(전체 부활) 로직 검증
    def test_tc_b_02_survival_auto_reset(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-B-02: 서바이벌 모드 전체 선정 후 자동 초기화 검증 시작")

        # 1. 서바이벌 모드 선택 (빠른 검증을 위해 항목은 기본 2개만 사용)
        page.select_mode(page.RADIO_MODE_B)
        menus = ["테스트1", "테스트2"]
        page.input_menus(menus)

        # 2. 1회차 스핀 (둘 중 하나 선정 및 제외)
        print("  - [1회차 스핀 시도 (1개 제외 예정)]")
        page.spin_roulette()
        page.get_result_and_close_popup()

        # 3. 2회차 스핀 (남은 하나 100% 선정 및 전체 종료)
        print("  - [2회차 스핀 시도 (마지막 항목 선정 예정)]")
        page.spin_roulette()
        page.get_result_and_close_popup()

        # 4. 검증: 2개가 모두 선정되었으므로, 시스템이 자동으로 둘 다 '활성화' 상태로 리셋했는지 확인
        print("\n[모든 항목 선정 후 자동 활성화 확인 시도]")
        time.sleep(1)  # 상태 갱신을 위한 짧은 대기

        # 검증 전 일단 모든 항목(all_enabled)이 활성화(True) 되어있다고 추측
        all_enabled = True
        # 메뉴의 0번과 1번을 RoulettePage의 check_item_enabled 함수를 사용하여 차례대로 돌아가며 비활성화된 항목이 남아있는지 확인
        for i in range(len(menus)):
            if not page.check_item_enabled(i):
                # 비활성화된 항목이 남아있다면 False로 반환
                all_enabled = False
                print(f"❌ TC-B-02 FAIL: '{menus[i]}' 항목 비활성화 상태.")
                break

        # all_enabled가 여전히 비활성화(False) 상태인지 기대값(assert) 체크
        assert all_enabled == True, "❌ TC-B-02 FAIL: 선정 가능한 잔여 항목이 없음에도 모든 항목이 재활성화 되지 않음"

        print("✅ TC-B-02 PASS: 잔여 항목이 없을 경우 모든 항목 재활성화 확인")