# -*- coding: utf-8 -*-

import base64
import cStringIO
import json
import urllib2
import re
from PIL import Image

import redis
import requests
import time

import CQImgReader
from BaseProcessModule import *
from RedisSession import redisPool
from Sender import *

redisConnection = redis.Redis(connection_pool=redisPool)


class RateAppearanceModule(BaseProcessModule):
    CONTEXT = "RATE"
    COOLQ_IMAGE_PATH = u"C:\\Users\Administrator\\Desktop\\{0}\\酷Q Pro\\data\\image\\"
    PICTURE_NAME = "[CQ:image,file={0}]"
    PICTURE_PATTERN = r"\[CQ:image,file=(.+)\]"
    UPLOAD_URL = "http://kan.msxiaobing.com/Api/Image/UploadBase64"
    RANK_URL = "http://kan.msxiaobing.com/Api/ImageAnalyze/Process?service=yanzhi"
    _RANK_URL = "http://kan.msxiaobing.com/Api/ImageAnalyze/Process?service=yanzhi&tid=4a3de9b27e5b4624b35a941669fdc57c"

    name = "RateAppearanceModule"

    @staticmethod
    def is_rate_appearance(message):
        if message.getContent().find(u"测颜值") == 0:
            return True
        else:
            return False

    @staticmethod
    def is_picture(message):
        if re.search(RateAppearanceModule.PICTURE_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def rate(url):
        pass

    @staticmethod
    def process(message):
        try:
            context = redisConnection.hget(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str())
            message = message[:]
            message.remove_group_at()
            # if (message.getSubType() == 1 or message.is_at()) and RateAppearanceModule.is_rate_appearance(message):
            if RateAppearanceModule.is_rate_appearance(message):
                print "[" + RateAppearanceModule.name + "]"
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(),
                                     RateAppearanceModule.CONTEXT)
                message.setContent(u"测颜值是吧，直接发图片給微微好啦~")
                message.group_at(message.getPersonQQ())
                send(message, True)
            elif RateAppearanceModule.is_picture(message) and context == RateAppearanceModule.CONTEXT:
                msg = message[:]
                message.setContent(u"微微正在识别中。。。。。。")
                message.group_at(message.getPersonQQ())
                send(message, False)
                redisConnection.hdel(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str())
                name = re.search(RateAppearanceModule.PICTURE_PATTERN, msg.getContent()).group(1)
                buffer = cStringIO.StringIO()
                img = CQImgReader.CQImgReader(
                    RateAppearanceModule.COOLQ_IMAGE_PATH.format(
                        msg.getTargetQQ()) + name + ".cqimg").get_pil_img()
                img.save("data\\" + str(message.getSendTime()) + ".jpg")
                img.save(
                    buffer, format="JPEG")
                response = requests.post(RateAppearanceModule.UPLOAD_URL, base64.b64encode(buffer.getvalue()))
                args = json.loads(response.text)
                response = requests.post(RateAppearanceModule._RANK_URL,
                                         {"Content[imageUrl]": args["Host"] + args["Url"]})
                args = json.loads(response.text)

                msg.setContent(args["content"]["text"])
                msg.group_at(msg.getPersonQQ())
                send(msg, False)
                #
                rtnImg = cStringIO.StringIO(urllib2.urlopen(args["content"]["imageUrl"]).read())
                rtnImg = Image.open(rtnImg)
                rtnImg.save(
                    RateAppearanceModule.COOLQ_IMAGE_PATH.format(msg.getTargetQQ()) + str(msg.getSendTime()) + "_.jpg")
                msg.setContent(RateAppearanceModule.PICTURE_NAME.format(str(msg.getSendTime()) + "_.jpg"))
                send(msg, True)
                #
            else:
                return
        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            traceback.print_exc()
            return

    def __init__(self):
        self.image = Image.open("1.jpg")

    def upload(self):
        buffer = cStringIO.StringIO()
        self.image.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())
        response = requests.post(RateAppearanceModule.UPLOAD_URL, img_str)
        response_args = json.loads(response.text)
        self.args = response_args["Host"] + response_args["Url"]
        print self.args
        return self

    def rank(self):
        # req = {u"MsgId": str(int(time.time())).decode("utf-8") + u"063", u"CreateTime": int(time.time()),
        #       u"Content%5BimageUrl%5D": self.args.decode("utf-8")}
        req = {"Content[imageUrl]": self.args}
        res = requests.post(RateAppearanceModule._RANK_URL, req)
        print res.text


if __name__ == "__main__":
    ram = RateAppearanceModule()
    ram.upload().rank()
