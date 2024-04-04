import flet as ft
from DBEngineWrapper import DBEngineWrapper
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.colors import Color


global_bill = []
global_customer = []
engine = DBEngineWrapper()

def get_invoice(invoice):
    global global_bill
    global_bill = invoice
    
def get_customer():
    global global_customer
    global_customer = engine.getCustomer(global_bill['customer_id'])
    
def generate_bill(e):
    page = e.page
    page.snack_bar = ft.SnackBar(ft.Text('Successful download!'))
    page.snack_bar.open = True
    generate_bill_pdf(f"{global_bill['invoice_bank_reference']}__{global_bill['invoice_due_date']}.pdf")
    page.update()
    
def generate_bill_pdf(filename):
    PDFPSReporte(filename)
    
class PDFPSReporte:

    def __init__(self, path):
        self.path = path
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        # colors - Azul turkeza 367AB3
        self.colorOhkaGreen0 = Color((45.0/255), (166.0/255), (153.0/255), 1)
        self.colorOhkaGreen1 = Color((182.0/255), (227.0/255), (166.0/255), 1)
        self.colorOhkaGreen2 = Color((140.0/255), (222.0/255), (192.0/255), 1)
        self.colorOhkaBlue0 = Color((54.0/255), (122.0/255), (179.0/255), 1)
        self.colorOhkaBlue1 = Color((122.0/255), (180.0/255), (225.0/255), 1)
        self.colorOhkaGreenLineas = Color((50.0/255), (140.0/255), (140.0/255), 1)
        
        self.PageHeader()
        self.tableMaker()
        self.PageFooter()
        # Build
        self.doc = SimpleDocTemplate(path, pagesize=LETTER)
        self.doc.multiBuild(self.elements)

    def PageHeader(self):
            get_customer()
            img = Image('TosiSopivaUI\img\logo.png', kind='proportional')
            img.drawHeight = 50
            img.drawWidth = 50
            img.hAlign = 'RIGHT'
            self.elements.append(img)
            
            psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT, justifyLastLine=1)
            name = f"Customer: {global_customer['customer_first_name']} {global_customer['customer_last_name']}"
            address = f"Address: {global_customer['customer_address']}"
            phone = f"Phone: {global_customer['customer_phone']}"
            email =  f"Email: {global_customer['customer_email']}"
            
            paragraphReportSummary = Paragraph(name, psDetalle)
            self.elements.append(paragraphReportSummary)
            paragraphReportSummary = Paragraph(address, psDetalle)
            self.elements.append(paragraphReportSummary)
            paragraphReportSummary = Paragraph(phone, psDetalle)
            self.elements.append(paragraphReportSummary)
            paragraphReportSummary = Paragraph(email, psDetalle)
            self.elements.append(paragraphReportSummary)

            psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_CENTER, borderWidth=3, textColor=self.colorOhkaGreen0)
            text = f"INVOICE {global_bill['invoice_id']}"
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 2
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 1)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 0.5
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)
            
    def PageFooter(self):
            get_customer()
            
            psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_RIGHT, justifyLastLine=1)
            due_date = f"Due date: {global_bill['invoice_due_date']}"
            bank_reference = f"Bank reference: {global_bill['invoice_bank_reference']}"
            due_date = f"Due date: {global_bill['invoice_due_date']}"
            due_date = f"Due date: {global_bill['invoice_due_date']}"
            
            paragraphReportSummary = Paragraph(due_date, psDetalle)
            self.elements.append(paragraphReportSummary)
            paragraphReportSummary = Paragraph(bank_reference, psDetalle)
            self.elements.append(paragraphReportSummary)


            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 2
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 1)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 0.5
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)


    def tableMaker(self):        
        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["Line id", "Product id", "Quantity", "Price", "Product description"]
                
        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)        

        data = [d]
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_CENTER),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]
        
        invoice_lines = global_bill['invoice_lines']
        
        for invoice_line in invoice_lines:
            lineData = []
            lineData.append(str(invoice_line['invoice_line_id']))  # Adding invoice line ID
            lineData.append(str(invoice_line['product_item_id']))  # Adding product item ID
            lineData.append(str(invoice_line['quantity']))  # Adding quantity
            lineData.append(str(invoice_line['price']))  # Adding price
            lineData.append(invoice_line['product_description'])  # Adding product description
    
            data.append(lineData)

        # totalRow = ["Total", "", "", "", "30:15"]
        totalRow = ["Total","","","",global_bill['invoice_total']]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)
        
        #print(data)
        table = Table(data, colWidths=[50, 70, 50, 60, 200])
        tStyle = TableStyle([ #('GRID',(0, 0), (-1, -1), 0.5, grey),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                #('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
                ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
                ('BACKGROUND',(0, 0), (-1, 0), self.colorOhkaGreenLineas),
                ('BACKGROUND',(0, -1),(-1, -1), self.colorOhkaBlue1),
                ('SPAN',(0,-1),(-2,-1))
                ])
        table.setStyle(tStyle)
        self.elements.append(table)
        spacer = Spacer(10, 10)
        self.elements.append(spacer)