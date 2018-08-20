from PIL import Image
import os
import glob

def crop(im,height,width):
    # im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(int(imgheight//height)):
        for j in range(int(imgwidth//width)):
            # print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__=='__main__':
    # change the path and the base name of the image files 
    imgdir = 'D:/a-star/Ghilotti/SMART/7-24-2018/'
    basename = 'R0010500.JPG'
    filelist = glob.glob(os.path.join(imgdir,basename))
    print(filelist)
    for filenum,infile in enumerate(filelist):
        # infile='/Users/alex/Documents/PTV/test_splitter/cal/Camera 1-1-9.tif'
        print(filenum) # keep the numbers as we change them here
        print(infile)
        
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        print('Image size is: %d x %d ' % (imgwidth, imgheight))
        height = imgheight
        width =  imgwidth//2
        start_num = 0
        for k,piece in enumerate(crop(im,height,width),start_num):
            # print k
            # print piece
            img=Image.new('RGB', (width,height))
            # print img
            img.paste(piece)
            path = os.path.join(imgdir, "%s_%d.JPG" % (os.path.splitext(infile)[0],k))
            print(path)
            img.save(path)
            #os.rename(path,os.path.join("cam%d.1%05d" % (int(k+1),filenum)))