#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Processing a log file that records visits"""

import argparse
import csv
import datetime
import operator
import re
import urllib2


def main():
    """ the main function."""
    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--url", help="Enter the URL to fetch a CSV file.")
    args = url_parser.parse_args()

    if args.url:
        try:
            csvData = downloadData(args.url)
            processData(csvData)       

        except urllib2.URLError as e:
            print "The URL entered is invalid."
    else:
        print "Please insert the URL."
        

def downloadData(url):
    """Obtains content from URL"""
    content = urllib2.urlopen(url)
    return content


def processData(content):
    """Processes data from CSV file"""
    csvData = csv.reader(content)
    dateFormat = "%Y-%m-%d %H:%M:%S"
    hits = 0
    imgHits = 0 
    safari = chrome = firefox = msie = 0

    times = {i:0 for i in range(0, 24)}

    for row in csvData:
        result = {"path":row[0], "date":row[1], "browser": row[2], "status": row[3], "size": row[4]}

        date = datetime.datetime.strptime(result["date"], dateFormat)
        times[date.hour] = times[date.hour] + 1

        hits += 1
        if re.search(r"\.(?:jpg|jpeg|gif|png)$", result["path"], re.I | re.M):
            imgHits += 1

        elif re.search("chrome/\d+", result["browser"], re.I):
            chrome += 1

        elif re.search("safari", result["browser"], re.I) and not re.search("chrome/\d+", result["browser"], re.I):
            safari += 1

        elif re.search("firefox", result["browser"], re.I):
            firefox += 1

        elif re.search("msie", result["browser"], re.I):
            msie += 1

    imageRequest = (float(imgHits) / hits) * 100
    browsers = {"Safari": safari, "Chrome": chrome, "Firefox": firefox, "MSIE": msie}

    print "Results are shown below:"
    print "Image requests account for {0:0.1f}% of all requests.".format(imageRequest)
    print "The most popular browser is %s." % (max(browsers.iteritems(), key=operator.itemgetter(1))[0])

    sorted_times = sorted(times.items(), key=operator.itemgetter(1))
    sorted_times.reverse()
    for i in sorted_times:
        print "Hour %02d has %s hits." % (i[0], i[1])

if __name__ == "__main__":
    main()
