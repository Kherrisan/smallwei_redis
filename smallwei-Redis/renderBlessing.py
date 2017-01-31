# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import re
import urllib2
import cStringIO

FONT_SIZE = 30


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


class RenderBlessing:
    logoApi = "http://q2.qlogo.cn/headimg_dl?dst_uin={0}&spec=100&url_enc=0&referer=bu_interface&term_type=PC"
    nickNameApi = "http://r.pengyou.com/fcg-bin/cgi_get_portrait.fcg?uins={0}"
    content_pos_1 = (132, 916)
    content_pos_2 = (62, 976)
    content_size = FONT_SIZE

    receiver_logo_region = (56, 762, 56 + 100, 762 + 100)
    receiver_logo_pos = (56, 762)
    receiver_logo_size = (103, 103)
    receiver_qq_pos = (194, 828)
    receiver_qq_size = FONT_SIZE
    receiver_name_pos = (194, 785)
    receiver_name_size = FONT_SIZE

    sender_logo_region = (441, 1057, 441 + 100, 1057 + 100)
    sender_logo_pos = (441, 1057)
    sender_logo_size = (103, 103)
    sender_qq_pos = (579, 1120)
    sender_qq_size = FONT_SIZE
    sender_name_pos = (579, 1077)
    sender_name_size = FONT_SIZE

    font_color = (0, 0, 0)

    @staticmethod
    def choose():
        blessingContent = u"中英混合abcdabcde五六七八九十1234567890一二三四五六七八九十"
        return RenderBlessing(459861669, 2972822179, blessingContent)

    def __init__(self, receiver, sender, uContent):
        self.background = Image.open("blessing.jpg")
        self.content = uContent
        self.length = len(self.content.encode("gbk"))
        self.font_other = ImageFont.truetype("simhei.ttf", FONT_SIZE)
        self.font_content = ImageFont.truetype("simhei.ttf", FONT_SIZE + 5)
        self.receiver_qq = receiver
        self.sender_qq = sender

    def get_logo(self, qq):
        img_bytes = cStringIO.StringIO(urllib2.urlopen(RenderBlessing.logoApi.format(qq)).read())
        return Image.open(img_bytes)

    def render(self):
        receiver_logo = self.get_logo(self.receiver_qq)
        receiver_logo.resize(RenderBlessing.receiver_logo_size)
        sender_logo = self.get_logo(self.sender_qq)
        sender_logo.resize(RenderBlessing.sender_logo_size)
        self.background.paste(receiver_logo, RenderBlessing.receiver_logo_region)
        self.background.paste(sender_logo, RenderBlessing.sender_logo_region)
        img_draw = ImageDraw.Draw(self.background)
        img_draw.text(RenderBlessing.receiver_name_pos, self.get_nickname(self.receiver_qq),
                      font=self.font_other,
                      fill=RenderBlessing.font_color)
        img_draw.text(RenderBlessing.receiver_qq_pos, str(self.receiver_qq), font=self.font_other,
                      fill=RenderBlessing.font_color)
        img_draw.text(RenderBlessing.sender_name_pos, self.get_nickname(self.sender_qq), font=self.font_other,
                      fill=RenderBlessing.font_color)
        img_draw.text(RenderBlessing.sender_qq_pos, str(self.sender_qq), font=self.font_other,
                      fill=RenderBlessing.font_color)
        linec = 0
        tempc=0
        for i in range(0, len(self.content)):
            tempc+=1
            if is_chinese(self.content[i]):
                linec += 2
            else:
                linec += 1
            if linec > 32:
                break
        img_draw.text(RenderBlessing.content_pos_1, self.content[:tempc], font=self.font_content,
                      fill=RenderBlessing.font_color)
        img_draw.text(RenderBlessing.content_pos_2, self.content[tempc:], font=self.font_content,
                      fill=RenderBlessing.font_color)
        self.background.save("C:\\Users\\Administrator\\Desktop\\web\\testwebpy\\static\\blessing_"+str(self.receiver_qq)+str(self.sender_qq)[:4]+".jpg")
        return self

    def get_url(self):
        return u"http://115.159.53.213/?qq="+str(self.receiver_qq)+str(self.sender_qq)[:4]

    def get_nickname(self, qq):
        raw_str = urllib2.urlopen(RenderBlessing.nickNameApi.format(qq)).read()
        nick = re.search(r',"(.*)",[0-9]+\]\}\)$', raw_str)
        if nick:
            print nick.group(1).decode("gbk")
            print type(nick.group(1).decode("gbk"))
            return nick.group(1).decode("gbk")
        else:
            return ""


if __name__ == "__main__":
    RenderBlessing.choose().render()
