#!/usr/bin/env python

import pprint
import time
import sys
import json
from slackclient import SlackClient

def fix_str(s):
    return s.replace('/projects/', '/gitlab_ci/projects/')

def fix_msg(m):
    if 'username' not in m or m['username'] != 'GitLab CI':
        return None

    if 'attachments' not in m:
        return None

    if len(m['text']) > 0:
        m['text'] = 'FIXED URLS: ' + fix_str(m['text'])
    else:
        m['text'] = 'asdf'

    for a in m['attachments']:
        del a['id']
        a['fallback'] = 'FIXED URLS: ' + fix_str(a['fallback'])
        a['text'] = 'FIXED URLS: ' + fix_str(a['text'])

        if 'fields' in a:
            for f in a['fields']:
                f['value'] = fix_str(f['value'])

    m['attachments'] = json.dumps(m['attachments'])
    m['username'] = 'GitLab CI Fixer'
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
