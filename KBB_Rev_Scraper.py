import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

main_page_list = []

for i in range(2,5):
    main_str = "https://www.kbb.com/car-finder/" + str(i) + "/?categories=sedan&morefilters=topratedexpert"
    main_page_list.append(main_str)

data = []

for page in main_page_list:
    print("Now scraping:", page)
    main_page = requests.get(main_str)
    main_soup = BeautifulSoup(main_page.content, "html.parser")
    names = main_soup.find_all("a", class_="css-y4ixr8 e5qxycd0")
    time.sleep(5)
    for name in names:
        product_str = name['href']
        print("Now scraping:", product_str)
        product_page = requests.get(product_str)
        product_soup = BeautifulSoup(product_page.content, 'html.parser')
        try:
            rev = product_soup.find("div", class_="css-mkt3oj e1u2rse51")
            all_reviews = "https://www.kbb.com/" + rev.a['href']
            print(all_reviews)
            review_page = requests.get(all_reviews)
            review_soup = BeautifulSoup(review_page.content, 'html.parser')
            time.sleep(5)
            every_review = review_soup.find_all("div", class_="css-1mcvy9w-StyledRow-grid-close e15r1ymc0")
            try:
                product = review_soup.find("h2", class_="css-1jlky2b-StyledHeading2-defaultStyles-h2 e1jv8h5t1").get_text().strip()
            except:
                product = "NA"
            print(product)
            for view in every_review:
                time.sleep(5)
                try:
                    review_id = view.find("div", class_="css-18pmvx8")
                    review_id = review_id.span.get_text().strip()
                except:
                    review_id = "NA"
                print(review_id)
                try:
                    thumbs_up = view.find("div", class_="css-1np1ojp e19gryfm2")
                    thumbs_up = thumbs_up.span.get_text().strip()
                except:
                    thumbs_up = "NA"
                print(thumbs_up)
                try:
                    thumbs = view.find("div", class_="css-1np1ojp e19gryfm2")
                    array = thumbs.find_all("span")
                    thumbs_down = array[1].get_text().strip()
                except:
                    thumbs_down = "NA"
                print(thumbs_down)
                try:
                    short_review = view.find("h3", class_="css-lg2ecn-StyledHeading3-defaultStyles-h3 e1jv8h5t2").get_text().strip()
                except:
                    short_review = "NA"
                print(short_review)
                try:
                    revs = view.find("div", class_="css-cumw5s")
                    lr = revs.find_all("div")
                    long_review = lr[8].get_text().strip()
                except:
                    long_review = "NA"
                print(long_review)
                try:
                    num = view.find("div", class_="css-18iaol3 ejetpgk0")
                    bum = num.find_all("span")
                    pros = bum[1].get_text().strip()
                except:
                    pros = "NA"
                print(pros)
                try:
                    one = view.find_all("div", class_="css-18iaol3 ejetpgk0")
                    two = one[1].find_all("span")
                    cons = two[1].get_text().strip()
                except:
                    cons = "NA"
                print(cons)
                data.append((product, review_id, thumbs_up, thumbs_down, short_review, long_review, pros, cons, all_reviews))
        except:
            product = "NA"
            review_id = "NA"
            thumbs_up = "NA"
            thumbs_down = "NA"
            short_review = "NA"
            long_review = "NA"
            pros = "NA"
            cons = "NA"
            all_reviews = "NA"
            data.append((product, review_id, thumbs_up, thumbs_down, short_review, long_review, pros, cons, all_reviews))

# create a tabular representation of the data
df = pd.DataFrame(np.array(data))

# Add the column names
df.columns = ['product', 'reviewid', 'thumbsup', 'thumbsdown', 'shortreview', 'longreview', 'pros', 'cons', 'link']

# print the tabular data
print(df)

# convert to csv file
df.to_csv("project.csv")
