from pdf2image import convert_from_path
import os

# pdftoppm hola.pdf ./hola/hoka

filename = input('Filename: ')
try:
    pages = convert_from_path(filename, 500)
except:
    print('erro')

directory = filename.replace('.pdf', '')
os.mkdir(directory)

count = 1
for page in pages:
    page.save('./'+directory+'/page'+str(count)+'.jpg', 'JPEG')
    count += 1
    print(str(count) + '/' + str(len(pages)))
