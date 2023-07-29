#!/usr/bin/env python

import fontforge
import psMat
import sys

font = fontforge.open(sys.argv[1])

for g in font.glyphs():
    g.transform(psMat.scale(0.94, 1.0))

family_name = font.familyname

for sfnt_names in font.sfnt_names:
    lang, strid, val = sfnt_names

    if strid == 'Preferred Family':
        family_name = val
        break

font_name_parts = font.fontname.split('-');

if len(font_name_parts) != 2:
    raise Exception('Unexpeced fontname')

font.fontname   = font.fontname.replace('Mono', 'MonoCondensed')
font.familyname = font.familyname.replace('Mono', 'Mono Condensed')
font.fullname   = font.fullname.replace('Mono', 'Mono Condensed')
version         = font.version.split(';')[0]
font_style      = font_name_parts[1]
unique_id       = version + ';NM;' + font.fontname + '-' + font_style
font.appendSFNTName('English (US)', 'UniqueID', unique_id);
font.appendSFNTName('English (US)', 'Preferred Family', family_name.replace('Mono', 'Mono Condensed'))

o = font.fontname.replace('Condensed ', 'Condensed-').replace(' ', '')
d = './'

if len(sys.argv) > 2:
    d = sys.argv[2] + '/'

font.generate(d + o + '.ttf')
