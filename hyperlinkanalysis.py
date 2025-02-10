from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://en.wikipedia.org/wiki/Web_scraping"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all hyperlinks
links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("/wiki/")]

# Convert to full URLs
base_url = "https://en.wikipedia.org"
full_links = [base_url + link for link in links]

# Save to CSV
df = pd.DataFrame(full_links, columns=["target"])
df.insert(0, "source", url)
df.to_csv("wikipedia_hyperlinks.csv", index=False)

print("Scraped and saved", len(full_links), "links.")