from rest_framework import serializers
from management.models import *

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ['url', 'name', 'phone', 'mobile', 'email', 'bin', 'tin', 'address', 'contact', 'account']


class VendorAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VendorAddress
        fields = "__all__"


class VendorContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VendorContact
        fields = "__all__"


class VendorAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VendorAccount
        fields = "__all__"



## Approval
    
class ItemTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = ItemType
        fields = "__all__"    


class MeasuringUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MeasuringUnit
        fields = "__all__"

        
class PartItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PartItem
        fields = ['id', 'part_no', 'rev_part', 'part_name', 'description', 'unit', 'item_type']



class TitleItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = TitleItem
        fields = "__all__"


class ApprovalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Approval
        fields = ['url', 'id', 'date','subject', 'description', 'conclusion', 'show_payment', 'signed', 'unlock', 'raise_by', 'submitted_to', 'quotation', 'title']
        depth=2


class QuotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Quotation
        fields = ['url', 'reference',  'date', 'advance_amount', 'security_amount', 'vat_deducted', 'ait_deducted', 'selected', 'approval', 'contact', 'item_type', 'item']

       
class QuotationItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = QuotationItem
        fields = "__all__"


class TitleQuoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = TitleQuote
        fields = "__all__"


class TitleQuoteItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = TitleQuoteItem
        fields = "__all__"




class PurchaseOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PurchaseOrder
        fields = "__all__"


class PurchaseOrderTermSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PurchaseOrderTerm
        fields = "__all__"


class PaymentNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PaymentNote
        fields = ['url','date', 'subject', 'recommendation', 'pay_to_company', 'advance', 'security', 'vatait_added', 'ait_percent', 'vat_percent', 'signed', 'vendor', 'received_on', 'raise_by', 'submitted_to', 'invoice' ]



class PaymentNoteInvoiceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PaymentNoteInvoice
        fields = "__all__"


class PaymentNoteApprovalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentNoteApproval
        fields = "__all__"
        

class PaymentOthersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PaymentOthers
        fields = "__all__"
        

class PaymentOthersItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PaymentOthersItem
        fields = "__all__"


        