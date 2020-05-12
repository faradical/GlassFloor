import requests
import bs4
import pandas as pd

fortune500list = pd.read_csv("fortune500.csv")
company_list = list(fortune500list['company'])
company_list.reverse()
company_list = [company_list[-12]]

for company in company_list:
    review_count = 0
    pagable = True
    reviews_list = []
    writetofilecount = 10000
    n = 1
    retry_count = 0
    while pagable == True:
        url = f"https://www.indeed.com/cmp/{company}/reviews?fcountry=ALL&start={review_count}&sort=rating_asc"
        if review_count == 0:
            retry_count += 1
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

        response = requests.get(url, headers=headers)
        print(url)
        if response.status_code == 200:    
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            buttons = soup.find_all("span", class_="cmp-Pagination-edgeButton")
            if not soup.find("div", class_="cmp-ReviewsZrpPromo-text"):
                if len(buttons) != 0:
                    reviews = soup.find_all("div", class_="cmp-ReviewsList-container")

                    for review in reviews:
                        try:
                            title = review.find('div', class_="cmp-Review-title").contents[0]
                            rating = review.find('div', class_="cmp-ReviewRating-text").contents[0]
                            if float(rating) >= 3.0:
                                binary_rating = "good"
                            else:
                                binary_rating = "bad"
                            info = [item for item in review.find('span', class_="cmp-ReviewAuthor").contents if type(item) == bs4.element.NavigableString]
                            status = info[1]
                            date = info[4]
                            info = review.find_all('a', class_="cmp-ReviewAuthor-link")
                            position = info[0].contents[0]
                            location = info[1].contents[0]
                            review_text = review.find('span', class_="cmp-NewLineToBr-text").contents[0]
                            reviews_list.append({'rating': binary_rating, 'review': review_text})
                        except:
                            #print("Error encountered, passing review.")
                            pass

                    if buttons[-1].contents[0] == "Next":
                        pagable = True
                        review_count += len(reviews)
                    else:
                        pagable = False
                else:
                    print("That weird error again, retrying page.")
                    # retry_count += 1
        if retry_count > 5:
            pagable = False
            retry_count = 0

        if review_count >= writetofilecount:
            reviewsDF = pd.DataFrame(reviews_list)
            company_name = company.replace(' ','_').replace('*','').replace("'",'').replace(',','').replace('.','').replace('/','_').replace('"','').replace('-','_')
            filename = f'Reviews/{company_name}_Reviews_part_{n}.csv'
            reviewsDF.to_csv(filename, index=False)
            writetofilecount += 10000
            n += 1
            reviews_list = []


    if len(reviews_list) != 0:
        reviewsDF = pd.DataFrame(reviews_list)
        company_name = company.replace(' ','_').replace('*','').replace("'",'').replace(',','').replace('.','').replace('/','_').replace('"','').replace('-','_')
        filename = f'Reviews/{company_name}_Reviews_part_{n}.csv'
        reviewsDF.to_csv(filename, index=False)