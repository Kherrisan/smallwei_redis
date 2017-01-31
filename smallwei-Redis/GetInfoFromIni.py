# -*- coding:utf-8 -*-

def getinfo(qq):
    class GetInfoFromIni:
        '''从QQ_SEU.ini文件中提取已注册用户的所有信息

        '''
        def _i_(self):
            self.f_obj = open('QQ_SEU.ini')
            self.card = 0
            self.dept = ""
            self.name = ""
            self.stuno = ""
            self.major = ""
            self.grade = ""
            try:
                for line in self.f_obj:
                    the_text = self.f_obj.next()
                    if the_text.find(str(qq)) != -1:
                        self.card = str(the_text[the_text.find('|') + 1:the_text.find('\t|1')])
                        self.name = str(the_text[the_text.find('|1') + 2:the_text.find('\t|2',the_text.find('|1'))])
                        self.dept = str(the_text[the_text.find('|3',the_text.find('\t|2')) + 2:the_text.find('\t|4',the_text.find('|3'))])
                        self.stuno = str(the_text[the_text.find('|2',the_text.find('\t|1')) + 2:the_text.find('\t|3',the_text.find('|2'))])
                        self.major = str(the_text[the_text.find('|4',the_text.find('\t|3')) + 2:the_text.find('\t|5',the_text.find('|4'))])
                        self.grade = str(the_text[the_text.find('|5',the_text.find('\t|4')) + 2:-1])
            except Exception as e:
                print str(e.message)
            finally:
                self.f_obj.close()
    stuinfo = GetInfoFromIni()
    stuinfo._i_()
    return (stuinfo.card,stuinfo.name,stuinfo.dept,stuinfo.stuno,stuinfo.major,stuinfo.grade)


def insertinfo(qq,card):
    class InsertInfoToIni:
        '''向QQ_SEU.ini中写入注册一卡通所对应的所有信息

        具体信息在all_info.txt中

        '''
        def _i_(self):
            self.f_obj_out = open('all_info.txt')
            self.f_obj_in = open('QQ_SEU.ini','a')
            for line in self.f_obj_out:
                the_text = self.f_obj_out.next()
                if the_text.find(str(card)) != -1:
                    self.qq = str(qq)
                    self.card = the_text[0:9]
                    self.stuno = the_text[10:18]
                    self.name = the_text[19:the_text.find('\t[')]
                    self.dept = the_text[the_text.find(']') + 1:the_text.find('\t[',the_text.find('['))]
                    self.major = the_text[the_text.find(']',the_text.find('\t[',the_text.find('['))) + 1:-1]
                    self.grade = the_text[3:5]
                    seq = [         self.qq + '\t|', 
                                    self.card.decode('utf-8').encode('utf-8') + '\t|1',
                                    self.name.decode('utf-8').encode('utf-8') + '\t|2',
                                    self.stuno.decode('utf-8').encode('utf-8') + '\t|3',
                                    self.dept.decode('utf-8').encode('utf-8') + '\t|4',
                                    self.major.decode('utf-8').encode('utf-8') + '\t|5',
                                    self.grade.decode('utf-8').encode('utf-8') + '\r' ]
                    self.f_obj_in.writelines(seq)
                    break
                else:
                    self.name = ""
            self.f_obj_in.close()
            self.f_obj_out.close()

    insert = InsertInfoToIni()
    insert._i_()
    if insert.name != "":
        return True
    else:
        return False