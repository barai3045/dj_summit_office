from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
import fiscalyear
import math
from io import BytesIO
from num2words import num2words
from xhtml2pdf import pisa


from management.models import Vendor, VendorAccount, VendorAddress, VendorContact

def vendor_home(request):
    template_path = "management/base/vendor/home.html"
    
    vendors = Vendor.objects.all().order_by('name')
    
    paginator = Paginator(vendors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'xs': page_obj
    }

    return render(request, template_path, context)


def vendor_view(request, pk):
    template_path = "management/base/vendor/view.html"
    
    vendor = get_object_or_404(Vendor, pk=pk)
    
    vendor.address = VendorAddress.objects.filter(vendor = vendor)[0]
    vendor.accounts = VendorAccount.objects.filter(vendor = vendor)
    vendor.contacts = VendorContact.objects.filter(vendor = vendor)
    
    context = {
        'x': vendor
    }

    return render(request, template_path, context)