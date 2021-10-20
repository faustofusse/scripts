from PIL import Image
import glob

directory = input('Directory: ')
image_format = input('Image format: ')
image_names = glob.glob('./'+directory+'/*.'+image_format)
image_names.sort()
first_image = image_names.pop(0)
first_image_file = Image.open(r''+first_image)
first_image_converted = first_image_file.convert('RGB')
image_files = []
images = []

print(image_names)
print(first_image)

count = 0
for image in image_names:
    count+=1
    if (count > 300 and count < 400):
        f = Image.open(r''+image)
        images.append(f.convert('RGB'))

first_image_converted.save(r'result.pdf', save_all=True, append_images=images)
