#!/usr/bin/env python

import fontforge
import os
import re
import sys

latest          = sys.argv[1]
previous        = sys.argv[2]
new_family_name = sys.argv[3]

latest_font   = fontforge.open(latest)
previous_font = fontforge.open(previous)

font_name_parts = latest_font.fontname.split('-');

if len(font_name_parts) != 2:
    raise Exception('Unexpeced fontname')

font_style = font_name_parts[1]

def copy_glyph(new_font, new_char, old_font, old_char):
    old_font.selection.select(old_char)
    old_font.copy()
    new_font.selection.select(new_char)
    new_font.paste()

def copy_variant_glyphs(font, variant):
    for glyph in font:
        if variant in glyph and not font[glyph].references:
            copy_glyph(font, glyph[:-len(variant)], font, glyph)

def delete_variants(font):
    for glyph in font:
        if re.search('.(ss|cv)[0-9][0-9]', glyph):
            font.removeGlyph(glyph)

copy_variants = [
    '.zero', # 0
    '.cv12', # u and related chars
    '.cv20', # 5 and related chars
]

old_chars = [
    'J',
    'IJ',
    'Jcircumflex',
    'uni0408',
]

for v in copy_variants:
    copy_variant_glyphs(latest_font, v)

for v in old_chars:
    copy_glyph(latest_font, v, previous_font, v)

delete_variants(latest_font)

# fixup: https://github.com/JetBrains/JetBrainsMono/issues/334
latest_font.os2_winascent   = previous_font.os2_winascent
latest_font.os2_windescent  = previous_font.os2_windescent
latest_font.os2_typoascent  = previous_font.os2_typoascent
latest_font.os2_typodescent = previous_font.os2_typodescent
latest_font.hhea_ascent     = previous_font.hhea_ascent
latest_font.hhea_descent    = previous_font.hhea_descent

old_family_name = latest_font.familyname

for sfnt_names in latest_font.sfnt_names:
    lang, strid, val = sfnt_names

    if strid == 'Preferred Family':
        old_family_name = val
        break

# change font info
old_compact_name = old_family_name.replace(' ', '')
new_compact_name = new_family_name.replace(' ', '')
latest_font.fontname = latest_font.fontname.replace(old_compact_name, new_compact_name)
latest_font.familyname = latest_font.familyname.replace(old_family_name, new_family_name)
latest_font.fullname = latest_font.fullname.replace(old_family_name, new_family_name)
version = latest_font.version.split(';')[0]
unique_id = version + ';NM;' + new_compact_name + '-' + font_style
latest_font.appendSFNTName('English (US)', 'UniqueID', unique_id);
latest_font.appendSFNTName('English (US)', 'Preferred Family', new_family_name)

outdir = './'

if len(sys.argv) > 4:
    outdir = sys.argv[4] + '/'

latest_font.generate(outdir + latest_font.fontname + '.ttf')
