from playwright.sync_api import sync_playwright

# Function to retrieve the table data
def scrape_table_data():
    url = "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            table = page.locator("//h3[text()='100 000+ articles']//parent::div//preceding-sibling::table")
            
            # Extracting all rows from the table
            rows = table.locator('tbody > tr')
            print(rows)
            
            # Dictionary to hold the languages and number of articles
            dict_language_article = {}
            
            for row in rows.all():
                cells = row.locator('td')
                if cells.count() >= 3:
                    language = cells.nth(1).inner_text().strip()
                    article_count = cells.nth(4).inner_text().strip().replace(",", "")
                    if article_count.isdigit():
                        dict_language_article[language] = int(article_count)
            
            browser.close()
            return dict_language_article

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Function to calculate the total number of articles
def findTotalArticlesByLanguages(languages):
    dict_language_article = scrape_table_data()
    
    if not dict_language_article:
        return 0

    total_articles = 0
    for language in languages:
        if language in dict_language_article:
            total_articles += dict_language_article[language]
        else:
            print(f"Language '{language}' not found in the dataset.")
    return total_articles


languages = ["English", "German"]
total = findTotalArticlesByLanguages(languages)
print(f"Total articles for {languages}: {total}")
