
# Snark

A Python tool for generating snarky citations from classical texts using MyCapytain.

## Description

Snark extracts passages from classical literature (e.g., Cicero, Virgil) and presents them in plain text format. Perfect for adding literary flair to your projects or just enjoying timeless wisdom with a twist.

## Installation

1. Install Python dependencies:
   ```bash
   uv install
   ```

2. Set up the texts corpus:
   - Create a `texts/` folder in the project root
   - Add TEI/XML formatted classical texts
   - Example: Download texts from [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/)

## Usage

Run the script to generate a citation:

```bash
python main.py
```

The `snarky_cite()` function will:
- Load the local corpus from `texts/`
- Select a work (e.g., Cicero's works)
- Retrieve a passage (currently hardcoded to "1.1")
- Export as plain text


## Requirements

- Python 3.8+
- MyCapytain library
- Rich (for console output)
- TEI/XML formatted texts in `texts/` folder

## Licenseß

See project license file.

## Links

- [MyCapytain Documentation](https://mycapytain.readthedocs.io/)
- [TEI Consortium](https://tei-c.org)
- [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/)