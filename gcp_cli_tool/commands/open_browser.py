# gcp_cli_tool/commands/open_browser.py
import webbrowser
import sys

def open_browser(url):
    """Open the specified URL in the default browser."""
    try:
        webbrowser.open(url)
        print(f"Opening URL: {url}")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m gcp_cli_tool.commands.open_browser <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    open_browser(url)