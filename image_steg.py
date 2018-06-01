__author__ = 'Dennis Qiu'
from PIL import Image

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
    default = Image.open(im)
    h = []
    for i in range(256):
        h.append(0)
    for x in range (default.width):
        for y in range (default.height):
            p = default.getpixel((x, y))
            h[p] += 1
    default.show()
    print('List h:\n{}'.format(h))

    default_copy2 = default.copy()
    size = default.width * default.height
    Lut = im_lut(h, size)
    for x in range (default.width):
        for y in range (default.height):
            p = default.getpixel((x, y))
            default_copy2.putpixel((x, y), Lut[p])
    default_copy2.show()

def im_lut(list_h, size_n):
    lut = []
    sum_h = 0
    for i in range(256):
        sum_h += list_h[i]
        lut.append(int((255 / size_n) * sum_h))
    print('List lut:\n{}'.format(lut))
    return lut

if __name__ == '__main__':
    encrypted = 'encrypted4bits.png encrypted4bits1.png encrypted4bits2.png encrypted4bits3.png'.split()
    for e in encrypted:
        de_steg(e)
    im_histogram()
