from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# python -m pytest tests/{test_file}.py --platform {OS} -v -s 로 테스트 실행

class RoulettePage:
    # ==========================================
    # 1. Locators (화면 요소의 고유 ID 모음)
    # ==========================================
    # Appium ID: radio_mode_a
    # Appium ID: radio_mode_b
    # Appium ID: radio_mode_c
    # Appium ID: btn_add_item
    # Appium ID: btn_dialog_result_confirm
    RADIO_MODE_A = "radio_mode_a"
    RADIO_MODE_B = "radio_mode_b"
    RADIO_MODE_C = "radio_mode_c"
    BTN_ADD = "btn_add_item"
    BTN_DIALOG_RESULT_OK = "btn_dialog_result_confirm"

    @staticmethod
    def item_text(index):
        """텍스트 입력칸의 동적 ID를 생성, (0, 1, 2번째 텍스트박스 등...)"""
        # Appium ID: input_item_text_{index}
        return f"input_item_text_{index}"

    @staticmethod
    def item_prob(index):
        """확률 입력칸의 동적 ID를 생성, (0, 1, 2번째 확률 텍스트박스 등...)"""
        # Appium ID: input_item_prob_{index}
        return f"input_item_prob_{index}"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 기본 10초 대기
        self.wait_long = WebDriverWait(driver, 20)  # 룰렛 회전 등 오래 걸리는 작업용 20초 대기
        self.platform = self.driver.capabilities.get('platformName', 'android').lower() # 플랫폼 판별 (android 또는 ios)

    # ==========================================
    # 2. 공통 유틸리티
    # ==========================================
    def scroll_to_element(self, element):
        """화면 스크롤 로직"""
        try:
            if self.platform == "ios":
                # iOS 전용 'mobile: scroll' 명령어를 사용해 특정 요소(element.id)를 향해 아래(down)로 스와이프
                self.driver.execute_script('mobile: scroll', {'element': element.id, 'direction': 'down'})
            else:
                # AOS 전용 'mobile: scrollGesture' 명령어를 사용해 화면의 100%(1.0)만큼 아래로 크게 스와이프
                self.driver.execute_script('mobile: scrollGesture',
                                           {'elementId': element.id, 'direction': 'down', 'percent': 1.0})
            time.sleep(0.5)
        except:
            # 화면에 보이는 요소가 없을 경우 중단하지 않고 다음으로 넘기기
            pass

    def hide_keyboard_safe(self):
        """키보드를 숨기거나 포커스를 해제하여 상태 동기화"""
        if self.platform == "ios":
            # iOS 전용 키보드 숨기기 로직
            try:
                # [1단계] 키보드의 '완료(return)' 버튼을 눌러서 닫기 시도
                self.driver.hide_keyboard(key_name='return')
            except:
                pass
            try:
                # [2단계] 화면의 빈 공간을 터치해서 닫기 시도
                self.driver.execute_script('mobile: hideKeyboard', {'strategy': 'tapOutside'})
            except:
                pass
            try:
                # [3단계] 화면 상단(빈 공간 확률이 높은 곳)의 특정 좌표를 터치해서 닫기 시도
                window_size = self.driver.get_window_size() # 화면 전체 크기를 가져옴
                x = int(window_size['width'] / 2)  # 가로의 중간
                y = int(window_size['height'] * 0.25) # 세로의 위에서 1/4 지점
                self.driver.tap([(x, y)])
            except:
                pass
            try:
                # [4단계] 룰렛 판(확실한 빈 공간)을 직접 클릭해서 키보드 포커스 비활성
                # Appium ID: canvas_roulette_wheel
                wheel = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "canvas_roulette_wheel")
                wheel.click()
            except:
                pass
            time.sleep(1) # 키보드가 내려갈 때까지 1초 대기
        else:
            # AOS 전용 키보드 숨기기 로직
            try:
                # [1단계] 안드로이드 기본 키보드 숨기기 명령어
                self.driver.hide_keyboard()
            except:
                # [2단계] 화면 구석(50, 50 좌표)을 터치해서 포커스 비활성
                self.driver.tap([(50, 50)])
            time.sleep(1) # 키보드가 내려갈 때까지 1초 대기

    # ==========================================
    # 3. 주요 액션
    # ==========================================
    def select_mode(self, mode_locator):
        """상단의 룰렛 모드(A, B, C) 라디오 버튼 선택"""
        print(f"\n[모드 선택: {mode_locator}]")
        # Appium ID: {mode_locator}
        # 각 테스트 파일의 page.select_mode를 통해 mode_locator가 A~C중 어느것인지 받아와 클릭 가능한 상태가 될 때까지 def __init__에서 언급해준 대기시간 만큼 대기 후 클릭
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, mode_locator))).click()

    def add_items(self, count):
        """'+ 항목 추가' 버튼을 임의 횟수만큼 반복 클릭"""
        print(f"[항목 추가 버튼 {count}회 클릭]")
        # Appium ID: btn_add_item
        # BTN_ADD으로 선언 된 btn_add_item이 화면에 나타나 클릭 가능한 상태까지 def __init__에서 언급해준 대기시간 만큼 대기 후 나타나면 btn 변수에 담기
        btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_ADD)))
        # 각 테스트 파일의 page.add_items를 통해 count가 선언된 횟수를 받아와 btn을 0.3초 간격으로 선언된 횟수만큼 클릭
        for _ in range(count):
            btn.click()
            time.sleep(0.3)

    def input_menus(self, menus):
        """항목 텍스트박스에 텍스트 입력 (AOS/iOS 맞춤 분기)"""
        # 각 테스트 파일의 page.input_menus에서 선언된 항목명들을 enumerate을 통해 인덱스 숫자를 포함하여 가져온 뒤 순서대로 정리
        # [i]로 인덱싱 된 개수만큼 항목명을 차례대로 불러와 입력
        for i, menu in enumerate(menus):
            # i가 0이면 "input_item_text_0" 이라는 글자가 만들어져서 선언된 menus의 개수만큼 반복하여 field_id에 대입
            field_id = self.item_text(i)
            print(f"['{field_id}'에 '{menu}' 입력 시도]")

            # Appium ID: input_item_text_{index}
            # field_id가 나타날때까지 def __init__에서 언급해준 대기시간 만큼 대기후 나타나면 element 변수로 낚아채기
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))
            self.scroll_to_element(element) #element 입력창까지 스크롤 (항목이 많아 화면에서 가려질 경우를 대비)

            element.click()
            time.sleep(0.5)

            if self.platform == "ios":
                # iOS 전용 입력 로직
                element.clear() # Appium의 기본 clear로 기존 글자를 지우기
                element.send_keys(menu) # Appium의 기본 send_keys로 menu 타이핑
            else:
                # AOS 전용 입력 로직
                self.driver.press_keycode(123) # 키보드의 'End 키(123)' 버튼을 눌러 텍스트 박스의 맨 마지막 부분으로 커서 이동
                for _ in range(20): self.driver.press_keycode(67) # 백스페이스 키(67)을 20번 연타
                self.driver.execute_script('mobile: type', {'text': menu}) # AOS 전용 고속 타자 명령어('mobile: type')를 사용하여 menu 타이핑

            time.sleep(0.5)
            self.hide_keyboard_safe()

    def input_probabilities(self, probabilities):
        """확률 모드(C)의 확률(%) 텍스트박스에 값을 입력 (AOS/iOS 맞춤 분기)"""
        # 각 테스트 파일의 page.input_probabilities에서 선언된 확률들을 enumerate을 통해 인덱스 숫자를 포함하여 가져온 뒤 순서대로 정리
        # [i]로 인덱싱 된 개수만큼 항목명을 차례대로 불러와 입력
        for i, prob in enumerate(probabilities):
            # i가 0이면 "input_item_prob_0" 이라는 글자가 만들어져서 선언된 probs의 개수만큼 반복하여 field_id에 대입
            field_id = self.item_prob(i)
            print(f"['{field_id}'에 확률 '{prob}%' 입력 시도]")

            # Appium ID: input_item_prob_{index}
            # field_id가 나타날때까지 def __init__에서 언급해준 대기시간 만큼 대기후 나타나면 element 변수로 낚아채기
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))
            self.scroll_to_element(element) #element 입력창까지 스크롤 (항목이 많아 화면에서 가려질 경우를 대비)

            element.click()
            time.sleep(0.5)

            if self.platform == "ios":
                # iOS 전용 입력 로직
                element.clear() # Appium의 기본 clear로 기존 글자를 지우기
                element.send_keys('\b' * 10) # 백스페이스(\b) 10번 연타
                element.send_keys(str(prob)) # 숫자(prob)을 str()로 감싸서 텍스트 형태로 입력 (send_keys는 텍스트 형태만 받을 수 있기 때문)
            else:
                # AOS 전용 입력 로직
                self.driver.press_keycode(123) # 키보드의 'End 키(123)' 버튼을 눌러 텍스트 박스의 맨 마지막 부분으로 커서 이동
                for _ in range(10): self.driver.press_keycode(67) # 백스페이스 키(67)을 10번 연타
                self.driver.execute_script('mobile: type', {'text': str(prob)}) # 숫자(prob)을 str()로 감싼 텍스를 mobile: type로 고속 입력 (mobile: type는 텍스트 형태만 받을 수 있기 때문)

            time.sleep(0.5)
            self.hide_keyboard_safe()

    def delete_item(self, index):
        """특정 인덱스의 항목 삭제 버튼 클릭"""
        # 각 테스트 파일의 page.delete_item에서 선언된 삭제 버튼의 위치를 가져온 뒤 변수 btn_id에 대입 (첫 번째 항목의 삭제 버튼일 경우 btn_delete_item_0)
        btn_id = f"btn_delete_item_{index}"
        print(f"['{btn_id}' (항목 {index + 1} 삭제) 클릭 시도]")

        # Appium ID: btn_delete_item_{index}
        # btn_id가 나타날때까지 def __init__에서 언급해준 대기시간 만큼 대기후 나타나면 element 변수로 낚아채기
        element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, btn_id)))
        self.scroll_to_element(element) #element 입력창까지 스크롤 (항목이 많아 화면에서 가려질 경우를 대비)

        element.click() # 삭제 버튼 클릭
        time.sleep(1)

    def spin_roulette(self):
        """START SPIN 버튼을 클릭하여 룰렛 회전"""
        print("['START SPIN' 버튼 클릭 (룰렛 회전)]")
        if self.platform == "ios":
            # iOS일 경우 떠 있을 수 있는 키보드를 미리 숨기기
            self.hide_keyboard_safe()

        # Appium ID: btn_spin_enabled
        # btn_spin_enabled이 나타날때까지 def __init__에서 언급해준 대기시간 만큼 대기후 나타나면 클릭
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_spin_enabled"))).click()

    def spin_roulette_rapidly(self, clicks=3, interval=0.1):
        """START SPIN 버튼을 지정된 횟수만큼 짧은 간격으로 연타 (중복 방지 테스트용)"""
        print(f"['START SPIN' 버튼 {clicks}회 연속 터치 시도]")
        self.hide_keyboard_safe() # 떠 있을 수 있는 키보드를 미리 숨기기

        # btn_spin_enabled이 나타날때까지 def __init__에서 언급해준 대기시간 만큼 대기후 나타나면 spin_btn 변수로 낚아채기
        spin_btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_spin_enabled")))

        # 선언 된 clicks 횟수만큼 interval 텀을 두고 연타
        for i in range(clicks):
            try:
                spin_btn.click()
                print(f"   - ({i + 1}번째 클릭 완료)")
            except:
                pass  # 룰렛이 이미 돌기 시작해서 상태가 변했더라도 무시
            time.sleep(interval)

    # ==========================================
    # 4. 검증 및 상태 확인
    # ==========================================
    def is_spin_button_enabled(self):
        """스핀 버튼 활성화 유무(True/False) 확인"""
        # 텍스트 입력 후 앱이 계산을 마칠 시간을 넉넉히 주기
        time.sleep(1)

        # 활성화 버튼 찾기
        try:
            # Appium ID: btn_spin_enabled
            # 화면에서 btn_spin_enabled 버튼을 찾기 (find_element)
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "btn_spin_enabled")
            # 에러 없이 찾았다면 True로 반환
            return True
        except:
            pass

        # 비활성화 버튼 찾기
        try:
            # Appium ID: btn_spin_disabled
            # 화면에서 btn_spin_disabled 버튼을 찾기 (find_element)
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "btn_spin_disabled")
            # 에러 없이 찾았다면 False로 반환
            return False
        except:
            # 둘 다 못 찾을 경우 False로 간주
            return False

    def check_item_enabled(self, index):
        """항목 텍스트 박스 활성화 유무(True/False) 확인"""
        # 룰렛 스핀 후 텍스트박스가 비활성화 되는 시간을 넉넉히 주기
        time.sleep(1)
        # 검사 할 텍스트박스 변수 지정
        normal_id = f"input_item_text_{index}"
        disabled_id = f"input_item_text_{index}_disabled"

        # 활성화 텍스트박스 찾기
        try:
            # Appium ID: input_item_text_{index}_disabled
            # 화면에서 비활성화된 텍스트박스(disabled_id) 찾기
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, disabled_id)
            # 에러 없이 찾았다면 False로 반환
            return False
        except:
            pass

        # 비활성화 텍스트박스 찾기
        try:
            # Appium ID: input_item_text_{index}
            # 화면에서 활성화된 텍스트박스(normal_id) 찾기
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, normal_id)
            # 에러 없이 찾았다면 True로 반환
            return True
        except:
            # 둘 다 못 찾을 경우 False로 간주
            return False

    def get_item_count(self):
        """현재 룰렛 항목(텍스트 박스)의 총 개수를 가져오기 (AOS/iOS 호환)"""
        # 화면의 모든 요소(//*[...])중에서 AOS 요소(@content-desc) 또는(or) iOS 요소(@name)에 'input_item_text_'가 포함(contains)된 모든것을 찾아 xpath_query로 저장하기
        xpath_query = "//*[contains(@content-desc, 'input_item_text_') or contains(@name, 'input_item_text_')]"
        # 조건에 맞는 복수(elements)의 항목들을 찾아 elements 리스트에 담기
        elements = self.driver.find_elements(AppiumBy.XPATH, xpath_query)
        # len() 함수를 써서 리스트 안에 요소가 몇 개 들어있는지 센 다음, 그 숫자를 반환
        return len(elements)

    def get_item_text(self, index):
        """텍스트 박스의 현재 입력값 읽어오기 (AOS 순정 로직 + iOS 호환)"""
        # 검사 할 텍스트박스 변수 지정
        normal_id = f"input_item_text_{index}"
        disabled_id = f"input_item_text_{index}_disabled"

        # AOS/iOS에 맞춰 요소의 텍스트만 빼 오기
        def _get_text(el):
            if self.platform == "ios":
                # iOS 텍스트 추출
                val = el.text # 기본적으로 화면에 보이는 텍스트 읽기
                if not val: val = el.get_attribute("value") # 안 되면 내부에 숨겨진 'value' 값을 파내기
                return val if val else "" # 값이 있으면 반환하고, 없으면 빈칸("")을 반환
            else:
                # AOS 텍스트 추출
                val = el.get_attribute("text") # 접근성 노드 내부에 숨겨진 'text' 속성만 가져오기
                return val if val else "" # 값이 있으면 반환하고, 없으면 빈칸("")을 반환

        # 활성화 텍스트박스의 텍스트 읽기 시도
        try:
            # 활성화 된 텍스트박스(normal_id)를 찾아 element에 대입
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, normal_id)))
            return _get_text(element) # 찾았으면 _get_text에 대입하여 글자 뽑아내기
        except:
            pass

        # 비활성화 텍스트박스의 텍스트 읽기 시도
        try:
            # 서바이벌 모드 등으로 비활성화된 항목 처리
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, disabled_id)))
            return _get_text(element) # 찾았으면 _get_text에 대입하여 글자 뽑아내기
        except:
            # 두 상태 모두 화면에 아예 없다면 빈칸 반환하기
            return ""

    def get_prob_text(self, index):
        """확률 박스의 현재 입력값 읽어오기 (AOS 순정 로직 + iOS 호환)"""
        time.sleep(1.5) # 확률 텍스트 박스 랜더링 시간이 미세하게 길기에 대기시간 추가
        # 각 테스트 파일의 page.get_prob_text를 통해 확률이 입력된 n번째 텍스트박스를 찾아 field_id로 저장
        field_id = self.item_prob(index)

        try:
            # field_id가 화면에 나타날때까지 기다린 뒤 나타나면 element로 낚아채기
            element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, field_id)))

            if self.platform == "ios":
                # iOS 텍스트 추출
                val = element.text # 기본적으로 화면에 보이는 텍스트 읽기
                if not val: val = element.get_attribute("value") # 안 되면 내부에 숨겨진 'value' 값을 파내기
                return val if val else "" # 값이 있으면 반환하고, 없으면 빈칸("")을 반환
            else:
                # AOS 텍스트 추출
                val = element.get_attribute("text") # 접근성 노드 내부에 숨겨진 'text' 속성만 가져오기
                return val if val else "" # 값이 있으면 반환하고, 없으면 빈칸("")을 반환
        except:
            # 두 상태 모두 화면에 아예 없다면 빈칸 반환하기
            return ""

    # ==========================================
    # 5. 팝업 제어
    # ==========================================
    def check_result_popup(self):
        """결과 팝업 닫기"""
        print("[결과 팝업 대기 후 닫기 시도]")
        # Appium ID: btn_dialog_result_confirm
        # BTN_DIALOG_RESULT_OK로 선언 된 btn_dialog_result_confirm가 보일때까지 대기 후 나타나면 result_ok로 대입
        result_ok = self.wait_long.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK)))
        result_ok.click()
        # 결과 팝업 확인 버튼을 닫고 True로 반환
        return True

    def get_result_and_close_popup(self):
        """결과 팝업에서 결과를 빼 오고 팝업을 닫기"""
        print("[결과 추출 시도]")
        # 화면의 모든 요소(//*[...])중에서 AOS 요소 @text, iOS 요소 @label, iOS 요소 @name 셋 모두에서 '결과'가 포함(contains)된 모든것을 찾아 xpath_query로 저장하기
        xpath_query = "//*[contains(@text, '결과') or contains(@label, '결과') or contains(@name, '결과')]"
        # 룰렛 회전이 끝날 때까지 최대 20초(long.until) 동안 대기 하면서 화면에서 결과 텍스트(xpath_query)를 찾게 되면 result_text_element에 넣기
        result_text_element = self.wait_long.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_query)))

        # 결과를 불러와 출력
        raw_text = result_text_element.text
        print(f"[결과 팝업 텍스트: '{raw_text}']")

        # Appium ID: btn_dialog_result_confirm
        # BTN_DIALOG_RESULT_OK로 선언 된 btn_dialog_result_confirm가 보일때까지 대기 후 나타나면 result_ok로 대입
        result_ok = self.wait_long.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK)))
        result_ok.click()
        # 결과 팝업 확인 버튼을 닫고 결과를 텍스트로 반환
        return raw_text

    def is_popup_present(self, timeout=3):
        """두번쨰 팝업이 안 나타나는지 확인"""
        try:
            # Appium ID: btn_dialog_result_confirm
            # self.wait, self.wait_long을 쓰지 않고 선언한 3초간 대기하면서 덮어쓰기 팝업의 확인 버튼을 찾기
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.BTN_DIALOG_RESULT_OK))
            )
            return True
        except TimeoutException:
            return False

    # ==========================================
    # 6. 프리셋 저장 / 불러오기
    # ==========================================
    def save_preset(self, preset_name):
        """프리셋 저장하기"""
        print(f"\n[프리셋 '{preset_name}' 저장 시도]")

        if self.platform == "ios":
            # iOS 전용 저장 버튼 누르기 & 입력
            # Appium ID: btn_topbar_save
            save_btn = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "btn_topbar_save")))
            # 버튼의 '왼쪽 위 모서리(x:5, y:5)'를 정밀 클릭 시도
            self.driver.execute_script("mobile: tap", {"element": save_btn.id, "x": 5, "y": 5})

            # Appium ID: input_preset_name
            # 화면의 모든 요소(//*[...])중에서 @content-desc, @name, @type, @value 4가지 요소에서 텍스트박스 찾기 시도
            input_xpath = "//*[@content-desc='input_preset_name' or @name='input_preset_name' or @type='XCUIElementTypeTextField' or @value='이름 입력']"
            # 텍스트박스를 찾았으면 input_field로 가져오기
            input_field = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, input_xpath)))
            input_field.click() # 한 번 탭하여 텍스트박스 활성화
            time.sleep(0.5)
            input_field.clear() # 기존 텍스트 지우기
            input_field.send_keys('\b' * 15) # 기존 텍스트 백스페이스를 사용하여 지우기
            input_field.send_keys(preset_name) # 프리셋 이름 입력 시도
        else:
            # AOS 전용 저장 버튼 누르기 & 입력
            # Appium ID: btn_topbar_save
            # 저장 버튼을 화면에서 찾가 누르기
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_topbar_save"))).click()
            # Appium ID: input_preset_name
            # 텍스트 박스를 찾아 클릭하여 활성화
            input_field = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "input_preset_name")))
            input_field.click()
            time.sleep(0.5)
            self.driver.press_keycode(123) # 백스페이스 키(123) 15번 시도
            for _ in range(15): self.driver.press_keycode(67)
            self.driver.execute_script('mobile: type', {'text': preset_name}) # mobile: type 고속 타자로 프리셋 이름 입력 시도

        time.sleep(0.5)
        self.hide_keyboard_safe()

        if self.platform == "ios":
            # iOS 전용 저장 버튼 누르기
            # Appium ID: btn_dialog_save_confirm
            # 화면의 모든 요소(//*[...])중에서 @content-desc, @name, @label 3가지 요소에서 저장 버튼 찾기 시도
            save_confirm_xpath = "//*[@content-desc='btn_dialog_save_confirm' or @name='저장' or @label='저장']"
            # 조건에 맞는 버튼들(elements)을 찾아 save_btns에 넣기
            save_btns = self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH, save_confirm_xpath)))
            save_btns[-1].click() # 화면 최상단에 올려져 있는 맨 마지막 요소(-1)의 버튼을 클릭 (화면 내부 팝업 너머의 버튼 클릭 시도 방지)
        else:
            # AOS 전용 저장 버튼 누르기
            # Appium ID: btn_dialog_save_confirm
            # 화면 상 btn_dialog_save_confirm을 찾아 클릭
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_dialog_save_confirm"))).click()

        try:
            # 덮어쓰기 팝업 대응
            short_wait = WebDriverWait(self.driver, 1.5)
            if self.platform == "ios":
                # iOS에서 덮어쓰기 버튼을 찾아 overwrite_btn로 넣기
                # Appium ID: btn_dialog_overwrite_confirm
                overwrite_xpath = "//*[@content-desc='btn_dialog_overwrite_confirm' or @name='덮어쓰기' or @label='덮어쓰기']"
                overwrite_btn = short_wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, overwrite_xpath)))
            else:
                # AOS에서 덮어쓰기 버튼을 찾아 overwrite_btn로 넣기
                # Appium ID: btn_dialog_overwrite_confirm
                overwrite_btn = short_wait.until(
                    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_dialog_overwrite_confirm")))

            print("  - [기존 데이터 '덮어쓰기' 승인 시도]")
            overwrite_btn.click() # 덮어쓰기 버튼 클릭
        except TimeoutException:
            # 선언한 1.5초동안 덮어쓰기 버튼이 나오지 않을 경우 최초 저장으로 간주
            print("  - [최초 저장 완료 (덮어쓰기 없음)]")

        time.sleep(1)

    def load_preset(self, preset_name):
        """프리셋 불러오기"""
        print(f"\n[프리셋 '{preset_name}' 불러오기 시도]")

        if self.platform == "ios":
            # iOS 전용
            # Appium ID: btn_topbar_load
            # 화면의 모든 요소(//*[...])중에서 @content-desc, @name, @name, @label 4가지 요소에서 불러오기 버튼 찾기 시도
            load_btn_xpath = "//*[@content-desc='btn_topbar_load' or @name='btn_topbar_load' or @name='불러오기' or @label='불러오기']"
            # 조건에 맞는 버튼들(elements)을 찾아 load_btns에 넣기
            load_btns = self.wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH, load_btn_xpath)))
            load_btns[-1].click() # 찾은 버튼 중 화면 최상단에 올려져 있는 맨 마지막 요소(-1)의 버튼을 클릭 (화면 내부 팝업 너머의 버튼 클릭 시도 방지)
            time.sleep(2)

            # Appium ID: row_load_preset_{preset_name}
            # 찾아온 진짜 불러오기 버튼을 actual_btn_id에 대입
            actual_btn_id = f"row_load_preset_{preset_name}"
            # 진짜 불러오기 버튼이 나타나면 preset_btn에 대입
            preset_btn = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, actual_btn_id)))
            preset_btn.click() # 불러오기 버튼을 클릭
            time.sleep(2)
        else:
            # AOS 전용
            # Appium ID: btn_topbar_load
            # 단순히 btn_topbar_load를 찾아 클릭
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "btn_topbar_load"))).click()
            time.sleep(0.5)

            # Appium ID: row_load_preset_{preset_name}
            # 진짜 불러오기 버튼이 나타나면 preset_row_id에 대입하여 클릭
            preset_row_id = f"row_load_preset_{preset_name}"
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, preset_row_id))).click()
            time.sleep(1)