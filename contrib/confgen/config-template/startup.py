import os
from abusehelper.core.config import relative_path
from abusehelper.core.startup import Bot

xmpp_jid = "@XMPP_JID@"
xmpp_password = "@XMPP_PASSWORD@"
service_room = "@SERVICE_ROOM@"

def basic(name, *args, **attrs):
    template = Bot.template(
        xmpp_jid=xmpp_jid,
        xmpp_password=xmpp_password,
        service_room=service_room,

        ## Uncomment the following lines, and the bots will keep
        ## persistent state and log to files, respectively.
        # bot_state_file=relative_path("state", name + ".state"),
        # log_file=relative_path("log", name + ".log")
    )
    return template(name, *args, **attrs)

def configs():
    # Launch a fine selection of abusehelper.core.* bots
    yield basic("mailer",
                smtp_host="@SMTP_HOST@",
                smtp_port="@SMTP_PORT@",
                smtp_auth_user="@SMTP_AUTH_USER@",
                smtp_auth_password="@SMTP_AUTH_PASSWORD@",
                mail_sender="@MAIL_SENDER@")
    yield basic("dshield")
    yield basic("roomgraph")
    yield basic("archivebot", archive_dir=relative_path("archive"))
    yield basic("runtime", config=relative_path("runtime.py"))

    # Find and launch modules named custom/*.sanitizer.py
    for filename in os.listdir(relative_path("custom")):
        if filename.endswith(".sanitizer.py"):
            yield basic(filename[:-3], relative_path("custom", filename))
