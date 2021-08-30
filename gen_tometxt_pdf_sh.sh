#!/bin/bash
# ex. bash ./gen_tometxt_pdf_sh.sh hoge.pdf jpn 3840
pdf="$1"
lang="$2"
scale="$3"
pdfwithoutext="${1%.pdf}"
pdfdir="${pdfwithoutext}.d"

mkdir "$pdfdir"
pdftoppm -png -scale-to "${scale}" "${pdf}" "${pdfdir}/img"

find ./${pdfdir}/ -type f -name "*.png" | sed 's/\.png$//' | xargs -P4 -n1 -I{} tesseract {}.png {} -l "${lang}" pdf

pdftk "./${pdfdir}"/*.pdf cat output "${pdfwithoutext}_ocr.pdf"

rm -r "./${pdfdir}" 
