from django.db import models
from hr.models import Employee, Office
from management.funs import FiscalYearNumber, FiscalYearText

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    bin = models.CharField(max_length=25, null=True, blank=True)
    tin = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class VendorAddress(models.Model):
    vendor = models.OneToOneField(Vendor, related_name="address", on_delete = models.CASCADE)
    address = models.TextField(max_length=200)
    district = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ["district", "address"]


class VendorAccount(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="account",  on_delete=models.CASCADE)
    name=models.TextField(max_length=200)
    number=models.CharField(max_length=50)
    routing = models.CharField(max_length=12)
    bank=models.CharField(max_length=50, null=True, blank=True)
    branch=models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "bank"]


class VendorContact(models.Model):
    name=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    mobile=models.CharField(max_length=25, null=True, blank=True)
    email=models.EmailField(max_length=50, null=True, blank=True)
    vendor=models.ForeignKey(Vendor, related_name="contact", on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s"%(self.name, self.vendor.name)

    class Meta:
        ordering = ["name"]


class ItemType(models.Model):
    item_type = models.CharField(max_length=50)
    def __str__(self):
        return "%s"%self.item_type


class MeasuringUnit(models.Model):
    unit = models.CharField(max_length=50)
    def __str__(self):
        return "%s"%self.unit


class TermText(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return "%s: %s"%(self.title, self.text)
    
    class Meta:
        ordering = ["title","text"]


class PartItem(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    part_no = models.CharField(max_length=50, null=True, blank=True)
    rev_part = models.CharField(max_length=50, null=True, blank=True)
    part_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit = models.ForeignKey(MeasuringUnit, on_delete=models.CASCADE, default=1)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return "%s: %s - %s"%(self.id,self.part_no, self.part_name)

    class Meta:
        ordering = ["id", "part_no","part_name"]


class TitleItem(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    item = models.TextField()

    def __str__(self):
        return "%s: %s" % (self.id, self.item)
    
    class Meta:
        ordering = ['id']


class Approval(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    conclusion = models.TextField(null=True, blank=True)
    show_payment = models.BooleanField(default=True)
    signed = models.BooleanField(default=False)
    unlock = models.BooleanField(default=True)
    raise_by = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99078', related_name="raised_by")
    submitted_to = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99090', related_name="submiited_to")
    
    def amount(self):
        amount = 0
        try:
            qid = Quotation.objects.all().filter(approval=self.id).filter(selected=True)[0].id 
            items = QuotationItem.objects.all().filter(quotation=qid)
            for i in items:
                amount = amount+i.price*i.quantity*(1+i.vat/100)
        
        except Exception as e:
            error = e

        try: 
            tid = TitleQuote.objects.all().filter(approval=self.id)[0].id
            items = TitleQuoteItem.objects.all().filter(title=tid)
            for i in items:
                amount = amount+i.amount
    
        except Exception as e:
            error = e
        return  "%s " % (amount)
        
    def ref(self):
        approvals = Approval.objects.all().order_by('id')
    
        ayear = FiscalYearNumber(self.date)
        fiscalYear = FiscalYearText(self.date)

        i = 0
        for y in approvals.filter(id__lte=self.id):
            if ayear == FiscalYearNumber(y.date):
                i = i+1
        return f"{fiscalYear}/{i:03d}"
    
    def __str__(self):
        return "%s %s" % (self.date, self.subject)

    class Meta:
        ordering = ["id"]


class Quotation(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    reference=models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField()
    advance_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    security_amount = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    vat_deducted = models.BooleanField(default=False)
    ait_deducted = models.BooleanField(default=True)
    selected=models.BooleanField(default=True)
    approval = models.ForeignKey(Approval, related_name='quotation', on_delete=models.CASCADE, default=1)
    contact = models.ForeignKey(VendorContact,on_delete=models.CASCADE, default=1)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, default=2)
    
    def __str__(self):
        return "%s-%s"%(self.id, self.reference)
    
    class Meta:
        ordering = ['id']
    

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name="item", on_delete=models.CASCADE)
    item = models.ForeignKey(PartItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1)
    price=models.DecimalField(max_digits=15, decimal_places=4, default=0)
    vat=models.DecimalField(max_digits=15, decimal_places=2, default=7.5)
    ait=models.DecimalField(max_digits=15, decimal_places=2, default=3.0)

    def __str__(self):
        return str(self.id)

    def line_amount(self):
        return self.price*self.quantity
    
    def vat_amount(self):
        return self.price*self.quantity*self.vat/100

    def line_total(self):
        return self.price*self.quantity*(1+self.vat/100)
    
    def ait_amount(self):
        return self.price*self.quantity*self.ait/100
    
    class Meta:
        ordering = ['id']

    

class TitleQuote(models.Model):
    title = models.TextField()
    approval = models.ForeignKey(Approval, related_name="title", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return "%s" %self.title
    
    class Meta:
        ordering = ['id']


class TitleQuoteItem(models.Model):
    item = models.ForeignKey(TitleItem, on_delete=models.CASCADE)
    desc = models.TextField(max_length=200, blank=True, null=True)
    amount=models.DecimalField(max_digits=15, decimal_places=2, default=0)
    title = models.ForeignKey(TitleQuote, on_delete=models.CASCADE)
   
    def __str__(self):
        return "%s" % str(self.id)
    

# Order models
class PurchaseOrder(models.Model):
    date = models.DateField()
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    order_by = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99078')
    
    def ref(self):
        orders = PurchaseOrder.objects.all().order_by('id')
    
        ayear = FiscalYearNumber(self.date)
        fiscalYear = FiscalYearText(self.date)

        i = 0
        for y in orders.filter(id__lte=self.id):
            if ayear == FiscalYearNumber(y.date):
                i = i+1
        return f"{fiscalYear}/{i:03d}"
    
    def amount(self):
        amount = 0
        try:
            items = QuotationItem.objects.all().filter(quotation=self.quotation)
            for i in items:
                amount = amount+i.price*i.quantity*(1+i.vat/100)
        
        except Exception as e:
            error = e

        return amount
    
    def __str__(self):
        return "%s: %s" % (self.id, str(self.date))
    
    class Meta: 
        ordering = ['id']

class PurchaseOrderTerm(models.Model):
    legend = models.CharField(max_length=100, blank=True, null=True)
    text = models.ForeignKey(TermText, on_delete=models.DO_NOTHING, null=True, blank=True)
    newtext = models.TextField(null=True, blank=True)
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)

    class Meta: 
        ordering = ['id']


#invoice models 
class PaymentNote(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)
    recommendation = models.TextField()
    pay_to_company = models.BooleanField(default=False)
    advance = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    security = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    vatait_added = models.BooleanField(default=True)
    ait_percent = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    vat_percent = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=1)
    received_on = models.DateField()
    signed = models.BooleanField(default=False)
    raise_by = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99078', related_name="payment_raised_by")
    submitted_to = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99090', related_name="payment_submiited_to")
    
    def ref(self):
        notes = PaymentNote.objects.all().order_by('id')
    
        ayear = FiscalYearNumber(self.date)
        fiscalYear = FiscalYearText(self.date)

        i = 0
        for y in notes.filter(id__lte=self.id):
            if ayear == FiscalYearNumber(y.date):
                i = i+1
        return f"{fiscalYear}/{i:03d}"
    
    def amount(self):
        amount = 0
        try:
            items = PaymentNoteInvoice.objects.all().filter(note=self.id)
            for i in items:
                amount = amount+i.amount
        
        except Exception as e:
            error = e

        return amount
    
    def __str__(self):
        return "%s" % self.subject 
    
    class Meta: 
        ordering = ['id']


class PaymentNoteInvoice(models.Model):
    number=models.CharField(max_length=25)
    date=models.DateField()
    particular=models.TextField(max_length=350)
    amount=models.FloatField(max_length=13, default=0.0)
    remark=models.CharField(max_length=250, null=True, blank=True)
    paid = models.BooleanField(default=False)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    note = models.ForeignKey(PaymentNote, related_name="invoice", on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['id',"number"]


class PaymentNoteApproval(models.Model):
    note = models.ForeignKey(PaymentNote, on_delete=models.CASCADE)
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)


class PaymentOthers(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    conclusion = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, models.CASCADE)
    signed = models.BooleanField(default=False)
    raise_by = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99078', related_name="others_raised_by")
    submitted_to = models.ForeignKey(Employee, on_delete=models.CASCADE, default='99090', related_name="others_submiited_to")

    def ref(self):
        notes = PaymentOthers.objects.all().order_by('id')
    
        ayear = FiscalYearNumber(self.date)
        fiscalYear = FiscalYearText(self.date)

        i = 0
        for y in notes.filter(id__lte=self.id):
            if ayear == FiscalYearNumber(y.date):
                i = i+1
        return f"{fiscalYear}/{i:03d}"
    
    def __str__(self):
        return "%s %s" % (self.date, self.subject)

    class Meta:
        ordering = ["id"]


class PaymentOthersItem(models.Model):
    item = models.ForeignKey(PartItem, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1)
    price=models.DecimalField(max_digits=15, decimal_places=3, default=0)
    vat=models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
    ait=models.DecimalField(max_digits=15, decimal_places=3, default=5.0)
    payment = models.ForeignKey(PaymentOthers, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.item.item_no)
    
    class Meta:
        ordering = ["id"]