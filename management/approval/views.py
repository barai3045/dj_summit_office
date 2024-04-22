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

from management.models import *

def approval_home(request):
    template_path = "management/approval/home.html"

    approvals = Approval.objects.all().order_by('-id')

    paginator = Paginator(approvals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'xs': page_obj
    }
    return render(request, template_path, context)

def approval_view(request, pk):
    template_path = "management/approval/view.html"
    
    approval = get_object_or_404(Approval, pk=pk)

    plant = EmpOffice(approval.raise_by.id, approval.date).stitle
    office = 'SPL'
        
    meta = {
        'ref': f"{office}/{plant}/Approval/{approval.ref()}",
        "title": EmpTitle(approval.raise_by.id, approval.date),
        "title2": EmpTitle(approval.submitted_to.id, approval.date)
    }


    context = {
       'x': approval, 
       'meta': meta
    }

    quotations = Quotation.objects.filter(approval=approval)
    titles = TitleQuote.objects.filter(approval=approval)
    sum_amount = 0
    
    if titles:
        title = titles[0]
        context['titles'] = title

        titleitems = TitleQuoteItem.objects.filter(title = title)
        
        context['titleItems'] = titleitems
        for item in titleitems:
            sum_amount = sum_amount + item.amount
        
        context['sum_amount'] = sum_amount
        context['txt_amount'] = num2words(math.floor(float(sum_amount) + 0.5), lang='en_IN').title()
   

    if quotations:
        count = quotations.count()
        context['xs']=quotations
        context['count']=count
        
        if count ==1:
            quotation = quotations[0]
            items = QuotationItem.objects.filter(quotation=quotation)
            total = vat = ait = vat_per = 0
            for x in items:
                total = total + x.price * x.quantity
                vat = vat + x.price * x.quantity * x.vat /100
                ait = ait + x.price * x.quantity * x.ait /100
                vat_per = vat_per + x.vat
            
            vat_per = vat_per / items.count()

            quotation.items = items
            quotation.total = total
            quotation.vat = vat
            quotation.ait = ait
            quotation.gross = total+vat
            quotation.vat_per = vat_per

            context['q1'] = quotation
            
        if count > 1:
            items = []
            y = []
            c = 0
            vats = []
            aits = []
            totals = []
            grosses = []
            vat_per = 0

            for i in range(count):
                itms = QuotationItem.objects.filter(quotation=quotations[i])
                total = vat = ait = 0
                for it in itms:
                    total = total + it.price * it.quantity
                    vat = vat + it.price * it.quantity * it.vat / 100
                    ait = ait + it.price * it.quantity * it.ait / 100
                    vat_per = it.vat
                
                totals.append(total)
                vats.append(vat)
                grosses.append(total+vat)
                aits.append(ait)
                items.append(itms)
                y.append(i)
                c = itms.count()
            text1 = f'VAT Amount({vat_per:.2f}%)'    
            text2 = "Total Amount including AIT"
            text3 = "Gross Amount"

            vats.insert(0, text1)
            totals.insert(0, text2)
            grosses.insert(0, text3)

            its = []
            prices = []
            vendors = []
            for i in range(c):
                its_dic = {}
                for j in y:
                    prices.append(items[j][i].price)
                    vendors.append(items[j][i].quotation.contact.vendor)
                its_dic["item"] = items[j][0].item
                its_dic["prices"] = prices
                its.append(its_dic)

            context["vendors"] = vendors
            context["vats"] = vats
            context["totals"] = totals
            context["grosses"] = grosses
            context["items"] = its
        
        for q in quotations:
            if q.selected:
                quotation_s = q
        
        adv_amount = quotation_s.advance_amount
        sec_amount = quotation_s.security_amount
        
        sitems = QuotationItem.objects.filter(quotation=quotation_s)
        
        sum_amount = 0
        for x in sitems:
            sum_amount = sum_amount + x.quantity * x.price * (1 + x.vat / 100)

        vendor = quotation_s.contact.vendor.name

        sl = 0
        p_advance = []
        if adv_amount > 0:
            sl = sl + 1
            p_advance.append(sl)
            p_advance.append(adv_amount)
            p_advance.append(vendor)
            p_advance.append("Pay In Advance with Purchase Order")

            context['p_advance'] = p_advance

        p_amount = []
        sl = sl + 1
        p_amount.append(sl)
        p_amount.append(math.floor(float(sum_amount - sec_amount - adv_amount) + 0.5))
        p_amount.append(vendor)
        p_amount.append("After submission of Original Bill")

        context['p_amount'] = p_amount

        p_security = []
        if sec_amount > 0:
            sl = sl + 1
            p_security.append(sl)
            p_security.append(sec_amount)
            p_security.append(vendor)

            context['p_security'] = p_security
        
    txt_amount = num2words(math.floor(float(sum_amount) + 0.5), lang='en_IN').title()
    txt_num = '{:,.2f}'.format(math.floor(float(sum_amount) + 0.5))
    salutation = f'Submitted for your kind approval for an amount of BDT ' + txt_num +'  (' + txt_amount + f') for above stated purpose'
    context['salutation'] = salutation
    
    return render(request, template_path, context)



