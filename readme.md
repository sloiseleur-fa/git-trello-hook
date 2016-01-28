# git-trello-hook
A github/gitlab webhook script written by python inspired by ruby gem [git-trello](https://github.com/zmilojko/git-trello).

#Instructions

    $pip -r requirements.txt

    # Update these placeholders in git-trello-hook.py
    TRELLO_CONFIG = {
        'api_key': 'TRELLO_API_KEY',
        'oauth_token': 'TRELLO_OAUTH_TOKEN_FOR_BOARD',
        'board_id': 'BOARD_ID'
    }

    WEBHOOK_CONFIG = {
        'host': '0.0.0.0',
        'port': 7343
    }

    # Open your github/gitlab repo settings, add an webhook URL according to your configs.
    e.g. For heroku deployment, add url https://git-trello-test.herokuapp.com/webhook
    e.g. For self hosting, add url https://your-ip-address:port/webhook

    $git commit -a -m "Fix [#1]"
    $git push

    # git-trello will add a comment to the card with the commit author, message and url

###`API_KEY`
https://trello.com/1/appKey/generate

###`OAUTH_TOKEN`
This is not so well explained in Trello, but I understood that you need to authorize the app with API_KEY to access each board separatelly. To do that:

https://trello.com/1/authorize?response_type=token&name=[BOARD+NAME+AS+SHOWN+IN+URL]&scope=read,write&expiration=never&key=[YOUR+API_KEY+HERE]

where [YOUR+API_KEY+HERE] is the one you entered in the previous step, while [BOARD+NAME+AS...] is, well, what it says. If your board url is 

https://trello.com/b/XLvlTFVA/git-trello

then you should type in "git-trello".


###`TRELLO_BOARD_ID`
It is the end of the URL when viewing the board. For example, for https://trello.com/b/XLvlTFVA/git-trello, board_id is XLvlTFVA.


#Credits

[git-trello](https://github.com/zmilojko/git-trello)
[git-trello-hook](https://github.com/hewigovens/git-trello-hook)
