 #!/usr/bin/env python2.7
#
# Copyright 2017 Edward G. Bruck <ed.bruck1@gmail.com>
#
# This file is part of Radiotray-NG.
#
# Radiotray-NG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radiotray-NG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radiotray-NG.  If not, see <http://www.gnu.org/licenses/>.

from lxml import etree
import json
import sys
import os.path

bookmarks = []

def walk_bookmarks(root, group_func, bookmark_func, group=""):
    children = root.xpath("/bookmarks" + group + "/group | " + "/bookmarks" + group + "/bookmark")

    for child in children:
        child_name = child.get('name')
        url = child.get('url')

        if not child_name:
            continue

        if  child.tag == 'group':
            group_func(child_name)
            walk_bookmarks(root, group_func, bookmark_func, group + "/group[@name='" + child_name + "']")
        else:
            bookmark_func(group, child_name, url)


def group_callback(group_name):
    if len(bookmarks):
        if not bookmarks[0].has_key(group_name):
            bookmarks.append({'group' : group_name, 'image' : '', 'stations' : [] })
    else:
        bookmarks.append({'group' : group_name, 'image' : '', 'stations' : [] })


def bookmark_callback(group, radio_name, url):
    group = group[group.rfind("@name='") + 7:].strip("']")

    if radio_name.startswith("[separator-"):
        pass
    else:
        for e in bookmarks:
            if e['group'] == group:
                for s in e['stations']:
                    if s['name'].lower() == radio_name.lower():
                        break
                else:
                    e['stations'].append({'name' : radio_name, 'image' : '', 'url' : url})
                break


def prune_empty_groups():
    bookmarks_tmp = bookmarks
    for item in list(bookmarks_tmp):
        if len(item['stations']) == 0:
            bookmarks.remove(item)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: rt2rtng <path to radiotray bookmarks.xml>"
        exit(1)

    if os.path.exists(sys.argv[1]):
        root = etree.parse(sys.argv[1]).getroot()
        walk_bookmarks(root, group_callback, bookmark_callback)
        prune_empty_groups()        
        print json.dumps(bookmarks, indent=4)
    else:
        print sys.argv[1], "not found!"
