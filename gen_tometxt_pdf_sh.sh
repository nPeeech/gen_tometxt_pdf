#!/bin/bash
# ex. bash ./gen_tometxt_pdf_sh.sh hoge.pdf jpn 3840
pdf="$1"
lang="$2"
dpi="$3"
pdfwithoutext="${1%.pdf}"
pdfdir="${pdfwithoutext}.d"

mkdir "$pdfdir"
pdftoppm -jpeg -jpegopt quality=70 -r "${dpi}" "${pdf}" "${pdfdir}/img"

find ./${pdfdir}/ -type f -name "*.jpg" | sed 's/\.jpg$//' | xargs -P4 -n1 -I{} tesseract {}.jpg {} -l "${lang}" pdf

pdftk "./${pdfdir}"/*.pdf cat output "${pdfwithoutext}_ocr.pdf"

rm -r "./${pdfdir}" 
