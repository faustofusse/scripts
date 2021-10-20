import requests
import json

codes_file = open('codes.json', 'rb')
codes = json.load(codes_file)
print(codes)

for country in codes:
    style = 'shiny' # flat 
    size = 64
    code = country['code']
    url = f'https://www.countryflags.io/{code}/{style}/{size}.png'
    img_data = requests.get(url).content
    img_file = open(f'{code}.png', 'wb')
    img_file.write(img_data)
