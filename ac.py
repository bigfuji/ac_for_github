import sys
import time
from hashlib import md5

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from recv_email import recv_email

# config 你的超级鹰帐号
user = 'chaojifuji'
pw = '*******'
password = md5(pw.encode('utf-8')).hexdigest()
soft_id = '892116'
headers = {'Connection': 'Keep-Alive', 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
           'Host': 'upload.chaojiying.net'}
payload = {'user': user, 'pass2': password, 'codetype': 1005, 'len_min': 4, 'softid': soft_id}
# 报错payload
payload_2 = {'user': user, 'pass2': password, 'softid': soft_id}


class create_id:
    def __init__(self, email_address, pw, country, proxy=None):
        print('init start')
        self.email_address = email_address
        self.pw = pw
        self.country = country
        if proxy == None:
            self.browser = webdriver.PhantomJS(executable_path="d:/phantomjs")
        else:
            self.proxy = ['--proxy=' + str(proxy), '--proxy-type=https']
            self.browser = webdriver.PhantomJS(executable_path="d:/phantomjs", service_args=self.proxy)
        self.browser.get('https://appleid.apple.com/account#!&page=create')
        print('init end')

    def fill_form(self):
        # email
        e_email = self.browser.find_element_by_css_selector('.field-has-info')
        e_email.send_keys(self.email_address)
        print('email end')
        # todo 密码要采用自动生成的方式来，好像相同密码会被发现？
        # todo 另外写一个webdriver看使用代理的方式是否成功
        # password
        e_pw = self.browser.find_element_by_css_selector('#password')
        e_pw.send_keys('YYFpangtouyu962')
        print('password end')
        # confrim
        e_cf = self.browser.find_element_by_css_selector('.confirm-field')
        e_cf.send_keys('YYFpangtouyu962')
        print('confirm end')
        # firstname
        e_firstname = self.browser.find_element_by_css_selector('#firstNameInput .field')
        e_firstname.send_keys('hehe')
        # lastname
        e_lastname = self.browser.find_element_by_css_selector('.last-name')
        e_lastname.send_keys('chandler')
        # birthday
        e_birth = self.browser.find_element_by_css_selector('#date')
        e_birth.click()
        e_birth.send_keys('12121997')
        print('birth end')
        # question 1
        q1 = self.browser.find_elements_by_css_selector('div.desktop.not-mobile > select')[0]
        Select(q1).select_by_index(2)
        # answer 1
        a1 = self.browser.find_element_by_css_selector('.qa-set0 .form-fieldNaN')
        a1.send_keys('a1a1a1')
        print('answer1 end')
        # question 2
        q2 = self.browser.find_elements_by_css_selector('div.desktop.not-mobile > select')[1]
        Select(q2).select_by_index(2)
        # answer 2
        a2 = self.browser.find_element_by_css_selector('.qa-set1 .form-fieldNaN')
        a2.send_keys('a2a2a2')
        print('answer2 end')
        # question 3
        q3 = self.browser.find_elements_by_css_selector('div.desktop.not-mobile > select')[2]
        Select(q3).select_by_index(2)
        # answer 3
        a3 = self.browser.find_element_by_css_selector('.qa-set2 .form-fieldNaN')
        a3.send_keys('a3a3a3')
        print('answer3 end')
        # country
        # todo 用了代理，选择了GBR英国作为国家，但是最后出来是US美国区的帐号，是否跟开了lantern有关
        e_country = self.browser.find_element_by_css_selector('#countryOptions')
        Select(e_country).select_by_value(self.country)
        # validate code
        e_img = self.browser.find_element_by_css_selector('#widget img')
        img_base64 = e_img.get_attribute('src')[24:]
        payload.update({'file_base64': img_base64})
        self.browser.save_screenshot('1.png')
        # 如果识别出结果，但是不知正确与否
        while self.browser.execute_script("return document.getElementById('send-email-code')") == None:
            e_img = self.browser.find_element_by_css_selector('#widget img')
            img_base64 = e_img.get_attribute('src')[24:]
            payload.update({'file_base64': img_base64})
            rq = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=payload, headers=headers)
            print(rq.json())
            if rq.json()['err_no'] == 0:
                pic_str = rq.json()['pic_str']
                self.pic_id = rq.json()['pic_id']
                e_captcha = self.browser.find_element_by_css_selector('#captchaInput')
                e_captcha.send_keys(pic_str)
                # click continue button
                e_continue = self.browser.find_element_by_css_selector(
                    '#widget > div.flow-footer.primary-footer.clearfix > div > button')
                e_continue.click()
                print('是时候拔网线了')
                # time.sleep(20)
                try:
                    print(element_to_be_clickable(
                        (By.CSS_SELECTOR, '#widget > div.flow-footer.primary-footer.clearfix > div > button')))
                    WebDriverWait(self.browser, 10, 1).until(
                        presence_of_element_located((By.ID, 'send-email-code')))
                    self.browser.save_screenshot('6.png')
                    print(element_to_be_clickable(
                        (By.CSS_SELECTOR, '#widget > div.flow-footer.primary-footer.clearfix > div > button')))
                    print('应该是见到输入邮箱验证码的地方了')
                    # 继续注册
                    time.sleep(30)
                    code = recv_email(self.email_address, self.pw)
                    print(code)
                    e_verify = self.browser.find_element_by_css_selector('#char0')
                    e_verify.click()
                    e_verify.send_keys(code)
                    self.browser.save_screenshot('before_click_verify.png')
                    e_verify_continue = self.browser.find_element_by_css_selector(
                        'verify-email > div.flow-footer.clearfix > div.btn-group.flow-controls.pull-right > button.button.link.last.continue')
                    e_verify_continue.click()
                    time.sleep(20)
                    self.browser.save_screenshot('after_click_verify.png')
                    break
                except TimeoutException:
                    element = self.browser.execute_script("return document.activeElement")
                    print('???这里是不知道什么element')
                    print(element.id)
                    print(element.tag_name)
                    print(element.text)
                    print(element.location)
                    print(element.get_attribute('class'))
                    print('超时了,开始检查是邮箱错误还是验证码错误')
                    # 检查是否邮箱问题
                    if 'email-field' in element.get_attribute('class'):
                        print('该邮箱已经被注册或其他邮箱相关问题')
                        break
                    # 不一定超时了就是验证码问题，有可能是因为还没得到服务器回复，特别是在用了代理的情况下
                    # 可以检查验证码图片有没有刷新 或者是 检查验证码输入框还有没有之前输入的字符
                    # todo 把输入什么的写进while里，这样当服务器没有返回结果时，刷新页面重新输入一遍
                    elif 'continue' in element.get_attribute('class'):
                        print('应该是服务器没有返回结果，还在等待中')
                        break
                    # 这里才是识别结果错误，需要回报拿回积分
                    else:
                        print('验证码问题')
                        self.report_img_error()
            # 识别服务器返回错误代码，不需要回报拿回积分
            else:
                print('重新验证码了')
                e_new_code = self.browser.find_element_by_css_selector('.first')
                e_new_code.click()
                self.browser.implicitly_wait(2)
            self.browser.save_screenshot('4.png')
        self.browser.save_screenshot('5.png')

    def verify_email(self):
        pass
        # get email verify and input in browser

    # 验证码错误，上报返分
    def report_img_error(self):
        payload_2.update({'pic_id': self.pic_id})
        report_url = 'http://code.chaojiying.net/Upload/ReportError.php'
        rq_2 = requests.post(report_url, data=payload_2)
        print('识别错误回报结果' + str(rq_2.json()))


if __name__ == '__main__':
    email_add = sys.argv[1]
    email_pw = sys.argv[2]
    country_code = sys.argv[3]
    proxy = sys.argv[4]
    g = create_id(email_add, email_pw, country_code, proxy)
    g.fill_form()
