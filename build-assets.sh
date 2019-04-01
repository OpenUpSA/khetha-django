#!/bin/sh -e

test -e build/assets && rm -r build/assets
mkdir -p build/assets

cp -anv node_modules/normalize.css/normalize.css -t build/assets

for package in button card floating-label layout-grid ripple textfield theme typography; do
    cp -anv "node_modules/@material/$package/dist/"*.min.* -t build/assets
done
