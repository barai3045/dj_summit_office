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

from management.models import Approval, Office, PaymentNote, PaymentNoteApproval, PaymentNoteInvoice, PaymentOthers, PaymentOthersItem, Quotation, QuotationItem, VendorAccount

fiscalyear.setup_fiscal_calendar(start_year='same', start_month=7, start_day=1)

def invoice_home(request):
    template_path = "management/payment/invoice/home.html"

    notes = PaymentNote.objects.all().order_by('-id')

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "xs":page_obj,
    }

    return render(request, template_path, context)


def invoice_view(request, pk):
    template_path = "management/payment/invoice/view.html"
    
    note  = get_object_or_404(PaymentNote, pk=pk)
    office = Office.objects.get(id=100)

    invocies = PaymentNoteInvoice.objects.all().filter(note=note)
    plant = EmpOffice(note.raise_by.id, note.date)
    raise_by_title = EmpTitle(note.raise_by.id, note.date)
    submitted_to_title = EmpTitle(note.submitted_to.id, note.date)

    meta = {
        "office": f'{office.title}',
        "plant": f'{plant.title}',
        "doc_title":f"{'Approval for Bill Payment'.title()}",
        "ref": f"{office.stitle}/{plant.stitle}/Bill/{note.ref()}",
        'raised_by_name': f'{note.raise_by.first_name} {note.raise_by.last_name}',
        'raised_by_title': f'{raise_by_title.title}',
        'submitted_to_title': f'{submitted_to_title.title}'
    }

    inv_amount= 0
    for inv in invocies:
        if inv.remark:
            inv.remark = inv.remark
        elif inv.paid:
            inv.remark = "Paid"
        else: 
            inv.remark = "Recomemded for Payment"
        if not inv.paid:
            inv_amount = inv_amount + inv.amount

    inv_base = inv_amount/(1-float(note.ait_percent/100))
    ait = inv_base*float(note.ait_percent/100)
    vat = inv_base*float(note.vat_percent/100)
    payment_amount = inv_amount - float(note.advance) - float(note.security)
    
    inv_tbl = []
    if note.vatait_added: 
        inv_tbl.append({"title": f'Total Amount', "amount": '{:,.2f}'.format(inv_amount)})
    else: 
        inv_tbl.append({"title": f'Amount without AIT & VAT', "amount": '{:,.2f}'.format(inv_amount)})
        inv_tbl.append({"title": f'AIT Amount', "amount":'{:,.2f}'.format(ait)})
        inv_tbl.append({"title": f'VAT Amount', "amount":'{:,.2f}'.format(vat)})
        inv_tbl.append({"title": f'Total Amount', "amount":'{:,.2f}'.format(inv_base+vat)})

    payment_amount_txt = num2words(payment_amount,lang='en_IN')

    if(note.pay_to_company):
        recomendation = f"Recommended for bill payment of Invoiced Amount BDT {'{:,.2f}'.format(payment_amount)} ({payment_amount_txt.title()}) in the name of Company"
        rcm_title = f'Recomended for payment in the name of Company'
        adj_title = f"Recomended for bill adjustment of the comapny."
    else:
        recomendation = f"Recommended for bill payment of Invoiced Amount BDT {'{:,.2f}'.format(payment_amount)} ({payment_amount_txt.title()})"
        rcm_title = f'Recomended for payment'  
        adj_title = f"Recomended for bill adjustment"

    
    rcm_tbl = []
    rcm_tbl.append({ 'col1':"",'title': 'Title', 'amount':'Amount','col4':""})
    if note.advance > 0:
        rcm_tbl.append({'col1':"", 'title': 'Advanced Payment', 'amount':'{:,.2f}'.format(note.advance), 'col4':""})
    if note.security > 0:
        rcm_tbl.append({'col1':"",'title': 'Security Amount', 'amount':'{:,.2f}'.format(note.security), 'col4':""})

    rcm_tbl.append({'col1':"",'title': rcm_title, 'amount':'{:,.2f}'.format(payment_amount),'col4':""})
    
    doc = {
        "total_txt" :f"In Word: BDT {num2words(math.floor(inv_base *(1+float(note.vat_percent/100))+0.5),lang='en_IN')} only.",
        "payment_amount": payment_amount,
        "payment_amount_txt": payment_amount_txt,
        
    }

    if payment_amount <= 0: 
        doc["adj_title"] = adj_title

    if (note.advance + note.security) <= 0:
        doc["recomendation"] = recomendation

    account = VendorAccount.objects.all().filter(vendor=note.vendor)[0]
    
    vendor = {
        "tin": note.vendor.tin,
        "bin": note.vendor.bin,
        "name": account.name,
        "number": account.number,
        "bank": account.bank,
        "routing": account.routing,
        "branch": account.branch,
    }

    try: 
        appr = PaymentNoteApproval.objects.all().filter(note=note)[0]
        approval = get_object_or_404(Approval, pk=appr.approval.id)
        note.approval = approval
        
    except Exception as e: 
        error = e

    context = {
        'doc': doc,
        'x':note,
        'inv_tbl': inv_tbl,
        'xs2':invocies,
        "meta": meta,
        'vendor': vendor
    }

    if (note.advance + note.security) > 0:
        context["rcm_tbl"] = rcm_tbl

    return render(request, template_path, context)


