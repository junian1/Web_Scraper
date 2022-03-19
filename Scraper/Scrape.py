from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        service=Service("C:/Users/junia/desktop/Web_Scraper/Webdriver/chromedriver.exe"))
        #executable_path="Users/junia/Downloads/chromedriver_win32", options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + keyword + '&locT=N&locId=170'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(3)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, ("selected")).click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.CLASS_NAME, ("ModalStyle__xBtn___29PT9")).click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, ("react-job-listing"))  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            # Close alert (popup)
            try:
                driver.find_element(By.CSS_SELECTOR, ('[alt="Close"]')).click()
            except NoSuchElementException:
                pass

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, ('.//div[@class="css-xuk5ye e1tk4kwz5"]')).text
                    location = driver.find_element(By.XPATH, ('.//div[@class="css-56kyx5 e1tk4kwz1"]')).text
                    job_title = driver.find_element(By.XPATH, ('.//div[@class="css-1j389vi e1tk4kwz2"]')).text
                    driver.find_element(By.XPATH, ('.//div[@class="css-t3xrds e856ufb2"]')).click()
                    job_description = driver.find_element(By.XPATH, ('.//div[@class="jobDescriptionContent desc"]')).text
                    collected_successfully = True
                except NoSuchElementException:
                    time.sleep(5)

                try:
                    salary_estimate = driver.find_element(By.XPATH, ('//li[@class="react-job-listing css-bkasv9 eigr9kq0"]/child::div[@class="d-flex flex-column pl-sm css-1buaf54 job-search-key-1mn3dn8 e1rrn5ka0"]/child::div[3]/child::div')).text
                except NoSuchElementException:
                    salary_estimate = -1  # You need to set a "not found value. It's important."

                try:
                    rating = driver.find_element(By.XPATH, ('//div[@class="d-flex flex-column job-search-key-1pzmdmc e1rrn5ka1"]/child::span')).text
                except NoSuchElementException:
                    rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH, ('.//div[@data-item="tab" and @data-tab-type="overview"]')).click()

                try:
                    size = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Size"]//following-sibling::*')).text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Founded"]//following-sibling::*')).text
                except NoSuchElementException:
                    founded = -1

                try:
                    ownership_type = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Type"]//following-sibling::*')).text
                except NoSuchElementException:
                    ownership_type = -1

                try:
                    sector = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Sector"]//following-sibling::*')).text
                except NoSuchElementException:
                    sector = -1

                try:
                    industry = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Industry"]//following-sibling::*')).text
                except NoSuchElementException:
                    industry = -1

                try:
                    revenue = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Revenue"]//following-sibling::*')).text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH, ('.//div[@class="p-std"]//*[text()="Competitors"]//following-sibling::*')).text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                ownership_type = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type: {}".format(ownership_type))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type": ownership_type,
                         "Sector": sector,
                         "Industry": industry,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, ('.//button[@class="page  css-1hq9k8 e13qs2071"]')).click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.





#This line will open a new chrome window and start the scraping.
df = get_jobs("data scientist", 5, False)
print(df)