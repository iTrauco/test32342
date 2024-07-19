import os
import subprocess
import argparse

def create_directory_structure(root_dir):
    dirs = [
        os.path.join(root_dir, 'gcp_cli_tool'),
        os.path.join(root_dir, 'gcp_cli_tool', 'commands'),
        os.path.join(root_dir, 'gcp_cli_tool', 'sample_functions'),
        os.path.join(root_dir, 'gcp_cli_tool', 'scripts'),
        os.path.join(root_dir, 'gcp_cli_tool', 'tests'),
        os.path.join(root_dir, 'gcp_cli_tool', 'test_utils'),
        os.path.join(root_dir, 'gcp_cli_tool', 'utils')
    ]
    
    files = {
        os.path.join(root_dir, 'gcp_cli_tool', 'cli.py'): '''import click
from gcp_cli_tool.commands.hello import hello

@click.group()
def cli():
    """A simple CLI tool."""
    pass

@cli.command()
def greet():
    """Greet the user."""
    hello()

if __name__ == "__main__":
    cli()
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'commands', 'hello.py'): '''def hello():
    """Print a hello message."""
    print("Hello from the hello command!")
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'dependencies.py'): '''# Placeholder for future dependencies or configuration
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'post_install.py'): '''# Placeholder for post-installation scripts or configuration
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'README.md'): '',  # Placeholder for README content
        os.path.join(root_dir, 'gcp_cli_tool', 'requirements.txt'): '''click
pytest
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'sample_functions', 'example_function.py'): '''def hello_world(request):
    """Return a hello world message."""
    return "Hello, World!"
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'scripts', 'scan_chrome_profiles.py'): '''def scan_chrome_profiles():
    """Functionality to scan Chrome profiles."""
    print("Scanning Chrome profiles...")
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'setup.py'): '''from setuptools import setup, find_packages

setup(
    name='gcp_cli_tool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Dependencies are listed in requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'gcp-cli = gcp_cli_tool.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'conftest.py'): '''# Configuration file for pytest, if needed
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_cli.py'): '''from click.testing import CliRunner
from gcp_cli_tool.cli import cli

def test_cli_greet():
    """Test the greet command in the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli, ['greet'])
    assert result.exit_code == 0
    assert "Hello from the hello command!" in result.output
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_chrome_utils.py'): '''from gcp_cli_tool.utils.chrome_utils import get_chrome_profiles

def test_get_chrome_profiles():
    """Test the get_chrome_profiles utility function."""
    result = get_chrome_profiles()  # Assuming it returns some value
    assert result is None  # Update this assertion based on actual function behavior
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_display_chrome_profiles.py'): '''# Placeholder for testing display of Chrome profiles
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_gcloud_utils.py'): '''# Placeholder for testing Google Cloud utilities
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_hello.py'): '''# Placeholder for testing hello command
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', 'test_sample.py'): '''# Placeholder for testing sample functions
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'test_utils', 'test_data_collector.py'): '''# Placeholder for testing data collector utilities
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'test_utils', 'test_logger.py'): '''# Placeholder for testing logger utilities
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'test_utils', 'test_sheets_exporter.py'): '''# Placeholder for testing sheets exporter utilities
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'utils', 'chrome_utils.py'): '''def get_chrome_profiles():
    """Functionality to get Chrome profiles."""
    pass
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'utils', 'gcloud_utils.py'): '''def get_gcloud_info():
    """Functionality to get Google Cloud info."""
    pass
''',
        os.path.join(root_dir, 'gcp_cli_tool', 'utils', '__init__.py'): '',
        os.path.join(root_dir, 'gcp_cli_tool', 'commands', '__init__.py'): '',
        os.path.join(root_dir, 'gcp_cli_tool', 'sample_functions', '__init__.py'): '',
        os.path.join(root_dir, 'gcp_cli_tool', 'scripts', '__init__.py'): '',
        os.path.join(root_dir, 'gcp_cli_tool', 'tests', '__init__.py'): '',
        os.path.join(root_dir, 'gcp_cli_tool', 'test_utils', '__init__.py'): ''
    }
    
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
    
    for file, content in files.items():
        with open(file, 'w') as f:
            f.write(content)

def initialize_git_repo_and_venv(root_dir):
    absolute_root_dir = os.path.abspath(root_dir)
    subprocess.run(["git", "init", absolute_root_dir], check=True)
    subprocess.run(["git", "-C", absolute_root_dir, "add", "."], check=True)
    subprocess.run(["git", "-C", absolute_root_dir, "commit", "-m", "Initial commit"], check=True)
    
    # Create and activate a virtual environment
    venv_path = os.path.join(absolute_root_dir, 'venv')
    subprocess.run(["python3", "-m", "venv", venv_path], check=True)
    
    pip_path = os.path.join(venv_path, 'bin', 'pip')
    requirements_path = os.path.join(absolute_root_dir, 'gcp_cli_tool', 'requirements.txt')
    
    # Install requirements
    subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
    
    # Open VS Code
    subprocess.run(["code", "."], cwd=absolute_root_dir, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up a new project structure.')
    parser.add_argument('root_dir', type=str, help='The name of the root directory for the project')
    args = parser.parse_args()

    create_directory_structure(args.root_dir)
    initialize_git_repo_and_venv(args.root_dir)
    print(f"Project structure created and initialized successfully in '{args.root_dir}'.")
