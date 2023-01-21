#!/usr/bin/python3

import inspect
import os
import subprocess
import time
import plac

from getpass import getpass
from pykeepass import PyKeePass
from urllib.request import urlopen


def get_icons(database):
    for entry in database.entries:
        print("URL: ", entry.url)
        if entry.url is None:
            continue
        try:
            with urlopen(f"https://www.google.com/s2/favicons?domain={entry.url}") as favicon:
                with open(f"temp/{entry.title}.png", "wb") as file:
                    file.write(favicon.read())
                # Can't set custom icons yet: https://github.com/libkeepass/pykeepass/pull/96
                # entry.icon = file
        except:
            pass


def move_kpa2_url_to_url(database):
    for entry in database.entries:
        custom_url_properties = list(filter(
            lambda prop: "KP2A_URL" in prop,
            entry.custom_properties.keys(),
        ))
        if len(custom_url_properties) == 0:
            continue
        if len(custom_url_properties) > 1 or (entry.url is not None and entry.url != entry.custom_properties[custom_url_properties[0]]):
            print(entry, "must be moved manually")
            print("URL:", entry.url)
            print("Custom properties:", entry.custom_properties)
            print()
            continue
        if entry.url == entry.custom_properties[custom_url_properties[0]]:
            continue
        entry.url = entry.custom_properties[custom_url_properties[0]]
        print("Moved", custom_url_properties[0], entry.url, "to URL")
        print()


def keepass_utils(database_filepath):
    database = PyKeePass(
        database_filepath,
        password=getpass("password: "),
    )
    get_icons(database)
    move_kpa2_url_to_url(database)
    database.save()
    print("done")


if __name__ == "__main__":
    plac.call(keepass_utils)
