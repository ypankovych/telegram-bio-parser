import time
import utils
from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait
from collections import namedtuple

USER = namedtuple('User', ['username', 'name', 'about'])
app = Client("account")
target = input('username чата без "@": ')  # Target channel/supergroup
users = []  # List that will contain all the users of the target chat
limit = 200  # Amount of users to retrieve for each API call
offset = 0  # Offset starts at 0

app.start()

while True:
    try:
        participants = app.send(
            functions.channels.GetParticipants(
                channel=app.resolve_peer(target),
                filter=types.ChannelParticipantsSearch(""),  # Filter by empty string (search for all)
                offset=offset,
                limit=limit,
                hash=0
            )
        )
    except FloodWait as e:
        # Very large channels will trigger FloodWait.
        # When happens, wait X seconds before continuing
        time.sleep(e.x)
        continue

    if not participants.participants:
        break  # No more participants left

    for i in participants.users:
        full_user = app.send(
            functions.users.GetFullUser(
                app.resolve_peer(i.id)
            )
        )
        username = full_user.user.username
        identifier = f'@{username}' if username else full_user.user.id
        users.append(USER(identifier, full_user.user.first_name, full_user.about))
        time.sleep(1)
    offset += limit

utils.dump_data(users)
app.stop()
