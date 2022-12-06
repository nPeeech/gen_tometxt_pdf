gen_tometxt_pdf
===
Python script is broken.  
You can use a shell script that can only convert a single file.
## Overview
Generate searchable-PDF from non-searchable-PDF.

## Description
- ~Recursively searche PDF files from the current directory.~
- ~Generate searchable-PDF from non-searchable-PDF.~
- ~The generated PDF has the prefix "_ocr".~
- ~"example.pdf" is ignored when "ocr_example.pdf" and "example.pdf" exist.~

## ~Requirement~
- ~tesseract-ocr~
- ~pdf2image~
- ~pdfminer.six~
- ~pyocr~

## ~Usage~
```
$ gen-tometxt-pdf --help
usage: gen_tometxt_pdf.py [-h] [-d DPI] [-r] [-p PREFIX] [-l LANGUAGE] [--overwrite-save]

This program recursively searches PDF files from the current directory and generates searchable-PDF from non-searchable-PDF. The generated PDF has the prefix "ocr_". "example.pdf" is ignored when "ocr_example.pdf" and "example.pdf" exist.

optional arguments:
  -h, --help            show this help message and exit
  -d DPI, --dpi DPI     Output PDF dpi, default 200[dpi]
  -r, --recursive       Recursively search for PDF files
  -p PREFIX, --prefix PREFIX
                        Prefix of generated PDF files, default "ocr_"
  -l LANGUAGE, --language LANGUAGE
                        Language options passed to tesseract. For example, "jpn", "jpn+eng".
  --overwrite-save      Overwrite the original PDF file
```

## Install
```
$ sudo apt install pdftk-java poppler-utils tesseract-ocr tesseract-ocr-jpn
$ git clone https://github.com/nPeeech/gen_tometxt_pdf
$ cd gen_tometxt_pdf
$ pip install -r ./requipments.txt
$ sudo cp ./gen_tometxt_pdf_sh.sh /usr/local/bin/gen_tometxt_pdf_sh
$ sudo chmod a+x /usr/local/bin/gen_tometxt_pdf_sh
```
