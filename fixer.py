#!/usr/bin/env python

import pprint
import time
import sys
import json
from slackclient import SlackClient

def fix_str(s):
    return s.replace('/projects/', '/gitlab_ci/projects/').replace('/gitlab/gitlab/', '/gitlab/')

def fix_msg(m):
    if 'username' not in m or m['username'] not in ('GitLab CI', 'Gitlab Notifications'):
        return None

    if 'attachments' not in m:
        return None

    did_fix = False

    if len(m['text']) > 0:
        fixed = fix_str(m['text'])
        if fixed != m['text']:
            did_fix = True
            m['text'] = 'FIXED URLS: ' + fixed

    for a in m['attachments']:
        del a['id']

        fixed = fix_str(a['fallback'])
        if fixed != a['fallback']:
            did_fix = True
            a['fallback'] = 'FIXED URLS: ' + fixed

        fixed = fix_str(a['text'])
        if fixed != a['text']:
            did_fix = True
            a['text'] = 'FIXED URLS: ' + fixed


        if 'fields' in a:
            for f in a['fields']:
                fixed = fix_str(f['value'])
                if fixed != f['value']:
                    did_fix = True
                    f['value'] = 'FIXED URLS: ' + fixed

    if not did_fix:
        return None

    m['attachments'] = json.dumps(m['attachments'])
    m['username'] += ' Fixer'
    return m

def loop(sc):
        while True:
            messages = sc.rtm_read()

            for m in messages:
                print ""
                print "================== BEFORE ==================="
                pprint.pprint(messages)

                m = fix_msg(m)

                if m is None:
                    print "NOPE"
                    continue

                print ""
                print "------------------ AFTER -------------------"
                pprint.pprint(m)
                print sc.api_call('chat.postMessage', **m)

            time.sleep(1)

def main(token):
    sc = SlackClient(token)
    if sc.rtm_connect():
        loop(sc)
    else:
        print "Connection Failed, invalid token?"

if __name__ == '__main__':
    main(sys.argv[1])
