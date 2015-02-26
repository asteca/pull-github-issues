#!/usr/bin/env python

import urllib
import re
import shlex
import datetime


def get_arxiv_data():
	'''
	Downloads issues data from Github.
	'''
	# ff = urllib.urlopen("https://github.com/asteca/asteca/issues?q=is%3Aissue+is%3Aclosed+sort%3Aupdated-desc")
	# lines = [str(line) for line in ff]
	# f = open('temp.txt', 'w')
	# f.write("".join(lines))
	# ff.close()

	f = open('temp.txt', 'r')
	lines = [str(line) for line in f]

	return lines


def get_issues(lines):
    '''
    Splits into numbers, titles, links and dates of last update
    for each issue.
    '''
    issues = [[], [], [], []]
    for index, line in enumerate(lines):
        # Get issue number.
        if line[:35] == '''    <a href="/asteca/asteca/issues/''':
        	if lines[index + 1] != '''      <span class="octicon octicon-comment"></span>\n''':
	        	a = re.split('''" class=''', line)
	        	b = re.split('''/asteca/asteca/issues/''', a[0])
	        	if b[1] != 'new':
	        		# iss_num = int(b[1])
	        		issues[0].append(b[1])
	    # Get issue title.
        if line[-45:] == '''class="issue-title-link js-navigation-open">\n''':
			# print lines[index + 1]
			issues[1].append(lines[index + 1][:-1].lstrip())
			# Get issue link.
			issues[2].append('https://github.com/asteca/asteca/issues/' + b[1])
		# Get time of last update.
        if line[-8:] == '''</time>\n''':
			a = re.split('''is="relative-time">''', line)
			b = re.split('''</time>''', a[1])
			date = datetime.datetime.strptime(b[0], "%b %d, %Y")
			# issues[3].append(date.strftime("%d/%m/%y"))
			issues[3].append(date.strftime("%d/%m"))

    return issues


lines = get_arxiv_data()
issues = get_issues(lines)

for iss in zip(*issues):
	print "<li>" + iss[3] + ''' - <a href="''' + iss[2] + '''">''' + iss[1] + "</a></li>"

# NEEDS FINISHING.
f1 = open('name.txt', 'r')
f2 = open('result.txt', 'w')
for line in f1:
    f2.write(line.replace('(StartNum)(.*)(/StartNum)',str(n)))
    if "StartNum" in line:
        re.sub('\nThis.*?ok','',a, flags=re.DOTALL)