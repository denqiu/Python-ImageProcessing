#http://pillow.readthedocs.io

from PIL import Image, ImageDraw, ImageMath, ImageFont

def de_steg(encrypted_file):
    f, e = encrypted_file.split('.')
    steg = Image.open(encrypted_file)
    out = Image.new('RGB', (steg.width,steg.height))
    for x in range(steg.width):
        for y in range(steg.height):
            r, g, b = steg.getpixel((x, y))
            rh, gh, bh = (r&0x0F)<<4, (g&0x0F)<<4, (b&0x0F)<<4
            out.putpixel((x, y), (rh, gh, bh))

    out.save(f+"hiddenImage.png")
    steg.show()
    out.show()

def im_histogram(im='lowContrastBW.png'):
    image = Image.open(im)
    image.show()
    h = [] 
    for i in range(256):
        h.append(0)
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x,y))
            h[p] += 1
    print('List **h:\n{}'.format(h)) 

    image2 = image.copy()
    imSize = image.width * image.height
    imLut = im_lut(h, imSize)
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x,y))
            image2.putpixel((x,y), imLut[p])
    image2.show() 

def im_lut(hList, nSize):
    """
    takes two parameters, list **h, and the product of the image<92>s width and height, **n. 
    Create an empty list, **lut and an accumulator variable, **sum_h. Iterate over **h, accumulating its 
    sum in **sum_h. Append the value 255/**n * **sum_h to **lut. 
    """
    lut = []
    sum_h = 0 
    for i in range(256):
        sum_h += hList[i] 
        lut.append(int(255 / nSize * sum_h))

    print('List **lut:\n{}'.format(lut)) 
    return lut
    
        
   
if __name__ == '__main__':
    # decode encrypted images
    encrypted = 'encrypted.png encrypted1.png encrypted2.png encrypted3.png'.split()
    for e in encrypted:
        de_steg(e)

    # generate histogram image
    im_histogram()
