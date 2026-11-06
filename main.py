import subprocess
import sys

def run(script):
    print("Pipeline started")

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        sys.exit(1)

    else:
        print(f" [Pipeline] {script} zakończony ")

if __name__ == "__main__":

    run("scraper.py")

    run("parser.py")

    run("load_to_db.py")
    