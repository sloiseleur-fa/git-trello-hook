#!/usr/bin/env python

from gevent import monkey;monkey.patch_all()
from bottle import route, request,run, default_app
from trello import Cards, Lists
import re
import json

TRELLO_CONFIG = {
    'api_key': 'cff1385e29ea0ddff0a36d0faef6a1fe',
    'oauth_token': '1607a16ab4ed2f51751179bd5b249e59ccd361e38a662656ccef0c5b3870f5fa',
    'board_id': 'ZcIBTf5i',
    'list_id_in_progress': '56a9d3ac7a688d41c24cbd38',
    'list_id_done': '56a9d3b0c0f71152ab6c651e',
}

WEBHOOK_CONFIG = {
    'host': '0.0.0.0',
    'port': 7343
}

TRELLO_LIST = Lists(TRELLO_CONFIG['api_key'], TRELLO_CONFIG['oauth_token'])
TRELLO_CARDS = Cards(TRELLO_CONFIG['api_key'], TRELLO_CONFIG['oauth_token'])


@route("/")
def index():
    return 'git webhook for move trello cards'


@route("/webhook", method='POST')
def handle_payload():
    json_payload = None
    from_gitlab = False
    if request.get_header('Content-Type', None) == 'application/json':
        json_payload = request.json
        from_gitlab = True
    else:
        body = request.forms['payload']
        json_payload = json.loads(body)
    print(json_payload)
    commits = json_payload['commits']
    cards_in_commit = []
    cards_commit_dict = {}
    card_pattern = '(\[)(#)([0-9]+)(\])'

    print(commits)
    for commit in commits:
        results = re.findall(
            card_pattern, commit['message'], flags=re.IGNORECASE)
        for result in results:
            cards_in_commit.append(result[2])
            if result[2] in cards_commit_dict:
                cards_commit_dict[result[2]].append(commit)
            else:
                cards_commit_dict[result[2]] = [commit]

    print(cards_in_commit)
    print(cards_commit_dict)
    if cards_in_commit:
        from_cards = TRELLO_LIST.get_card(
            TRELLO_CONFIG['list_id_in_progress'])

        for card in from_cards:
            if str(card['idShort']) in cards_in_commit:
                i = 0
                while i < len(cards_commit_dict[str(card['idShort'])]):
                    commit = cards_commit_dict[str(card['idShort'])][i]
                    print(commit['author']['name'].encode('utf-8'))
                    desc_with_commit = 'Commit by {0}\n{2}\n{3}'.format(commit['author']['name'].encode('utf-8'), commit['message'].encode('utf-8'), commit['url'])
                    TRELLO_CARDS.new_action_comment(card['id'], desc_with_commit)
                    i = i+1

    return "done"

if __name__ == '__main__':
    run(host=WEBHOOK_CONFIG['host'],
               port=WEBHOOK_CONFIG['port'], server='gevent', debug=True)

app = default_app()
