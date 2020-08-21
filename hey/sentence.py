class Sentence():
    def __init__(self, s):
        self.s = s
        # 句子的目的。0不明，1寒暄，2询问原因，3获得认同，4表达情绪，5教育机器，表明态度
        self.aim = 0
        # 句子的类型。0不明，1陈述句，2疑问句，3反问句...
        self.type = ''
        # 先不用。说话人。1机器，2用户，3他人。
        # self.owner = 1
        # 主谓宾及其修饰语
        # 主语。人或物，0没有，1机器，2用户，3他人，4死物，5动物
        self.zhu = 0
        self.zhu_how = 0
        self.wei = 0
        self.wei_how=0
        self.bing = 0
        self.bing_how=0
        self.reply='不明白'

        # 清理句子中无意义的字词
        self.clean()
        self.get_aim()
        self.get_reply()


    def clean(self):
        clean_word='啊额哦呢哼唔吧么呗啦哈呵呐呀吖耶哇嗯嘻'
        for word in clean_word:
            self.s=self.s.replace(word,'')
        #如果没有内容了，就敷衍一句
        if self.s=='':
            self.reply='嘻嘻'


    def get_aim(self):
        hellos=['你好','早上好','晚上好','中午好','hello','HELLO','Hello','hi','Hi','HI']
        if (any(hello in self.s for hello in hellos)):
            self.aim = 1
            self.reply=self.s
        if '请问' in self.s:
            self.aim = 2

    def get_reply(self):
        pass

