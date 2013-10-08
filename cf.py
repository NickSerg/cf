#! /usr/bin/env python

import re
import sys
import json
import time
import urllib
import urllib2
import os.path
import ConfigParser

CONFIG = '.cfrc'
CONFIG_SECTION = 'config'

def login(url, handle, password):
    data = {}
    data['action'] = 'enter'
    data['handle'] = handle
    data['password'] = password
    encoded_data = urllib.urlencode(data)
    urllib2.urlopen(url, encoded_data)

def submit(url, problem, language, solution):
    data = {}
    data['action'] = 'submitSolutionFormSubmitted'
    data['submittedProblemIndex'] = problem
    data['programTypeId'] = language
    with open(solution) as f:
        data['source'] = f.read()
    encoded_data = urllib.urlencode(data)
    response = urllib2.urlopen(url, encoded_data)
    html = response.read()
    match = re.search('data-submission-id="([0-9]*)"', html)
    submission = match.groups(1)
    return submission

def check(url, submission):
    data = {}
    data['submissionId'] = submission
    encoded_data = urllib.urlencode(data)
    response = urllib2.urlopen(url, encoded_data)
    submission_results = json.load(response)
    return submission_results

def write(match, problem, case, extension):
    with open('{0}.{1}.{2}'.format(problem, case, extension), 'w') as f:
        str1 = match.group(1)
        str2 = str1.replace('<br />', '\n')
        f.write(str2)

def download(url, problem):
    response = urllib2.urlopen(url, problem)
    html = response.read()
    iter1 = re.finditer('<div class="input"><div class="title">.*?</div>'
'<pre>(.*?)</pre></div>', html)
    iter2 = re.finditer('<div class="output"><div class="title">.*?</div>'
'<pre>(.*?)</pre></div>', html)
    case = 0
    for pair in zip(iter1, iter2):
        case += 1
        write(pair[0], problem, case, 'in')
        write(pair[1], problem, case, 'ans')




config_parser = ConfigParser.ConfigParser()
config_parser.read(CONFIG)

if len(sys.argv) == 2:

    handler1 = urllib2.HTTPRedirectHandler()
    handler2 = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(handler1, handler2)

    urllib2.install_opener(opener)

    handle = config_parser.get(CONFIG_SECTION, 'handle')
    password = config_parser.get(CONFIG_SECTION, 'password')
    login_url = config_parser.get(CONFIG_SECTION, 'login_url')

    login(login_url, handle, password)

    solution = sys.argv[1]
    problem, extension = os.path.splitext(solution)
    language = config_parser.get(CONFIG_SECTION, extension)
    submit_url = config_parser.get(CONFIG_SECTION, 'submit_url')

    submission = submit(submit_url, problem, language, solution)

    check_url = config_parser.get(CONFIG_SECTION, 'check_url')
    while True:

        submission_results = check(check_url, submission)
        print submission_results

        if submission_results['waiting'] == 'false':
            break

        time.sleep(1)

elif len(sys.argv) == 1:

    download_url_base = config_parser.get(CONFIG_SECTION, 'download_url_base')

    for problem in ['a', 'b', 'c', 'd', 'e']:
        download_url = '{0}/{1}'.format(download_url_base, problem) 
        download(download_url, problem)

else:

    print "Usage: cf.py or cf.py solution"
