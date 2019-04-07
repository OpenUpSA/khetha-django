#!/bin/sh -e

test -e build/assets && rm -r build/assets
mkdir -p build/assets

cp -av node_modules/normalize.css/normalize.css build/assets
cp -av node_modules/material-components-web/dist/material-components-web.min.* build/assets
cp -av node_modules/zepto/dist/zepto.min.js build/assets

cp -av node_modules/autosize/dist/autosize.js build/assets
