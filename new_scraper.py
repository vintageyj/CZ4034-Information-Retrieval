from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
import time

dummy_email = "inforetcz4034@gmail.com"
dummy_password = "Inforat@4034"

def get_company_reviews(driver, key, value):
    Company_list = []
    OverallRatings = []
    ReviewDates = []
    ReviewTitles = []
    JobTitles = []
    JobDetails = []
    Locations = []
    Pros = []
    Cons = []

    max_pages = 10
    init_reviews_count = len(OverallRatings)
    for page in range(1, max_pages+1):
        if page == 1:
            url = get_company_links(key, value, 1)
            print(url)
            print("Company Name:", key, "EID:", value, "Page:", page)
            # if not signed_in:
            #     await sign_in(driver, dummy_email, dummy_password, url)
            #     signed_in = True
            # else:
            sign_in(driver, dummy_email, dummy_password, url)
            # await driver.wait_for_cdp("Page.domContentEventFired", timeout=20)
        else:
            # Wait for the button to be clickable
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="pagination-next"]')
            next_button.click()
            time.sleep(1)
            # await driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # await driver.wait_for_cdp("Page.domContentEventFired")

        # time.sleep(np.random.choice(range(4, 10)))
        driver.sleep(5)
        elem = driver.find_element(By.ID, "ReviewsRef", timeout=5)
        inner_html = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_html, 'html.parser')

        list_items = soup.find_all('li', class_='noBorder')
        for list_item in list_items:
            overallRating = list_item.find('span', class_="review-details__review-details-module__overallRating").text
            OverallRatings.append(overallRating)
            reviewDate = list_item.find('span', class_="review-details__review-details-module__reviewDate").text
            ReviewDates.append(reviewDate)
            reviewTitle = list_item.find('a', class_="review-details__review-details-module__detailsLink review-details__review-details-module__title").text
            ReviewTitles.append(reviewTitle)
            jobTitle = list_item.find('span', class_="review-details__review-details-module__employee").text
            JobTitles.append(jobTitle)
            jobDetails = list_item.find('div', class_="review-details__review-details-module__employeeDetails").text
            JobDetails.append(jobDetails)
            try:
                location = list_item.find('span', class_="review-details__review-details-module__location").text
            except:
                location = None
            Locations.append(location)
            pros_and_cons = list_item.find_all('p', class_="review-details__review-details-module__isCollapsed")
            if len(pros_and_cons) < 2:
                pros_and_cons = list_item.find_all('p', class_="review-details__review-details-module__isExpanded")
            pros = pros_and_cons[0].text
            Pros.append(pros)
            cons = pros_and_cons[1].text
            Cons.append(cons)

    final_reviews_count = len(OverallRatings)
    company_list = [key] * (final_reviews_count - init_reviews_count)
    Company_list += company_list

    return Company_list, OverallRatings, ReviewDates, ReviewTitles, JobTitles, JobDetails, Locations, Pros, Cons

def sign_in(driver, email, password, url):
    driver.get(url)
    driver.sleep(0.5)
    time.sleep(5)
    sign_in_button = driver.find_element(By.CLASS_NAME, "button__button-module__Button button-base__button-base-module__Button",timeout=2)
    sign_in_button.click()
    time.sleep(1)

    input_email = driver.find_element(By.ID, "fishbowlCoRegEmail",timeout=2)
    input_email.write(email)
    input_email.write("\n")

    # next_button = await driver.find_element(By.CLASS_NAME, 'Button Button', timeout=2)
    # await next_button.click()
    # await asyncio.sleep(1)

    time.sleep(3)

    input_password = driver.find_element(By.ID, "fishbowlCoRegPassword",timeout=2)
    input_password.write(password)
    input_password.write("\n")
    # next_button = await driver.find_element(By.CLASS_NAME, 'Button Button', timeout=2)
    # await next_button.click()
    # await asyncio.sleep(1)

    time.sleep(3)

def get_company_links(company_name, eid, page=1):
    return f"https://www.glassdoor.com/Reviews/{company_name}-Reviews-E{eid}_P{page}.htm?filter.iso3Language=eng"

def main(company_count):
    # options = webdriver.ChromeOptions()
    max_companies = 200
    count = 0
    try:
        companies.items()
    except:
        df = pd.read_csv('companies_sg.csv')
        companies = dict(zip(df['Company Name'], df['Employer ID']))
    print(len(companies))

    with webdriver.Chrome() as driver:
        for key, value in companies.items():
            count += 1
            if count != company_count: # <----------------CHANGE THIS TO THE AMOUNT REQUIRED
                # print("Skip")
                continue
            print("count:", count)
            Company_list, OverallRatings, ReviewDates, ReviewTitles, JobTitles, JobDetails, Locations, Pros, Cons = get_company_reviews(driver, key, value)

            Reviews = pd.DataFrame(list(zip(Company_list, OverallRatings, ReviewDates, ReviewTitles, JobTitles, JobDetails, Locations, Pros, Cons)), 
                                columns = ['Company Name', 'Overall Rating', 'Review Date', 'Review Title', 'Job Title', 'Job Details', 'Location', 'Pros', 'Cons'])
            Reviews.to_csv(f'company_reviews/sg_companies_reviews{count}.csv', index=False, encoding='utf-8') # Rename csv file accordingly
            
            if count >= max_companies:
                break
            
# if __name__ == "__main__":
#     asyncio.run(main())

for i in range(1,201):
    # if i in []:
    try:
        main(i)
    except:
        try:
            main(i)
        except Exception as e:
            print("Failed",e)
            continue