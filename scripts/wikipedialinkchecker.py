# -*- coding: utf-8 -*-

import sys
import requests

import pywikibot
from pywikibot.pagegenerators import LinkedPageGenerator
from pywikibot.textlib import replace_links

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'

linking_page_title = pywikibot.input(u'Which page do you want to process?')
linking_page = pywikibot.Page(pywikibot.Link(linking_page_title,
                                             pywikibot.Site()))

if not linking_page.exists():
    print 'That page does not exist.'
    sys.exit(0)

corrected_text = {}
wikipedia_pages = {}
red_linked_pages = [p for p in list(LinkedPageGenerator(linking_page))
                    if not p.exists()]

chunk_size = 20
for i in range(0, len(red_linked_pages), chunk_size):
    rlp = red_linked_pages[i:i+chunk_size]
    for p in rlp:
        wikipedia_pages[p.title()] = p

    query = u'https://en.wikipedia.org/w/api.php?titles=' + \
            u'|'.join([p.title() for p in rlp]) + \
            u'&action=query&format=json&formatversion=2&utf8=&redirects='
    res = requests.get(query).json()

    if 'redirects' in res['query']:
        for r in res['query']['redirects']:
            assert r['from'] in wikipedia_pages
            wikipedia_pages[r['from']].wikipedia_title = r['to']

    for p in res['query']['pages']:
        if p['pageid'] < 0 or p['title'] not in wikipedia_pages:
            continue
        else:
            wikipedia_pages[p['title']].wikipedia_title = p['title']

links_to_fix = []
for k, v in wikipedia_pages.items():
    to_fix = pywikibot.input(k)
    if to_fix == u'y':
        links_to_fix.append(k)

for l in links_to_fix:
    backlinks = wikipedia_pages[l].backlinks()
    print 'processing backlinks for', l

    def replace(link, text, groups, rng):
        if link.title == l:
                if groups['label'] is not None:
                        label = groups['label']
                else:
                        label = link.title
                return u'[[wikipedia:%s|%s]]' % \
                    (wikipedia_pages[l].wikipedia_title, label)
        else:
                return None

    for b in backlinks:
        if b.namespace() != 0:
            continue
        print 'Processing page:', b.title()
        if b.title() not in corrected_text:
            corrected_text[b.title()] = b.text
        corrected_text[b.title()] = replace_links(corrected_text[b.title()],
                                                  replace,
                                                  site=pywikibot.Site())

for page_title, text in corrected_text.items():
        linking_page = pywikibot.Page(pywikibot.Link(page_title,
                                                     pywikibot.Site()))
        linking_page.text = text
        print '--- corrected text for %s ---' % page_title
        linking_page.save(u'Fix links to Wikipedia')
