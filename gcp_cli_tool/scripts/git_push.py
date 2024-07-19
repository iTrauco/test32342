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
    if len(sys.argv) != 2:
        print("Usage: python script.py <new-branch-name>")
        sys.exit(1)

    new_branch_name = sys.argv[1]

    # Get the current working directory (existing repo)
    existing_repo_path = os.getcwd()

    # Prompt for the repo URL
    default_url = "https://github.com/iTrauco/geek-cli"
    use_default = input(f"Use default repo URL ({default_url})? [y/N]: ").strip().lower()
    
    if use_default == 'y':
        repo_url = default_url
    else:
        repo_url = input("Enter the URL of the local repository: ").strip()
    
    # Validate repo URL
    if not repo_url:
        print("Repository URL cannot be empty.")
        sys.exit(1)

    # Check if the new branch already exists in the existing repo
    try:
        result = subprocess.run("git branch --list " + new_branch_name, cwd=existing_repo_path, check=True, shell=True, text=True, capture_output=True)
        if result.stdout.strip():
            print(f"Branch '{new_branch_name}' already exists.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        pass

    # Create and switch to the new branch
    run_command(f"git checkout -b {new_branch_name}", cwd=existing_repo_path)
    
    # Add the new repository as a remote
    run_command(f"git remote add local-repo {repo_url}", cwd=existing_repo_path)
    
    # Fetch the content from the new repository
    run_command("git fetch local-repo", cwd=existing_repo_path)
    
    # Merge content from the fetched repository
    run_command(f"git merge local-repo/main --allow-unrelated-histories", cwd=existing_repo_path)
    
    # Commit the changes
    run_command("git add .", cwd=existing_repo_path)
    run_command(f"git commit -m 'Add content from {repo_url}'", cwd=existing_repo_path)
    
    # Push the new branch to the remote repository
    run_command(f"git push origin {new_branch_name}", cwd=existing_repo_path)
    
    print(f"Branch '{new_branch_name}' has been successfully created and pushed.")

if __name__ == "__main__":
    main()
