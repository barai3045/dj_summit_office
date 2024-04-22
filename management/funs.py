import os
import fiscalyear
from django.conf import settings
from django.contrib.staticfiles import finders 

def FiscalYearNumber(date):
    f1 = fiscalyear.FiscalDate(date.year,date.month,date.day)        
    return fiscalyear.FiscalYear(f1.fiscal_year)


def FiscalYearText(date):
    f1 = fiscalyear.FiscalDate(date.year,date.month,date.day)        
    return str(f1.fiscal_year) +"-"+ str(f1.fiscal_year+1)[2:4]


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path
