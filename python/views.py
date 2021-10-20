import os
import requests

url = input('url: ')
views = int(input('views: '))

split = url.split('/')
origin = url[0:20]
host = split[2]
viewed_url = origin + '/api/events/user/videoViewed'
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0'
content_id = split[4].split('?')[0]
ref_user_id = url.split('=')[-1]

headers = {'User-Agent': agent, 'Referer': url, 'Origin': origin, 'Host': host}
data = {"contentId": content_id, "refUserId": ref_user_id,"utms":"utm_source=share&utm_medium=direct"}

for i in range(0, views):
	c = os.system('sudo protonvpn connect --fastest')
	response = requests.post(viewed_url, headers=headers, data=data)
	print(response.content)

