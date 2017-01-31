import threading
from Message import *
import time
import Queue
import traceback
from DatabaseSession import *
from sqlalchemy import desc

mutex = threading.Lock()


class DuplicateRemoval:
    messagelist=[]

    @staticmethod
    def check_depulicate(message):
        # if len(DuplicateRemoval.messagelist)>0 and time.time()-DuplicateRemoval.messagelist[0].getSendTime()>10:
        #     del DuplicateRemoval.messagelist[0]
        # for i in range(0,len(DuplicateRemoval.messagelist)):
        #     if message.getContent()==DuplicateRemoval.messagelist[i].getContent() and message.getPersonQQ()==DuplicateRemoval.messagelist[i].getPersonQQ() and message.getSubType()==DuplicateRemoval.messagelist[i].getSubType():
        #         del DuplicateRemoval.messagelist[i]
        #         return True
        # DuplicateRemoval.messagelist.append(message)
        # return False
        session = Session()
        try:
            query = session.query(MessageModel).filter(MessageModel.content == message.getContent(),
                                                       MessageModel.personQQ == message.getPersonQQ(),
                                                       MessageModel.groupQQ == message.getGroupQQ(),
                                                       MessageModel.subType == message.getSubType()).order_by(desc(MessageModel.sendTime)).first()
            if query and message.getSendTime() - query.sendTime < 3:
                return True
            else:
                return False
        except Exception as e:
            traceback.print_exc()
        finally:
            session.close()

# class DuplicateRemovalTimer(threading.Thread):
#     def __init__(self):
#         super(DuplicateRemovalTimer, self).__init__()
#         self.queue = []
#
#     def push_back(self, message):
#         self.queue.append(message)
#
#     def find_duplicate(self, message):
#         for im in self.queue:
#             if im.getContent() == message.getContent()
#                 and im.getSubType() == message.getSubType()
#                 and im.getPersonQQ() == message.getPersonQQ()
#                 and im.getGroupQQ() == message.getGroupQQ():
#                 mutex.acquire()
#                 self.queue.remove(im)
#                 mutex.release()
#                 return True
#         return False
#
#     def run(self):
#         while True:
#             try:
#                 for im in self.queue:
#                     if time.time() - im.getSendTime() > 5:
#                         mutex.acquire()
#                         self.queue.remove(im)
#                         mutex.release()
#             except Exception as e:
#                 traceback.print_exc()
