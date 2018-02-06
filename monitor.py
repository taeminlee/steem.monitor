#%% run with jupyter
from steem.account import Account
from slacker import Slacker
import time
#%% user list
users = [{
    "id":"tmkor"
}, {
    "id":"noctisk"
}, {
    "id":"pys"
}]

token = '[SLACK BOT TOKEN]'
slack = Slacker(token)
#%% find_last_index
def find_last_index(U):
    for u in U:
        a = Account(u['id'])
        for comment in a.history_reverse(filter_by="comment"):
            u['last_index'] = comment['index']
            break
#%% get new comments
def get_new_comments(U):
    for u in U:
        print("GET NEW COMMENT : %s" % u['id'])
        a = Account(u['id'])
        for comment in a.history(start=u['last_index']+1, filter_by="comment"):
            print("NEW COMMENT FROM %s -> %s" % (comment['author'], u['id']))
            u['last_index'] = comment['index']
            if comment['author'] != u['id']:
                author = comment['author']
                text = comment['body']
                url = "https://steemit.com/@%s/%s" % (comment['parent_author'], comment['parent_permlink'])
                attachments_dict = dict()
                attachments_dict['title'] = "%s -> %s" % (comment['author'], u['id'])
                attachments_dict['title_link'] = url
                attachments_dict['text'] = text
                attachments_dict['mrkdwn_in'] = ["text"]
                attachments = [attachments_dict]
                slack.chat.post_message(channel="#%s" % u['id'], text=None, attachments=attachments)
def run():       
    find_last_index(users)
    while True:         
        try:
            get_new_comments(users)
            print("COOLDOWN")
            time.sleep(60)
        except Exception as e:
            print("failed with error code: {}".format(e))
run()