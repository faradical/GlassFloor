import requests
import bs4
import pandas as pd
import sys
from splinter import Browser
import time
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

companies = ['NorfolkSouthern','TimeWarner']

for company in companies:
	url = f'https://twitter.com/search?q=%23{company}'

	browser.visit(url)
	def wait_for_element(tag, browser):
		if browser.is_element_present_by_tag(tag, wait_time=1) != True:
			return wait_for_element(tag, browser)
	
	wait_for_element("article", browser)
	articles = []
	previous_length = 0
	n = 0

	while len(articles) < 1000 and n < 10:
		browser.execute_script("window.scrollTo(10000, document.body.scrollHeight);")
		soup = bs4.BeautifulSoup(browser.html, 'html.parser')
		for a in soup.find_all("article"):
			if a not in articles:
				articles.append(a)
				n -= 1
		if len(articles) == previous_length:
			n += 1
		previous_length = len(articles)

	tweets = []
	for a in articles:
		try:
			username = a.find('div', class_="css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs").find("span").find("span").contents[0]
			handle = a.find('div', class_="css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd").find("span").contents[0]
			tweet_contents = a.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
			time = a.find('time')['datetime']
			tweet_contents_list = [c.get_text() for c in tweet_contents.children if c.get_text() != '']
			tweet_text = ''.join(tweet_contents_list).replace("\n","")
		except:
			pass

		tweets.append({'username':username, 'handle':handle, 'tweet_text':tweet_text, 'time':time})

	tweetsDF = pd.DataFrame(tweets)
	filename = scriptdir + "/tweets/" + company + "_tweets.csv"
	tweetsDF.to_csv(filename, index=False)

print("Mining complete.")
browser.quit()