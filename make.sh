#!/bin/bash

UPSTREAM="https://github.com/JetBrains/JetBrainsMono.git"
NEWTTFDIR="New/fonts/ttf"
OLDTTFDIR="Old/ttf/No ligatures"
SRCFONTNAME="JetBrainsMonoNL"
NEWFONTTITLE="Spray Minds Mono"
NEWFONTNAME="$(echo "$NEWFONTTITLE" | sed 's/ //g')"

[ -d "$NEWTTFDIR" ] || git clone "$UPSTREAM" "New" --depth=1
[ -d "$OLDTTFDIR" ] || git clone "$UPSTREAM" "Old" --depth=1 --branch=v2.001

mkdir -p "$NEWFONTNAME"

for previous in "$OLDTTFDIR/$SRCFONTNAME"*.ttf; do
	previous_file="$(basename "$previous")"
	latest_file="$(echo "$previous_file" | sed -e 's/Bold-/Bold/' -e 's/Medium-/Medium/')"
	latest="$NEWTTFDIR/$latest_file"

	if [ -f "$latest" ]; then
		final_name="$(echo "$latest_file" | sed 's/'$SRCFONTNAME'/'$NEWFONTNAME'/g')"
		python3 patch.py "$latest" "$previous" "$NEWFONTTITLE" "$NEWFONTNAME"
		python3 condenser.py "$NEWFONTNAME/$final_name" "$NEWFONTNAME"
	fi
done

tar -I "zstd -19" -cf "$NEWFONTNAME.tar.zst" "$NEWFONTNAME"
