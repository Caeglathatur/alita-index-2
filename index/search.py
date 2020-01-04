"""
Copyright © 2019-2020 Alita Index / Caeglathatur

This file is part of Alita Index.

Alita Index is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Alita Index is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Alita Index.  If not, see <https://www.gnu.org/licenses/>.
"""

import math

from . import models


search_fields = {
    "Entry": ["title", "description", "url", "keywords"],
    "SubEntry": ["title", "description", "url"],
    "Category": ["name", "keywords"],
    "Tag": ["name"],
    "Author": ["name", "url"],
    "EntryIdentifier": ["value"],
    "SubEntryIdentifier": ["value"],
}


def add_hits(all_terms, scores, entry, term, inc):
    if entry not in scores:
        scores[entry] = {"hits": {t: 0 for t in all_terms}}
    scores[entry]["hits"][term] += inc


def search_entries(query):
    """Searches entries, ranks results with TF-IDF.

    :returns: ordered list of (
        <Entry>,
        {
            "hits": {<term>: <count>},
            "tf": {<term>: <term freq score>},
            "tfidf": {<term>: <term freq inverse doc freq score>},
            "tfidf_sum": <sum of tfidf scores>,
        }
    )
    """

    terms = query.lower().split()
    if not terms:
        return []

    # {
    #     <Entry>: {
    #         "hits": {<term>: <count>},
    #         "tf": {<term>: <term freq score>},
    #         "tfidf": {<term>: <term freq inverse doc freq score>},
    #         "tfidf_sum": <sum of tfidf scores>,
    #     },
    # }
    scores = {}

    entries = models.Entry.objects.filter(is_visible=True)
    N = entries.count()
    sub_entries = models.SubEntry.objects.all()
    categories = models.Category.objects.all()
    authors = models.Author.objects.all()
    tags = models.Tag.objects.all()
    entry_identifiers = models.EntryIdentifier.objects.all()
    sub_entry_identifiers = models.SubEntryIdentifier.objects.all()

    # Search in entries
    for e in entries:
        for field in search_fields["Entry"]:
            if not hasattr(e, field):
                continue
            content = getattr(e, field).lower()
            for term in terms:
                if term in content:
                    add_hits(terms, scores, e, term, content.count(term))

    # Search in sub entries
    for s in sub_entries:
        for field in search_fields["SubEntry"]:
            if not hasattr(s, field):
                continue
            content = getattr(s, field).lower()
            for term in terms:
                if term in content:
                    add_hits(
                        terms, scores, s.entry_traversed, term, content.count(term)
                    )

    # Search in categories
    for c in categories:
        for field in search_fields["Category"]:
            if not hasattr(c, field):
                continue
            content = getattr(c, field).lower()
            for term in terms:
                if term in content:
                    for e in c.entries_visible_traversed:
                        add_hits(terms, scores, e, term, content.count(term))

    # Search in authors
    for a in authors:
        for field in search_fields["Author"]:
            if not hasattr(a, field):
                continue
            content = getattr(a, field).lower()
            for term in terms:
                if term in content:
                    for e in a.entries_visible:
                        add_hits(terms, scores, e, term, content.count(term))

    # Search in tags
    for t in tags:
        for field in search_fields["Category"]:
            if not hasattr(t, field):
                continue
            content = getattr(t, field).lower()
            for term in terms:
                if term in content:
                    for e in t.entries_visible:
                        add_hits(terms, scores, e, term, content.count(term))

    # Search in entry identifiers
    for i in entry_identifiers:
        for field in search_fields["EntryIdentifier"]:
            if not hasattr(i, field):
                continue
            content = getattr(i, field).lower()
            for term in terms:
                if term in content:
                    add_hits(terms, scores, i.entry, term, content.count(term))

    # Search in sub entry identifiers
    for i in sub_entry_identifiers:
        for field in search_fields["SubEntryIdentifier"]:
            if not hasattr(i, field):
                continue
            content = getattr(i, field).lower()
            for term in terms:
                if term in content:
                    add_hits(terms, scores, i.entry, term, content.count(term))

    entry_count_per_term = {}
    for term in terms:
        count = 0
        for entry in scores:
            if scores[entry]["hits"][term] > 0:
                count += 1
        entry_count_per_term[term] = count

    idf_per_term = {}
    for term in terms:
        idf_per_term[term] = math.log(N / (1 + entry_count_per_term[term]))

    for entry in scores:
        scores[entry]["tf"] = tf(scores[entry]["hits"])

    for entry in scores:
        scores[entry]["tfidf"] = tfidf(idf_per_term, scores[entry]["tf"])
        scores[entry]["tfidf_sum"] = sum(
            [val for term, val in scores[entry]["tfidf"].items()]
        )

    # Only return visible entries
    scores = list(filter(lambda e: e[0].is_visible, scores.items()))
    # Sort by title
    scores = sorted(scores, key=lambda e: e[0].title)
    # Sort by tfidf sum
    scores = sorted(scores, key=lambda e: e[1]["tfidf_sum"], reverse=True)

    return scores


def tf(entry_hits):
    tf = {}
    for term, hits in entry_hits.items():
        tf[term] = math.log(1 + hits)
    return tf


def tfidf(idf_per_term, entry_tf):
    tfidf = {}
    for term, tf in entry_tf.items():
        tfidf[term] = tf * idf_per_term[term]
    return tfidf