def invoice_report(request, pk):
    template_path = "management/payment/invoice/report.html"
    note  = get_object_or_404(PaymentNote, pk=pk)
    office = Office.objects.get(id=100)

    invocies = PaymentNoteInvoice.objects.all().filter(note=note)
    plant = EmpOffice(note.raise_by.id, note.date)
    raise_by_title = EmpTitle(note.raise_by.id, note.date)
    submitted_to_title = EmpTitle(note.submitted_to.id, note.date)

    meta = {
        "office": f'{office.title}',
        "plant": f'{plant.title}',
        "doc_title":f"{'Bill Payment Note'.title()}",
        "ref": f"{office.stitle}/{plant.stitle}/Bill/{note.ref()}",
        'raised_by_name': f'{note.raise_by.first_name} {note.raise_by.last_name}',
        'raised_by_title': f'{raise_by_title.title}',
        'submitted_to_title': f'{submitted_to_title.title}'
    }

    inv_amount= 0
    for inv in invocies:
        if inv.remark:
            inv.remark = inv.remark
        elif inv.paid:
            inv.remark = "Paid"
        else: 
            inv.remark = "Recomemded for Payment"
        if not inv.paid:
            inv_amount = inv_amount + inv.amount

    inv_base = inv_amount/(1-float(note.ait_percent/100))
    ait = inv_base*float(note.ait_percent/100)
    vat = inv_base*float(note.vat_percent/100)
    payment_amount = inv_amount - float(note.advance) - float(note.security)
    
    inv_tbl = []
    if note.vatait_added:
        total_amount = math.floor(inv_amount+0.5)
        inv_tbl.append({'col1':" ","title": f'Total Amount', "amount": '{:,.2f}'.format(inv_amount),'col4':" " })
    else: 
        total_amount = math.floor(inv_base *(1+float(note.vat_percent/100))+0.5)
        inv_tbl.append({ 'col1':" ","title": f'Amount without AIT & VAT', "amount": '{:,.2f}'.format(inv_amount),'col4':" "})
        inv_tbl.append({'col1':" ","title": f'AIT Amount', "amount":'{:,.2f}'.format(ait),'col4':" "})
        inv_tbl.append({'col1':" ","title": f'VAT Amount', "amount":'{:,.2f}'.format(vat),'col4':" "})
        inv_tbl.append({'col1':" ","title": f'Total Amount', "amount":'{:,.2f}'.format(inv_base+vat),'col4':" "})


    payment_amount_txt = num2words(payment_amount,lang='en_IN')

    if(note.pay_to_company):
        recomendation = f"Recommended for bill payment of Invoiced Amount BDT {'{:,.2f}'.format(payment_amount)} ({payment_amount_txt.title()}) in the name of Company"
        rcm_title = f'Recomended for payment in the name of Company'
        adj_title = f"Recomended for bill adjustment of the comapny."
    else:
        recomendation = f"Recommended for bill payment of Invoiced Amount BDT {'{:,.2f}'.format(payment_amount)} ({payment_amount_txt.title()})"
        rcm_title = f'Recomended for payment'  
        adj_title = f"Recomended for bill adjustment"

    
    rcm_tbl = []
    rcm_tbl.append({'title': 'Title', 'amount':'Amount'})
    if note.advance > 0:
        rcm_tbl.append({'title': 'Advanced Payment', 'amount':'{:,.2f}'.format(note.advance)})
    if note.security > 0:
        rcm_tbl.append({'title': 'Security Amount', 'amount':'{:,.2f}'.format(note.security)})

    rcm_tbl.append({'title': rcm_title, 'amount':'{:,.2f}'.format(payment_amount)})


    doc = {
        "total_txt" :f"In Word: {num2words(total_amount,lang='en_IN')} Taka only.",
        "payment_amount": payment_amount,
        "payment_amount_txt": payment_amount_txt,
        
    }

    if payment_amount <= 0: 
        doc["adj_title"] = adj_title

    if (note.advance + note.security) <= 0:
        doc["recomendation"] = recomendation

    account = VendorAccount.objects.all().filter(vendor=note.vendor)[0]
    
    vendor = {
        "tin": note.vendor.tin,
        "bin": note.vendor.bin,
        "name": account.name,
        "number": account.number,
        "bank": account.bank,
        "routing": account.routing,
        "branch": account.branch,
    }

    try: 
        appr = PaymentNoteApproval.objects.all().filter(note=note)[0]
        approval = get_object_or_404(Approval, pk=appr.approval.id)
        note.approval = approval
        
    except Exception as e: 
        error = e

    context = {
        'doc': doc,
        'x':note,
        'inv_tbl': inv_tbl,
        'xs2':invocies,
        "meta": meta,
        'vendor': vendor
    }

    if (note.advance + note.security) > 0:
        context["rcm_tbl"] = rcm_tbl

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

