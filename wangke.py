import base64
import json
import shelve
import tkinter as tk
from tkinter import messagebox
import execjs
import requests
from bs4 import BeautifulSoup

sub_courses = []
class_ls = []
c_ls = []


window = tk.Tk()
window.geometry('800x400')


class dkl(object):
    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password


    @staticmethod
    def login():
        # 获取验证码
        code_url = 'https://daikanla.com/home/index/imgcode.html'
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }
        re_get = requests.get(code_url, headers=headers)

        with open('file/dkl_code.png', 'wb') as f:
            f.write(re_get.content)

        # 冰拓验证码识别
        api_post_url = "http://www.bingtop.com/ocr/upload/"
        with open('file/dkl_code.png', 'rb') as pic_file:
            img64 = base64.b64encode(pic_file.read())
        params = {
            "username": "%s" % '1453994097',
            "password": "%s" % 'pzy000116.',
            "captchaData": img64,
            "captchaType": 1000
        }
        response = requests.post(api_post_url, data=params)
        dictdata = json.loads(response.text)
        code = dictdata['data']['recognition']

        # 登陆
        data = {
            'qq': '1453994097',
            'pwd': '769935554',
            'imgcode': code
        }
        login_url = 'https://daikanla.com/home/index/login.html'
        re_post = requests.post(login_url, cookies=re_get.cookies, data=data)
        #re_post.cookies['welcome'] = '0'
        # 保存cookies
        cookies = shelve.open('file/cookies')
        re_get.cookies['token'] = re_post.cookies['token']
        cookies['dkl_cookies'] = re_get.cookies
        print(cookies['dkl_cookies'])
        cookies.close()


    def query_(self, type):
        key_url = 'https://daikanla.com/agent/index/mooclogin.html'
        headers = {
            'referer': 'https://daikanla.com/agent/index/index.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }
        data = {
            'type': type,
            'userinfo': self.name + ' ' + self.password
        }
        cookies = shelve.open('file/cookies')
        dkl_cookies = cookies['dkl_cookies']
        cookies.close()

        re_key = requests.post(key_url, headers=headers, data=data, cookies=dkl_cookies)
        if re_key.text == 'error':
            re_key = requests.post(key_url, headers=headers, data=data, cookies=dkl_cookies)
        dic = eval(re_key.text)
        if dic['state'] == '0':
            messagebox.showerror(message=dic['msg'] + self.name)
            return 0
        query_url = 'https://daikanla.com/agent/index/course.html?course=' + dic['course']
        query_re = requests.get(query_url, cookies=dkl_cookies)
        soup = BeautifulSoup(query_re.text, 'lxml')
        tr = soup.find_all('tr')
        query_ls = [self.name, self.password]
        query_dic = {'course': dic['course']}
        for i in tr:
            td_soup = BeautifulSoup(str(i), 'lxml')
            try:
                query_ls.append(td_soup.find('td').getText())
                query_dic[td_soup.find('td').getText()] = td_soup.find('input')['value']
            except:
                pass
        print(query_ls)
        return query_ls, query_dic


    def submit_(self, course, value):
        sub_url = 'https://daikanla.com/agent/index/submittask.html'
        cookies = shelve.open('file/cookies')
        dkl_cookies = cookies['dkl_cookies']
        cookies.close()
        data = {
            'course': course,
            'videoTask': value,
            'examTask': value
        }
        re = requests.post(sub_url, cookies=dkl_cookies, data=data)
        if re.status_code != 200:
            messagebox.showerror(title=course, message=self.name + value + '提交失败')


class cx_dkl(dkl):
    def query(self):
        return dkl.query_(self, 'cx')

    def submit(self, course):
        if course in query_dic:
            dkl.submit_(self,course, query_dic[course])

class zhs_dkl(dkl):
    def query(self):
        return dkl.query_(self, 'zhs')

    def submit(self, course):
        if course in query_dic:
            dkl.submit_(self,course, query_dic[course])

class yxy_dkl(dkl):
    def query(self):
        return dkl.query_(self, 'yxy')

    def submit(self, course):
        if course in query_dic:
            dkl.submit_(self,course, query_dic[course])

class xty3_dkl(dkl):
    def query(self):
        return dkl.query_(self, 'xty3')

    def submit(self, course):
        if course in query_dic:
            dkl.submit_(self,course, query_dic[course])


class Uxiaoyuan(object):
    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    @staticmethod
    def login():
        def get_modulus_cookies():
            url = 'http://www.weidaike.cn/AgentSys/login/keyPair'
            re = requests.get(url)
            U_cookies = re.cookies
            return eval(re.text)['modulus'], U_cookies

        modulus, U_cookies = get_modulus_cookies()


        with open('file/Ujs.js', 'r') as f:
            js_text = f.read()
        js = execjs.compile(js_text)
        key = js.call('get_key', modulus)

        url = 'http://www.weidaike.cn/AgentSys/login/view'
        data = {
            'modulus': modulus,
            'exponent': '010001',
            'accountCode': '17860773151',
            'accountPwd': key,

        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }

        re = requests.post(url, data=data, headers=headers, cookies=U_cookies)
        if re.status_code == 200:
            print('登陆成功')

            # 保存cookies
            cookies = shelve.open('file/cookies')
            cookies['U_cookies'] = U_cookies
            cookies.close()
            return '登陆成功'
        else:
            print(re.text)


    def query(self):
        url = 'http://www.weidaike.cn/AgentSys/Uschool/getMessageLevel?school=1&userName=' + self.name + '&passWord=' + self.password
        # 读取cookies
        cookies = shelve.open('file/cookies')
        U_cookies = cookies['U_cookies']
        cookies.close()
        query_ls = [self.name,self.password]
        re = requests.get(url, headers=headers, cookies=U_cookies)
        soup = BeautifulSoup(re.text, 'lxml')
        for tk in soup.find_all('option'):
            query_ls.append(tk['value'])
        print(query_ls)
        return query_ls


    def submit(self,sub_course):
        url = 'http://www.weidaike.cn/AgentSys/Uschool/submitNpelsOrder'

        # 读取cookies
        cookies = shelve.open('file/cookies')
        U_cookies = cookies['U_cookies']
        cookies.close()
        data = {
            'school': '1',
            'userName': self.name,
            'passWord': self.password,
            'qq': '',
            'YXYMessage.beginLevel': sub_course,
            'isDoUnit': 0,
            'YXYMessage.presentUnit': 1,
            'YXYMessage.goalUnit': 10,
            'YXYMessage.doType': '普通代刷',
            'YXYMessage.spaceTimeDto': 0,
            'YXYMessage.unitTimeDto': 1,
            'YXYMessage.minScore': 90,
            'YXYMessage.maxScore': 99,
            'YXYMessage.sex': '男'

        }
        re = requests.post(url, data=data, cookies=U_cookies)
        if re.status_code != 200:
            print(sub_course, '提交失败')
        else:
            print(sub_course,'提交成功')

platform_var = tk.StringVar()
Uxioayuan_b = tk.Radiobutton(window, text='U校园', variable=platform_var, value='Uxiaoyuan')
Uxioayuan_b.place(x=10, y=30)
dkl_b = tk.Radiobutton(window, text='超星', variable=platform_var, value='cx')
dkl_b.place(x=10, y=60)
dkl_b = tk.Radiobutton(window, text='智慧树', variable=platform_var, value='zhs')
dkl_b.place(x=10, y=90)
dkl_b = tk.Radiobutton(window, text='优学院', variable=platform_var, value='yxy')
dkl_b.place(x=10, y=120)
dkl_b = tk.Radiobutton(window, text='学堂云3', variable=platform_var, value='xty3')
dkl_b.place(x=10, y=150)
text = tk.Text(window, width=30, height=15, font=('Arial', 12))
text.place(x=100, y=30)




def get_ls(str):
    def f(ls):
        return ls.split()

    ls = list(map(f, str.split('\n')))[:-1]  # 去除最后一个空列表
    return ls


def f_query():
    global sub_courses
    global class_ls
    global c_ls
    if c_ls != None :
        for c in c_ls:
            c.destroy()
    sub_courses = []
    class_ls = []
    platform_dic = {
        'Uxiaoyuan': Uxiaoyuan,
        'cx': cx_dkl,
        'zhs': zhs_dkl,
        'yxy': yxy_dkl,
        'xty3': xty3_dkl
    }
    ls = get_ls(text.get('1.0','end'))
    class_ls = []
    query_course = []
    x_l = 400
    x = 400
    for customer in ls:
        a = platform_dic[platform_var.get()](customer[0],customer[1])
        class_ls.append(a)
        L = tk.Label(text=customer[0])
        L.place(x=x_l,y=20)
        x_l += 200
    for class_ in class_ls:
        y = 50
        sub_course = []
        try:
            query_ls, query_dic = class_.query()
        except:
            query_ls = class_.query()
        print(query_ls)
        query_course.append(query_ls)
        for i in query_ls[2:]:
            var = tk.StringVar()
            c = tk.Checkbutton(text=i, variable=var, onvalue=i, offvalue='')
            sub_course.append(var)
            c_ls.append(c)
            c.place(x=x, y=y)
            y +=20
        x +=200
        sub_courses.append(sub_course)


def f_login():
    global platform_var
    platform_dic = {
        'Uxiaoyuan': Uxiaoyuan,
        'cx':dkl,
        'zhs': dkl,
        'yxy': dkl,
        'xty3': dkl
    }
    platform = platform_dic[platform_var.get()]
    platform.login()


def f_submit():
    global sub_courses
    global class_ls
    for i in range(len(sub_courses)):
        for course in sub_courses[i]:
            if course.get():
                class_ls[i].submit(course.get())


query_b = tk.Button(window, command=f_query, text='查询')
query_b.place(x=60, y=330)

b_lgoin = tk.Button(window, command=f_login, text='登陆')
b_lgoin.place(x=400, y=330)

b_submit = tk.Button(window, command=f_submit, text='提交')
b_submit.place(x=700, y=330)

window.mainloop()
