import sys
import nltk
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def extract(args):
    print('In extract')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(args[0], 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)


    text = retstr.getvalue()
    tokens = nltk.word_tokenize(text)
    trigrams = ngrams(tokens,3)

    out = open(args[0]+'.txt', 'w')
    out.write(trigrams)


    fp.close()
    device.close()
    retstr.close()
    out.close()

if __name__ == '__main__':
    #nltk.download('punkt')
    extract(sys.argv[1:])
