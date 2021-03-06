#!/usr/bin/env python

import urllib, json
import re
import time
import subprocess
import os
import logging


def get_github_data(full_github_repo):
    '''
    Downloads closed issues from Github, ordered with latest modified
    issue first.
    '''
    lines = []
    response = urllib.urlopen(full_github_repo)
    data = json.loads(response.read())
    # Define number of issues to list.
    N = 7
    for d in data[:N]:
        lines.append([str(d["closed_at"].split("T")[0]), str(d["html_url"]),
                      str(d["title"])])

    # f = open('temp.txt', 'w')
    # f.write("".join(lines))
    # ff.close()

    # f = open('temp.txt', 'r')
    # lines = [str(line) for line in f]

    return lines


def html_format(issues):
    '''
    Format issues as HTML lines.
    '''
    # Define color of link.
    color = '4B7F69'
    html_issues = ''
    for iss in issues:
        html_issues = html_issues + '''<li><font color="''' + color + \
            '''"><b>''' + iss[0] + '''</b></font> - <a href="''' + iss[1] + \
            '''">''' + iss[2] + "</a></li>\n"

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
        # Re-write file with new, replaced with pattern, string var.
        f.write(text2)


def git_acp(mypath, repo_path):
    '''
    Add, commit and push changes to index.html file in the
    corresponding git dir.
    '''
    # Position in correct dir.
    os.chdir(repo_path)

    # Add file.
    filename = 'index.html'
    add_cmd = ["git", "add", filename]
    try:
        a = subprocess.check_output(add_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        a = cpe.output

    # Commit changes.
    c_mssg = "Auto commit, {}".format(time.strftime("%c"))
    commit_cmd = ["git", "commit", "-m", c_mssg]
    try:
        c = subprocess.check_output(commit_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        c = cpe.output

    # Push changes.
    push_cmd = ["git", "push"]
    try:
        p = subprocess.check_output(push_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        p = cpe.output

    # Log to file.
    logging.basicConfig(filename=mypath + '/commit.log', filemode='a',
                        level=logging.DEBUG)
    logging.info(" {}\n{} {} {}".format(time.strftime("%c"), a, c, p))


def main():
    '''
    Call functions sequentially.
    '''
    # Define path where this script is located
    mypath = os.path.dirname(os.path.realpath(__file__))
    # Define path of git repo to update in the system.
    repo_path = os.path.realpath(__file__)[:-42] + 'asteca.github.io/'

    # Full path to closed issues in Github repo, ordered according to the
    # latest updated.
    full_github_repo = 'https://api.github.com/repos/asteca/ASteCA/' +\
        'issues?per_page=1000&state=closed&sort=updated-desc'

    # Download data.
    issues = get_github_data(full_github_repo)

    # Format issues as HTML lines.
    html_issues = html_format(issues)
    print html_issues

    # Replace old issues with new ones in file.
    replace_old_issues(repo_path, html_issues)
    # Add, commit and push changes.
    git_acp(mypath, repo_path)


if __name__ == "__main__":
    main()
