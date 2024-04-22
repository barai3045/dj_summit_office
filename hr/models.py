import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Office(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    stitle = models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    parent = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return '%s' %(self.title)
    
    class Meta:
        ordering = ['id']


class Title(models.Model):
    id=models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    stitle = models.CharField(max_length=15)

    def __str__(self):
        return '%s-%s' % (self.id, self.title)

    class Meta:
        ordering = ["id"]


class Employee(models.Model):
    gender_choices = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    ]
    
    blood_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    id = models.CharField(max_length=5, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=gender_choices, default="M")
    blood = models.CharField(max_length=5,choices=blood_choices, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    hire_title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='hire_title', default=1402)
    hire_office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='hire_office', default=100)
    present_title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='present_title', blank=True, null=True)
    present_office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='present_office', blank=True, null=True)

    def save(self, *args, **kwargs):
        ttl = EmployeeTitle.objects.all().filter(employee=self.id).filter(date__lte=datetime.date.today()).order_by('-date')
        if ttl:
            ttl0 = ttl[0]
            self.present_title = ttl0.title
        else:
            self.present_title = self.hire_title

        off = EmployeeOffice.objects.all().filter(employee=self.id).filter(date__lte=datetime.date.today()).order_by('-date')
        if off:
            off0 = off[0]
            self.present_office = off0.office
        else:
            self.present_office = self.hire_office
        super().save(*args, **kwargs)
    
    def __str__(self):
        return '%s-%s %s'%(self.id, self.first_name, self.last_name)

    def name(self):
        return '%s %s'%(self.first_name, self.last_name)

    class Meta:
        ordering = ["id"]


class EmployeeTitle(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


@receiver(post_save, sender=EmployeeTitle)
def change_title(sender, instance, **kwargs):
    employee = Employee.objects.get(pk=instance.employee.id)
    employee.save()


class EmployeeOffice(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    office = models.ForeignKey(Office, on_delete=models.CASCADE)


@receiver(post_save, sender=EmployeeOffice)
def change_office(sender, instance, **kwargs):
    employee = Employee.objects.get(pk=instance.employee.id)
    employee.save()
