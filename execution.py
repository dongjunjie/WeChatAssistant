#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import re

import itchat

import config
import screenshoot
from autoreply import MsgAutoReply
from keywordlistener import KeywordListener as Keyword
from signin import SignInMPS
# from takephoto import TakeGIF


class Execution:
    REVOCATIONPATH = "./Revocation/"

    def __init__(self):
        self.keyword = Keyword()
        self.snin = SignInMPS()
        self.reply = MsgAutoReply()

    def Execution(self, message):
        """
        执行命令
        :param message: 微信消息中提取的命令
        :return: 无
        """
        # "%s%s%s%s%s关键词" % ("="*4, "Command Message", "="*4, "\n\n", action)

        command = message['Text']
        msg_send = u"机器人自动回复:\n\n"
        if re.match(ur"^查看文件\[.*\]", command):
            filename = re.search(ur"^查看文件\[(.*?)\]$", command).group(1)
            result = self.ShowFile(filename)
            if result == True:
                pass
            else:
                msg_send += result
                itchat.send(msg_send, toUserName='filehelper')

        elif re.match(ur"^删除文件\[.*\]", command):
            filename = re.search(ur"^删除文件\[(.*?)\]$", command).group(1)
            msg_send += self.DeleteFile(filename)
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(ur"^添加关键词\[.*\]", command):
            keyword = re.search(ur"^添加关键词\[(.*?)\]", command).group(1)
            msg_send += self.keyword.AddKeyword(keyword)
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(ur"^删除关键词\[.*\]", command):
            keyword = re.search(ur"^删除关键词\[(.*?)\]", command).group(1)
            msg_send += self.keyword.DeleteKeyword(keyword)
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(ur"^撤回附件列表$", command):
            self.ReturnAttachmentList()

        elif re.match(ur"^清空附件列表$", command):
            self.ClearAttachmentList()

        elif re.match(u"^查看关键词$", command):
            msg_send += self.keyword.ShowKeyword()
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^清空关键词$", command):
            msg_send += self.keyword.ClearKeyword()
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^查看签到口令$", command):
            msg_send += self.snin.ShowComd()
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^清空签到口令$", command):
            msg_send += self.snin.ClearComd()
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^添加签到口令\[.*?\]$", command):
            mps, cmd = re.search(u"^添加签到口令\[(.*?):(.*?)\]$", command).group(1, 2)
            self.snin.AddComd(mps, cmd)
            msg_send += u"添加签到口令[{}:{}]成功".format(mps, cmd)
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^删除签到口令\[.*?\]$", command):
            mps = re.search(u"^删除签到口令\[(.*?)\]$", command).group(1)
            msg_send += self.snin.DeleteComd(mps)
            itchat.send(msg_send, toUserName='filehelper')

        elif re.match(u"^截图$", command):
            screenshoot.SC()
        elif re.match(u"^添加自动回复\[.*?\]$", command):
            keyword, content = re.search(u"^添加自动回复\[(.*?):(.*?)\]$", command).group(1, 2)
            msg_send += self.reply.AddRule(keyword, content)
            itchat.send(msg_send, toUserName="filehelper")
        elif re.match(u"^删除自动回复\[.*\]$", command):
            keyword = re.search(u"^删除自动回复\[(.*?)\]$", command).group(1)
            msg_send += self.reply.DeleteRule(keyword)
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^清空自动回复$", command):
            msg_send += self.reply.ClearRule()
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^查看自动回复$", command):
            msg_send += self.reply.ShowRule()
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^关闭自动回复$", command):
            msg_send += self.reply.CloseAutoReply()
            print msg_send
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^打开自动回复$", command):
            msg_send += self.reply.OpenAutoReply()
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^拍照$", command):
            msg_send += u"功能未开发，敬请期待"
            itchat.send(msg_send, toUserName='filehelper')
            """
           img_name = TakePhoto()
            if img_name:
                itchat.send("@img@{}".format(img_name), toUserName='filehelper')
            else:
                msg_send += "拍照失败，请重试"
                itchat.send(msg_send, toUserName='filehelper')
            """

        elif re.match(u"^拍动图\d{0,2}$", command):
            msg_send += u"功能未开发，敬请期待"
            itchat.send(msg_send, toUserName='filehelper')
            """
            seconds = re.findall("^拍动图(\d+)", command)
            if seconds:
                seconds = int(seconds[0])
                if seconds not in range(1, 61):
                    msg_send += "时间输入错误，请重试"
                    itchat.send(msg_send, toUserName='filehelper')
                    return
            else:
                seconds = 5
            img_name = TakeGIF(seconds)
            if img_name:
                itchat.send("@img@{}".format(img_name), toUserName='filehelper')
            else:
                msg_send += "拍照失败，请重试"
                itchat.send(msg_send, toUserName='filehelper')
            """
        elif re.match(u"^今天吃什么$", command):
            today_choice = random.choice(config.today_menu)
            emotion = random.choice(config.emoticons)
            msg_send += u"今天就吃 {} 吧{}{}".format(today_choice, '\n', emotion)
            itchat.send(msg_send, toUserName='filehelper')
        elif re.match(u"^退出程序$", command):
            itchat.send(u"退出程序成功", toUserName='filehelper')
            itchat.logout()
            os._exit(0)
        else:
            itchat.send(ur"暂时支持以下指令：{1}"
                        ur"查看/删除文件[文件名]{0}e.g.查看[123345234.mp3]{1}"
                        ur"撤回附件列表(查看都有哪些保存在电脑中的已撤回附件){1}"
                        ur"清空附件列表(清空已经保存在电脑中的附件){1}"
                        ur"添加关键词[关键词]{0}e.g.设置关键词[在不在]{1}"
                        ur"删除关键词[关键词]{0}e.g.删除关键词[在不在]{1}"
                        ur"清空关键词  清空已经设置的所有关键词{1}"
                        ur"查看关键词  查看目前设置的关键词{1}"
                        ur"添加签到口令[公众号:签到口令]{0}e.g.添加签到口令[招商银行信用卡:签到]{1}"
                        ur"删除签到口令[公众号]{0}e.g.删除签到口令[招商银行信用卡]{1}"
                        ur"查看签到口令  查看已经存在的公众和和对应的签到口令{1}"
                        ur"清空签到口令  清空所有签到口令{1}"
                        ur"截图 截取运行本程序的机器当前界面{1}"
                        ur"添加自动回复[针对的关键词:回复内容]{0}e.g.添加自动回复[在不在:我现在有事情，待会儿回复你]{1}"
                        ur"删除自动回复[针对的关键词]{0}e.g.删除自动回复[在不在]{1}"
                        ur"清空自动回复{1}"
                        ur"关闭自动回复{1}"
                        ur"打开自动回复{1}"
                        ur"今天吃什么{1}"
                        ur"退出程序{1}"
                        ur"其他指令暂不支持，请期待最新版本。".format("\n", "\n\n"),
                        toUserName="filehelper")

    def ShowFile(self, filename):
        if not os.path.exists(r"./Revocation/" + filename):
            return "文件:{} 不存在".format(filename)

        if re.search(r"png|jpg|bmp|jpeg|gif|webp", filename):
            msg_type = "img"
        elif re.search(r"avi|rm|mp4|wmv", filename):
            msg_type = "vid"
        else:
            msg_type = "fil"

        itchat.send("@{}@{}".format(msg_type, r"./Revocation/" + filename),
                    toUserName="filehelper")

        return True

    def DeleteFile(self, filename):
        if not os.path.exists(r"./Revocation/" + filename):
            return "文件:{} 不存在".format(filename)
        else:
            os.remove(r"./Revocation/" + filename)
            return "文件:{} 删除成功".format(filename)

    def ClearAttachmentList(self):
        if self.REVOCATIONPATH:
            try:
                for item in os.listdir(self.REVOCATIONPATH):
                    os.remove(self.REVOCATIONPATH + item)

                msg = "{0}{1}{0}{2}撤回助手：清空附件成功".format(
                    "=" * 6, "助手消息", "\n\n")
                itchat.send(msg, toUserName='filehelper')
            except:
                msg = "{0}{1}{0}{2}撤回助手：清空附件失败，请重试".format(
                    "=" * 6, "助手消息", "\n\n")
                itchat.send(msg, toUserName='filehelper')
        else:
            msg = "{0}{1}{0}{2}撤回助手：暂时没有附件".format(
                "=" * 6, "助手消息", "\n\n")
            itchat.send(msg, toUserName='filehelper')

    # 返回撤回附件所有文件名
    def ReturnAttachmentList(self):
        if os.listdir(self.REVOCATIONPATH):
            print u"有附件"
            msg_send = u"助手消息：所有储存的附件如下：\n"
            print msg_send
            for item in os.listdir(self.REVOCATIONPATH):
                msg_send += u"{} {}".format(item, "\n")
            print msg_send
            itchat.send(msg_send, toUserName="filehelper")
        else:
            print u"无附件"
            msg = u"助手消息：暂时没有撤回的附件\n"
            itchat.send(msg, toUserName="filehelper")
