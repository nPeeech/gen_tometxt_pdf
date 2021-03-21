import os
from os import path
import time
from datetime import timedelta
import argparse
import pyocr
import pdf2image
from typing import Iterable
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
# import glob

def printmsg(msg :str):
    print("\033[32m", msg, "\033[37m")

def printlog(name, msg :str):
    print("[", name, "]", msg)


def find_pdf(pdf_base_dir :str, is_recursive :bool) -> Iterable[str]:
    # return glob.glob(os.path.join(path, "**/*.pdf"), recursive=True)
    if not is_recursive:
        for child in os.listdir(path=pdf_base_dir):
            abs_child = os.path.join(pdf_base_dir, child)
            if os.path.isfile(abs_child) and os.path.splitext(abs_child)[1] == ".pdf":
                printlog("find_pdf", f"Dtected {abs_child}")
                yield abs_child
    else:
        for child in os.listdir(path=pdf_base_dir):
            abs_child = os.path.join(pdf_base_dir, child)
            if os.path.isdir(abs_child):
                yield from find_pdf(abs_child, is_recursive=True)
            elif os.path.splitext(abs_child)[1] == ".pdf":
                printlog("find_pdf", f"Dtected {abs_child}")
                yield abs_child

def check_pdf(pdf_list :Iterable[str], prefix :str) -> Iterable[str]:
    for pdf in pdf_list:
        ocr_file_exists = False
        for cur_file in os.listdir(os.path.split(pdf)[0]):
            if os.path.splitext(cur_file)[1] != ".pdf":
                continue
            elif not os.path.split(cur_file)[1].startswith(prefix):
                continue
            elif os.path.split(cur_file)[1] == prefix + os.path.split(pdf)[1]:
                ocr_file_exists = True
        
        if ocr_file_exists:
            printlog("check_pdf", f"Skip {pdf}, because ocr_{os.path.split(pdf)[1]} already exists")
            continue

        try:
            text = extract_text(pdf)
        except PDFPasswordIncorrect:
            printlog("check_pdf", f"Skip {pdf}, because it is encrypted")
            continue

        text = text.strip()
        if len(text) != 0:
            printlog("check_pdf", f"Skip {pdf}, because it is already searchable")
            continue

        printlog("check_pdf", f"It will be processed {pdf}")
        yield pdf

def ocr_pdf(pdf :str, dpi :int, prefix :str, language :str):
    start = time.time()
    printlog("ocr_pdf", f"Process {pdf}")
    printlog("ocr_pdf", "Convert pdf to image")
    images = pdf2image.convert_from_path(pdf, dpi=dpi, fmt='png')
    builder = pyocr.libtesseract.LibtesseractPdfBuilder()
    output_file = os.path.join(os.path.split(pdf)[0], prefix + os.path.splitext(os.path.basename(pdf))[0])
    for image in images:
        builder.add_image(image)
    builder.set_output_file(output_file)
    builder.set_lang(language)
    printlog("ocr_pdf", f"Generate {output_file}.pdf")
    builder.build()
    printlog("ocr_pdf", f"Elapsed time: {int(time.time() - start)}[sec]")

def main():
    base_dir = os.getcwd()
    parser = argparse.ArgumentParser(description='This program recursively searches PDF files from the current directory and generates searchable-PDF from non-searchable-PDF. The generated PDF has the prefix "ocr_". "example.pdf" is ignored when "ocr_example.pdf" and "example.pdf" exist.')
    parser.add_argument("--dpi", default=200, type=int, help="Output PDF dpi, default 200[dpi]")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for PDF files")
    parser.add_argument("-p", "--prefix", default="ocr_", help='Prefix of generated PDF files, default "ocr_"')
    parser.add_argument("-l", "--language", default="eng", help='Language options passed to tesseract. For example, "jpn", "jpn+eng".')
    args = parser.parse_args()

    start = time.time()
    pdf_list = [pdf for pdf in find_pdf(base_dir, args.recursive)]
    printmsg(f"Detected {len(pdf_list)} PDF-files")
    checked_pdf_list = [pdf for pdf in check_pdf(pdf_list, prefix=args.prefix)]
    printmsg(f"Detected {len(checked_pdf_list)} non-searchable-PDF-files")
    for pdf in checked_pdf_list:
        printmsg("- " + pdf)
    for i, pdf in enumerate(checked_pdf_list):
        printmsg(f"[{i+1} / {len(checked_pdf_list)}]")
        ocr_pdf(pdf, dpi=args.dpi, prefix=args.prefix, language=args.language)

    printmsg(f"Elapsed time: {timedelta(seconds=time.time()-start)}")


if __name__ == "__main__":
    main()