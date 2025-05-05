# Axonius task1 - Airbnb Automated Test Suite

This repository contains an automated test suite for interacting with the Airbnb website.

---

## Prerequisites

Before running the tests, ensure you have the following prerequisites installed:

- **Python 3.9+**: This test suite is written in Python, so ensure Python 3.9 or higher is installed.
- **Playwright**: Playwright is used for browser automation.
- **Allure**: For generating test reports.
- **Logging**: The test suite uses logging to capture logs during the execution.
---
### Install and Run

1. Clone the repository:
   ```bash
   git clone git@github.com:ppoltar/axonius_task1.git
   cd axonius_task1.git
    ```
2. Give Permissions:
    ```bash
    chmod -R +x .
    ```
3. Run setup bash script:
    ```bash
    ./setup.sh
    source venv/bin/activate
    ```
4. Run tests:
   ```bash
   pytest --suite-timeout 900
   ```
   
*** Run with Docker (after step 1):
   ```bash
   make install
   ```
--- 
### Project Structure

```bash
├── locators/               
│   ├── airbnb_locators.py  
│   ├── basepage_locators.py
│   └── rooms_locators.py    
├── pages/                  
│   ├── base_page.py   
│   ├── rooms_locators.py        
│   └── airbnb_main_page.py  
├── tests/                  
│   ├── e2e_data.py
│   └── e2e_test.py                        
├── requirements.txt        
├── README.md
├── conftest
├── pytest.ini
├── setup.sh 
├── Makefile               
└── Dockerfile                
```
---
# Test Suite Overview

### 1. **E2E Test**
1. **Navigate to Airbnb**: Opens the Airbnb website.
2. **Search for Apartments**: Searches for apartments in Tel Aviv for 2 adults and a child, with random check-in and check-out dates.
3. **Validate Search Parameters**: Validates the search parameters in both the URL and the UI.
4. **Analyze Results**:
   - Identifies the cheapest result among the highest-rated ones.
   - Logs the details of the selected result and saves them to a JSON file in the “reports” folder.
5. **Attempt Reservation**:
   - Clicks the "Reserve" button.
   - Re-validates the reservation details and logs them, saving them to a JSON file in the “reports” folder.
---

## Reports and Logs

Report and Logs created automatically in run directory in folder with prefix <reports/>

### 1. Allure report
Allure files created automatically in reports/allure-results, 
Allure report generated automatically in reports/allure-report include index.html file.

You can generate the report by yourself with command:
```bash
allure generate reports/allure-results --clean -o reports/allure-report
```

In the test execution process, if a test fails, Allure will attach the following to the report:

- **Video Recording**
Each test is recorded, and the videos are saved in the reports/videos/ directory. The video is automatically attached to the Allure report if the test fails.

- **Screenshot**
If a test fails, a screenshot is automatically taken and stored in reports/screenshots/. It is then attached to the Allure report for further analysis.


### 2. Trace Files
Playwright captures trace files of each test execution. Trace files contain detailed information on every action performed during a test, including network requests, DOM states, and screenshots.

These trace files are saved in the reports/playwright-traces/ directory. If you encounter a failure, you can inspect the trace file for more detailed insights.

Viewing trace file is generated, you can view it using the Playwright Trace Viewer. 

You can run the following command to open the trace viewer:
```bash
playwright show-trace reports/playwright-traces/{test_name}-trace.zip
```


### 3. HTML Report
The HTML report is generated automatically using configuration in pytest.ini file.

You can open the generated HTML report directly in any browser by navigating to - **reports/report.html.**