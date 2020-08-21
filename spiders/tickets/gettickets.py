start_urls = ['http://www.chinaticket.com/']
# （2）获取其他票务网站的网址，用来爬取数据。
urls = {
    'yanchanghui':"http://www.chinaticket.com/wenyi/yanchanghui/",
    'huaju':"http://www.chinaticket.com/wenyi/huaju/",
    'yinlehui':"http://www.chinaticket.com/wenyi/yinlehui/",
    'yinleju':"http://www.chinaticket.com/wenyi/yinleju/",
    'xiqu':"http://www.chinaticket.com/wenyi/xiqu/",
    'baleiwu':"http://www.chinaticket.com/wenyi/baleiwu/",
    'qinzijiating':"http://www.chinaticket.com/wenyi/qinzijiating/",
    'zaji':"http://www.chinaticket.com/wenyi/zaji/",
    'xiangshengxiaopin':"http://www.chinaticket.com/wenyi/xiangshengxiaopin/",
    'zongyijiemu':"http://www.chinaticket.com/wenyi/zongyijiemu/",
    'zuqiu':"http://www.chinaticket.com/tiyu/zuqiu/",
    'gaoerfuqiu':"http://www.chinaticket.com/tiyu/gaoerfuqiu/",
    'Cbalanqiu':"http://www.chinaticket.com/tiyu/Cbalanqiu/",
    'saiche':"http://www.chinaticket.com/tiyu/saiche/",
    'quanji':"http://www.chinaticket.com/tiyu/quanji/",
    'dianyingpiao':"http://www.chinaticket.com/qita/dianyingpiao/",
    'jingdianmenpiao':"http://www.chinaticket.com/qita/jingdianmenpiao/",
    'zhanlan':"http://www.chinaticket.com/qita/zhanlan/",
    'yundongxiuxian':"http://www.chinaticket.com/qita/yundongxiuxian/",
    'lipinquan':"http://www.chinaticket.com/qita/lipinquan/",
    'huiyi':"http://www.chinaticket.com/qita/huiyi/",
}

def start_requests(self):
    try:
        for key,value in self.urls.items():                          #请求页面的循环
            yield Request(value.encode('utf-8'),meta= {"type":key.encode('utf-8')}, callback = self.parse)
    except Exception as err:                                            #没有则报错
        print (err)                                                     #会输出错误

def get_next_url(self):
    try:                                                                                     #遍历所有页面
         pass
    except Exception as  err:
         print (err)


def parse(self, response):
    try:
         item = TicketCrawlerItem()
         meta = response.meta
         result = response.text.encode("utf-8")                    #编码格式为UTF-8
         if result == '' or result == 'None':                        #页面结果为空
              print ("Can't get the sourceCode ")                  #报告没有信息
              sys.exit()
         tree = etree.HTML(result)                                     #存放结果
         data = []
            #演出条数
         page = tree.xpath("//*[@class='s_num']/text()")[1].replace("\n","").
             replace("",""). encode("utf-8")
            #页数
         calculateNum = calculatePageNumber()
         pageNUM = calculateNum.calculate_page_number(page)
         count = (pageNUM/10)+1
         listDoms = tree.xpath("//*[@class='s_ticket_list']//ul")
         if(listDoms):
              for itemDom in listDoms:                                          #循环遍历
              # #数据存放
                  item['type'] = meta['type'].encode("utf-8")
                  try:
                       titleDom = itemDom.xpath("li[@class='ticket_list_tufl']/a/text()")
                       if(titleDom[0]):                                         #检查标题情况
                       item['name'] = titleDom[0].encode("utf-8")
                  except Exception as err:                               #没有则报错
                       print (err)                                               #会输出错误
                  try:
                       urlDom = itemDom.xpath("li[@class='ticket_list_tu fl']/a/@href")
                      if(urlDom[0]):                                                   #检查票务信息
                           item['url'] = urlDom[0].encode("utf-8")
                  except Exception as err:                               #没有则报错￼
                       print (err)                                         #会输出错误￼
                  try:
                  timeDom = itemDom.xpath("li[@class='ticket_list_tu fl']/span[1]/text()")
                  if(timeDom[0]):                                            #检查时间信息￼
                       item['time'] = timeDom[0].encode("utf-8").replace ('时间:','')
                  except Exception as err:                                #没有则报错￼
                       print (err)                                        #会输出错误￼
                  try:
                  addressDom = itemDom.xpath("li[@class='ticket_list_tu fl']/span[2] /text()")
                  if(addressDom[0]):                                            #检查地点信息￼
                       item['address'] = addressDom[0].encode("utf-8").replace('地点:','')
                  except Exception as err:                              #没有则报错￼
                       print (err)                                               #会输出错误￼
                  try:
                       priceDom = itemDom.xpath("li[@class='ticket_list_tu fl']/span[3] / text()")
                  if(priceDom[0]):                                                #检查票价信息￼
                       item['price'] = priceDom[0].encode("utf-8").replace('票价:','')
                  except Exception as err:                             #没有则报错￼
                        print (err)                                             #会输出错误￼
                  yield item
        for i in range(2,count+1):                  #循环操作，用于不断获取下一票务页面的信息￼
              next_page = "http://www.chinaticket.com/wenyi/" + str(meta
                  ['type'])+ "/?o = 2&page = "+str(i)
              if next_page is not None:                           #检查是否还有未爬取的页面￼
                  yield scrapy.Request(next_page, meta={"type":meta['type']},
                  callback=self.parse)
    except Exception as err:                                                       #没有则报错￼
        print (err)                                                                        #会输出错误
