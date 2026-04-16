import pytest
import os
import pytest_html
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Ensures folders exist BEFORE tests start (Professional Environment Setup)
def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless") # Ready for CI/CD pipelines
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(45) # Increased for network stability
    
    yield driver
    
    # --- AUTOMATIC SCREENSHOT LOGIC ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("screenshots", f"test_run_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"\nCaptured: {file_path}")
    
    driver.quit()

# --- LINK SCREENSHOT TO HTML REPORT ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    
    # Using 'extras' to avoid DeprecationWarnings
    extras = getattr(report, "extras", [])

    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver:
            # Embedded Base64 screenshot for a portable, self-contained HTML report
            screenshot = driver.get_screenshot_as_base64()
            extras.append(pytest_html.extras.image(screenshot, "Screenshot"))
        report.extras = extras