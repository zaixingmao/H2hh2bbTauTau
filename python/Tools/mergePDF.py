#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from glob import glob
from pyPdf import PdfFileReader, PdfFileWriter



def opts():
    parser = optparse.OptionParser()
    parser.add_option("--path", dest="path", default = '.', help="")
    parser.add_option("--output", dest="fName", default = 'merged.pdf', help="")

    options, args = parser.parse_args()
    return options

def merge(path, output_filename):
    output = PdfFileWriter()

    for pdffile in glob('*.pdf'):
        if pdffile == output_filename:
            continue
        print("Parse '%s'" % pdffile)
        document = PdfFileReader(open(pdffile, 'rb'))
        for i in range(document.getNumPages()):
            output.addPage(document.getPage(i))

    print("Start writing '%s'" % output_filename)
    output_stream = file(output_filename, "wb")
    output.write(output_stream)
    output_stream.close()

op = opts()
merge(op.path, op.fName)
