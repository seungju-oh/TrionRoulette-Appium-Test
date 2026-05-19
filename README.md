# AOS/iOS Roulette App - QA UI Automation Test

AI를 활용하여 직접 개발한 AOS(Jetpack Compose) / iOS(SwiftUI) 룰렛 앱을 대상으로 한 **Appium 크로스플랫폼 UI 자동화 테스트 프로젝트**입니다. 
하나의 테스트 스크립트로 두 운영체제(Android/iOS)의 핵심 기능과 예외 상황(Edge Cases)을 동시에 검증할 수 있도록 설계하였으며, 유지보수성과 확장성을 극대화하기 위해 **POM (Page Object Model)** 디자인 패턴을 적용했습니다.

## Target App
- [TrionRoulette for Android](https://github.com/seungju-oh/TrionRouletteAOS)
- [TrionRoulette for iOS](https://github.com/seungju-oh/TrionRouletteAOS)

## Tech Stack
- **Language:** Python 3.x
- **Testing Framework:** Pytest
- **Automation Tool:** Appium, Selenium WebDriver
- **Appium Driver:** UIAutomator2 (Android), XCUITest (iOS)
- **Target OS:** Android, iOS

## Project Architecture (POM)
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

## Key Test Scenarios & Coverage
Full TC: [Roulette_Testsuit](https://docs.google.com/spreadsheets/d/e/2PACX-1vQhfKgoulnXGsKzU27oW8cVXLnvv9xbmZtBpArXROjRXamM5n7OGvxu8kdv9H1nkJhDt1kyCU9LNZa5/pubhtml)

이 프로젝트는 단순한 해피 패스(Happy Path) 검증을 넘어, 모바일 앱 환경에서 발생할 수 있는 다양한 예외 상황에 대한 방어 로직을 꼼꼼하게 검증합니다.

| 분류 | 주요 검증 시나리오 (Test Cases) |
| --- | --- |
| **공통 (Mode A)** | - 최소 항목(2개) 미만 삭제 시 방어 로직 작동 확인<br>- 빈 텍스트("") 입력 시 스핀 버튼 비활성화 검증<br>- 스핀 버튼 중복 클릭(따닥) 방어 검증 |
| **서바이벌 (Mode B)** | - 룰렛 결과에 따른 당첨 항목 비활성화(Dim) 및 재스핀 제외 검증<br>- 모든 항목 당첨 완료 후 상태 자동 초기화 및 무결성 검증 |
| **확률/가챠 (Mode C)** | - 소수점 둘째 자리(n.nn%) 초과 입력 시 정규식 마스킹 방어 검증<br>- 0% 확률 입력 시 동적 렌더링 및 당첨 풀(Pool) 제외 확인<br>- 확률 총합 부동소수점 오차(99.99%, 100.01%) 시 스핀 방어 검증 |
| **데이터 무결성** | - 현재 룰렛 상태(메뉴명, 커스텀 확률) 프리셋 저장 및 동적 덮어쓰기 분기 처리 검증<br>- 데이터 임의 훼손 후 프리셋 불러오기를 통한 UI/데이터 완벽 복구 검증 |

## Troubleshooting (주요 트러블슈팅)

**1. 선언형 UI(Compose / SwiftUI) 접근성 트리 동기화(State Sync) 이슈 해결**
- **문제:** Jetpack Compose와 SwiftUI 특성상 버튼의 활성화/비활성화 상태(`enabled`)가 변경될 때 Appium이 이를 즉각적으로 인식하지 못하거나 과거의 캐시 된 속성을 반환하는 버그 발생.
- **해결 방안:** 앱 개발 코드(Kotlin, Swift)에 개입하여 UI 컴포넌트 상태에 따라 변하는 **동적 ID(Stateful ID)** 적용 (예: `btn_spin_enabled`, `btn_spin_disabled`). Appium이 요소의 속성(Attribute)을 우회 검사하는 대신, 화면 내 특정 ID의 존재 여부(Presence)를 스캔하도록 검증 로직을 고도화하여 두 OS 모두에서 테스트의 견고함(Robustness) 확보.

**2. 텍스트 지우기 버그(Silent Fail) 우회 및 크로스플랫폼 대응**
- **문제:** Appium의 `.clear()` 함수가 Compose의 `OutlinedTextField`나 iOS `TextField`에서 에러 없이 무시되는 현상 발생.
- **해결 방안:** Android의 경우 키보드 커서를 강제로 맨 뒤로 이동(`KEYCODE_MOVE_END`)시킨 후, 물리적인 백스페이스(`KEYCODE_DEL`) 이벤트를 반복 전송하고, iOS의 경우 문자열 길이만큼 `\b` (백스페이스)를 전송하도록 Page Object 내에 **OS 분기형 물리적 텍스트 삭제 로직**을 구현하여 완벽한 데이터 초기화 성공.

**3. 단일 식별자(Single Locator) 전략 수립
- **문제:** 안드로이드와 iOS의 UI 요소 접근 방식이 달라 유지보수 포인트가 2배로 늘어나는 문제.
- **해결 방안:** 개발 단계에서부터 Android의 `Modifier.semantics { contentDescription = "ID" }`와 iOS의 `.accessibilityIdentifier("ID")`를 1:1로 완벽히 동일하게 부여. 이를 통해 Appium Page Object에서 `By.ACCESSIBILITY_ID` 하나만으로 두 플랫폼의 UI 요소를 동시에 찾을 수 있는 크로스플랫폼 자동화 달성.

## How to Run

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
