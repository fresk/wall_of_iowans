#!/bin/bash
SCRIPT_PATH="${BASH_SOURCE[0]}";
if([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
SCRIPT_PATH=`dirname ${SCRIPT_PATH}`

cd $SCRIPT_PATH;

#rm -r cache
mkdir -p ./cache/original
mkdir -p ./cache/128
mkdir -p ./cache/256
mkdir -p ./cache/512


curl -X GET http://www.fresksite.net/dcadb/wp-content/themes/dca/api/iowans.php > _iowans.json
python sanitize.py



cp ../img/anon.jpg cache/original/anon.jpg
cp ../img/anon.jpg cache/original/alt-anon.jpg


if [[ "$OSTYPE" =~ ^darwin ]]; then

    sips -Z 128 cache/original/* --out ./cache/128
    sips -Z 256 cache/original/* --out ./cache/256 
    sips -Z 512 cache/original/* --out ./cache/512
    kivy -m kivy.atlas cache/128atlas 2048x2048 ./cache/128/*
    kivy -m kivy.atlas cache/256atlas 2048x2048 ./cache/256/*
    kivy -m kivy.atlas cache/512atlas 2048x2048 ./cache/512/*

    kivy -m kivy.atlas cache/alt 2048x2048 ./cache/256/alt-*

else

    for file in cache/original/*; do 
        convert $file -resize 128x128 cache/128atlas/`basename $file`; 
        convert $file -resize 256x256 cache/256atlas/`basename $file`; 
        convert $file -resize 512x512 cache/512atlas/`basename $file`; 
        echo -n "."
    done

    # echo "cropping alt images"
    # for file in cache/original/alt-*; do    
    #     convert $file -resize 205x256^ -gravity center   cache/256/`basename $file`; 
    #     echo "."
    # done

    echo "generating atlases"
    # sips -Z 256 cache/original/* --out ./cache/256 
    # sips -Z 512 cache/original/* --out ./cache/512
    #python -m kivy.atlas cache/128 2048x2048 ./cache/128/*
    #python -m kivy.atlas cache/alt 2048x2048 ./cache/256/alt-*
    #python -m kivy.atlas cache/256 2048x2048 ./cache/128/*
    python -m kivy.atlas cache/512 2048x2048 ./cache/512/*


fi