# data_parser.py
# Proiect Programarea Translatoarelor – Tema 6
# Autor: Voiasciuc Vlad
# Parser multi-format (JSON, XML, CSV, BIB, Markdown) folosind expresii regulate

import re
import argparse
import json
import sys


def parse_json(content: str) -> dict:
    """Regex 1 și 2 – extrage chei și valori din JSON (include escaping)"""
    if not content.strip():
        raise ValueError("Fișier JSON gol sau invalid")

    # Chei între ghilimele (permite \" în interior)
    key_pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"\s*:'
    keys = re.findall(key_pattern, content)

    # Valori: stringuri, numere, true/false/null
    value_pattern = r':\s*"([^"\\]*(?:\\.[^"\\]*)*)"|:?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)|:\s*(true|false|null)\b'
    raw_values = re.findall(value_pattern, content)
    values = []
    for v in raw_values:
        # v este tuplu – luăm prima parte nenulă
        values.append(next(item for item in v if item != ""))

    if len(keys) != len(values):
        print("Avertisment: JSON-ul pare malformat (număr chei ≠ valori)")

    return dict(zip(keys, values))


def parse_xml(content: str) -> dict:
    """Regex 3 – extrage taguri cu atribute și conținut"""
    # <tag attr="val">conținut</tag>
    tag_pattern = r'<(\w+)\s*(.*?)(?:>(.*?)</\1>|/>)'
    matches = re.findall(tag_pattern, content, re.DOTALL)

    result = {}
    for tag_name, attrs_raw, content in matches:
        # Extragem atributele tagului
        attr_pattern = r'(\w+)="([^"]*)"'
        attrs = dict(re.findall(attr_pattern, attrs_raw))
        result[tag_name] = {"atribute": attrs, "continut": content.strip()}

    # Edge case: taguri neînchise
    if re.search(r'<(\w+)[^>]*(?<!/)>', content):
        print("Avertisment: Unele taguri XML nu sunt închise corect")
    return result


def parse_csv(content: str) -> list:
    """Regex 4 – parsează CSV cu câmpuri quoted care conțin virgulă"""
    if not content.strip():
        raise ValueError("Fișier CSV gol")

    # Acceptă câmpuri cu ghilimele (ex: "Ana, Maria") și fără
    row_pattern = r'(?:"([^"]*(?:""[^"]*)*)"|([^,\n]*))(?:,|$)'
    rows = []
    for line in content.splitlines():
        if not line.strip():
            continue
        matches = re.findall(row_pattern, line)
        row = [field[0] if field[0] else field[1] for field in matches]
        rows.append(row)

    # Edge case: număr coloane diferit
    lengths = [len(r) for r in rows if r]
    if lengths and len(set(lengths)) > 1:
        print(f"Avertisment: CSV cu număr inconsistent de coloane: {set(lengths)}")
    return rows


def parse_bib(content: str) -> dict:
    """Regex 5 – extrage intrări BibTeX"""
    # @article{key, author = {Ana}, ...}
    entry_pattern = r'@(\w+){([^,]+),\s*(.+?)}\s*(?=@|$)'
    entries = re.findall(entry_pattern, content, re.DOTALL)

    result = {}
    for entry_type, key, fields_raw in entries:
        # author = {Nume}, title = {Titlu} etc.
        field_pattern = r'(\w+)\s*=\s*{(.*?)}'
        fields = dict(re.findall(field_pattern, fields_raw, re.DOTALL))
        result[key.strip()] = {"tip": entry_type, "campuri": fields}

    if re.search(r'@\w+{[^}]*$', content):
        print("Avertisment: Există intrare .bib incompletă (lipsește })")
    return result


def parse_markdown(content: str) -> dict:
    """Bonus regex – headere și linkuri Markdown"""
    headers = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

    return {
        "headere": [(len(level), title.strip()) for level, title in headers],
        "linkuri": links
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parser multi-format – Proiect Programarea Translatoarelor (Tema 6)")
    parser.add_argument("--file", required=True, help="Calea către fișier")
    parser.add_argument("--type", required=True,
                        choices=["json", "xml", "csv", "bib", "md"],
                        help="Tipul fișierului")
    parser.add_argument("--json", action="store_true",
                        help="Afișează rezultatul ca JSON frumos (bonus)")

    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Eroare: Fișierul '{args.file}' nu a fost găsit!")
        sys.exit(1)

    try:
        if args.type == "json":
            rezultat = parse_json(content)
        elif args.type == "xml":
            rezultat = parse_xml(content)
        elif args.type == "csv":
            rezultat = parse_csv(content)
        elif args.type == "bib":
            rezultat = parse_bib(content)
        elif args.type == "md":
            rezultat = parse_markdown(content)

        print("\nRezultat parsare:")
        if args.json or args.type in ["json", "xml", "bib", "md"]:
            print(json.dumps(rezultat, indent=4, ensure_ascii=False))
        else:  # CSV – afișăm ca tabel
            for row in rezultat:
                print(" | ".join(row))
    except Exception as e:
        print(f"Eroare la parsare: {e}")


if __name__ == "__main__":
    main()