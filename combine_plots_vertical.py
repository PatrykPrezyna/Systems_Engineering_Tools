from PIL import Image

def get_concat_v(name):
    print("test")
    image1 = Image.open(r'Tradespace0.png')
    image2 = Image.open(r'Tradespace1.png')
    image3 = Image.open(r'Tradespace2.png')
    image4 = Image.open(r'Tradespace3.png')
    image5 = Image.open(r'Tradespace4.png')
    image6 = Image.open(r'Tradespace5.png')
    image7 = Image.open(r'Tradespace6.png')
    image8 = Image.open(r'Tradespace7.png')

    im1 = image1.convert('RGB')
    im2 = image2.convert('RGB')
    im3 = image3.convert('RGB')
    im4 = image4.convert('RGB')
    im5 = image5.convert('RGB')
    im6 = image6.convert('RGB')
    im7 = image7.convert('RGB')
    im8 = image8.convert('RGB')

    dst = Image.new('RGB', (im1.width+im2.width+im3.width+im4.width, im1.height + im3.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (im1.width+im2.width, 0))
    dst.paste(im4, (im1.width+im2.width+im3.width, 0))
    dst.paste(im5, (0, im1.height))
    dst.paste(im6, (im1.width, im1.height))
    dst.paste(im7, (im1.width+im2.width, im1.height))
    dst.paste(im8, (im1.width+im2.width+im3.width, im1.height))
    dst.save('Tradespaces_' + name + '.png')
    return True



if (__name__ == '__main__'):
    print('Executing as standalone script')
    get_concat_v()