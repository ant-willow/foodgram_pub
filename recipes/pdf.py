import reportlab
from foodgram import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate


class PDFMaker:
    def __init__(self, buffer, pagesize):

        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        else:
            self.width, self.height = self.pagesize

        reportlab.rl_config.TTFSearchPath.append(str(settings.STATIC_ROOT))
        pdfmetrics.registerFont(TTFont('natural_mono', 'natural_mono.ttf'))

    def create_pdf(self, values_dict):
        buffer = self.buffer
        doc = SimpleDocTemplate(
            buffer, rightMargin=36, leftMargin=36, topMargin=36,
            bottomMargin=0, pagesize=self.pagesize)

        styles = getSampleStyleSheet()
        heading2_cyrillic = ParagraphStyle(
            name='cyrillic_heading',
            parent=styles['Heading2'],
            fontName="natural_mono")
        normal_cyrillic = ParagraphStyle(
            name="cyrillic",
            fontName="natural_mono")

        elements = []
        elements.append(Paragraph('Список покупок', heading2_cyrillic))

        for key, value in values_dict.items():
            paragraph = Paragraph(
                # название (ед. изм) - количество
                f'{key} ({value[1]}) - {value[0]}', normal_cyrillic)
            elements.append(paragraph)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