def others_home(request):
    template_path = "management/payment/others/home.html"

    others = PaymentOthers.objects.all().order_by('-id')

    for x in others: 
        fy1 = FiscalYearNumber(x.date)        
        x.fiscalYear = FiscalYearText(x.date)

        i=0
        for y in others.filter(id__lte=x.id):
            fy2 = FiscalYearNumber(y.date)
            if fy1==fy2:
                i = i+1
        x.sl = i

    paginator = Paginator(others, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "xs":page_obj,
    }

    return render(request, template_path, context)


def others_view(request, pk):
    template_path = "management/payment/others/view.html"
    payment = get_object_or_404(PaymentOthers, pk=pk)
    payments = PaymentOthers.objects.all().order_by('id')

    fy1 = FiscalYearNumber(payment.date)        
    payment.fiscalYear = FiscalYearText(payment.date)

    i=0
    for x in payments.filter(id__lte=payment.id):
        fy2 = FiscalYearNumber(x.date)
        if fy1==fy2:
            i = i+1
    payment.sl = i

    items = PaymentOthersItem.objects.all().filter(payment=payment)
    sum_amount=0
    vat_amount=0
    ait_amount=0
    vat = 0
    ait =0 
    for it in items:
        it.amount = it.quantity*it.price
        sum_amount=sum_amount+it.quantity*it.price
        vat_amount=vat_amount+(it.quantity*it.price)*it.vat/100
        ait_amount=ait_amount+(it.quantity*it.price)*it.ait/100
        vat = it.vat
        ait = it.ait

    gross_amount = sum_amount + vat_amount
    payment.items = items
    payment.vat = vat
    payment.ait = ait
    payment.sum_amount = math.trunc(sum_amount)
    payment.vat_amount = math.trunc(vat_amount)
    payment.ait_amount = math.trunc(ait_amount)
    payment.gross_amount = math.trunc(gross_amount)
    gross_amount_txt = num2words(math.trunc(gross_amount), lang='en_IN')

    plant = EmpOffice(payment.raise_by.id, payment.date)
    office = 'SPL'
    payment.ref = f"{office}/{plant.stitle}/Others/{payment.ref()}"
    payment.plant = plant

    payment.raise_by.title = EmpTitle(payment.raise_by.id, payment.date)
    payment.submitted_to.title = EmpTitle(payment.submitted_to.id, payment.date)

    payment.salutation = f"Submitted for your kind approval for payment of amount BDT {format(gross_amount, '.2f')} (BDT {gross_amount_txt} only) for above stated purpose"

    payment.account = get_object_or_404(VendorAccount, vendor=payment.vendor.id)
    
    context = {
        'x':payment,
        
    }

    return render(request, template_path, context)


def others_report(request, pk):
    template_path = "management/payment/others/report.html"
    payment = get_object_or_404(PaymentOthers, pk=pk)
    payments = PaymentOthers.objects.all().order_by('id')

    fy1 = FiscalYearNumber(payment.date)        
    payment.fiscalYear = FiscalYearText(payment.date)

    i=0
    for x in payments.filter(id__lte=payment.id):
        fy2 = FiscalYearNumber(x.date)
        if fy1==fy2:
            i = i+1
    payment.sl = i

    items = PaymentOthersItem.objects.all().filter(payment=payment)
    sum_amount=0
    vat_amount=0
    ait_amount=0
    vat = 0
    ait =0 
    for it in items:
        it.amount = it.quantity*it.price
        sum_amount=sum_amount+it.quantity*it.price
        vat_amount=vat_amount+(it.quantity*it.price)*it.vat/100
        ait_amount=ait_amount+(it.quantity*it.price)*it.ait/100
        vat = it.vat
        ait = it.ait

    gross_amount = sum_amount + vat_amount
    payment.items = items

    payment.vat = vat
    payment.ait = ait
    payment.sum_amount = math.trunc(sum_amount)
    payment.vat_amount = math.trunc(vat_amount)
    payment.ait_amount = math.trunc(ait_amount)
    payment.gross_amount = math.trunc(gross_amount)
    payment.gross_amount_txt = num2words(math.trunc(gross_amount), lang='en_IN')

    plant = EmpOffice(payment.raise_by.id, payment.date)
    office = 'SPL'
    payment.ref = f"{office}/{plant.stitle}/Others/{payment.ref()}"
    payment.plant = plant

    payment.raise_by.title = EmpTitle(payment.raise_by.id, payment.date)
    payment.submitted_to.title = EmpTitle(payment.submitted_to.id, payment.date)

    payment.account = get_object_or_404(VendorAccount, vendor=payment.vendor.id)

    context = {
        'x':payment,
        
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