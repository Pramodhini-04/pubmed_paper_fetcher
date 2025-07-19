# PubMed Paper Fetcher

A CLI tool to search PubMed and extract research papers authored by individuals affiliated with non-academic (pharma/biotech) companies.

## 🔧 Installation

```bash
git clone https://github.com/your-username/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
poetry install
```

## 🚀 Usage

```bash
poetry run get-papers-list "cancer therapy"
```

With file output:
```bash
poetry run get-papers-list "lung cancer biomarkers" -f results.csv
```

Enable debug mode:
```bash
poetry run get-papers-list "covid vaccine" -d
```

## 🧪 CLI Options

- `-f`, `--file`: Specify filename to save output as CSV
- `-d`, `--debug`: Print debug logs
- `-h`, `--help`: Show help

## 🛠 Technologies Used

- Python 3.9+
- Poetry
- Typer (CLI framework)
- lxml (XML parser)
- pandas
- NCBI PubMed E-utilities
- LLM(Chatgpt)

## 📦 Publishing (bonus)

To publish the module to TestPyPI:

```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish -r test-pypi --build
```

## 👤 Author

Your Name – V.Gnana Pramodhini
Your Gmail -pramodinivennapusa2004@gmail.com
