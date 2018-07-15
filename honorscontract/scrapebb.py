import mechanize
import os
import cookielib
import random
import urllib2
from BeautifulSoup import BeautifulSoup
import Queue
import re
from time import sleep


header = { 
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

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

def get_db_course_page(course_id):
	url ='https://myasucourses.asu.edu/webapps/discussionboard/do/conference?toggle_mode=read&action=list_forums&course_id={}&nav=discussion_board_entry&mode=view'.format( course_id )
	req2 = mechanize.Request(url, None, header)
	resp = browser.open(req2)
	html = resp.get_data()
	return html

def get_db_message_frame(course_id, conf_id, forum_id, message_id):
	url = 'https://myasucourses.asu.edu/webapps/discussionboard/do/message?action=message_frame&course_id={}&conf_id={}&forum_id={}&nav=db_thread_list_entry&nav=discussion_board_entry&message_id={}&thread_id=null'.format(course_id, conf_id, forum_id, message_id)
	req = mechanize.Request(url, None, header)
	resp = browser.open(req)
	return resp.get_data()

def extract_message(message_frame_html):
	try:
		soup = BeautifulSoup(message_frame_html)
		return soup.find('p').text
	except:
		pass
	return None


def save_message(course_id, conf_id, forum_id, message_id, text):
    filename = "{}-{}-{}-{}.txt".format(course_id, conf_id, forum_id, message_id)
    message_dir = 'bb_messages'

    path = os.path.join(message_dir, filename)
    f = open(path, 'w')
    f.write(text.encode('utf-8'))
    f.close() 

def extract_conf_id(db_course_html):
	try:
		soup = BeautifulSoup(db_course_html)
		c = soup.find(id='conf_id')
		if c.has_key('value'):
			return c['value']
	except: 
		pass
	return None 

def extract_forum_ids(db_course_html):
	try:
		l = []
		soup = BeautifulSoup(db_course_html)
		ids = soup.findAll(name='tr')
		for id in ids:
			if id.has_key('id'):
				s = id['id']
				if s.startswith('listContainer_row:', 0, 18):
					l.append(s[18:])
		return l 
	except:
		pass
	return [] 

def extract_message_ids(db_forum_html):
	try:
		l = set()
		message_ids = re.findall("message_id=([_|0-9]+)", db_forum_html)
		return message_ids
	except:
		pass
	return [] 

def load_login():
        import my_config
        return (my_config.username, my_config.password)

def get_db_forum_page(course_id, conf_id, forum_id):
	url = "https://myasucourses.asu.edu/webapps/discussionboard/do/forum?action=list_threads&course_id={}&nav=discussion_board_entry&conf_id={}&forum_id={}".format(course_id, conf_id, forum_id)
	req = mechanize.Request(url, None, header)
	resp = browser.open(req)
	return resp.get_data()

# ASU Login Portal 
url = 'https://weblogin.asu.edu/cas/login'



browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.set_cookiejar(cookielib.LWPCookieJar())

# Request to login portal 
req = mechanize.Request(url, None, header)



# Open login portal 
resp = browser.open(req)

# Fill out password form 
browser.select_form(nr = 0)
username, password = load_login()
browser.form['username'] = username
browser.form['password'] = password
resp = browser.submit()

course_id = '_360953_1'
# course_id = '_361395_1'

db_course_html = get_db_course_page(course_id)
conf_id = extract_conf_id(db_course_html)
forum_ids = extract_forum_ids(db_course_html)
print conf_id
print forum_ids 


"""
I realize the below code could easily be multithreaded but I didn't want
blackboard to get mad at me for doing too many requests too quickly :-)

Instead, I just let it run while I went to the gym
"""

# Request all the forums 
queue = Queue.Queue()
message_queue = Queue.Queue()

num_messages = 0

# for i in range(1): # testing 
for i in range(len(forum_ids)):
	forum_id = forum_ids[i]
	queue.put((course_id, conf_id, forum_id))

while not queue.empty():
	course_id, conf_id, forum_id = queue.get()
	db_forum_html = get_db_forum_page(course_id, conf_id, forum_id)
	message_ids = list(set(extract_message_ids(db_forum_html))) # removes duplicates
	
        print message_ids

	# for i in range(1):
	for i in range(len(message_ids)):
		message_id = message_ids[i]
		num_messages += 1 
                message_queue.put((course_id, conf_id, forum_id, message_id))
	sleep(0.5) # apparently this is enough for them to not realize were scraping their website 

print "[+] Downloading {} messages".format(num_messages)

download_count = 0
# Download message frames ?? 
while not message_queue.empty():
	course_id, conf_id, forum_id, message_id = message_queue.get()
	message_frame_html = get_db_message_frame(course_id, conf_id, forum_id, message_id)
	text = extract_message(message_frame_html)
        
        if text:
            save_message(course_id, conf_id, forum_id, message_id, text)
        
        download_count += 1
        if download_count % 100 == 0:
            print "Progress: {}\t Downloads: {}".format(download_count, float(download_count)/float(num_messages))

        sleep(0.25)

