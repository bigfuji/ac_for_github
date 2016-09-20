import os
import poplib
import re
import sys

import pyzmail


def recv_email(email, password):
    # 判定是否成功
    if email.endswith('163.com'):
        pop3_server = 'pop3.163.com'
    if email.endswith('sina.com'):
        pop3_server = 'pop.sina.com'
    if email.endswith('sohu.com'):
        pop3_server = 'pop3.sohu.com'
    if email.endswith('tom.com'):
        pop3_server = 'pop.tom.com'
    result = None
    # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(email)
    try:
        server.pass_(password)
        # stat()返回邮件数量和占用空间:
        print('Messages: %s. Size: %s' % server.stat())
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        # print(mails)
        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        # print(index)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("多半是邮箱异常不能登录")
        result = 2
        return result

    for i in range(index):
        # 先收取最新的邮件
        i = index - 1 - i
        resp, lines, octets = server.retr(i + 1)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        # print(lines)
        # print(len(lines))
        # print(type(lines))
        linesep = os.linesep.encode('utf-8')
        msg_content = linesep.join(lines)
        # 稍后解析出邮件:
        msg = pyzmail.PyzMessage.factory(msg_content)
        # print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
        # print(guess_charset(msg))
        # 如果不是来自Apple的邮件则删除
        print(msg.get_subject())
        if not ('Apple' in (msg.get_address('from')[1])):
            pass
            # server.dele(i+1)
        if msg.get_subject() == 'Verify your Apple ID email address':
            # print(msg.text_part.get_payload().decode('utf-8','ignore'))
            # print(msg.html_part.get_payload())
            s1 = "\d{6}"
            p1 = re.compile(s1)
            code = re.search(p1, msg.text_part.get_payload().decode(errors='ignore')).group()
            # print(code)
            # print(type(code))
            # server.dele(i+1)
            result = code
            break
    # server.dele(index)
    # 关闭连接:
    server.quit()
    return result


if __name__ == '__main__':
    email_address = '******'
    email_pw = '********'
    # pop3_server = 'pop3.163.com'
    recv_email(email_address, email_pw)
