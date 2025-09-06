from rich.console import Console
import random
from pathlib import Path

console = Console()

def snarky_cite():
    # Load snark comments from external file
    quotes_file = Path(__file__).parent / "snark_quotes.txt"
    if not quotes_file.exists():
        console.print(f"[red]Error: Quotes file not found: {quotes_file}[/red]")
        return
    try:
        quotes = [line.strip() for line in quotes_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        snark = random.choice(quotes)
    except Exception as e:
        console.print(f"[red]Error loading quotes: {e}[/red]")
        return

    console.print(f"[blue]\n— {snark}[/blue]")

if __name__ == "__main__":
    snarky_cite()
