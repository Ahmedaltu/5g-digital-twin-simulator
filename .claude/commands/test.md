Run the full test suite and report results.

1. Run all tests across the repo:
   ```
   python -m pytest tests/ simulator/tests/ -v 2>&1
   ```
2. Also run the sub-package tests:
   ```
   cd 5g-digital-twin-simulator && python -m pytest tests/ -v 2>&1
   ```
3. Summarize:
   - Total tests passed / failed / errored
   - Any failing test names and their error messages
   - Any missing imports or setup issues
4. If there are failures, identify the root cause and suggest a fix.
