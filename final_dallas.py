from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()


base_url = 'https://www.dice.com/jobs?q=data%20engineer&location=Dallas,%20TX,%20USA&latitude=32.7766642&longitude=-96.79698789999999&countryCode=US&locationPrecision=City&adminDistrictCode=TX&radius=30&radiusUnit=mi&page={}&pageSize=100&filters.postedDate=ONE&filters.workplaceTypes=On-Site&language=en'

page = 1
jobs_list = []

while True:
    url = base_url.format(page)
    driver.get(url)

    try:
        jobs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "card")]'))
        )
        print(f"Found {len(jobs)} jobs on page {page}!")

        if len(jobs) == 0:
            print("No more jobs found.")
            break

        for idx, job in enumerate(jobs):
            try:
                job_title = job.find_element(By.XPATH, './/h5/a').text
                job_company = job.find_element(By.XPATH, './/div[@class="card-company"]/a').text
                job_location = job.find_element(By.XPATH, './/span[@class="search-result-location"]').text
                job_salary = job.find_element(By.XPATH, './/div[@class="card-salary"]').text if job.find_elements(By.XPATH, './/div[@class="card-salary"]') else 'Not provided'
                job_description = job.find_element(By.XPATH,'.//div[@class="card-description"]').text if job.find_elements(By.XPATH, './/div[@class="card-description"]') else 'Not provided'
                job_postedDate = job.find_element(By.XPATH, './/span[@class="posted-date"]').text

                jobs_list.append({
                    'Title': job_title,
                    'Company': job_company,
                    'Location': job_location,
                    'Salary': job_salary,
                    'Description': job_description,
                    'PostedDate': job_postedDate,
                })

            except Exception as e:
                print(f"Error extracting data from job listing {idx + 1}: {e}")

        if len(jobs) < 100:
            print("Reached the last page.")
            break

        page += 1
        time.sleep(2)

    except Exception as e:
        print(f"Error loading jobs on page {page}: {e}")
        break

if jobs_list:
    df = pd.DataFrame(jobs_list)
    df.to_csv('dallas_today_jobs.csv', index=False)
    print("Data saved to Excel Sheet.csv.")
else:
    print("No jobs were found or extracted.")

driver.quit()

