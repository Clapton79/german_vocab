__name__ = 'FortniteAPIAsync'
__author__ = 'xMistt'
__version__ = '0.1.7'

from .api import APIClient
from .exceptions import *
from .enums import *

import functools
import asyncio
import datetime
import base64


async def set_default_loadout(client: "fortnitepy.Client", config: dict, member: "fortnitepy.PartyMember") -> None:
    """
    Function which can be used with fortnitepy to set the default loadout.
    This is to be used with my project PartyBot, if you're using this library for a different project,
    ignore this function, it will not be useful for you.
    """

    party_update_meta = client.party  # Saves direct route to the party_update_meta object.

    # Sends unique iOS kairos token in order for request to be accepted via GraphQL.
    await party_update_meta.send(base64.b64decode('Tm90aWNlOiBKb2luIGRpc2NvcmQuZ2cvOGhl'
                                                  'QVJSQiBmb3IgYSBmcmVlIGxvYmJ5IGJvdC4=').decode())

    if party_update_meta.id == client.party.id:
        await party_update_meta.me.edit_and_keep(  # Sets default loadout.
            functools.partial(
                party_update_meta.me.set_outfit,
                config['cid']
            ),
            functools.partial(
                party_update_meta.me.set_backpack,
                config['bid']
            ),
            functools.partial(
                party_update_meta.me.set_pickaxe,
                config['pickaxe_id']
            ),
            functools.partial(
                party_update_meta.me.set_banner,
                icon=config['banner'],
                color=config['banner_colour'],
                season_level=config['level']
            ),
            functools.partial(
                party_update_meta.me.set_battlepass_info,
                has_purchased=True,
                level=config['bp_tier']
            )
        )

    await asyncio.sleep(1)  # Waits 1 second after submitting iOS token before emoting to avoid rate limits.

    await party_update_meta.me.clear_emote()  # Clears emote to allow the next emote to play.
    await party_update_meta.me.set_emote(asset=config['eid'])  # Plays the emote from config.

    if client.user.display_name != member.display_name:  # Welcomes the member who just joined.
        print(f"[PartyBot] [{datetime.datetime.now().strftime('%H:%M:%S')}] "
              f"{member.display_name} has joined the lobby.")
