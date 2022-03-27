from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    # options = webdriver.ChromeOptions()

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
            try:
                job_button.click()
                time.sleep(2)  # Depending on internet speed, can increase/decrease sleep time
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
                        driver.find_element(By.XPATH, ('.//div[@class="css-t3xrds e856ufb2"]')).click()  # Click 'Show More' for full description
                        job_description = driver.find_element(By.XPATH, ('.//div[@class="jobDescriptionContent desc"]')).text
                        collected_successfully = True
                    except NoSuchElementException:
                        time.sleep(5)

                    try:
                        salary_estimate = driver.find_element(By.XPATH, ('//li[@class="react-job-listing css-bkasv9 eigr9kq0"]//span[@data-test="detailSalary"]')).text
                    except NoSuchElementException:
                        salary_estimate = -1  # You need to set a "not found value. It's important."

                    try:
                        rating = driver.find_element(By.XPATH, ('//span[@data-test="detailRating"]')).text
                    except NoSuchElementException:
                        rating = -1  # You need to set a "not found value. It's important."

                # Printing for debugging
                if verbose:
                    print("Company_Name: {}".format(company_name))
                    print("Location: {}".format(location))
                    print("Job_Title: {}".format(job_title))
                    print("Job_Description: {}".format(job_description[:500]))
                    print("Salary_Estimate: {}".format(salary_estimate))
                    print("Rating: {}".format(rating))

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

                except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                    size = -1
                    founded = -1
                    ownership_type = -1
                    sector = -1
                    industry = -1
                    revenue = -1

                if verbose:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type: {}".format(ownership_type))
                    print("Sector: {}".format(sector))
                    print("Industry: {}".format(industry))
                    print("Revenue: {}".format(revenue))

                jobs.append({"Company_Name": company_name,
                             "Location": location,
                             "Job_Title": job_title,
                             "Job_Description": job_description,
                             "Salary_Estimate": salary_estimate,
                             "Rating": rating,
                             "Size": size,
                             "Founded": founded,
                             "Type": ownership_type,
                             "Sector": sector,
                             "Industry": industry,
                             "Revenue": revenue})
                # add job to jobs
            except StaleElementReferenceException:
                print("Stale element error")
                pass

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, ('.//button[@class="nextButton css-1hq9k8 e13qs2071"]')).click()
            time.sleep(3)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.



