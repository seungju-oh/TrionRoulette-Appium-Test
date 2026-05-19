import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# 1. 터미널에서 실행 시 --platform 옵션을 받을 수 있도록 설정
def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="android", help="테스트 대상 OS 선택: android 또는 ios"
    )

# 2. 선택된 플랫폼 값을 가져오는 픽스처
@pytest.fixture(scope="session")
def platform(request):
    return request.config.getoption("--platform").lower()

# 3. 플랫폼에 맞춰 드라이버를 단 한 번만 생성 (테스트 속도 최적화)
@pytest.fixture(scope="session")
def driver(platform):
    if platform == "ios":
        print("\n iOS(XCUITest) Appium 테스트 시작...")
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.automation_name = "XCUITest"
        options.platform_version = "26.5"
        options.device_name = "Torimaru’s iPhone 15 Pro 🇳🇱"
        options.bundle_id = "com.torimaru.TrionRoulette"
        options.udid = "(개인정보 GitHub 비공개)"
        options.xcode_org_id = "(개인정보 GitHub 비공개)"
        options.xcode_signing_id = "Apple Development"
        options.updated_wda_bundleid = "com.torimaru.WebDriverAgentRunner"
        options.use_prebuilt_wda = True
        options.no_reset = True  # 앱 재설치는 막고 세션만 유지

    elif platform == "android":
        print("\n Android(UiAutomator2) Appium 테스트 시작...")
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.automation_name = 'uiautomator2'
        options.device_name = 'Google Pixel 10 Pro'
        options.app_package = 'com.torimaru.trionroulette'
        options.app_activity = '.MainActivity'
        options.no_reset = True  # 앱 재설치는 막고 세션만 유지

    else:
        raise ValueError(f"유효하지 않은 OS: {platform}. 'android' 또는 'ios'")

    # Appium 서버 공통 연결
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    driver.implicitly_wait(10)

    yield driver

    print(f"\n {platform.upper()} Appium 테스트 종료...")
    driver.quit()

# 4. 각 테스트가 시작될 때마다 앱을 껐다 켜서(초기화) 깨끗한 상태를 만듭니다.
@pytest.fixture(scope="function", autouse=True)
def reset_app(driver, platform):
    print(f"\n {platform.upper()} Refreshing")

    # 플랫폼별 패키지명(Bundle ID) 분기 처리
    if platform == "ios":
        app_id = "com.torimaru.TrionRoulette"
    else:
        app_id = "com.torimaru.trionroulette"

    # 앱 강제 종료 후 다시 실행
    driver.terminate_app(app_id)
    driver.activate_app(app_id)

    yield  # 각각의 테스트 실행 지점