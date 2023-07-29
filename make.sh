#!/bin/bash

UPSTREAM="https://github.com/JetBrains/JetBrainsMono.git"
NEWTTFDIR="New/fonts/ttf"
OLDTTFDIR="Old/ttf"
SRCFONTNAME="JetBrainsMonoNL"
NEWFONTTITLE="Spray Minds Mono"
NEWFONTNAME="$(echo "$NEWFONTTITLE" | sed 's/ //g')"

[ -d "$NEWTTFDIR" ] || git clone "$UPSTREAM" "New" --depth=1
[ -d "$OLDTTFDIR" ] || git clone "$UPSTREAM" "Old" --depth=1 --branch=v1.0.6

for previous in "$OLDTTFDIR/$SRCFONTNAME"*.ttf; do
	previous_file="$(basename "$previous")"
	latest_file="$(echo "$previous_file" | sed -e 's/Bold-/Bold/' -e 's/Medium-/Medium/')"
	latest="$NEWTTFDIR/$latest_file"
	final_name="$(echo "$latest_file" | sed 's/'$SRCFONTNAME'/'$NEWFONTNAME'/g')"
	python3 patch.py "$latest" "$previous" "$NEWFONTTITLE"
	python3 condenser.py "$final_name"
done
