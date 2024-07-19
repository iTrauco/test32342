import os
import subprocess
import sys

def run_command(command, cwd=None):
    """ Run a shell command and handle errors. """
    try:
        result = subprocess.run(command, cwd=cwd, check=True, shell=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command `{command}`:\n{e.stderr}")
        sys.exit(1)

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python add_branch.py <branch-name> [new-branch-name]")
        sys.exit(1)

    new_branch_name = None
    if len(sys.argv) == 3:
        new_branch_name = sys.argv[2]
    else:
        # Prompt to create a new branch or use the current branch
        use_current_branch = input("Use the current branch? [y/N]: ").strip().lower()
        if use_current_branch == 'y':
            new_branch_name = subprocess.run("git branch --show-current", check=True, shell=True, text=True, capture_output=True).stdout.strip()
        else:
            new_branch_name = input("Enter the name for the new branch: ").strip()
    
    # Validate new branch name
    if not new_branch_name:
        print("Branch name cannot be empty.")
        sys.exit(1)

    # Get the current working directory (existing repo)
    existing_repo_path = os.getcwd()

    # Prompt for the repo URL
    default_url = "https://github.com/iTrauco/geek-cli.git"
    use_default = input(f"Use default repo URL ({default_url})? [y/N]: ").strip().lower()
    
    if use_default == 'y':
        repo_url = default_url
    else:
        repo_url = input("Enter the URL of the local repository: ").strip()
    
    # Validate repo URL
    if not repo_url:
        print("Repository URL cannot be empty.")
        sys.exit(1)

    # Remove the existing remote if it exists
    run_command("git remote remove local-repo || true", cwd=existing_repo_path)
    
    # Create and switch to the new branch if necessary
    current_branch = subprocess.run("git branch --show-current", check=True, shell=True, text=True, capture_output=True).stdout.strip()
    if new_branch_name != current_branch:
        run_command(f"git checkout -b {new_branch_name}", cwd=existing_repo_path)

    # Add the new repository as a remote
    run_command(f"git remote add local-repo {repo_url}", cwd=existing_repo_path)
    
    # Fetch the content from the new repository
    run_command("git fetch local-repo", cwd=existing_repo_path)
    
    # Merge content from the fetched repository
    run_command(f"git merge local-repo/main --allow-unrelated-histories", cwd=existing_repo_path)
    
    # Stage all changes
    run_command("git add -A", cwd=existing_repo_path)

    # Commit the changes
    commit_message = input("Enter a commit message (or press Enter to use the default): ").strip()
    if not commit_message:
        commit_message = "workflow testing, nothing special..."
    run_command(f"git commit -m \"{commit_message}\"", cwd=existing_repo_path)
    
    # Push the new branch to the remote repository
    run_command(f"git push origin {new_branch_name}", cwd=existing_repo_path)
    
    print(f"Branch '{new_branch_name}' has been successfully created, committed, and pushed.")

if __name__ == "__main__":
    main()
