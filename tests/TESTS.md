# Test Documentation for 5G Digital Twin Simulator

This document describes the test strategy, test cases, and coverage for both backend and frontend components of the 5G Digital Twin Simulator.

## 1. Test Strategy
- **Unit Tests:** Validate individual functions (KPI calculations, utility functions).
- **Integration Tests:** Validate simulation runs, CSV output, and dashboard data loading.
- **System/UI Tests:** Validate dashboard metrics, charts, and error messages.
- **Negative/Edge Cases:** Test invalid configs, empty/malformed CSV, and extreme values.

## 2. Test Cases

### Backend
- **KPI Functions:**
  - Test with known input/output for each KPI (including edge cases: zero users, zero bandwidth, all equal allocations).
- **Simulation Engine:**
  - Run with 0, 1, many users; 0, low, high bandwidth; different schedulers.
  - Assert all required columns in metrics and CSV.
  - Test config overrides and error handling.
- **CSV Output:**
  - Validate file creation, column order, and data integrity.
  - Test with file write errors (e.g., permission denied).
- **Error Handling:**
  - Simulate and assert on invalid configs, missing dependencies, and runtime exceptions.

### Frontend
- **Dashboard Data Loading:**
  - Test with valid, empty, and malformed CSV.
  - Assert all KPIs are loaded and displayed.
- **Metrics Display:**
  - Check correct values for each metric at last timestep.
  - Test with extreme values (very high/low KPIs).
- **Charts:**
  - Assert line charts render for all KPIs.
  - Test with missing columns (should show error/warning).
- **Error Messages:**
  - Simulate missing/empty/corrupt CSV and check user feedback.
- **Responsiveness:**
  - Test dashboard layout on different screen sizes.

## 3. Test Coverage
- All requirements and KPIs are covered.
- Edge cases and error handling are explicitly tested.
- Test documentation is clear and up to date.

## 4. How to Run Tests
- Backend: `python -m pytest 5g-digital-twin-simulator/tests/`
- Frontend: Manual or automated UI testing (e.g., Selenium, Playwright).

## 5. Test Artifacts
- Test scripts: Located in `tests/`.
- Test results: Output by pytest or UI test runner.
- This documentation: `tests/TESTS.md`
