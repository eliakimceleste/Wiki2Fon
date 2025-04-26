import os
import json
import re
import sys
def extract_articles_from_file(filepath):
    
    """
    Extract articles from a single extracted Wikipedia file.
    
    Args:
        filepath (str): Path to the extracted text file.

    Returns:
        list of dict: List of articles, each with id, title, url, and content.
    """
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    articles = []
    # Extract the documents using regex
    docs = re.findall(r'<doc id="(.*?)" url="(.*?)" title="(.*?)">(.*?)</doc>', content, re.DOTALL)
    for doc_id, url, title, body in docs:
        articles.append({
            "id": int(doc_id),
            "title": title,
            "url": url,
            "content": body.strip()
        })

    return articles


def build_database_from_extracted(folder_path, output_json='wikipedia_articles.json'):
    
    """
    Build a database from all extracted Wikipedia articles and save it as a JSON file.
    
    Args:
        folder_path (str): Path to the folder containing extracted Wikipedia files.
        output_json (str): Path to the output JSON file.
    """
    
    all_articles = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('wiki_'):
                path = os.path.join(root, file)
                print(f"Processing {path}...")
                articles = extract_articles_from_file(path)
                all_articles.extend(articles)

    # Save the database to a JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    print(f"✅ Base enregistrée dans {output_json} avec {len(all_articles)} articles.")


if __name__ == "__main__":
    """
    Entry point for command-line execution.
    Example:
        python build_database.py [folder_path] [output_json]
    """
    if len(sys.argv) < 2:
        print("Usage: python extract_articles_to_json.py <folder_path> [output_json]")
        sys.exit(1)

    folder = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        build_database_from_extracted(folder, output)
    else:
        build_database_from_extracted(folder)

    
# Utilisation
