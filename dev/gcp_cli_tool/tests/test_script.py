import subprocess
import os
import pytest

def test_scan_chrome_profiles():
    """Test the scan_chrome_profiles script."""
    # Temporarily make sure the script file is executable
    script_path = os.path.join('gcp_cli_tool', 'scripts', 'scan_chrome_profiles.py')
    os.chmod(script_path, 0o755)
    
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "Scanning Chrome profiles..." in result.stdout