def approval_report(request, pk):
    template_path = "management/approval/report.html"
    
    approval = get_object_or_404(Approval, pk=pk)
    
    
    plant = EmpOffice(approval.raise_by.id, approval.date)
    office = 'SPL'
        
    meta = {
        'ref': f"{office}/{plant.stitle}/Approval/{approval.ref()}",
        'office': plant.title,
        "title": EmpTitle(approval.raise_by.id, approval.date),
        "title2": EmpTitle(approval.submitted_to.id, approval.date)
    }


    context = {
       'x': approval, 
       'meta': meta
    }

    quotations = Quotation.objects.filter(approval=approval)
    titles = TitleQuote.objects.filter(approval=approval)
    sum_amount = 0

    if titles:
        title = titles[0]
        context['titles'] = title
        
        titleitems = TitleQuoteItem.objects.filter(title = title)
        context['titleItems'] = titleitems
        for item in titleitems:
            sum_amount = sum_amount + item.amount
        context['sum_amount'] = sum_amount
        context['txt_amount'] = num2words(math.floor(float(sum_amount) + 0.5), lang='en_IN').title()

    if quotations:
        count = quotations.count()
        context['xs']=quotations
        context['count']=count
        
        
        if count ==1:
            quotation = quotations[0]
            items = QuotationItem.objects.filter(quotation=quotation)
            total = vat = ait = vat_per = 0
            for x in items:
                total = total + x.price * x.quantity
                vat = vat + x.price * x.quantity * x.vat /100
                ait = ait + x.price * x.quantity * x.ait /100
                vat_per = vat_per + x.vat
            
            vat_per = vat_per / items.count()

            quotation.items = items
            quotation.total = total
            quotation.vat = vat
            quotation.ait = ait
            quotation.gross = total+vat
            quotation.vat_per = vat_per

            context['q1'] = quotation
            print(total, vat, ait, vat_per)
        if count > 1:
            items = []
            y = []
            c = 0
            vats = []
            aits = []
            totals = []
            grosses = []
            vat_per = 0

            for i in range(count):
                itms = QuotationItem.objects.filter(quotation=quotations[i])
                total = vat = ait = 0
                for it in itms:
                    total = total + it.price * it.quantity
                    vat = vat + it.price * it.quantity * it.vat / 100
                    ait = ait + it.price * it.quantity * it.ait / 100
                    vat_per = it.vat
                
                totals.append(total)
                vats.append(vat)
                grosses.append(total+vat)
                aits.append(ait)
                items.append(itms)
                y.append(i)
                c = itms.count()
            text1 = f'VAT Amount({vat_per:.2f}%)'    
            text2 = "Total Amount including AIT"
            text3 = "Gross Amount"

            vats.insert(0, text1)
            totals.insert(0, text2)
            grosses.insert(0, text3)

            its = []
            prices = []
            vendors = []
            for i in range(c):
                its_dic = {}
                for j in y:
                    prices.append(items[j][i].price)
                    vendors.append(items[j][i].quotation.contact.vendor)
                its_dic["item"] = items[j][0].item
                its_dic["prices"] = prices
                its.append(its_dic)

            context["vendors"] = vendors
            context["vats"] = vats
            context["totals"] = totals
            context["grosses"] = grosses
            context["items"] = its
        
        for q in quotations:
            if q.selected:
                quotation_s = q

        adv_amount = quotation_s.advance_amount
        sec_amount = quotation_s.security_amount
        
        sitems = QuotationItem.objects.filter(quotation=quotation_s)

        sum_amount = 0
        for x in sitems:
            sum_amount = sum_amount + x.quantity * x.price * (1 + x.vat / 100)

        vendor = quotation_s.contact.vendor.name

        sl = 0
        p_advance = []
        if adv_amount > 0:
            sl = sl + 1
            p_advance.append(sl)
            p_advance.append(adv_amount)
            p_advance.append(vendor)
            p_advance.append("Pay In Advance with Purchase Order")

            context['p_advance'] = p_advance

        p_amount = []
        sl = sl + 1
        p_amount.append(sl)
        p_amount.append(math.floor(float(sum_amount - sec_amount - adv_amount) + 0.5))
        p_amount.append(vendor)
        p_amount.append("After submission of Original Bill")

        context['p_amount'] = p_amount

        p_security = []
        if sec_amount > 0:
            sl = sl + 1
            p_security.append(sl)
            p_security.append(sec_amount)
            p_security.append(vendor)

            context['p_security'] = p_security

    txt_amount = num2words(math.floor(float(sum_amount) + 0.5), lang='en_IN').title()
    txt_num = '{:,.2f}'.format(math.floor(float(sum_amount) + 0.5))
    salutation = f'Submitted for your kind approval for an amount of BDT ' + txt_num +'  (' + txt_amount + f') for above stated purpose'
    context['salutation'] = salutation

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


