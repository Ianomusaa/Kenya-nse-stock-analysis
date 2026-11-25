from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent

SCRIPTS = [
    "data_collection.py",
    "data_quality.py",
    "metrics.py",
    "technical_analysis.py",
    "visualization.py"
]

print("=" * 60)
print("KENYA NSE STOCK ANALYSIS")
print("=" * 60)

for script_name in SCRIPTS:
    script_path = PROJECT_ROOT / "src" / script_name

    print(f"\nRunning {script_name}...")
    print("-" * 60)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True
    )

print("\n" + "=" * 60)
print("ALL ANALYSIS STEPS COMPLETED SUCCESSFULLY")
print("=" * 60)
