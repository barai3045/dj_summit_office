from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
import fiscalyear
import math
from io import BytesIO
from num2words import num2words
from xhtml2pdf import pisa
from hr.funs import EmpOffice, EmpTitle
from management.funs import FiscalYearNumber, FiscalYearText, link_callback

from management.models import PurchaseOrder, PurchaseOrderTerm, QuotationItem, VendorAddress

def order_home(request):
    template_path = "management/order/home.html"

    orders = PurchaseOrder.objects.all().order_by('-id')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'xs': page_obj
    }
    return render(request, template_path, context)

def order_view(request, pk):
    template_path = "management/order/view.html"

    order = get_object_or_404(PurchaseOrder, pk=pk)
    order.address = VendorAddress.objects.all().filter(vendor = order.quotation.contact.vendor)[0]
    orders = PurchaseOrder.objects.all().order_by('id')
    
    items = QuotationItem.objects.all().filter(quotation =order.quotation)
    total = vat = ait = vat_per= 0
    
    for x in items:
        vat = vat + x.quantity * x.price * x.vat/100
        ait = ait + x.quantity * x.price * x.ait/100
        total = total + x.quantity * x.price 

        vat_per = x.vat
    
    txt_amount = num2words(math.floor(float(total+vat) + 0.5), lang='en_IN').title()
    txt_num = '{:,.2f}'.format(math.floor(float(total+vat) + 0.5))
    salutation = f'Submitted for your kind approval for an amount of BDT ' + txt_num +'  (' + txt_amount + f') for above stated purpose'
    
    order.terms = PurchaseOrderTerm.objects.filter(order=order)

    order.total = '{:,.2f}'.format(math.floor(float(total) + 0.5))
    order.vat = '{:,.2f}'.format(math.floor(float(vat) + 0.5))
    order.vat_per = vat_per
    order.ait = ait
    order.gross = '{:,.2f}'.format(math.floor(float(vat+total) + 0.5)) 
    order.txt_amount = txt_amount
    
    service = False
    if order.quotation.item_type.item_type == 'Service':
        service = True
    
    order.service = service

    company = 'SPL'
    plant = EmpOffice(order.order_by.id, order.date)
    referance = f'{company}/{plant.stitle}/PO/{order.ref()}'
    order.ref = referance
    order.office = plant
    order.order_by_title = EmpTitle(order.order_by.id, order.date)
   
    context = {
        'x': order,
        'xs':items
    }
    return render(request, template_path, context)


def order_report(request, pk):
    template_path = "management/order/report.html"

    order = get_object_or_404(PurchaseOrder, pk=pk)
    order.address = VendorAddress.objects.all().filter(vendor = order.quotation.contact.vendor)[0]
    orders = PurchaseOrder.objects.all().order_by('id')
    
    items = QuotationItem.objects.all().filter(quotation =order.quotation)
    total = vat = ait = vat_per= 0
    
    for x in items:
        vat = vat + x.quantity * x.price * x.vat/100
        ait = ait + x.quantity * x.price * x.ait/100
        total = total + x.quantity * x.price 

        vat_per = x.vat
        x.price1 = '{:,.2f}'.format(math.floor(x.price))
        x.line_total1 = '{:,.2f}'.format(math.floor(x.price*x.quantity))
    
    for item in items:
        print(item.price1, item.line_total1)
       
    
    txt_amount = num2words(math.floor(float(total+vat) + 0.5), lang='en_IN').title()
    txt_num = '{:,.2f}'.format(math.floor(float(total+vat) + 0.5))
    salutation = f'Submitted for your kind approval for an amount of BDT ' + txt_num +'  (' + txt_amount + f') for above stated purpose'
    
    order.terms = PurchaseOrderTerm.objects.filter(order=order).order_by('id')

    order.total = '{:,.2f}'.format(math.floor(float(total) + 0.5))
    order.vat = '{:,.2f}'.format(math.floor(float(vat) + 0.5))
    order.vat_per = vat_per
    order.ait = ait
    order.gross = '{:,.2f}'.format(math.floor(float(vat+total) + 0.5)) 
    order.txt_amount = txt_amount
    
    service = False
    if order.quotation.item_type.item_type == 'Service':
        service = True
    
    order.service = service

    company = 'SPL'
    plant = EmpOffice(order.order_by.id, order.date)
    referance = f'{company}/{plant.stitle}/PO/{order.ref()}'
    order.ref = referance
    order.office = plant
    order.order_by_title = EmpTitle(order.order_by.id, order.date)
   
    context = {
        'x': order,
        'xs':items
    }

    # template_path = 'user_printer.html'
    # context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response