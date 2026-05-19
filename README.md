# AI-Assisted AOS/iOS Roulette App - QA UI Automation Test Portfolio

AI를 활용하여 직접 개발한 AOS(Jetpack Compose) / iOS(SwiftUI) 룰렛 앱을 대상으로 한 **Appium 크로스플랫폼 UI 자동화 테스트 프로젝트**입니다. 
하나의 테스트 스크립트로 두 운영체제(Android/iOS)의 핵심 기능과 예외 상황(Edge Cases)을 동시에 검증할 수 있도록 설계하였으며, 유지보수성과 확장성을 극대화하기 위해 **POM (Page Object Model)** 디자인 패턴을 적용했습니다.

---

## 📑 목차 (Table of Contents)
1. [🎬 Demo (시연 영상)](#-demo-시연-영상)
2. [🛠️ Tech Stack & Target App](#️-tech-stack--target-app)
3. [🏗️ Project Architecture (POM)](#️-project-architecture-pom)
4. [🤖 AI-Assisted Development (AI 활용 및 한계 극복)](#-ai-assisted-development-ai-활용-및-한계-극복)
5. [🧪 Key Test Scenarios & Coverage](#-key-test-scenarios--coverage)
6. [🔥 Troubleshooting (주요 트러블슈팅)](#-troubleshooting-주요-트러블슈팅)
7. [⚡ Test Optimization Strategy (테스트 최적화 전략)](#-test-optimization-strategy-테스트-최적화-전략)
8. [💻 How to Run (실행 방법)](#-how-to-run-실행-방법)

---

## 🎬 Demo (시연 영상)
[![Watch the demo](https://img.youtube.com/vi/TJylaLFEBDg/mqdefault.jpg)](https://www.youtube.com/watch?v=TJylaLFEBDg)
> 썸네일을 클릭하여 YouTube에서 전체 데모를 시청하실 수 있습니다.

## 🛠️ Tech Stack & Target App
- **Language:** Python 3.14
- **Testing Framework:** Pytest
- **Automation Tool:** Appium, Selenium WebDriver
- **Appium Driver:** UIAutomator2 (Android), XCUITest (iOS)
- **Target OS:** Android, iOS
- **Target App Repositories:**
  - [TrionRoulette for Android](https://github.com/seungju-oh/TrionRouletteAOS)
  - [TrionRoulette for iOS](https://github.com/seungju-oh/TrionRouletteiOS)
- **Assist AI:** Google Gemini 3.1 Pro Standard

## 🏗️ Project Architecture (POM)
> 안드로이드의 `contentDescription`과 iOS의 `accessibilityIdentifier`를 1:1로 완벽하게 매칭하여, 단일 테스트 스크립트(`tests/`)가 플랫폼에 구애받지 않고 동일한 `RoulettePage` 객체를 통해 UI를 제어하도록 설계했습니다.

```
📦 TionRouletteTest
 ┣ 📂 pages
 ┃ ┗ 📜 roulette_page.py   # Android/iOS 공용 화면 요소(Locators) 및 주요 동작(Actions) 모음
 ┣ 📂 tests
 ┃ ┣ 📜 conftest.py        # OS별 Appium Driver 동적 초기화 및 셋업/티어다운 로직
 ┃ ┣ 📜 test_mode_a.py     # 공통 로직 및 기본 모드 검증
 ┃ ┣ 📜 test_mode_b.py     # 서바이벌 모드 전용 검증
 ┃ ┣ 📜 test_mode_c.py     # 커스텀 확률 모드 전용 검증
 ┃ ┗ 📜 test_preset.py     # 데이터 저장 및 복구(프리셋) 검증
```

## 🤖 AI-Assisted Development (AI 활용 및 한계 극복)

본 프로젝트는 기획부터 테스트 코드 구현까지 **Google Gemini**를 적극적으로 활용한 AI 주도 개발(AI-Driven Development) 방식으로 진행되었습니다. 코드를 단순히 생성하는 것을 넘어, AI가 가진 한계와 편향을 인지하고 이를 QA 엔지니어의 도메인 지식으로 통제하는 프롬프트 엔지니어링 역량을 증명하는 데 집중했습니다.

### 1. 주요 AI 활용 범위 (How I used AI)
- **보일러플레이트 및 아키텍처 설계:** Page Object Model(POM)의 초기 뼈대 클래스와 폴더 구조를 빠르게 스캐폴딩(Scaffolding)하여 세팅 시간을 대폭 단축했습니다.
- **크로스플랫폼 하이브리드 검색기 생성:** 안드로이드와 iOS의 파편화된 속성(text, label, name)을 통합하여 검색할 수 있는 복잡한 XPath 쿼리를 AI를 통해 빠르고 정확하게 도출했습니다.

### 2. AI의 한계 극복 및 프롬프트 엔지니어링 사례 (Troubleshooting with AI)

**① 플랫폼 특유의 버그에 대한 AI의 '표준 문법 맹신' 극복**
- **이슈:** AI는 텍스트를 지울 때 무조건 Appium의 표준 문법인 `element.clear()`를 제안했습니다. 하지만 Android Jetpack Compose 환경에서는 이 명령어가 무시되고 기존 텍스트 뒤에 새 글자가 이어붙는 'Silent Fail(조용한 에러)' 버그가 발생했습니다.
- **극복:** AI의 제안을 맹신하지 않고 현상을 직접 분석한 뒤, "clear() 대신 안드로이드 시스템 키코드(`KEYCODE_MOVE_END`, `KEYCODE_DEL`)를 활용해 물리적으로 백스페이스를 20번 연타하는 우회(Workaround) 로직으로 다시 짜줘"라고 명확히 프롬프팅하여 문제를 완벽히 해결했습니다.

**② UI 렌더링 딜레이를 무시하는 AI의 '이상적인 논리' 통제**
- **이슈:** AI는 팝업 애니메이션이나 렌더링에 소요되는 '물리적인 시간'을 인지하지 못하고, 코드가 실행되자마자 즉각적으로 다음 요소를 클릭하도록 작성하여 잦은 `Timeout` 에러를 유발했습니다.
- **극복:** AI가 임시방편으로 남발하는 정적 대기(`time.sleep`)를 걷어내고, 상황에 맞게 1.5초짜리 초단기 대기조와 20초짜리 장기 대기조(`WebDriverWait`)를 혼용하는 **'동적 대기(Dynamic Wait) 아키텍처'를** 직접 기획하여 AI의 코드 구조를 전면 교정했습니다.

**③ AI의 'Happy Path' 편향을 깨는 엣지 케이스 주입**
- **이슈:** AI에게 프리셋 저장/불러오기 테스트 코드를 요청하면, 저장 직후 그 자리에서 바로 불러오는 단순하고 순조로운(Happy Path) 시나리오만 생성하여 QA 테스트로서의 변별력이 떨어졌습니다.
- **극복:** AI에게 **"저장 직후, 일부러 화면 모드를 바꾸고 더미 데이터를 잔뜩 입력하여 화면을 완전히 오염(Data Pollution)시켜라. 그 상태에서 프리셋을 불러와야 진짜 무결성 검증이다**라는 시나리오 흐름을 강제 주입했습니다. 이를 통해 AI가 단순 반복 코드가 아닌 현업 수준의 깐깐한 교차 검증 로직을 작성하도록 리드했습니다.

### 3. '블랙박스'를 거부하는 코드 오너십 (Code Ownership) 확보
- **단순 Copy & Paste 지양:** AI가 생성한 코드를 '제대로 작동하니까 넘어가는' 블랙박스(Black-box)처럼 취급하지 않았습니다. 
- **한 줄 단위 분석과 내재화:** 코드를 프로젝트에 적용하기 전, Appium의 `WebDriverWait`, 크로스플랫폼 `Locator` 전략, 모바일 UI 렌더링 생명주기 등 핵심 로직을 한 줄 한 줄 분석하고 **저만의 언어로 상세한 주석(Annotation)을 작성**했습니다.
- **결과:** 이 과정을 통해 AI의 산출물을 단순 '차용'하는 것에 그치지 않고, 자동화 프레임워크의 동작 원리를 100% 나의 것으로 '내재화(Internalize)'하여 코드에 대한 완벽한 통제권과 오너십을 확보했습니다.

### 4. Lesson Learned (배운 점)
AI는 압도적인 속도를 자랑하는 훌륭한 타이피스트지만, 완벽한 QA 엔지니어는 아니라는 것을 배웠습니다. 맹목적인 코드 복사-붙여넣기가 아닌, 로직의 주도권을 인간이 쥐고 지속해서 엣지 케이스를 검증하는 **Human-in-the-Loop** 방식의 중요성을 깊이 체감했습니다. AI를 도구로서 완벽히 통제할 때 비로소 앱의 품질을 극한으로 끌어올릴 수 있음을 증명한 프로젝트입니다.

## 🧪 Key Test Scenarios & Coverage
Full TC: [Roulette_Testsuit](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhfKgoulnXGsKzU27oW8cVXLnvv9xbmZtBpArXROjRXamM5n7OGvxu8kdv9H1nkJhDt1kyCU9LNZa5/pubhtml)

이 프로젝트는 단순한 해피 패스(Happy Path) 검증을 넘어, 모바일 앱 환경에서 발생할 수 있는 다양한 예외 상황에 대한 방어 로직을 꼼꼼하게 검증합니다.

| 분류 | 주요 검증 시나리오 (Test Cases) |
| --- | --- |
| **공통 (Mode A)** | - 최소 항목(2개) 미만 삭제 시 방어 로직 작동 확인<br>- 빈 텍스트("") 입력 시 스핀 버튼 비활성화 검증<br>- 스핀 버튼 중복 클릭(따닥) 방어 검증 |
| **서바이벌 (Mode B)** | - 룰렛 결과에 따른 당첨 항목 비활성화(Dim) 및 재스핀 제외 검증<br>- 모든 항목 당첨 완료 후 상태 자동 초기화 및 무결성 검증 |
| **확률/가챠 (Mode C)** | - 소수점 둘째 자리(n.nn%) 초과 입력 시 정규식 마스킹 방어 검증<br>- 0% 확률 입력 시 동적 렌더링 및 당첨 풀(Pool) 제외 확인<br>- 확률 총합 부동소수점 오차(99.99%, 100.01%) 시 스핀 방어 검증 |
| **데이터 무결성 및 상태 복구** | - 현재 룰렛 상태(메뉴명, 커스텀 확률) 프리셋 저장 및 동적 덮어쓰기 경고 팝업 처리(Dynamic Wait) 검증<br>- **화면 오염(Data Pollution) 기법** 적용: 저장 직후 모드 변경 및 더미 데이터를 주입하여 UI를 완전히 훼손한 뒤, 프리셋 불러오기를 수행하여 원래 데이터가 원상 복구되는지 3중 교차 검증 (개수, 텍스트, 확률). |


## 🔥 Troubleshooting (주요 트러블슈팅)

**1. 선언형 UI(Compose / SwiftUI) 접근성 트리 동기화(State Sync) 이슈 해결**
- **문제:** Jetpack Compose와 SwiftUI 특성상 버튼의 활성화/비활성화 상태(`enabled`)가 변경될 때 Appium이 이를 즉각적으로 인식하지 못하거나 과거의 캐시 된 속성을 반환하는 버그 발생.
- **해결 방안:** 앱 개발 코드(Kotlin, Swift)에 개입하여 UI 컴포넌트 상태에 따라 변하는 **동적 ID(Stateful ID)** 적용 (예: `btn_spin_enabled`, `btn_spin_disabled`). Appium이 요소의 속성(Attribute)을 우회 검사하는 대신, 화면 내 특정 ID의 존재 여부(Presence)를 스캔하도록 검증 로직을 고도화하여 두 OS 모두에서 테스트의 견고함(Robustness) 확보.

**2. 텍스트 지우기 버그(Silent Fail) 우회 및 크로스플랫폼 대응**
- **문제:** Appium의 `.clear()` 함수가 Compose의 `OutlinedTextField`나 iOS `TextField`에서 에러 없이 무시되는 현상 발생.
- **해결 방안:** Android의 경우 키보드 커서를 강제로 맨 뒤로 이동(`KEYCODE_MOVE_END`)시킨 후, 물리적인 백스페이스(`KEYCODE_DEL`) 이벤트를 반복 전송하고, iOS의 경우 문자열 길이만큼 `\b` (백스페이스)를 전송하도록 Page Object 내에 **OS 분기형 물리적 텍스트 삭제 로직**을 구현하여 완벽한 데이터 초기화 성공.

**3. 단일 식별자(Single Locator) 전략 수립**
- **문제:** 안드로이드와 iOS의 UI 요소 접근 방식이 달라 유지보수 포인트가 2배로 늘어나는 문제.
- **해결 방안:** 개발 단계에서부터 Android의 `Modifier.semantics { contentDescription = "ID" }`와 iOS의 `.accessibilityIdentifier("ID")`를 1:1로 완벽히 동일하게 부여. 이를 통해 Appium Page Object에서 `By.ACCESSIBILITY_ID` 하나만으로 두 플랫폼의 UI 요소를 동시에 찾을 수 있는 크로스플랫폼 자동화 달성.

**4. iOS 팝업 중복 DOM(Shadow Element) 및 터치 영역(Hitbox) 버그 해결**
- **문제:** iOS에서 프리셋 저장/불러오기 팝업이 뜰 때, 배경에 가려진 동일한 이름의 기존 버튼이 DOM에 남아있어 `find_element` 시 엉뚱한 곳을 클릭하거나, 버튼 크기에 비해 실제 터치 판정 영역이 좁아 `.click()`이 무시되는 현상 발생.
- **해결 방안:** 요소들을 `find_elements`로 모두 찾은 뒤 파이썬 리스트의 맨 마지막 요소(`[-1]`)를 선택하여 항상 최상단 팝업의 버튼을 누르도록 해결. 또한, 터치 무시 버그는 `execute_script("mobile: tap", {"x": 5, "y": 5})`를 사용해 버튼의 좌측 상단을 핀포인트로 물리 타격하는 우회(Workaround) 기법을 적용.

**5. AOS Jetpack Compose 텍스트 추출 한계 극복 (XML 투망 검증)**
- **문제:** Android 환경에서 비정상적인 값(소수점 3자리 등)을 고속 타자 입력 시, UI 요소 내부의 텍스트를 `el.text`로 정밀하게 추출하려 하면 캐시(Cache)된 이전 데이터를 읽어오거나 렌더링 지연으로 빈 값을 반환하는 문제.
- **해결 방안:** 특정 요소에 얽매이지 않고, Appium의 `driver.page_source`를 활용해 현재 화면에 그려진 전체 XML 구조를 문자열로 추출. 이를 통해 화면 어딘가에 비정상 데이터가 단 한 글자라도 노출(Leak)되었는지 이중 검증(`not in` 과 `in` 결합)하는 '데이터 무결성 투망 스캔' 로직을 구축.

**6. 속성(Attribute) 파편화에 대응하는 하이브리드 XPath 설계**
- **문제:** 결과 팝업 등에서 OS(AOS/iOS)와 프레임워크 구현 방식에 따라 텍스트가 `@text`, `@label`, `@name` 등 서로 다른 속성에 파편화되어 담기는 문제.
- **해결 방안:** `//*[contains(@text, '결과') or contains(@label, '결과') or contains(@name, '결과')]` 와 같이 `or` 조건으로 묶은 하이브리드 XPath 검색 구축. 단 한 줄의 쿼리로 OS나 개발 구현 방식의 변경에 구애받지 않고 견고하게 텍스트를 추출해 내는 유지보수성 확보.

## ⚡ Test Optimization Strategy (테스트 최적화 전략)
- **Appium Lifecycle 제어:** `conftest.py`에서 `no_reset = True` 옵션으로 무거운 드라이버 세션 생성은 테스트 전체에서 딱 1번만 수행하고, 각 단위 테스트(`scope="function"`)가 시작될 때마다 `terminate_app` / `activate_app`을 호출하여 1~2초 만에 앱을 초기(Clean) 상태로 되돌리도록 극도로 최적화했습니다.
- **동적 대기(Dynamic Wait):** 불안정한 `time.sleep()` 사용을 최소화하고, `WebDriverWait`과 예외 처리(`TimeoutException`)를 결합하여 안 뜰지도 모르는 팝업(덮어쓰기 경고 등)을 단 1.5초 만에 판별하고 넘어가는 척후병 로직을 구현해 전체 테스트 소요 시간을 대폭 단축했습니다.

## 💻 How to Run

해당 자동화 테스트를 실행하기 위한 명령어입니다.

```bash
# AOS/iOS 전체 테스트 슈트 한 번에 실행 (추천)
python -m pytest tests/ --platform android -v -s
python -m pytest tests/ --platform ios -v -s

# 특정 모드만 단독으로 실행하고 싶을 때
python -m pytest tests/test_mode_a.py --platform android -v -s
python -m pytest tests/test_mode_b.py --platform android -v -s
python -m pytest tests/test_mode_c.py --platform android -v -s
python -m pytest tests/test_preset.py --platform android -v -s

python -m pytest tests/test_mode_a.py --platform ios -v -s
python -m pytest tests/test_mode_b.py --platform ios -v -s
python -m pytest tests/test_mode_c.py --platform ios -v -s
python -m pytest tests/test_preset.py --platform ios -v -s