def quotation_home(request):
    template_path = "management/quotation/home.html"

    quotations = Quotation.objects.all().order_by('-id')


    paginator = Paginator(quotations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'xs': page_obj
    }
    return render(request, template_path, context)


def quotation_view(request, pk):
    template_path = "management/quotation/view.html"

    quotation = get_object_or_404(Quotation, pk=pk)

    quotation.items = QuotationItem.objects.all().filter(quotation=quotation.id)

    total_line_amount =0 
    total_vat_amount =0 
    total_amount =0 
    total_ait_amount =0 
    for x in quotation.items:
        total_line_amount = total_line_amount + x.price*x.quantity
        total_vat_amount = total_vat_amount + x.price*x.quantity*x.vat/100
        total_amount = total_amount + x.price*x.quantity*(1+x.vat/100)
        total_ait_amount = total_ait_amount + x.price*x.quantity*x.ait/100

    quotation.total_line_amount = total_line_amount
    quotation.total_vat_amount = total_vat_amount
    quotation.total_amount = total_amount
    quotation.total_ait_amount = total_ait_amount
    
    context = {
        'x': quotation,
        
    }
    return render(request, template_path, context)


def title_home(request):
    template_path = "management/title/home.html"

    titles = TitleQuote.objects.all().order_by('-id')


    paginator = Paginator(titles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'xs': page_obj
    }
    return render(request, template_path, context)


def title_view(request, pk):
    template_path = "management/title/view.html"

    title = get_object_or_404(TitleQuote, pk=pk)

    items = TitleQuoteItem.objects.filter(title=title)

    total = 0 
    for x in items:
        total = total + x.amount
    
    title.total = total
    

    context = {
        "x": title, 
        "xs": items, 
    }

    return render(request, template_path, context)