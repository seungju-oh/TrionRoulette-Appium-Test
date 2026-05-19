import pytest
import time
from pages.roulette_page import RoulettePage


class TestModeA:
    # ▶ TC-COM-E03: 최소 항목(2개) 미만 삭제 방어 로직 검증
    def test_tc_com_e03_min_items_defense(self, driver):
        # 기능이 정리 된 roulette_page의 Class RoulettePage를 호출
        page = RoulettePage(driver)
        print("\n▶ TC-COM-E03: 최소 항목(2개) 삭제 방어 로직 검증 시작")

        print("[항목 2개에 정상적인 이름 입력 시도]")
        # RoulettePage의 input_menus의 함수를 사용하여 두 가지 항목을 메뉴 입력, 키보드 닫기 등을 수행
        page.input_menus(["테스트1", "테스트2"])

        print("[항목이 2개인 상태에서 삭제 버튼 터치 시도]")
        # RoulettePage의 delete_item 함수를 사용하여 첫(0) 번째 항목 삭제를 선언
        page.delete_item(0)

        print("\n[방어 로직에 의해 항목 개수가 2개로 유지되는지 확인]")
        # RoulettePage의 get_item_count 함수를 이용하여 항목 개수를 계산하여 after_delete_count로 대입
        after_delete_count = page.get_item_count()
        # 계산된 after_delete_count가 2개인지 기대값(assert) 체크
        assert after_delete_count == 2, f"❌TC-COM-E03 FAIL: 항목이 2개일 때 삭제가 수행됨. (현재: {after_delete_count}개)"

        # 계산된 RoulettePage의 is_spin_button_enabled를 is_spin_enabled로 대입
        is_spin_enabled = page.is_spin_button_enabled()
        # 버튼이 활성화 되어있는지 기대값(assert) 체크
        assert is_spin_enabled == True, "❌TC-COM-E03 FAIL: 이름이 입력된 항목이 2개 이상임에도 스핀 버튼 비활성화."

        print("✅ TC-COM-E03 PASS: 최소 항목 2개 삭제 방어 로직 작동 확인")

    # ▶ TC-COM-E04: 빈 텍스트 입력 시 스핀 버튼 방어 로직 검증
    def test_tc_com_e04_empty_text_defense(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-COM-E04: 빈 텍스트 입력 시 스핀 버튼 방어 검증 시작")

        print("[첫 번째 항목의 텍스트 삭제 시도]")
        # RoulettePage의 input_menus 함수를 사용하여 두 가지 항목을 메뉴 입력, 키보드 닫기 등을 수행
        page.input_menus(["", "테스트2"])

        print("\n[항목 이름이 하나라도 비어있을 때 스핀 버튼이 비활성화 되는지 검증 시도]")
        # 계산된 RoulettePage의 is_spin_button_enabled를 is_spin_enabled로 대입
        is_spin_enabled = page.is_spin_button_enabled()
        # 버튼이 활성화 되어있는지 기대값(assert) 체크
        assert is_spin_enabled == False, "❌ TC-COM-E04 FAIL: 빈 항목이 존재함에도 스핀 버튼이 활성화됨."

        print("✅ TC-COM-E04 PASS: 빈 텍스트 입력 시 스핀 방어 로직 작동 확인")

    # ▶ TC-A-01: 기본 모드 정상 실행 테스트
    def test_tc_a_01_normal_spin(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-A-01: 기본 모드 정상 실행 검증 시작")
        # RoulettePage의 select_mode 함수를 사용하여 RADIO_MODE_A 메뉴를 선택
        page.select_mode(page.RADIO_MODE_A)
        # 기존 두개였던 항목에 항목 하나를 더 추가하여 총 3개 항목으로 설정
        page.add_items(1)
        # RoulettePage의 input_menus의 함수를 사용하여 두 가지 항목을 메뉴 입력, 키보드 닫기 등을 수행
        page.input_menus(["테스트1", "테스트2", "테스트3"])

        # RoulettePage의 spin_roulette 함수를 사용하여 룰렛 화전버튼 클릭 후 대기
        page.spin_roulette()
        # RoulettePage의 check_result_popup 함수를 사용하여 결과 팝업 닫은 뒤 True로 반환한 값울 is_popup_closed로 널기
        is_popup_closed = page.check_result_popup()
        # 팝업이 닫혔는지 기대값(assert) 체크
        assert is_popup_closed == True

        print("✅ TC-A-01 PASS: 기봄 모드 정상 실행 확인")

    # ▶ TC-A-E01: 스핀 중복 실행(따닥) 방어 테스트
    def test_tc_a_e01_prevent_double_spin(self, driver):
        page = RoulettePage(driver)
        print("\n▶ TC-A-E01: 스핀 중복 실행 방어 검증 시작")

        page.select_mode(page.RADIO_MODE_A)
        page.add_items(1)
        page.input_menus(["테스트1", "테스트2", "테스트3"])

        # RoulettePage의 spin_roulette_rapidly 함수를 사용하여 클릭 횟수, 간격을 지정하여 연타
        page.spin_roulette_rapidly(clicks=3, interval=0.1)

        # 첫 번째 정상 팝업 닫기
        page.check_result_popup()

        # RoulettePage의 is_popup_present 함수를 사용하여 선언한 시간동안 팝업 확인 후 False로 리턴한 값을 대입
        print("[중복 클릭 방어(2번째 팝업 미발생) 확인 시도]")
        is_duplicate_popup_shown = page.is_popup_present(timeout=3)

        # 팝업이 나타나지 않앟는지 기대값(assert) 체크
        assert is_duplicate_popup_shown == False, "❌ TC-A-E01 FAIL: 중복 클릭 방어 실패, 팝업이 복수 노출됨."
        print("✅ TC-A-E01 PASS: 스핀 중복 클릭 방어 작동 확인")