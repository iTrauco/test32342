# cli_setup.py

import os
import subprocess

def setup_project(root_dir):
    """Set up the new project directory with necessary files and structure."""
    # Create project directory
    os.makedirs(root_dir, exist_ok=True)
    
    # Create subdirectories and files
    subdirs = [
        'commands', 'scripts', 'utils', 'tests', 'test_utils'
    ]
    files = [
        'cli.py', 'dependencies.py', 'post_install.py', 'README.md', 'requirements.txt', 'setup.py'
    ]
    
    for subdir in subdirs:
        os.makedirs(os.path.join(root_dir, subdir), exist_ok=True)

    for file in files:
        with open(os.path.join(root_dir, file), 'w') as f:
            f.write(f'# {file} placeholder\n')

    # Sample command in commands/hello.py
    hello_command = '''\
# commands/hello.py

def hello():
    print("Hello from the CLI!")
'''
    with open(os.path.join(root_dir, 'commands/hello.py'), 'w') as f:
        f.write(hello_command)
    
    # Sample CLI entry point in cli.py
    cli_entry = '''\
# cli.py

import click
from commands.hello import hello

@click.command()
def cli():
    hello()

if __name__ == '__main__':
    cli()
'''
    with open(os.path.join(root_dir, 'cli.py'), 'w') as f:
        f.write(cli_entry)
    
    # Setup virtual environment and install packages
    subprocess.run(['python3', '-m', 'venv', 'venv'], check=True)
    subprocess.run(['venv/bin/pip', 'install', 'click'], check=True)
    subprocess.run(['venv/bin/pip', 'install', 'pytest'], check=True)

if __name__ == '__main__':
    setup_project('.')

