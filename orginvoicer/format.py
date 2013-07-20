# -*- coding: utf-8 -*-

from copy import copy
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)
#from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from .personal import address_paragraph

PAGE_HEIGHT = 792.0
PAGE_WIDTH = 612.0
stylesheet = getSampleStyleSheet()

TABLE_STYLE = TableStyle([
    ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])
    #('LINEABOVE', (0,0), (-1,0), 2, colors.green),
        #('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
        #('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),

class Layout(object):

    def __init__(self, title):
        self.title = title

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, self.title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Invoice page %d" % (doc.page,))
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Invoice page %d" % (doc.page,))
        canvas.restoreState()

def format_invoice(title, entries):
    doc = SimpleDocTemplate('invoice.pdf', pagesize=letter)
    style = stylesheet["Normal"]
    times = copy(style)
    times.fontName = 'Times-Roman'
    times.fontSize = 12
    times.leading = 14

    story = [Spacer(1,0.75*inch), Paragraph(address_paragraph, times)]

    entries = sorted(entries, key=lambda entry: entry.start)
    data = [[u'', u'', u'Time', u'Rate', u'Total']]

    for i, entry in enumerate(entries):
        d0 = entry.start.date()
        d1 = entry.end.date()
        if d0 == d1:
            dates = '{:%B %d}'.format(d0).replace(u' 0', u' ')
        else:
            dates = u'{:%b %d} – {:%b %d}'.format(d0, d1).replace(u' 0', u' ')

        h, m = divmod(entry.minutes, 60)
        elapsed = u'{}:{:02}'.format(int(h), int(m))

        p = Paragraph(entry.description, style)
        #story.append(p)
        #story.append(Spacer(1,0.2*inch))

        dollar = u'' if i else u'$'
        data.append([dates, p, elapsed,
                     u'{} {:,}'.format(dollar, entry.rate),
                     u'{} {:,}'.format(dollar, entry.amount)])

    total_amount = sum(entry.amount for entry in entries)
    total_elapsed = sum(entry.minutes for entry in entries)

    data.append([u'', u'Total ' + '.' * 80,
                 u'{}:{:02}'.format(*divmod(total_elapsed, 60)),
                 u'', u'$ {:,}'.format(total_amount)])

    table = Table(data, colWidths=[84.0, 260.0, 36.0, 30.0, 40.0],
                  style=TABLE_STYLE)
    story.append(table)

    layout = Layout(title)
    doc.build(
        story,
        onFirstPage=layout.myFirstPage,
        onLaterPages=layout.myLaterPages,
        )
