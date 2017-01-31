# -*- coding: utf-8 -*-

import traceback
import cStringIO
from PIL import Image
import urllib2


class CQImgReader:
    def __init__(self, path):
        file = None
        self.url = None
        try:
            file = open(path)
            for line in file.readlines():
                if line.find("url") == 0:
                    self.url = line[4:]
                    break
        except Exception as e:
            traceback.print_exc()
        finally:
            file.close()

    def get_bytes(self):
        return cStringIO.StringIO(urllib2.urlopen(self.url).read())

    def get_pil_img(self):
        img_bytes = cStringIO.StringIO(urllib2.urlopen(self.url).read())
        return Image.open(img_bytes)


if __name__ == "__main__":
    img = CQImgReader(
        u"D:\Document\SmallWei\[Dev] 酷Q Air [正式版]\酷Q Air\data\image\C321ADD56FF4D1E92B1CA1F9BD4A767D.jpg.cqimg")
    img = img.get_pil_img()
    img.show()
