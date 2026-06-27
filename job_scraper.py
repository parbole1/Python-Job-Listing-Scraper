import requests
from bs4 import BeautifulSoup
import csv

# 1. Get the webpage content
url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)

# 2. Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# 3. Find all job posting containers
job_cards = soup.find_all("div", class_="card-content")

# 4. Open a CSV file to save the data
csv_filename = "fake_jobs.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Header row
    writer.writerow(["Job Title", "Company Name", "Location", "Job Detail URL"])

    # 5. Loop through each job card to extract the desired fields
    for card in job_cards:
        # Job Title (<h2 class="title is-5">)
        title_element = card.find("h2", class_="title")
        job_title = title_element.text.strip() if title_element else "N/A"

        # Company Name (<h3 class="subtitle is-6 company">)
        company_element = card.find("h3", class_="company")
        company_name = company_element.text.strip() if company_element else "N/A"

        # Location (<p class="location">)
        location_element = card.find("p", class_="location")
        location = location_element.text.strip() if location_element else "N/A"

        # Job Detail URL
        # Each card has two links in the footer: "Learn" and "Apply"
        # The detail page is the "Apply" link, which is the second <a> tag
        links = card.find_all("a")
        job_url = links[1]["href"] if len(links) > 1 else "N/A"

        # 6. Write the extracted data as a row in the CSV
        writer.writerow([job_title, company_name, location, job_url])

print(f"Successfully scraped {len(job_cards)} jobs and saved to '{csv_filename}'.")