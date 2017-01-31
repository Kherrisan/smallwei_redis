# -*- coding: utf-8 -*-

class testStatic:
    def static1():
        print "static1"
        pass

    def statci2():
        static1()
        print "static2"
        return

if __name__=="__main__":
    testStatic.statci2()