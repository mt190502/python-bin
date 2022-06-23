#!/bin/python3
import feedparser, configparser, json, requests, time, schedule, os

config = configparser.ConfigParser()
config.read("config.ini")

interval = int(config["General"]["interval"])


class rssWebHook:
    def __init__(self):
        self.numberOfPostsToCheck = int(config["General"]["numberOfPostsToCheck"])
        self.rssBotWebhook = config["Webhooks"]["rssBotWebhook"]
        self.ytBotWebhook = config["Webhooks"]["ytBotWebhook"]
        self.ytBotTitle = config["Configuration"]["ytBotTitle"]
        self.termcls = int(os.get_terminal_size().columns / 2)



    def refreshlogs(self, feedtype, feedname, feedlink, mode):
        logfile = "".join([a for a in feedname if a.isalnum()])
        with open(f"logs/{feedtype}/{logfile}", mode) as f:
            for a in range(self.numberOfPostsToCheck):
                posttitle = feedparser.parse(feedlink)['entries'][a]['title']
                postlink = feedparser.parse(feedlink)['entries'][a]['link']
                f.writelines(f"{postlink}\n")
            f.close()



    def checkfeed(self, feedtype, feedname, feedlink):
        logfile = "".join([a for a in feedname if a.isalnum()])
        if not os.path.exists(f"logs/{feedtype}/{logfile}"):
            self.refreshlogs(feedtype, feedname, feedlink, "a")
            self.sendpost(feedname, feedparser.parse(feedlink)['entries'][0]['title'], feedparser.parse(feedlink)['entries'][0]['link'], self.dcWebhookUrl, feedtype)
        else:
            for a in range(self.numberOfPostsToCheck):
                posttitle = feedparser.parse(feedlink)['entries'][a]['title']
                postlink = feedparser.parse(feedlink)['entries'][a]['link']

                postLinkOnlyAlnum = "".join([b for b in postlink if b.isalnum()])

                with open(f"logs/{feedtype}/{logfile}", "r+") as f:
                    logFileOnlyAlnum = "".join([c for c in f.read() if c.isalnum()])
                    if logFileOnlyAlnum.find(postLinkOnlyAlnum) == -1:
                        self.sendpost(feedname, posttitle, postlink, self.dcWebhookUrl, feedtype)
                        self.refreshlogs(feedtype, feedname, feedlink, "w")
                    else:
                        print(f"{feedname.ljust(self.termcls)} : Bu feed adresi yeni bir içerik paylaşmadı.")



    def feedshandler(self, feedsfile):
        with open(feedsfile) as f:
            feeds = f.read().strip()
            for a in feeds.split("\n"):
                feedtype = a.split(" -- ")[0]
                feedname = a.split(" -- ")[1]
                feedlink = a.split(" -- ")[2]

                if feedtype == "RSS":
                    self.dcWebhookUrl = self.rssBotWebhook
                elif feedtype == "YT":
                    self.dcWebhookUrl = self.ytBotWebhook
                else:
                    print(f"{feedname.ljust(self.termcls)} : Devre dışı")

                if (feedtype == "RSS") or (feedtype == "YT"):
                    self.checkfeed(feedtype, feedname, feedlink)



    def sendpost(self, feedname, postname, postlink, dcWebhookUrl, feedtype):
        rsscontent = [postname, "\n", postlink]

        if feedtype == "RSS":
            data = {"username" : feedname, "content" : "{}{}{}".format(*rsscontent)}
        else:
            data = {"username" : "{} ({})".format(self.ytBotTitle, feedname), "content" : "{}{}{}".format(*rsscontent)}

        result = requests.post(dcWebhookUrl, json = data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Hata oluştu.")
        else:
            print(feedname.ljust(self.termcls), ":", "İçerik {} kodu ile yollandı.".format(result.status_code))

        time.sleep(1)



    def run(self, feedsfile):
        self.feedshandler(feedsfile)


if os.path.exists("rssfeeds.txt"):
    feedsfile = "rssfeeds.txt"
else:
    feedsfile = input("Feed linklerinin bulunduğu dosya yolu: ")
    if not feedsfile.isalnum():
        print("Geçerli bir dosya adı girin.")
        exit()
    if not os.path.exists(feedsfile):
        print("Dosya bulunamadı.")
        exit()


session = rssWebHook()
session.run(feedsfile)
schedule.every(interval).minutes.do(session.run, feedsfile)
while True:
    schedule.run_pending()
    time.sleep(1)



