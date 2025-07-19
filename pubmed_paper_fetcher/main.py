import typer
import pandas as pd
import os
import re
from typing import Optional
from pubmed_paper_fetcher.pubmed import search_pubmed, fetch_details

app = typer.Typer()

def sanitize_filename(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name + ".csv"

@app.command()
def get_papers_list(
    query: str,
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Filename to save the CSV output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode")
):
    if debug:
        typer.echo(f"Searching PubMed for: {query}")

    ids = search_pubmed(query)
    if debug:
        typer.echo(f"Found {len(ids)} articles")

    data = fetch_details(ids)
    df = pd.DataFrame(data)

    if not file:
        file = sanitize_filename(query)

    base, ext = os.path.splitext(file)
    if not ext:
        file += ".csv"
    counter = 1
    original_file = file
    while os.path.exists(file):
        file = f"{base}_{counter}.csv"
        counter += 1
    if file != original_file:
        typer.echo(f"File {original_file} exists. Saving as {file} instead.")
    df.to_csv(file, index=False)
    typer.echo(f"Results saved to {file}")

if __name__ == "__main__":
    app()
