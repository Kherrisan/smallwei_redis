# -*- coding: utf-8 -*-
import socket
import threading
import Queue
from Message import MessageModel
from Model import Message, Session
import requests
import json

PORTCPP2PY = 10000  # The port to listen.
# The capacity of readin buffer of socket.Same as the buffer size in cpp
# socket.
MAX_MSG = 4096
MAX_PROCESS_THREAD_NUM = 5  # The max number of process threads.


class SenderThread(threading.Thread):

    def __init__(self, connection, outQueue):
        super(SenderThread, self).__init__(name="SenderThread")
        self.connection = connection
        self.outQueue = outQueue
        self.runFlag = True
        self.isError = False

    def run(self):
        try:
            while self.runFlag:
                if not self.outQueue.empty():
                    dataStream = self.outQueue.get()
                    if dataStream:
                        print "[send] " + self.getName() + " " + dataStream
                        self.connection.send(dataStream)
        except Exception as e:
            print "[error] " + self.getName() + " ", e
            self.isError = True
            return

    def stop(self):
        print "[info] " + self.getName() + " stop."
        self.runFlag = False

    def hasErr(self):
        return self.isError


class ReceiverThread(threading.Thread):

    def __init__(self, connection, inQueue):
        super(ReceiverThread, self).__init__(name="ReceiverThread")
        self.connection = connection
        self.inQueue = inQueue
        self.runFlag = True
        self.isError = False

    def run(self):
        try:
            while self.runFlag:
                dataStream = self.connection.recv(MAX_MSG)
                if dataStream:
                    print "[receive] " + self.getName() + " " + dataStream
                    self.inQueue.put(dataStream)
        except Exception as e:
            print "[error] " + self.getName() + " ", e
            self.isError = True
            return

    def stop(self):
        print "[info] " + self.getName() + " stop."
        self.runFlag = False

    def hasErr(self):
        return self.isError


class ProcessThread(threading.Thread):

    def __init__(self, threadName, inQueue, outQueue):
        super(ProcessThread, self).__init__(name=threadName)
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.runFlag = True
        self.session = Session()

    def process(self, dataStream):
        try:
            self.session.add(MessageModel.produceDBMessage(dataStream))
            self.session.commit()
            socketMessage = MessageModel.produceMessege(dataStream)
            # socketMessage.setContent("test")
            # here to process the socketMessege from the cpp socket
            # Ex :
            #   socketMessege=func(socketMessege)
            # here to process the socketMessege from the cpp socket
            rtn = requests.post("http://www.tuling123.com/openapi/api", data=json.dumps(
                {"key": "bbb5b4a65e80438a8bc4809784c70b7f", "info": socketMessage.getContent(),
                 "uesrid": socketMessage.getPersonQQ()}))
            socketMessage.setContent(json.loads(rtn.text)["text"])
            dataStream = socketMessage.getDataStream()
            print "[process] " + self.getName() + " " + dataStream
            return dataStream
        except Exception as e:
            print "[error] " + self.getName() + " ",e
            self.session=Session()


    def run(self):
        print "[info] " + self.getName() + " start."
        while self.runFlag:
            if not self.inQueue.empty():
                dataStream = self.inQueue.get()
                dataStream = self.process(dataStream)
                if dataStream:
                    self.outQueue.put(dataStream)

    def stop(self):
        print "[info] " + self.getName() + " stop."
        self.runFlag = False


class MainThread:

    def __init__(self):
        self.inQueue = Queue.Queue()
        self.outQueue = Queue.Queue()
        self.sender = 0
        self.receiver = 0
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(("", PORTCPP2PY))
        self.serverSocket.listen(MAX_PROCESS_THREAD_NUM)
        self.processThreadList = []
        for i in range(0, MAX_PROCESS_THREAD_NUM):
            self.processThreadList.append(ProcessThread(
                "processThread_" + str(i), self.inQueue, self.outQueue))
            self.processThreadList[i].start()

    def run(self):
        while True:
            print "[info] Waiting to be connected."
            conn, addr = self.serverSocket.accept()
            if conn:
                print "[info] Connected."
                self.sender = SenderThread(conn, self.outQueue)
                self.sender.start()
                self.receiver = ReceiverThread(conn, self.inQueue)
                self.receiver.start()
                while not (self.sender.hasErr() or self.receiver.hasErr()):
                    continue
                self.sender.stop()
                self.receiver.stop()


class SocketServer:

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(("", PORTCPP2PY))
        self.serverSocket.listen(MAX_PROCESS_THREAD_NUM)
        self.session = Session()
        self.conn = 0

    def run(self):
        while True:
            try:
                print "[info] Waiting to be connected."
                self.conn, addr = self.serverSocket.accept()
                while self.conn:
                    dataStream = self.conn.recv(4096)
                    print "[receive] ", dataStream
                    self.session.add(MessageModel.produceDBMessage(dataStream))
                    self.session.commit()
                    socketMessage = MessageModel.produceMessege(
                        dataStream)
                    # =========================================================
                    #
                    # =========================================================
                    print "[send] ", dataStream
                    self.conn.send(socketMessage.getDataStream())
            except Exception as e:
                print e
                continue


if __name__ == "__main__":
    # ss = SocketServer()
    # ss.run()
    mainThread = MainThread()
    mainThread.run()
