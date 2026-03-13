# Testing

## Unit Tests
- Tests for simulation engine, scheduler, user equipment, etc.
- Run with `pytest` or `unittest`

## UI Tests
- Selenium-based tests for dashboard UI
- Verifies both 'no results' and 'results present' states

## How to Run
- Backend: `pytest` or `python -m unittest`
- UI: `python -m unittest tests/test_dashboard_ui.py` and `tests/test_dashboard_ui_with_results.py`
