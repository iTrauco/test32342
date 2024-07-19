# run_tests.py
import subprocess

def run_tests():
    result = subprocess.run(['pytest', '--maxfail=5', '--disable-warnings', '-q'], capture_output=True, text=True)
    with open('test_results.log', 'a') as log_file:
        log_file.write(result.stdout)
        log_file.write(result.stderr)

if __name__ == "__main__":
    run_tests()