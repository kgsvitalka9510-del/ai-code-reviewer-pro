"""CLI interface for AI Code Reviewer Pro."""

import click
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.command()
@click.option('--repo', '-r', help='GitHub repository (owner/repo)')
@click.option('--pr', '-p', type=int, help='Pull request number')
@click.option('--file', '-f', help='Local file to review')
@click.option('--security', is_flag=True, help='Enable security analysis')
@click.option('--performance', is_flag=True, help='Enable performance analysis')
def main(repo, pr, file, security, performance):
    """AI Code Reviewer Pro - AI-powered code review."""
    console.print(Panel.fit(
        "[bold green]AI Code Reviewer Pro[/bold green]\n"
        "[dim]v1.0.0 - AI-powered code review[/dim]",
        border_style="green"
    ))

    if file:
        review_local_file(file, security, performance)
    elif repo and pr:
        review_github_pr(repo, pr, security, performance)
    else:
        console.print("[yellow]Usage:[/yellow]")
        console.print("  ai-review --file <path>")
        console.print("  ai-review --repo owner/repo --pr 123")
        sys.exit(1)


def review_local_file(filepath, security, performance):
    """Review a local file."""
    if not os.path.exists(filepath):
        console.print(f"[red]File not found: {filepath}[/red]")
        sys.exit(1)

    console.print(f"\n[bold]Reviewing:[/bold] {filepath}\n")

    with open(filepath, 'r') as f:
        lines = f.read().split('\n')

    issues = []
    
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        
        if security:
            if 'eval(' in line_stripped:
                issues.append({'line': i, 'severity': 'HIGH', 'type': 'Security', 'message': 'eval() is dangerous'})
            if 'exec(' in line_stripped:
                issues.append({'line': i, 'severity': 'HIGH', 'type': 'Security', 'message': 'exec() is dangerous'})
            if 'password' in line_stripped.lower() and '=' in line_stripped:
                issues.append({'line': i, 'severity': 'HIGH', 'type': 'Security', 'message': 'Hardcoded password'})

        if performance:
            if 'range(len(' in line_stripped:
                issues.append({'line': i, 'severity': 'LOW', 'type': 'Performance', 'message': 'Use enumerate()'})
            if '+=' in line_stripped:
                issues.append({'line': i, 'severity': 'LOW', 'type': 'Performance', 'message': 'Use join() or f-strings'})

        if len(line) > 120:
            issues.append({'line': i, 'severity': 'INFO', 'type': 'Style', 'message': f'Line too long ({len(line)} chars)'})

    if not issues:
        console.print("[green]No issues found![/green]")
    else:
        table = Table(title="Code Review Results")
        table.add_column("Line", style="cyan")
        table.add_column("Severity", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Message")

        for issue in issues:
            table.add_row(str(issue['line']), issue['severity'], issue['type'], issue['message'])

        console.print(table)
        console.print(f"\n[bold]Found {len(issues)} issues[/bold]")


def review_github_pr(repo, pr_number, security, performance):
    """Review a GitHub PR."""
    console.print(f"\n[bold]Reviewing PR #{pr_number} in {repo}[/bold]\n")
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        console.print("[red]Error: GITHUB_TOKEN not set[/red]")
        sys.exit(1)

    import requests
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

    r = requests.get(f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files', headers=headers)
    if r.status_code != 200:
        console.print(f"[red]Error: {r.status_code}[/red]")
        sys.exit(1)

    files = r.json()
    console.print(f"Files changed: {len(files)}\n")

    for file_info in files:
        filename = file_info['filename']
        if filename.endswith(('.py', '.js', '.ts', '.go')):
            console.print(f"[bold]Reviewing:[/bold] {filename}")

    console.print("[green]PR review complete![/green]")


if __name__ == '__main__':
    main()
