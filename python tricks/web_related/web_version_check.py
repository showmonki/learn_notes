'''
check frequently website, and find the current mac pkg version without open website.
'''

import urllib
from bs4 import BeautifulSoup
import re

def getHtml(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
	html_req = urllib.request.Request(url, headers=headers)
	page = urllib.request.urlopen(html_req)
	html = page.read()
	return html

def get_version(url):
	html = getHtml(url)
	web = BeautifulSoup(html, 'html.parser')
	container = web.select("main > section > div")[0]
	nodes = container.find_all("p")
	version_pattern = '.*?(V\d\.\d\.\d).*?'
	current_version = [re.findall(version_pattern,node.text) for node in nodes if re.findall(version_pattern,node.text)][0][0]
	return current_version


if __name__ == '__main__':
	website = 'https://veee453.vip/c_mac'
	v_num = get_version(website)
	print('Current Version is {}'.format(v_num))