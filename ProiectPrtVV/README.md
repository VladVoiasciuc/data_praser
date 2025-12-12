# Parser Multi-Format de Date – Proiect Programarea Translatoarelor

**Tema 6** – Parsarea fișierelor cu date pentru a formata sau extrage informații  
Autor: [Numele tău complet + grupa]

## Ce face proiectul
- Parsează 5 tipuri de fișiere: JSON, XML, CSV, BibTeX, Markdown
- Folosește cel puțin 5 expresii regulate complexe
- Handlează edge cases (escaping, fișiere malformate, taguri neînchise etc.)
- Interfață linie de comandă cu argparse
- Bonus: opțiune `--json` pentru output frumos + detectare automată erori

## Utilizare
```bash
python data_parser.py --file test.json --type json --json
python data_parser.py --file test.csv --type csv