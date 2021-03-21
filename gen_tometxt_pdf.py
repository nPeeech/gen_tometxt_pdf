import os
import time
from datetime import timedelta
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


def find_pdf(pdf_base_dir :str) -> Iterable[str]:
    # return glob.glob(os.path.join(path, "**/*.pdf"), recursive=True)
    for child in os.listdir(path=pdf_base_dir):
        abs_child = os.path.join(pdf_base_dir, child)
        if os.path.isdir(abs_child):
            yield from find_pdf(abs_child)
        elif os.path.splitext(abs_child)[1] == ".pdf":
            printlog("find_pdf", f"Dtected {abs_child}")
            yield abs_child

def check_pdf(pdf_list :Iterable[str]) -> Iterable[str]:
    for pdf in pdf_list:
        ocr_file_exists = False
        for cur_file in os.listdir(os.path.split(pdf)[0]):
            if os.path.splitext(cur_file)[1] != ".pdf":
                continue
            elif not os.path.split(cur_file)[1].startswith("ocr_"):
                continue
            elif os.path.split(cur_file)[1] == "ocr_"+os.path.split(pdf)[1]:
                ocr_file_exists = True
        
        if ocr_file_exists:
            printlog("check_pdf", f"Skip {pdf}, because ocr_{os.path.split(pdf)[1]} already exists.")
            continue

        try:
            text = extract_text(pdf)
        except PDFPasswordIncorrect:
            printlog("check_pdf", f"Skip {pdf}, because it is encrypted.")
            continue

        text = text.strip()
        if len(text) != 0:
            printlog("check_pdf", f"Skip {pdf}, because it is already searchable.")
            continue

        printlog("check_pdf", f"It will be processed {pdf}.")
        yield pdf

def ocr_pdf(pdf :str):
    start = time.time()
    printlog("ocr_pdf", f"Process {pdf}")
    printlog("ocr_pdf", "Convert pdf to image")
    images = pdf2image.convert_from_path(pdf, dpi=400, fmt='png')
    builder = pyocr.libtesseract.LibtesseractPdfBuilder()
    output_file = os.path.join(os.path.split(pdf)[0], "ocr_" + os.path.splitext(os.path.basename(pdf))[0])
    for image in images:
        builder.add_image(image)
    builder.set_output_file(output_file)
    builder.set_lang("jpn+eng")
    printlog("ocr_pdf", f"Generate {output_file}.pdf")
    builder.build()
    printlog("ocr_pdf", f"Elapsed time: {int(time.time() - start)}[sec]")

def main():
    base_dir = os.getcwd()
    start = time.time()
    pdf_list = [pdf for pdf in find_pdf(base_dir)]
    printmsg(f"Detected {len(pdf_list)} pdf-files.")
    checked_pdf_list = [pdf for pdf in check_pdf(pdf_list)]
    printmsg(f"Detected {len(checked_pdf_list)} non-searchable-pdf-files.")
    for pdf in checked_pdf_list:
        printmsg("- " + pdf)
    for i, pdf in enumerate(checked_pdf_list):
        printmsg(f"[{i+1} / {len(checked_pdf_list)}]")
        ocr_pdf(pdf)

    printmsg(f"Elapsed time: {timedelta(seconds=time.time()-start)}")


if __name__ == "__main__":
    main()