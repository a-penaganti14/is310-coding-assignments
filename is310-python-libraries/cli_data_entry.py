"""Collect college athletics spending records with a terminal interface."""
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
OUTPUT_FILE = Path(__file__).resolve().parent / "college_sports_spending.json"
FIELDS = ("School", "Year", "Category", "Amount USD", "Source")
EXAMPLES = [{'School': 'University of Illinois Urbana-Champaign', 'Year': '2024', 'Category': 'Total athletic expenses', 'Amount USD': 169474512.0, 'Source': 'https://www.knightnewhousedata.org/fbs/big-ten/university-illinois-urbana-champaign'}, {'School': 'University of Michigan', 'Year': '2024', 'Category': 'Total athletic expenses', 'Amount USD': 241856430.0, 'Source': 'https://www.knightnewhousedata.org/fbs/big-ten/university-michigan'}, {'School': 'Ohio State University', 'Year': '2024', 'Category': 'Total athletic expenses', 'Amount USD': 295174868.0, 'Source': 'https://www.knightnewhousedata.org/fbs/big-ten/ohio-state-university'}]


def show_records(records, title):
    table = Table(title=title)
    for field in FIELDS:
        table.add_column(field, style="cyan" if field == "School" else None)
    for record in records:
        table.add_row(*(f"${record[field]:,.2f}" if field == "Amount USD" else str(record[field]) for field in FIELDS))
    console.print(table)


def collect_record():
    while True:
        record = {}
        for field in FIELDS:
            while True:
                value = console.input(f"Enter {field}: ").strip()
                if not value:
                    console.print("Please enter a value.", style="red")
                    continue
                if field == "Year":
                    if not (value.isdigit() and len(value) == 4):
                        console.print("Enter a four-digit year.", style="red")
                        continue
                if field == "Amount USD":
                    try:
                        amount = float(value.replace(",", "").replace("$", ""))
                        if amount < 0 or not (amount < float("inf")):
                            raise ValueError
                        value = round(amount, 2)
                    except ValueError:
                        console.print("Enter a nonnegative dollar amount, like 250000.", style="red")
                        continue
                record[field] = value
                break
        show_records([record], "Review this record")
        answer = console.input("Is this correct? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return record
        console.print("Let's enter the record again.\n", style="yellow")


def main():
    console.print("[bold magenta]College Sports Spending Data Entry[/bold magenta]")
    console.print("Example spending amounts are verified 2024 totals from the Knight-Newhouse College Athletics Database.\n")
    show_records(EXAMPLES, "Example records")
    records = []
    console.print("\nEnter at least two records. Type the details for each record.\n")
    while True:
        records.append(collect_record())
        console.print(f"[green]Confirmed {len(records)} record(s).[/green]")
        if len(records) < 2:
            console.print("Please enter at least one more record.\n")
            continue
        answer = console.input("Would you like to add another record? (yes/no): ").strip().lower()
        if answer not in ("yes", "y"):
            break
    # Write only confirmed records, and preserve previously saved entries.
    existing = []
    if OUTPUT_FILE.exists():
        try:
            stored = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
            if isinstance(stored, list):
                existing = stored
        except (json.JSONDecodeError, OSError):
            console.print("Existing output is unreadable. No data was overwritten.", style="red")
            return
    all_records = existing + records
    OUTPUT_FILE.write_text(json.dumps(all_records, indent=2), encoding="utf-8")
    console.print(f"\n[bold green]Saved {len(records)} new records to:[/bold green] {OUTPUT_FILE.resolve()}")
    show_records(records, "Newly saved records")


if __name__ == "__main__":
    main() 
