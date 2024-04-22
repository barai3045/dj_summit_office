
from rest_framework import generics, viewsets, permissions
from management import serializers
from management import models

# Create your views here.
class VendorViewSet(viewsets.ModelViewSet):
    queryset = models.Vendor.objects.all().order_by('name')
    serializer_class = serializers.VendorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VendorAddressViewSet(viewsets.ModelViewSet):
    queryset  = models.VendorAddress.objects.all()
    serializer_class = serializers.VendorAddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VendorContactViewSet(viewsets.ModelViewSet):
    queryset  = models.VendorContact.objects.all()
    serializer_class = serializers.VendorContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VendorAccountViewSet(viewsets.ModelViewSet):
    queryset  = models.VendorAccount.objects.all()
    serializer_class = serializers.VendorAccountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset  = models.ItemType.objects.all()
    serializer_class = serializers.ItemTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MeasuringUnitViewSet(viewsets.ModelViewSet):
    queryset  = models.MeasuringUnit.objects.all()
    serializer_class = serializers.MeasuringUnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PartItemViewSet(viewsets.ModelViewSet):
    queryset  = models.PartItem.objects.all()
    serializer_class = serializers.PartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TitleItemViewSet(viewsets.ModelViewSet):
    queryset  = models.TitleItem.objects.all()
    serializer_class = serializers.TitleItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset  = models.Approval.objects.all().order_by('-id')
    serializer_class = serializers.ApprovalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuotationViewSet(viewsets.ModelViewSet):
    queryset  = models.Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuotationItemViewSet(viewsets.ModelViewSet):
    queryset  = models.QuotationItem.objects.all().order_by("-id")
    serializer_class = serializers.QuotationItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TitleQuoteViewSet(viewsets.ModelViewSet):
    queryset  = models.TitleQuote.objects.all()
    serializer_class = serializers.TitleQuoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TitleQuoteItemViewSet(viewsets.ModelViewSet):
    queryset  = models.TitleQuoteItem.objects.all()
    serializer_class = serializers.TitleQuoteItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset  = models.PurchaseOrder.objects.all().order_by('-id')
    serializer_class = serializers.PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PurchaseOrderTermViewSet(viewsets.ModelViewSet):
    queryset  = models.PurchaseOrderTerm.objects.all()
    serializer_class = serializers.PurchaseOrderTermSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class PaymentNoteViewSet(viewsets.ModelViewSet):
    queryset  = models.PaymentNote.objects.all().order_by('-id')
    serializer_class = serializers.PaymentNoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class PaymentNoteInvoiceViewSet(viewsets.ModelViewSet):
    queryset  = models.PaymentNoteInvoice.objects.all()
    serializer_class = serializers.PaymentNoteInvoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentNoteApprovalViewSet(viewsets.ModelViewSet):
    queryset  = models.PaymentNoteApproval.objects.all()
    serializer_class = serializers.PaymentNoteApprovalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentOthersViewSet(viewsets.ModelViewSet):
    queryset  = models.PaymentOthers.objects.all()
    serializer_class = serializers.PaymentOthersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentOthersItemViewSet(viewsets.ModelViewSet):
    queryset  = models.PaymentOthersItem.objects.all()
    serializer_class = serializers.PaymentOthersItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
