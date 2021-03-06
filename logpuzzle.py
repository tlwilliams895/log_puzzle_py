#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = """TL Williams (tlwilliams895)
            worked with Deidre Boddie and Dessance Chandler to complete
            assessment; received assistance from Tim La, Q3 Student/Mentor"""

import os
import re
import sys
import urllib.request
import argparse


# The sort_url function will sort through the URLS group to return the
# proper inclued parts of the URL (host_name, url_group, and four letters)
def sort_url(x):
    unique_url = re.search(r"-(\w+)-(\w+)\.\w+", x)
    if unique_url:
        return unique_url.group(2)
    else:
        return x


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    under_score = filename.index("_")
    host_name = filename[under_score + 1:]
    with open(filename, "r") as log_file:
        no_duplicates = {}
        for lines in log_file:
            puzzle_url = re.search(r"GET\s(\S+)", lines)
            if puzzle_url:
                url_group = puzzle_url.group(1)
                if "puzzle" in url_group:
                    # Combine the path from each URL with the server name from
                    # the filename to form a full URL by providing a key to
                    # the value
                    no_duplicates["https://" + host_name + url_group] = 1
        # Use sorted method to sort the URL in alphabetical order and
        # without duplicates
        sorted_urls = sorted(no_duplicates.keys(), key=sort_url)
        return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    result_url_list = []
    # Use if statement to check if the dest_dir and created dir exists
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    for count, img_name in enumerate(img_urls):
        # Folder name, img name, stringify the count, and retrieve the dot
        # extension of the URL
        file_name = dest_dir + "/img" + str(count) + img_name[-4:]
        # URLretrieve method will retrieve the photos in a URL into and
        # adds into a temporary folder/directory
        urllib.request.urlretrieve(img_name, file_name)
        result_url_list.append("img" + str(count) + img_name[-4:])
    # Create HTML file to store all the images in a directory
    with open(dest_dir + "/" + "index.html", "w") as html_file:
        html_file.write(f'{"<html><body>"}')
        for photo in result_url_list:
            html_file.write(f"<img src={photo}>")
        html_file.write(f'{"</body></html>"}')


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
