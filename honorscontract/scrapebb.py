import mechanize
import cookielib
import random
import urllib2
from BeautifulSoup import BeautifulSoup


class AnonBrowser(mechanize.Browser):
	def __init__(self, proxies = [], useragents=[]):
		mechanize.Browser.__init__(self)
		self.set_handle_robots(False)
		self.proxies = proxies 
		self.useragents = useragents + ['Mozilla/4.0', 'FireFox6.01', 'ExactSearch','Nokia7110/1.0']
		self.cookie_jar = cookielib.LWPCookieJar()
		self.set_cookiejar(self.cookie_jar)
		self.anonymize()

	def clear_cookies(self):
		self.cookie_jar = cookielib.LWPCookieJar()
		self.set_cookiejar(self.cookie_jar)

	def change_user_agent(self):
		# index = random.randrange(0, len(self.useragents))
		self.addheaders = [
		('User-Agent', ('Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'))

		]

	def change_proxy(self):
		print 'change_proxy: not implemented'	

	def anonymize(self):
		self.clear_cookies()
		self.change_user_agent()
		self.change_proxy()

def print_links(html):
	try:
		print "\t[+] printing links from beautifulsoup"
		soup = BeautifulSoup(html)
		links = soup.findAll(name='a')
		for link in links:
			if link.has_key('href'):
				print link['href']
	except:
		pass 



url = 'https://myasucourses.asu.edu/webapps/discussionboard/do/conference?toggle_mode=read&action=list_forums&course_id=_360953_1&nav=discussion_board_entry&mode=view'
# url = 'https://myasucourses.asu.edu'
header = { 
'User-Agent':'Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'
}

browser = mechanize.Browser()
browser.set_handle_robots(False)
req = mechanize.Request(url, None, header)

resp = browser.open(req)
# browser.select_form(nr = 0)
# browser.form['username'] = 'tswheel1'
# browser.form['password'] = '=GoFuckYourself66TimesBitch'
# resp = browser.submit()


html = resp.get_data()
print_links(html)
