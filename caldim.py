try:
    from requests.exceptions import RequestException
    import requests, re, json, time, os, sys
    from rich.console import Console
    from rich.panel import Panel
    from rich import print as printf
    from requests.exceptions import SSLError
except (ModuleNotFoundError) as e:
    __import__('sys').exit(f"[Error] {str(e).capitalize()}!")

SUKSES, GAGAL, FOLLOWERS, STATUS, BAD, CHECKPOINT, FAILED, TRY = [], [], {
    "COUNT": 0
}, [], [], [], [], []

class KIRIMKAN:

    def __init__(self) -> None:
        pass

    def PENGIKUT(self, session, username, password, host, your_username):
        global SUKSES, GAGAL, STATUS, FAILED, BAD, CHECKPOINT
        session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Mode': 'navigate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Host': '{}'.format(host),
            'Sec-Fetch-Dest': 'document',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Connection': 'keep-alive'
        })
        response = session.get('https://{}/login'.format(host))
        self.ANTI_FORGERY_TOKEN = re.search(r'"&antiForgeryToken=(.*?)";', str(response.text))
        if self.ANTI_FORGERY_TOKEN != None:
            self.TOKEN = self.ANTI_FORGERY_TOKEN.group(1)
            session.headers.update({
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://{}/login'.format(host),
                'Sec-Fetch-Mode': 'cors',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Sec-Fetch-Dest': 'empty',
                'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()]),
                'Origin': 'https://{}'.format(host)
            })
            data = {
                'username': f'{username}',
                'antiForgeryToken': f'{self.TOKEN}',
                'userid': '',
                'password': f'{password}'
            }
            response2 = session.post('https://{}/login?'.format(host), data=data)
            self.JSON_RESPONSE = json.loads(response2.text)
            if '\'status\': \'success\'' in str(self.JSON_RESPONSE):
                session.headers.update({
                    'Referer': 'https://{}/tools/send-follower'.format(host),
                    'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                })
                data = {
                    'username': f'{your_username}',
                }
                response3 = session.post('https://{}/tools/send-follower?formType=findUserID'.format(host), data=data)
                if 'name="userID"' in str(response3.text):
                    self.USER_ID = re.search(r'name="userID" value="(\d+)">', str(response3.text)).group(1)
                    session.headers.update({
                        'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                    })
                    data = {
                        'userName': f'{your_username}',
                        'adet': '500',
                        'userID': f'{self.USER_ID}',
                    }
                    response4 = session.post('https://{}/tools/send-follower/{}?formType=send'.format(host, self.USER_ID), data=data)
                    self.JSON_RESPONSE4 = json.loads(response4.text)
                    if '\'status\': \'success\'' in str(self.JSON_RESPONSE4):
                        SUKSES.append(f'{self.JSON_RESPONSE4}')
                        STATUS.append(f'{self.JSON_RESPONSE4}')
                    elif '\'code\': \'nocreditleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] YOUR CREDITS HAVE RAN OUT!          ", end='\r')
                        time.sleep(4.5)
                    elif '\'code\': \'nouserleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] NO USERS FOUND!                     ", end='\r')
                        time.sleep(4.5)
                    elif 'istek engellendi.' in str(self.JSON_RESPONSE4):
                        TRY.append(f'{self.JSON_RESPONSE4}')
                        if len(TRY) >= 3:
                            TRY.clear()
                            printf(f"[bold bright_black]   ──>[bold red] REQUEST TO SEND FOLLOWERS BLOCKED!  ", end='\r')
                            time.sleep(4.5)
                            return (False)
                        else:
                            self.PENGIKUT(session, username, password, host, your_username)
                    else:
                        GAGAL.append(f'{self.JSON_RESPONSE4}')
                        printf(f"[bold bright_black]   ──>[bold red] ERROR WHILE SENDING FOLLOWERS!      ", end='\r')
                        time.sleep(4.5)
                    printf(f"[bold bright_black]   ──>[bold green] FINISH FROM {str(host).split('.')[0].upper()} SERVICE!           ", end='\r')
                    time.sleep(5.0)
                    return (True)
                else:
                    printf(f"[bold bright_black]   ──>[bold red] TARGET USERNAME NOT FOUND!           ", end='\r')
                    time.sleep(4.5)
                    return (False)
            elif 'Güvenliksiz giriş tespit edildi.' in str(self.JSON_RESPONSE):
                CHECKPOINT.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] YOUR ACCOUNT IS CHECKPOINT!          ", end='\r')
                time.sleep(4.5)
                return (False)
            elif 'Üzgünüz, şifren yanlıştı.' in str(self.JSON_RESPONSE):
                BAD.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] YOUR PASSWORD IS WRONG!              ", end='\r')
                time.sleep(4.5)
                return (False)
            else:
                FAILED.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] LOGIN ERROR!                          ", end='\r')
                time.sleep(4.5)
                return (False)
        else:
            printf(f"[bold bright_black]   ──>[bold red] FORGERY TOKEN NOT FOUND!          ", end='\r')
            time.sleep(2.5)
            return (False)

class INFORMASI:

    def __init__(self) -> None:
        pass

    def PENGIKUT(self, your_username, updated):
        global FOLLOWERS
        with requests.Session() as session:
            session.headers.update({
                'User-Agent': 'Instagram 317.0.0.0.3 Android (27/8.1.0; 360dpi; 720x1280; LAVA; Z60s; Z60s; mt6739; en_IN; 559698990)',
                'Host': 'i.instagram.com',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            })
            response = session.get('https://i.instagram.com/api/v1/users/web_profile_info/?username={}'.format(your_username))
            if '"status":"ok"' in str(response.text):
                self.EDGE_FOLLOWED_BY = json.loads(response.text)['data']['user']['edge_followed_by']['count']
                if bool(updated) == True:
                    FOLLOWERS.update({
                        "COUNT": int(self.EDGE_FOLLOWED_BY)
                    })
                    return (True)
                else:
                    self.JUMLAH_MASUK = (int(self.EDGE_FOLLOWED_BY) - int(FOLLOWERS['COUNT']))
                    return (f'+{self.JUMLAH_MASUK} > {self.EDGE_FOLLOWED_BY}')
            else:
                if bool(updated) == True:
                    FOLLOWERS.update({
                        "COUNT": 0
                    })
                    return (False)
                else:
                    return ('-+500')

class MAIN:

    def __init__(self):
        global CHECKPOINT, BAD, FAILED
        try:
            self.LOGO()
            printf(Panel(f"[bold white]Please fill in your Instagram account details such as username and password, use `[bold red]:[bold white]` as a\nseparator, you must also use a fake account to log in!", width=59