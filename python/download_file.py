from bs4 import BeautifulSoup
import requests
import os
import sys
import js2py

def download_hls(filename, url):
    command = f'python -m ffpb -i "{url}" -c copy -bsf:a aac_adtstoasc "{filename}"'
    os.system(command)

def download_mp4(filename, url):
    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length'))
    downloaded = 0
    r.raise_for_status()
    f = open(filename, 'wb')
    for chunk in r.iter_content(chunk_size=8192): 
        if chunk:
            downloaded += len(chunk)
            percentage = (downloaded * 100) / total_length
            f.write(chunk)
            sys.stdout.write('\rDownloading File: ' + str(int(downloaded / 1000000)) + '/' + str(int(total_length / 1000000)) + ' Mb (' + str(int(percentage)) + '%)')
    print('')
    return f.close()

def dfp(filename, url):
    res = requests.get(url).text
    soup = BeautifulSoup(res, features='lxml')
    div = soup.find('div', {'id':'player', 'class':'original'})
    video_id = div['data-video-id']
    script = div.find('script')
    scrip = 'function result(){playerObjList = {};' + str(script.text) + ' return qualityItems_'+video_id+';}';
    result = js2py.eval_js(scrip)
    elements = eval(str(result()))
    video_url = elements[len(elements)-1]['url']
    print(video_url)
    download_mp4(filename, video_url)

def dfx(filename, url):
	pass

d_type = input('Download type: ')
url = input('File URL: ')
destination = input('Destination: ')

if d_type == 'mp4': download_mp4(destination, url)
if d_type == 'hls': download_hls(destination, url)
if d_type == 'dfp': dfp(destination, url)
if d_type == 'dfx': dfx(destination, url)
