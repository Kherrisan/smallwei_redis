import urllib
import urllib2
import cookielib

def getpaocao(inputid):
    class seu_paocao:
        def __init__(self):
            self.loginurl = 'http://115.159.189.89/seu/api.php'
            self.cookiejar = cookielib.CookieJar()
            self.postdata = urllib.urlencode({'cardnum':str(inputid)})
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
            self.num = -1

        def paocao_init(self):
            myRequest = urllib2.Request(url = self.loginurl,data = self.postdata)
            result = self.opener.open(myRequest)
            self.num = str(result.read())

    Paocao = seu_paocao()
    Paocao.paocao_init()
    return Paocao.num