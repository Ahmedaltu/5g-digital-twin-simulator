import os
import sys
import json
import subprocess
import pandas as pd
import tempfile

def test_simulation_respects_config_user_count():
    # Arrange: create a temp config file with a unique user count
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        output_file = os.path.join(tmpdir, "simulation_results.csv")
        config = {
            "simulation_steps": 5,
            "users": 40,
            "total_bandwidth_mbps": 100.0,
            "scheduler": "round_robin",
            "output_file": output_file
        }
        with open(config_path, "w") as f:
            json.dump(config, f)

        # Act: run the simulation via subprocess
        result = subprocess.run([
            sys.executable, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "5g-digital-twin-simulator", "main.py")),
            "--config", config_path
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Simulation failed: {result.stderr}"
        assert os.path.exists(output_file), "Output file not created"

        # Assert: check that all rows have the correct user count
        df = pd.read_csv(output_file)
        assert not df.empty, "Output CSV is empty"
        assert (df["users"] == 40).all(), f"Not all rows have 40 users: {df['users'].unique()}"
