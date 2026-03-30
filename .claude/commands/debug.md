Run the simulator in debug mode and surface any errors or warnings.

1. Run the simulation with verbose output from the `5g-digital-twin-simulator` directory:
   ```
   cd 5g-digital-twin-simulator && python -u main.py 2>&1
   ```
2. Check the last 50 lines of `logs/dashboard.log` for any warnings or errors.
3. If the simulation produced `data/simulation_results.csv`, print a quick statistical summary of the output (shape, describe, any nulls).
4. Report any exceptions, missing files, or configuration issues found. Suggest fixes for anything broken.
