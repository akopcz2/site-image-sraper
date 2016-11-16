from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import os, fnmatch, sys
import exifread

os.chdir(sys.path[0])
path_to_image = 'path to save images to'
file_extension = 'file extension you want to get exif data from'

# use this image scraper from the location that 
#you want to save scraped images to
url = raw_input("Enter the url  ")


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def get_images(url):
    soup = make_soup(url)
    #this makes a list of bs4 element tags
    images = [img for img in soup.findAll('img')]
    imgCount = str(len(images))
    print (imgCount + " images found.")
    print 'Downloading images to current working directory.'
    #compile our unicode list of image links
    image_links = [each.get('src') for each in images]
    for each in image_links:
        filename=each.split('/')[-1]
        urllib.urlretrieve(each, filename)
    return image_links

make_soup(url)
get_images(url)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

for filename in find_files(path_to_image, '*' + file_extension):
    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if "Image Software" in tag:
            print "Key: %s, value %s" % (tag,tags[tag])









