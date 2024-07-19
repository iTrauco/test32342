from click.testing import CliRunner
from gcp_cli_tool.cli import cli

def test_cli_greet():
    """Test the greet command in the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli, ['greet'])
    assert result.exit_code == 0
    assert "Hello from the hello command!" in result.output
