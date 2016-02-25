import sys
import nltk
from nltk.corpus import stopwords
import string
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def extract(args):
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

    #Lowercase
    text = retstr.getvalue().lower()

    #Remove puntuations
    text = text.translate(string.maketrans("",""), string.punctuation)

    #Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = nltk.word_tokenize(text.decode('utf-8'))

    tokens = [word for word in tokens if not word in stop_words]
    #trigrams = nltk.trigrams(tokens)

    out = open(args[0]+'.txt', 'w')
    #out.write(trigrams)
    out.write(text)

    fp.close()
    device.close()
    retstr.close()
    out.close()

if __name__ == '__main__':
    #nltk.download('punkt')
    extract(sys.argv[1:])
