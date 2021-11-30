#!/usr/bin/env python

"""
Pandoc filter to read special comments for layouting.

Currently supported:
- <!-- PAGE BREAK -->

"""

from pandocfilters import RawBlock, toJSONFilter
import re

def layout(key, value, format, meta):
    changes = []
    if key == "RawBlock":
        changes.extend(handlePageBreak(key, value, format, meta))
    changes = list(filter(None, changes))
    return changes if len(changes) > 0 else None

def handlePageBreak(key, value, format, meta):
    p_pagebreak = re.compile("<!--\s+PAGE\s*BREAK\s+-->", re.IGNORECASE)
    fmt, s = value
    if p_pagebreak.match(s):
        return pageBreak(format)
    return []

def pageBreak(format):
    if format == "docx":
        return [RawBlock("openxml", "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>")]
    return []

if __name__ == "__main__":
    toJSONFilter(layout)
