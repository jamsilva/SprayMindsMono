#!/usr/bin/env python

import fontforge
import sys
import os

latest          = sys.argv[1]
previous        = sys.argv[2]
new_family_name = sys.argv[3]

latest_font   = fontforge.open(latest)
previous_font = fontforge.open(previous)

font_name_parts = latest_font.fontname.split('-');

if len(font_name_parts) != 2:
    raise Exception('Unexpeced fontname')

font_style = font_name_parts[1]

def swap_glyph(new_font, new_char, old_font, old_char):
    reserved_codepoint = 0xEBAC;
    reserved_name = 'EBACkup'

    # Step 1 - old backup
    old_font.createChar(reserved_codepoint, reserved_name)
    old_font.selection.select(old_char)
    old_font.copy()
    old_font.selection.select(reserved_name)
    old_font.paste()

    # Step 2 - copy new to old
    new_font.selection.select(new_char)
    new_font.copy()
    old_font.selection.select(old_char)
    old_font.paste()

    # Step 3 - copy old backup to new
    old_font.selection.select(reserved_name)
    old_font.copy()
    new_font.selection.select(new_char)
    new_font.paste()

    # Step 4 - delete old backup
    old_font.removeGlyph(reserved_name)

def swap_variant_glyphs(font, variant):
    for glyph in font:
        if glyph.endswith(variant) and not font[glyph].references:
            swap_glyph(font, glyph[:-len(variant)], font, glyph)

variants = [
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

for v in variants:
    swap_variant_glyphs(latest_font, v)

for v in old_chars:
    swap_glyph(latest_font, v, previous_font, v)

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
