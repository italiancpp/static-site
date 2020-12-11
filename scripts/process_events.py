import os
import xml.etree.ElementTree as ET
import re
import pathlib

print(os.getcwd())



olddir = "/Users/fm/Documents/Projects/static-site/jekyll-export/_posts/"
newdir = "/Users/fm/Documents/Projects/static-site/src/_posts/"

tree = ET.parse('italiancpp-events.xml')
root = tree.getroot()

events = root.findall(".//item")

for e in events:

    title = e.find("title").text.replace(":", ",")
    date = e.find("wp_post_date").text
    name = e.find("wp_post_name").text
    author = e.find("dc_creator").text
    content = e.find("content_encoded").text

    datelist = re.findall("(\\d+)-(\\d+)-(\\d+)\s(\\d+):(\\d+):(\\d+)", date)    

    print("event title: '%s'" % title)
    print("event name:  '%s'" % name)
    print("event date:  '%s'" % datelist)
    print("event auth:  '%s'" % author)
    
    categories = e.findall("category")

    tags = []
    for c in categories:
        if c.get("domain") == "post_tag":
            n = c.get("nicename")
            tags.append(n)

    print("event tags:  '%s'" % tags)

    fname = newdir + "%s-%s-%s-%s" % (datelist[0][0], datelist[0][1], datelist[0][2], name) + ".md"
    # fname = newdir + "%s-%s-%s-%s" % ("2020", "11", "20", name) + ".md"
    print("file name:   '%s'" % fname)
    


    # fp = pathlib.Path(fname)
    # if fp.is_file():
    #     os.remove(fname)
    # else:
    #     print("not")

    # continue

    f = open(fname, "w")

    f.write("---\n")
    f.write("title: %s\n" % title)
    f.write("author: %s\n" % author)
    f.write("layout: post\n")
    f.write("categories: Eventi\n")

    if len(tags) > 0:
        f.write("tags:\n")
        for t in tags:
            f.write("  - %s\n" % t.lower())

    f.write("---\n")
    f.write("\n\n")

    # f.write(content)
    f.write("%s\n" % content)

    f.close()
    print("")
    # break
    pass

"""
---
title: Qualcosa-anche e è é
author: marco
layout: post
categories: Eventi
tags:
  - Community
  - Reddit
  - Slack
---


hello
---
"""