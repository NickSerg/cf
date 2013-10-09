#! /usr/bin/env python

import re
import sys
import json
import time
import urllib
import urllib2
import os.path
import ConfigParser

def login(handle, password):
    data = {}
    data['action'] = 'enter'
    data['handle'] = handle
    data['password'] = password
    encoded_data = urllib.urlencode(data)
    urllib2.urlopen('http://codeforces.ru/enter', encoded_data)

def submit(contest, problem, language, solution):
    data = {}
    data['action'] = 'submitSolutionFormSubmitted'
    data['submittedProblemIndex'] = problem
    data['programTypeId'] = language
    with open(solution) as f:
        data['source'] = f.read()
    encoded_data = urllib.urlencode(data)
    url = 'http://codeforces.ru/contest/{0}/submit'.format(contest)
    response = urllib2.urlopen(url, encoded_data)
    html = response.read()
    match = re.search('data-submission-id="([0-9]*)"', html)
    return match.groups(1)

def check(submission):
    data = {}
    data['submissionId'] = submission
    encoded_data = urllib.urlencode(data)
    response = urllib2.urlopen('http://codeforces.ru/data/submissionVerdict',
        encoded_data)
    submission_results = json.load(response)
    return submission_results

def write(match, problem, case, extension):
    with open('{0}.{1}.{2}'.format(problem, case, extension), 'w') as f:
        str1 = match.group(1)
        str2 = str1.replace('<br />', '\n')
        f.write(str2)

def download(contest, problem):
    url = 'http://codeforces.ru/contest/{0}/problem/{1}'.format(contest,
        problem)
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




if len(sys.argv) > 2:
    print "Usage: cf.py or cf.py solution"
elif len(sys.argv) == 2
    config_parser = ConfigParser.ConfigParser()
    config_parser.read('.cfrc')

    handler1 = urllib2.HTTPRedirectHandler()
    handler2 = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(handler1, handler2)
    urllib2.install_opener(opener)

    handle = config_parser.get('cf', 'handle')
    password = config_parser.get('cf', 'password')
    login(handle, password)

    solution = sys.argv[1]
    contest = config_parser.get('cf', 'contest')
    problem, extension = os.path.splitext(solution)
    language = config_parser.get('cf', extension)
    submission = submit(contest, problem, language, solution)

    while True:
        submission_results = check(submission)
        print submission_results
        if submission_results['waiting'] == 'false':
            break
        time.sleep(1)
elif len(sys.argv) == 1:
    config_parser = ConfigParser.ConfigParser()
    config_parser.read('.cfrc')
    contest = config_parser.get('cf', 'contest')
    for problem in ['a', 'b', 'c', 'd', 'e']:
        download(contest, problem)
   
