import pandas as pd
from pypdf import PdfReader
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import os, sys

BATCH_SIZE = 10
SLEEP_BETWEEN = 10  # secondes
CSV_OUTPUT = "translated_data_fon.csv"


def initialize_driver():
    
    """
    Initialize a headless Chrome WebDriver instance.
    Returns:
        webdriver.Chrome: Configured Chrome driver
    """
    
    options = Options()
    options.add_argument("--headless")  # Activer le mode headless
    options.add_argument("--no-sandbox")
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)
    
    return driver


def split_text(text, max_length=3900):
    
    """
    Split a long text into smaller chunks to fit translation input limitations.
    Args:
        text (str): The original text to split
        max_length (int): Maximum allowed characters per chunk
    Returns:
        List[str]: List of text chunks
    """
    
    # Diviser le texte en morceaux plus petits si la longueur dépasse la limite
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# Fonction to translate text to Fon using Google Translate
# Note: This function uses Selenium to automate the translation process
def translate_to_fon(text: str):
    
    """
    Translate a given text into Fon using Google Translate via Selenium.
    Args:
        text (str): Text to translate
    Returns:
        str: Translated text in Fon language
    """
    
    driver = initialize_driver()
    driver.get("https://translate.google.com/details?hl=fr&sl=auto&tl=fon&op=translate")
    
    # Divide the text into appropriately sized chunks
    text_parts = split_text(text)
    translated_text = ""

    try:
        for part in text_parts:
            # Enter the text into the input box
            driver.find_element(by=By.CLASS_NAME, value="er8xn").send_keys(part) 

            
            # Waiting for traduction
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "HwtZe"))
            )
            
            # Get the translation for this chunck
            translated_text += element.text + " "  

        return translated_text.strip()
    
    except Exception as e:
        print(f"Erreur : {e}")
        return None
    
    finally:
        driver.quit()

def process_batch(input_json, output_csv = "translated_data_fon.csv"):
    
    """
    Process all articles, translate them into Fon, and save periodically.
    Supports automatic recovery if the script is interrupted.
    
    """
    
    data = pd.read_json(input_json)
    
    if os.path.exists(CSV_OUTPUT):
        df_translated = pd.read_csv(CSV_OUTPUT)
        already_done_ids = set(df_translated["id"])
        print(f"🔁 Resuming: {len(already_done_ids)} articles already translated.")
    else:
        df_translated = pd.DataFrame(columns=["id", "title", "url", "content", "content_fon"])
        already_done_ids = set()


    try:
        for idx, row in data.iterrows():
            if row["id"] in already_done_ids:
                continue  # Skip already processed articles

            print(f"➡️  [{idx+1}] Traduction de : {row['title']}")
            translated = translate_to_fon(row["content"])
            new_row = {
                "id": row["id"],
                "title": row["title"],
                "url": row["url"],
                "content": row["content"],
                "content_fon": translated
            }
            df_translated = pd.concat([df_translated, pd.DataFrame([new_row])], ignore_index=True)

            # Sauvegarder toutes les BATCH_SIZE traductions
            if len(df_translated) % BATCH_SIZE == 0:
                df_translated.to_csv(CSV_OUTPUT, index=False)
                print(f"💾 Auto-saved after {len(df_translated)} articles.")
                time.sleep(SLEEP_BETWEEN)  # Pause between batches

        # Final save
        print("💾 Final save...")
        df_translated.to_csv(CSV_OUTPUT, index=False)
        print("✅ Translation completed. Final file: translated_data_fon.csv")

    except KeyboardInterrupt:
        print("⏹️ Manual interruption detected. Saving progress...")
        df_translated.to_csv(CSV_OUTPUT, index=False)
        print("✅ Progression sauvegardée.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate_to_fon.py <input_json_file> [output_csv_file]")
        sys.exit(1)
    if len(sys.argv) == 1 and sys.argv[1].split(".") != "json":
        print("Vous devez fournir un fichier json comme fichier d'entré")
        sys.exit(1)

    input_json = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output_csv:
        process_batch(input_json, output_csv)
    else:
        process_batch(input_json)

    