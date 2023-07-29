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

if (len(font_name_parts) != 2):
    raise Exception('Unexpeced fontname')

font_style = font_name_parts[1]

character_variants = {
        'zero': 'zero.zero',

        # 'five':      'five.cv20',
        # 'five.dnom': 'five.dnom.cv20',
        # 'five.numr': 'five.numr.cv20',

        # 'f': 'f.cv09.ss20',

        # 'g':           'g.cv03',
        # 'uni01F5':     'uni01F5.cv03',
        # 'gbreve':      'gbreve.cv03',
        # 'gcaron':      'gcaron.cv03',
        # 'gcircumflex': 'gcircumflex.cv03',
        # 'uni0123':     'uni0123.cv03',
        # 'gdotaccent':  'gdotaccent.cv03',

        'u':             'u.cv12',
        'uacute':        'uacute.cv12',
        'ubreve':        'ubreve.cv12',
        'ucircumflex':   'ucircumflex.cv12',
        'udieresis':     'udieresis.cv12',
        'uni1EE5':       'uni1EE5.cv12',
        'ugrave':        'ugrave.cv12',
        'uni1EE7':       'uni1EE7.cv12',
        'uhorn':         'uhorn.cv12',
        'uni1EE9':       'uni1EE9.cv12',
        'uni1EF1':       'uni1EF1.cv12',
        'uni1EEB':       'uni1EEB.cv12',
        'uni1EED':       'uni1EED.cv12',
        'uni1EEF':       'uni1EEF.cv12',
        'uhungarumlaut': 'uhungarumlaut.cv12',
        'umacron':       'umacron.cv12',
        'uogonek':       'uogonek.cv12',
        'uring':         'uring.cv12',
        'utilde':        'utilde.cv12'
}

old_variants = {
	'J': 'J'
}

def replace_glyph(new_font, new_char, old_font, old_char):
	new_font.removeGlyph(new_char)
	old_font.selection.select(old_char)
	old_font.copy()
	new_font.selection.select(new_char)
	new_font.paste()

for k in character_variants.keys():
    replace_glyph(latest_font, k, latest_font, character_variants[k])

for k in old_variants.keys():
    replace_glyph(latest_font, k, previous_font, old_variants[k])

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
