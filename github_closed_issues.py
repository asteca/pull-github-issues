#!/usr/bin/env python

import urllib
import re
import shlex
import datetime
import time
import os


def get_github_data(full_github_repo):
	'''
	Downloads closed issues from Github, ordered with latest modified
	issue first.
	'''
	ff = urllib.urlopen(full_github_repo)
	lines = [str(line) for line in ff]
	f = open('temp.txt', 'w')
	f.write("".join(lines))
	ff.close()

	# f = open('temp.txt', 'r')
	# lines = [str(line) for line in f]

	return lines


def get_issues(lines):
    '''
    Splits file into numbers, titles, links and dates of last update
    for each issue.
    '''
    issues = [[], [], [], []]
    for index, line in enumerate(lines):
        # Get issue number.
        if line[:35] == '''    <a href="/asteca/asteca/issues/''':
        	if lines[index + 1] != \
        	'''      <span class="octicon octicon-comment"></span>\n''':
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


def html_format(issues, color):
	'''
	Format issues as HTML lines.
	'''
	# Define number of issues to list.
	N = 7
	html_issues = ''
	for iss in zip(*issues)[:N]:
		html_issues = html_issues + "<li>" + iss[3] + ''' - <a href="''' + \
		iss[2] + '''"><font color="''' + color + '''">''' + iss[1] + \
		"</font></a></li>\n"

	return html_issues


def replace_old_issues(path, html_issues):
	'''
	Replace list of old issues with new ones.
	'''
	# Define full path to index.html file.
	index_file = path + 'index.html'

	# Read index.html file.
	with open(index_file, 'r') as f:
		# Read file as string.
		text = f.read()
		# Define pattern to search.
		pattern = '<!-- Issues_0 -->\n.*\n<!-- Issues_1 -->'
		# Define replacement pattern.
		replacement = '<!-- Issues_0 -->\n' + html_issues + '<!-- Issues_1 -->'
		# Replace pattern and store in new string var.
		text2 = re.sub(pattern, replacement, text, flags=re.DOTALL)

	# Write index.html file.
	with open(index_file, 'w') as f:
		# Re-write file with new, replaced with patter, string var.
		f.write(text2)


def git_acp(path):
	'''
	Add, commit and push changes to index.html file in the
	corresponding git dir.
	'''
	# Position in correct dir.
	os.chdir(path)

	# Add file.
	filename = 'index.html'
	add_cmd = """git add "%s" """
	os.system(add_cmd % filename)

    # Commit changes.
	commit_cmd = """git commit -m "%s" """
	message = 'Auto commit, %s' % time.strftime("%c")
	print message
	os.system(commit_cmd % message)

    # Push changes.
	push_cmd = """git push"""
	os.system(push_cmd)


def main():
	'''
	Call functions sequentially.
	'''

	# Define name of git repo where issues are stored.
	github_repo = "asteca/asteca"
	# Define path of git repo to update in the system.
	repo_path = '/media/rest/github/asteca-project/asteca.github.io/'

	# Full path to closed issues in Github repo, ordered according to the
	# latest updated.
	github0 = 'https://github.com/'
	github1 = '/issues?q=is%3Aissue+is%3Aclosed+sort%3Aupdated-desc'
	full_github_repo = github0 + github_repo + github1

	# Define color of link.
	color = '005555'

	# Download data.
	lines = get_github_data(full_github_repo)
	# Extract issues.
	issues = get_issues(lines)
	# Format issues as HTML lines.
	html_issues = html_format(issues, color)
	# Replace old issues with new ones in file.
	replace_old_issues(path, html_issues)
	# Add, commit and push changes.
	git_acp(repo_path)


if __name__ == "__main__":
    main()