Regenerate simulation data and refresh project context.

1. Re-run the simulation to produce a fresh `data/simulation_results.csv`:
   ```
   cd 5g-digital-twin-simulator && python main.py --config config.json
   ```
2. Print the simulation summary output.
3. Read the updated `data/simulation_results.csv` and show: row count, column names, and key stats (mean throughput, mean cell load, user count).
4. Check if `CLAUDE.md` at the repo root is still accurate — flag any modules, files, or config options that have changed since it was last written.
5. If CLAUDE.md is stale, update it to reflect the current state of the project.
