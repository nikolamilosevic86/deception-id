#!/usr/bin/env python
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer


def createPDFDoc(fpath):
    fp = open(fpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password='')
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise "Not extractable"
    else:
        return document

class DocumentContent():
    def __init__(self):
        self.ticker = ''
        self.stock_exchange = ''
        self.presentations = []
        self.questions_answers = []

class FollowUpQuestion():
    def __init__(self,follow_up_question_asker="",follow_up_question_asker_role="",follow_up_question="",
                 follow_up_question_responder="",follow_up_question_responder_role="",follow_up_question_response=""):
        self.follow_up_question_asker = follow_up_question_asker
        self.follow_up_question_asker_role = follow_up_question_asker_role
        self.follow_up_question = follow_up_question
        self.follow_up_question_responder = follow_up_question_responder
        self.follow_up_question_responder_role = follow_up_question_responder_role
        self.follow_up_question_response = follow_up_question_response



def createDeviceInterpreter():
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return device, interpreter



def ProcessDocuments(doc_path):
    # Reads earning calls in PDF format from WWW.SPCAPITALIQ.COM
    #document=createPDFDoc('Amazon.com Inc., Q1 2012 Earnings Call, Apr 26, 2012.pdf')
    document = createPDFDoc(doc_path)
    dc = DocumentContent()
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document)
    presentation = False
    questions = False
    presentation_tuples = []
    Speaker = False
    #tuple is presenter, role, presentation
    np = pages.next()
    presentation_text = ''
    q_block_speaker = ""
    q_block_role = ""
    q_block_text = ""
    speaker_role = ''
    speaker = ''
    stock_exchange = ''
    ticker = ''
    operator_q = False
    while np:
        interpreter.process_page(np)
        layout = device.get_result()
        objs = layout._objs
        for obj in objs:
            if isinstance(obj, pdfminer.layout.LTTextBox):
                print(obj.get_text)
                for o in obj._objs:
                    if isinstance(o,pdfminer.layout.LTTextLine):
                        text=o.get_text()
                        print(text)

                        if text.strip():
                            firstChat = True
                            for c in  o._objs:
                                if isinstance(c, pdfminer.layout.LTChar) and firstChat:
                                    print("fontname %s %s"%(c.fontname,c.size))
                                    if c.size>31:
                                        try:
                                            tokens = text.split(' ')
                                            token_len = len(tokens)
                                            last = tokens[token_len-1]
                                            gr = last.split(':')
                                            stock_exchange = gr[0]
                                            ticker = gr[1]
                                        except:
                                            stock_exchange = ''
                                            ticker = ''
                                    firstChat = False
                                    if questions:
                                        if c.size<10:
                                            continue
                                        elif '........' in text:
                                            continue
                                        elif text.isupper():
                                            continue
                                        elif text.replace('\n','').isnumeric():
                                            continue
                                        elif 'Bold' in c.fontname:
                                            if q_block_text!="":
                                                dc.questions_answers.append((q_block_speaker.replace('\n',''),q_block_role.replace('\n',''),q_block_text))
                                                q_block_role = ""
                                                q_block_text = ""
                                            q_block_speaker = text
                                        elif "Italic" in c.fontname:
                                            q_block_role = text
                                        elif operator_q:
                                            continue
                                        else:
                                            q_block_text = q_block_text + ' '+text.replace('\n', ' ')

                                    if presentation:
                                        if c.size <10:
                                            continue
                                        if 'Bold' in c.fontname and 'www.' not in text.lower() and text.isupper()!=True and text.replace('\n','').isnumeric()!=True:
                                            if presentation_text!='' and presentation_text!=None:
                                                if speaker == '' and speaker_role == '' and presentation_text == '':
                                                    pass
                                                dc.presentations.append((speaker.replace('\n',''),speaker_role.replace('\n',''),presentation_text))
                                                presentation_text = ''
                                                speaker_role = ''
                                                speaker = ''
                                            speaker = text
                                            Speaker = True
                                        elif Speaker and 'Italic' in c.fontname:
                                            speaker_role = text
                                        elif '........' in text:
                                            pass
                                        else:
                                            presentation_text = presentation_text + text.replace('\n', ' ')
                                    if text == 'Presentation\n' and 'Bold' in c.fontname and c.size>18:
                                        presentation = True
                                        questions = False
                                    if text == 'Question and Answer\n' and 'Bold' in c.fontname and c.size>18:
                                        questions = True
                                        presentation = False
            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                pass
    #            parse_obj(obj._objs)
            else:
                pass
        try:
            np = pages.next()
        except:
            np = False
    dc.stock_exchange = stock_exchange
    dc.ticker = ticker
    return dc





#print(pdf_to_text('Activision Blizzard, Inc., Q1 2015 earnings Call, May 06, 2015.pdf'))



