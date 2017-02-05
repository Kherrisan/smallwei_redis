# -*- coding: utf-8 -*-
import threading
import traceback

mutex = threading.Lock()


def log(threadName=None, moduleName=None, level="info", content="process"):
    if not threadName:
        threadName=threading.currentThread().getName()
    mutex.acquire()
    try:
        print u"[{0}][{1}][{2}]{3}".format(level, moduleName, threadName, content)
        if level == "error":
            err=traceback.format_exc()
            print err
            file=open("log.txt","a")
            file.write(err)
            file.close()
    except Exception as e:
        print u"[{0}][{1}][{2}]{3}".format("error", "Log", threadName, e.message)
	err=traceback.format_exc()
        print err
    finally:
        mutex.release()
