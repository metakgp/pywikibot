# -*- coding: utf-8 -*-

import sys
import requests
import re

import pywikibot
from pywikibot.pagegenerators import LinkedPageGenerator
from pywikibot.textlib import replace_links

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'

page_title = pywikibot.input(u'Which page do you want to process?')

page_to_process = pywikibot.Page(pywikibot.Site(), page_title);

page_text = page_to_process.text;

date_regex = re.compile('[0-9]{4}-{0-9]{2}-[0-9]{2}')

page_text.replace('\n', ' ')

matches = date_regex.findall(page_text)

if len(matches) == 0:

    print 'There are no date strings on this page'
    exit(0)

replace_array = []

for i in matches:
    
    date_components = i.split('-')
    assert date_components.length == 3
    date_components = [int(i) for i in date_components]
    this_date = datetime.date(date_components[0], date_components[1], date_components[2]).strftime('%B %d, %Y')
    replace_array.append([i, this_date_string])

for old_date_string, new_date_string in replace_array:

    page_text.replace(old_date_string, new_date_string);

page_to_process.text = page_text;
page_to_process.save(u'Fix date strings');

