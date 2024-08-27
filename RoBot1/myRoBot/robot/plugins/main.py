# coding=utf-8
import time
import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import json
import os

useCookie = False


def to_old_num(text):
    pattern = r'\d+'
    result = re.findall(pattern, text)
    return result


def to_old(courseid, knowledgeId, clazzid, enc, cpi):
    mooc1Domain = 'https://mooc1.chaoxing.com'
    referUrl = mooc1Domain + "/mycourse/studentstudy?chapterId=" + knowledgeId + "&courseId=" + courseid + "&clazzid=" + clazzid + "&cpi=" + cpi + "&enc=" + enc + "&mooc2=1"
    transferUrl = mooc1Domain + "/mycourse/transfer?moocId=" + courseid + "&clazzid=" + clazzid + "&ut=s&refer=" + quote(
        referUrl)
    return transferUrl


class ChaoXing:
    def __init__(self):
        self.session = None
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }
        self.check_cookie_file()

    def get_session(self):
        if not self.session:
            self.session = requests.session()
        return self.session

    def check_cookie_file(self):
        if os.path.exists('./cookies') and useCookie:
            with open('./cookies', 'r') as f:
                cookies = f.read().replace('"', '')
            self.headers['Cookie'] = cookies
        else:
            self.get_cookies()

    def get_cookies(self):
        self.get_session()
        phone = input("输入手机号：")
        password = input("输入密码：")
        login_path = 'https://passport2.chaoxing.com/fanyalogin'
        data = {
            'fid': -1,
            'uname': f'{phone}',
            'password': f'{password}',
            'refer': 'https%3A%2F%2Fi.chaoxing.com',
            't': 'false',
            'forbidotherlogin': 0,
            'validate': '',
            'doubleFactorLogin': 0,
            'independentId': 0,
        }
        post_header = self.session.post(login_path, data=data)
        text = post_header.headers['Set-Cookie']
        res = self.session.get('https://i.chaoxing.com/base')
        if res.cookies:
            with open('./cookies', 'w') as f:
                json.dump(self.format_cookie(text), f)
            self.headers['Cookie'] = self.format_cookie(text)
        else:
            print('获取失败')

    def format_cookie(self, text):
        keys = ['lv', 'fid', '_uid', 'uf', '_d', 'UID', 'vc', 'vc2', 'vc3', 'cx_p_token', 'xxtenc', 'DSSTASH_LOG']
        pattern = re.compile(r'(?P<key>{})=(?P<value>[^;,\s]+)'.format('|'.join(keys)))
        matches = pattern.finditer(text)
        result = {}
        res = ''
        for match in matches:
            result[match.group('key')] = match.group('value')
        for name, value in zip(result.keys(), result.values()):
            res += name + '=' + value + ';'
        return res

    def get_course_object(self):
        course_list_li = BeautifulSoup(self.get_session().get(
            f'https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list?v={str(int(round(time.time() * 1000)))}&rss=1&start=0&size=500&catalogId=0&superstarClass=0&searchname=',
            headers=self.headers).content, 'lxml').select_one('#courseList').select('li > .course-info')
        course_object = {}
        for i in course_list_li:
            name = i.select_one('.course-name')['title']
            url = i.select_one('a')['href']
            if not url.find('http'):
                course_object[name] = url
        return course_object

    def student_course(self, url, oldenc, cpi):
        soup = BeautifulSoup(self.session.get(url).content, 'lxml')
        unit_list = soup.select_one('.chapter_td').select('.chapter_unit')
        unit_url = {}
        for i in unit_list:
            unit_data = {}
            unit_title = i.select_one('.catalog_name > span')['title']
            unit_item_data = i.select('.catalog_level .chapter_item')
            unit_item_name = i.select('.catalog_level .catalog_sbar')
            for name, data in zip(unit_item_name, unit_item_data):
                if data.get('onclick'):
                    unit_data[name.text.strip()] = to_old(*to_old_num(data['onclick']), oldenc, cpi)
            unit_url[unit_title] = unit_data
        return unit_url

    def toltal_video_url(self) -> dict:
        course = self.get_course_object()
        session = self.get_session()
        course_list = {}
        hasPowerClassSize = 0
        for name, url in zip(course.keys(), course.values()):
            soup = None
            # 先去掉所有报错其余的以后再说
            try:
                soup = BeautifulSoup(session.get(url, headers=chaoxing.headers).content, 'lxml')
                oldenc = soup.select_one('#oldenc')['value']
                courseid = soup.select_one('#courseid')['value']
                clazzid = soup.select_one('#clazzid')['value']
                cpi = soup.select_one('#cpi')['value']
                t = soup.select_one('#t')['value']
                heardUt = soup.select_one('#heardUt')['value']
                se_url = f'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?courseid={courseid}&clazzid={clazzid}&cpi={cpi}&ut={heardUt}&t={t}'
                unit_url = chaoxing.student_course(se_url, oldenc, cpi)
            except:
                continue

            hasPowerClassSize += 1
            course_list[name] = unit_url
        print('---------', hasPowerClassSize)
        return course_list

    # 得到课程的所有的模块
    def get_work_model(self):
        course = self.get_course_object()
        session = self.get_session()
        course_work = {}
        for name, url in zip(course.keys(), course.values()):
            # 先去掉所有报错其余的以后再说
            try:
                soup = BeautifulSoup(session.get(url, headers=chaoxing.headers).content, 'lxml')
                workEnc = soup.select_one('#workEnc')['value']
                oldenc = soup.select_one('#oldenc')['value']
                courseid = soup.select_one('#courseid')['value']
                clazzid = soup.select_one('#clazzid')['value']
                cpi = soup.select_one('#cpi')['value']
                t = soup.select_one('#t')['value']
                heardUt = soup.select_one('#heardUt')['value']

                work_url = f'https://mooc1.chaoxing.com/mooc2/work/list?courseId={courseid}&classId={clazzid}&cpi={cpi}&ut={heardUt}&enc={workEnc}'

                # 访问课程的work作业
                work_content = BeautifulSoup(session.get(work_url, headers=chaoxing.headers).content, 'lxml')
                work_content = work_content.select('.bottomList>ul>li')
                mes_list = []
                for i in work_content:
                    # 先看有无时间，没时间是已经过期的，只看有时间的
                    name_status_time = {}
                    if i.select_one('.notOver'):
                        name_status_time['name'] = i.select_one('.overHidden2').string
                        name_status_time['status'] = i.select_one('.status').string
                        name_status_time['time'] = i.select_one('.notOver').text.replace('\r', '').replace('\n',
                                                                                                           '').strip()
                        mes_list.append(name_status_time)

                course_work[name] = mes_list

            except:
                continue
        return course_work

    def get_todo_work(self):
        course_work = self.get_work_model()
        todo_work = {}
        for classname, aclass, in zip(course_work.keys(), course_work.values()):
            if len(aclass) == 0:
                continue
            list = []
            for awork in aclass:
                if awork['status'] == '未交':
                    list.append(awork)
            if len(list) == 0:
                continue
            todo_work[classname] = list
        return todo_work

    def get_task_model(self):
        course = self.get_course_object()
        session = self.get_session()
        course_task = {}
        for name, url in zip(course.keys(), course.values()):
            # 先去掉所有报错其余的以后再说
            try:
                soup = BeautifulSoup(session.get(url, headers=chaoxing.headers).content, 'lxml')
                workEnc = soup.select_one('#workEnc')['value']
                oldenc = soup.select_one('#oldenc')['value']
                cfid = soup.select_one('#cfid')['value']
                courseid = soup.select_one('#courseid')['value']
                clazzid = soup.select_one('#clazzid')['value']
                cpi = soup.select_one('#cpi')['value']
                t = soup.select_one('#t')['value']
                heardUt = soup.select_one('#heardUt')['value']

                task_url = f'https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist?fid={cfid}&courseId={courseid}&classId={clazzid}'

                # 访问课程的task任务
                task_json = session.get(task_url, headers=chaoxing.headers).json()
                activeList = task_json['data']['activeList']
                task_list = []
                for i in activeList:
                    # 1为正在进行的
                    if i['status'] != 1:
                        break
                    name_time = {}
                    name_time['name'] = i['nameOne']
                    name_time['time'] = i['nameFour']
                    task_list.append(name_time)
                course_task[name] = task_list
            except:
                continue
        return course_task

    def get_now_task(self):
        course_task = self.get_task_model()
        now_task = {}
        for classname, aclass, in zip(course_task.keys(), course_task.values()):
            if len(aclass) == 0:
                continue
            list = []
            for awork in aclass:
                list.append(awork)
            if len(list) == 0:
                continue
            now_task[classname] = list
        return now_task


if __name__ == '__main__':
    chaoxing = ChaoXing()
    urls = chaoxing.toltal_video_url()
    session = chaoxing.get_session()
    todo_work = chaoxing.get_todo_work()
    print(todo_work)
    now_task = chaoxing.get_now_task()
    print(now_task)

    # for course in urls.values():
    #     for unit in course.values():
    #         for unit_item in unit.values():
    #             soup = BeautifulSoup(session.get(unit_item, headers=chaoxing.headers).content, 'lxml')
    #             print(soup.prettify())
    #             break
    #         break
    #     break
