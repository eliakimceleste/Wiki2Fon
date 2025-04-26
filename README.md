# 📚 Wiki2Fon

## Overview

**Wiki2Fon** is a project aimed at translating the entirety of the French Wikipedia into Fon, a major West African language.  
This work is part of a broader initiative to localize global knowledge into African languages, including Fon, Ewe, Dendi, and Yoruba.

Due to better data availability and previous preparation work, Fon was selected as the first target language.  
Wiki2Fon seeks to enhance knowledge accessibility, support cultural preservation, and empower education initiatives through technology.

## Context

Access to vast information repositories like Wikipedia in native African languages remains limited.  
Wiki2Fon leverages automated tools to process large-scale translations and aims to fill this digital knowledge gap.

The project's goal is to create a structured bilingual dataset mapping original French Wikipedia articles to their translations in Fon.

## Project Workflow

### 1. Download the French Wikipedia Dump

The starting point is the official French Wikipedia dump:


This file contains the current versions of all Wikipedia articles without full edit history.  
It can be downloaded from:  
> [Wikimedia Dumps - frwiki](https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2)

### 2. Extract Articles with WikiExtractor

To process the compressed XML dump and obtain readable text, we used **WikiExtractor**:

- Official repository: [https://github.com/attardi/wikiextractor](https://github.com/attardi/wikiextractor)

**Extraction command:**

```bash
python3 -m wikiextractor.wikiextractor.WikiExtractor -o extracted --processes 2 --no-templates PATH_TO_YOUR_DUMP/frwiki-latest-pages-articles.xml.bz2
```

### 3. Translating Articles Using Selenium and Google Translate

After extracting the articles, the next phase involves translating them from French to Fon. Since Google Translate does not officially support Fon, **Selenium** is used to automate the translation process by interacting with the Google Translate web interface.

#### Tools:

- Selenium (for browser automation)
- Google Translate Web Interface

#### Implementation Steps:
- Install Required Libraries:

    ```
    pip install selenium 
    pandas webdriver-manager
    ```
- Selenium Web Scraping:
    
    - Open Google Translate (web interface) and automatically paste the French text.

    - Retrieve the translation into Fon from Google Translate's output field.


- Splitting Text:

    - Since Google Translate has a character limit for text input (~3900 characters), the text is split into smaller chunks.

- Batch Processing:

    - Introduce time.sleep() to avoid being blocked by Google.

    - Process translations in batches to handle large volumes of articles.

    - Save progress regularly to allow resuming from the last successful translation in case of interruption.


### 4.  Handling Large-Scale Translations
Given the large volume of Wikipedia articles, the translation process is managed carefully:


- Batch processing to avoid overload.

- Saving periodically to avoid data loss.

- Resuming after interruption using saved CSV files.

## Data Structure
The final output is a structured bilingual dataset with the following columns:

- ```Title```: The title of the Wikipedia article.

- ```URL```: A link to the article on the French Wikipedia.

- ```French Content```: The original content in French.

- ```Fon Content```: The translated content in Fon.

## License

This project is licensied under the [Apache License](LICENSE)

## Dependencies