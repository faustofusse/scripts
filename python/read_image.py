from PIL import Image
import pytesseract
name = 'PRIMER PARCIAL 2.jpg'
t = pytesseract.image_to_string(Image.open(name))
t2 = t.replace('\n','')
print(t2)