from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
import json
from django.db.models import Count, F, Sum, Q
import re
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=150, default=None, null=True, blank=True)
    affichage=models.CharField(max_length=150, default=None, null=True, blank=True)
    code=models.CharField(max_length=150, default=None, null=True)
    masqueclients=models.BooleanField(default=False)
    excludedrep=models.ManyToManyField('Represent', default=None, blank=True)
    image=models.ImageField(upload_to='categories_images/', null=True, blank=True)
    def __str__(self) -> str:
        return self.name




class Mark(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='marques_images/', null=True, blank=True, default=None)
    masqueclients=models.BooleanField(default=False)
    excludedrep=models.ManyToManyField('Represent', default=None, blank=True)
    def __str__(self) -> str:
        return self.name


class Carlogos(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='carlogos_images/', null=True, blank=True, default=None)
    def __str__(self) -> str:
        return self.name


class Produit(models.Model):
    name=models.CharField(max_length=500, null=True)
    block=models.CharField(max_length=500, null=True, default=None)
    # code = classement
    code=models.CharField(max_length=500, null=True)
    #this iniqcide will be used to match local products with server products
    uniqcode=models.CharField(max_length=500, null=True)
    coderef=models.CharField(max_length=500, null=True, default=None)
    #price
    buyprice= models.FloatField(default=None, null=True, blank=True)
    supplier=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='supplier')
    sellprice=models.FloatField(default=None, null=True, blank=True)
    sellpricebrut=models.FloatField(default=None, null=True, blank=True)
    coutmoyen=models.FloatField(default=None, null=True, blank=True)
    remise=models.IntegerField(default=0, null=True, blank=True)
    #checkprice= models.FloatField(default=None, null=True, blank=True)
    prixnet=models.FloatField(default=None, null=True, blank=True)
    devise=models.FloatField(default=None, null=True, blank=True)
    representprice=models.FloatField(default=None, null=True, blank=True)
    representremise=models.FloatField(default=0, null=True, blank=True)
    lastsellprice=models.FloatField(default=None, null=True, blank=True)
    #stock
    refeq1=models.CharField(max_length=500, default=None, null=True, blank=True)
    refeq2=models.CharField(max_length=500, default=None, null=True, blank=True)
    refeq3=models.CharField(max_length=500, default=None, null=True, blank=True)
    refeq4=models.CharField(max_length=500, default=None, null=True, blank=True)
    stockprincipal=models.IntegerField(default=None, null=True, blank=True)
    stockdepot=models.IntegerField(default=None, null=True, blank=True)
    stocktotal=models.IntegerField(default=None, null=True, blank=True)
    stockinitial=models.IntegerField(default=0, null=True, blank=True)
    stockfacture=models.IntegerField(default=0, null=True, blank=True)
    stockbon=models.IntegerField(default=None, null=True, blank=True)
    # stock=models.BooleanField(default=True)
    # add equivalent in refs
    equivalent=models.TextField(default=None, null=True, blank=True)
    famille=models.CharField(max_length=500, default=None, null=True, blank=True)
    cars=models.TextField(default=None, null=True, blank=True)
    #ref
    newfob=models.FloatField(default=0, null=True, blank=True)
    ref=models.CharField(max_length=50)
    diametre=models.CharField(max_length=500, default=None, null=True, blank=True)

    # reps that will have the price applied
    repsprice=models.CharField(max_length=500, default=None, null=True, blank=True)
    #image
    image = models.ImageField(upload_to='products_imags/', null=True, blank=True)
    mark=models.ForeignKey(Mark, on_delete=models.CASCADE, default=None, null=True, blank=True)
    #cartgrise
    # n_chasis=models.CharField(max_length=50, null=True)
    # minstock is used to indicate the quantity being shipped now
    minstock=models.IntegerField(default=None, null=True, blank=True)
    carlogos=models.ManyToManyField(Carlogos, default=None, blank=True)
    # min cmmand
    isnew=models.BooleanField(default=False)
    # use min to indicate the quantity commandé
    min=models.IntegerField(default=1, null=True, blank=True)
    qtycommande=models.IntegerField(default=0, null=True, blank=True)
    isoffer=models.BooleanField(default=False)
    offre=models.CharField(max_length=500, default=None, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, default=None, null=True, blank=True)
    isactive=models.BooleanField(default=True)
    # commande
    iscommanded=models.BooleanField(default=False)
    suppliercommand=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='suppliercommand')
    near=models.BooleanField(default=False)
    # adashi code is the exact code, eq is equivalent update1: adashi code will be used as the categry holder (assambly)
    adashicode=models.CharField(max_length=500, default=None, null=True, blank=True)
    adashieq=models.CharField(max_length=500, default=None, null=True, blank=True)
    # stock facture
    # stock bon
    def __str__(self) -> str:
        return self.ref
    def code_sort_key(self):
        # Custom sorting key function
        parts = [part.isdigit() and int(part) or part for part in re.split(r'(\d+)', self.code)]
        return parts
    def totalofstock(self):
        return 0 if self.ref=='divers' else self.stocktotal*self.buyprice

    def getprofit(self):
        try:
            # prix vente net - cout moyen
            # use Stockin model to get total quantity entered of this product
            entered=Stockin.objects.filter(product=self).aggregate(Sum('quantity'))['quantity__sum']
            cost=round(entered*self.coutmoyen,2)
            # use Orderitem model to get total quantity sold of this product
            sold=Livraisonitem.objects.filter(product=self).aggregate(Sum('total'))['total__sum']
            return round(sold-cost, 2)
        except:
            return 'NO DATA'
    def getpercentage(self):
        try:
            return 100*(self.prixnet-self.buyprice)/self.prixnet
        except:
            return 0
    def getequivalent(self):
        if self.equivalent:
            if '+' in self.equivalent:
                return self.equivalent.split('+')+['-', '-']
            return [self.equivalent, '-', '-']
    def getcommercialsprice(self):
        try:
            return json.loads(self.repsprice)
        except:
            return []

    def getcars(self):
        try:
            return self.cars.split(',')
        except:
            return []
    # brand=models.CharField(max_length=25, default=None)
    # model=models.CharField(max_length=25, default=None)
    # mark=models.CharField(max_length=25, default=None)

# cupppon codes table
class YearEndStock(models.Model):
    product = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="year_end_stocks")
    ref=models.CharField(max_length=500, null=True)
    stocktotal = models.IntegerField(default=0, null=True, blank=True)
    stockfacture = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField()
    name=models.CharField(max_length=500, null=True)
    # code = classement
    #price
    buyprice= models.FloatField(default=None, null=True, blank=True)
    supplier=models.CharField(max_length=500, null=True)
    sellprice=models.FloatField(default=None, null=True, blank=True)
    sellpricebrut=models.FloatField(default=None, null=True, blank=True)
    coutmoyen=models.FloatField(default=None, null=True, blank=True)
    remise=models.IntegerField(default=0, null=True, blank=True)
    #checkprice= models.FloatField(default=None, null=True, blank=True)
    prixnet=models.FloatField(default=None, null=True, blank=True)
    devise=models.FloatField(default=None, null=True, blank=True)
class Damagedproducts(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True, blank=True)
    qty=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)


class Attribute(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=50)


class Supplier(models.Model):
    name=models.CharField(max_length=500)
    address=models.CharField(max_length=500, default=None, null=True, blank=True)
    phone=models.CharField(max_length=500, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    def __str__(self) -> str:
        return self.name



class Itemsbysupplier(models.Model):
    #is manual will indicate if this bon achat is manual
    ismanual=models.BooleanField(default=False)
    supplier= models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='provider')
    date = models.DateTimeField(default=None)
    #date saisie
    dateentree=models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    items = models.TextField(blank=True, null=True, help_text='Quantity and Product name would save in JSON format')
    total = models.FloatField(default=0.00)
    tva = models.FloatField(default=0.00, null=True, blank=True)
    rest = models.FloatField(default=0.00)
    nbon = models.CharField(max_length=100, blank=True, null=True)
    ispaid=models.BooleanField(default=False)
    isfacture=models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.nbon} - {self.id}'

class Stockin(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    date=models.DateField()
    quantity=models.IntegerField()
    ref=models.CharField(max_length=500, default=None, null=True, blank=True)
    name=models.CharField(max_length=500, default=None, null=True, blank=True)
    price=models.FloatField(default=0.00)
    devise=models.FloatField(default=0.00)
    # to delete stock facture is stock in is facture
    facture=models.BooleanField(default=False)
    # to track ligns that will be inventaire (stock stsem 8 stock reel 10, 2 is difference, 2 needs to be inventaire here adkchmnt 4stock s stockin line)
    isinventaire=models.BooleanField(default=False)
    # qtyofprice will be used to track qty of this price
    qtyofprice=models.IntegerField(default=0)
    remise=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    nbon=models.ForeignKey(Itemsbysupplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    isavoir=models.BooleanField(default=False)
    avoir=models.ForeignKey('Avoirclient', on_delete=models.CASCADE, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.nbon} - {self.product}'
class Pricehistory(models.Model):
    date=models.DateField()
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    price=models.FloatField()

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()

class Region(models.Model):
    name=models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.name
# can command
class Client(models.Model):
    represent=models.ForeignKey('Represent', on_delete=models.CASCADE, default=None, null=True, related_name="repclient")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True)
    moderegl=models.CharField(max_length=200, default=0, null=True, blank=True)
    name=models.CharField(max_length=200)
    clientname=models.CharField(max_length=200, null=True, default=None, blank=True)
    code=models.CharField(max_length=200, null=True, default=None)
    ice=models.CharField(max_length=200, null=True, default=None)
    city=models.CharField(max_length=200, null=True, default=None)
    region=models.CharField(max_length=200, null=True, default=None)
    total=models.FloatField(default=0.00, null=True, blank=True)
    soldtotal=models.FloatField(default=0.00, null=True, blank=True)
    soldbl=models.FloatField(default=0.00, null=True, blank=True)
    soldfacture=models.FloatField(default=0.00, null=True, blank=True)
    address=models.CharField(max_length=200)
    location=models.TextField(default='', null=True, blank=True)
    phone=models.CharField(max_length=200, default=None, null=True)
    phone2=models.CharField(max_length=200, default=None, null=True)
    diver=models.BooleanField(default=False)
    accesscatalog=models.BooleanField(default=False)
    @property
    def mehtodsoldbl(self):
        norangeavoirsbl=round(Avoirclient.objects.filter(client=self, avoirfacture=False).aggregate(Sum('total'))['total__sum'] or 0, 2)
        norangereglementsbl=round(PaymentClientbl.objects.filter(client=self).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        norangebons=round(Bonlivraison.objects.filter(client=self, total__gt=0).aggregate(Sum('total'))['total__sum'] or 0, 2)
        soldbbb=round(norangebons-norangereglementsbl-norangeavoirsbl, 2)
        # self.doldbl=soldbbb
        # self.save()
        return soldbbb
    @property
    def methodsoldfc(self):
        norangeavoirsfc=round(Avoirclient.objects.filter(client=self, avoirfacture=True).aggregate(Sum('total'))['total__sum'] or 0, 2)

        norangereglementsfc=round(PaymentClientfc.objects.filter(client=self).aggregate(Sum('amount'))['amount__sum'] or 0, 2)

        norangefactures=round(Facture.objects.filter(client=self).aggregate(Sum('total'))['total__sum'] or 0, 2)
        soldfff=round(norangefactures-norangereglementsfc-norangeavoirsfc, 2)
        # Update the soldfacture field and save the instance
        # self.soldfacture = soldfff
        # self.save()  # This will save the updated value to the database

        return soldfff


    def __str__(self) -> str:
        return self.name+'-'+str(self.city)

class Represent(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True)
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50, default=None, null=True)
    phone2=models.CharField(max_length=50, default=None, null=True)
    region=models.CharField(max_length=100, default=None, null=True)
    image = models.ImageField(upload_to='slasemen_imags/', null=True, blank=True)
    caneditprice=models.BooleanField(default=False)
    info=models.TextField(default=None, null=True, blank=True)
    # wether the products will be displaied in owlcarousel or not
    slides=models.BooleanField(default=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, related_name='working_client')
    def __str__(self) -> str:
        return self.name

# orders table
class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    code=models.CharField(max_length=50, null=True, default=None)

    # name will be a string
    # email will be a string and not requuired
    salseman=models.ForeignKey(Represent, on_delete=models.SET_NULL, default=None, null=True)
    modpymnt=models.CharField(max_length=50, null=True, default=None)
    modlvrsn=models.CharField(max_length=50, null=True, default=None)
    note=models.TextField(default=None, null=True, blank=True)
    total=models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    # totalremise will be there i ncase pymny is cash
    totalremise=models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    # true if its generated to be a bon livraison
    isdelivered = models.BooleanField(default=False)
    ispaied = models.BooleanField(default=False)
    isclientcommnd = models.BooleanField(default=False)
    clientname=models.CharField(max_length=500, null=True, default=None)
    clientphone=models.CharField(max_length=500, null=True, default=None)
    clientaddress=models.CharField(max_length=500, null=True, default=None)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True)
    order_no=models.CharField(max_length=500, null=True, default=None)
    senttoserver=models.BooleanField(default=False)

    # order by date
    class Meta:
        ordering = ['-date']
    # return the name and phone

    # methode to determine wether it's delivered or not
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)  #
    def __str__(self) -> str:
        return self.client.name+' '+str(self.total)

class Bonlivraison(models.Model):
    iscontre=models.BooleanField(default=False)
    paymenttype=models.CharField(max_length=50, null=True, default='simple')
    commande=models.ForeignKey(Order, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    salseman=models.ForeignKey(Represent, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    modlvrsn=models.CharField(max_length=50, null=True, default=None)
    code=models.CharField(max_length=50, null=True, default=None)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    # true when the bon is generated to be a facture
    isfacture=models.BooleanField(default=False)
    # true when the bon is DELIVERED
    isdelivered=models.BooleanField(default=False)
    # true when its paid
    ispaid=models.BooleanField(default=False)
    note=models.TextField(default=None, null=True, blank=True)
    #statud if regl == r0
    statusreg=models.CharField(max_length=50, null=True, default='n1', blank=True)
    #statud if factur == f1
    statusfc=models.CharField(max_length=50, null=True, default='b1', blank=True)
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.bon_no

class Facture(models.Model):
    #hascopy means there is a copy
    iscontre=models.BooleanField(default=False)
    hascopy=models.BooleanField(default=False)
    copynumber=models.CharField(max_length=50, null=True, default=None)
    bon=models.ForeignKey(Bonlivraison, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    code=models.CharField(max_length=50, null=True, default=None)
    total=models.FloatField(default=0.00)
    tva=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    ispaid=models.BooleanField(default=False)
    facture_no=models.CharField(max_length=50, null=True, default=None)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True)
    salseman=models.ForeignKey(Represent, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    # notes of fc
    transport=models.CharField(max_length=500, null=True, default=None)
    # printed indicates that this facture was received by the client
    printed = models.BooleanField(default=False)
    note=models.TextField(default=None, null=True, blank=True)
    # true if facture is accounting
    isaccount=models.BooleanField(default=False)
    statusreg=models.CharField(max_length=50, null=True, default='b1', blank=True)
    def getreglement(self):
        regls=self.reglementsfc.all()
        text=""
        for i in regls:
            text+=f'{i.mode} {i.amount} '
        return text
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.facture_no


class PaymentSupplier(models.Model):
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=None)
    amount = models.FloatField(default=0.00)
    mode=models.CharField(max_length=10, default=None)
    echeance=models.DateField(default=None, null=True, blank=True)
    #factures reglé onetomanys
    bons=models.ManyToManyField(Itemsbysupplier, default=None, blank=True, related_name="reglementssupp")
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)

class Notesrepresentant(models.Model):
    represent=models.ForeignKey('Represent', on_delete=models.SET_NULL, default=None, null=True)
    note=models.TextField()
    def __str__(self) -> str:
        return self.represent.name




class PaymentClientbl(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    date = models.DateTimeField(default=None)
    amount = models.FloatField(default=0.00)
    mode=models.CharField(max_length=10, default=None)
    amountofeachbon=models.CharField(max_length=100000, default=None, null=True, blank=True)
    bons=models.ManyToManyField(Bonlivraison, default=None, blank=True, related_name="reglements")
    # mode: 0 bl, 1 facture
    echance=models.DateField(default=None, null=True, blank=True)
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    # if the regelement is used to regle facture
    usedinfacture=models.BooleanField(default=False)
    # if regl is paid if it has echeaance
    ispaid=models.BooleanField(default=False)
    #refused means impyé
    refused=models.BooleanField(default=False)

class Bonsregle(models.Model):
    payment=models.ForeignKey(PaymentClientbl, on_delete=models.CASCADE, default=None, null=True, blank=True)
    bon=models.ForeignKey('Bonlivraison', on_delete=models.CASCADE, default=None, null=True, blank=True)
    amount=models.FloatField(default=0.00)



class PaymentClientfc(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    date = models.DateTimeField(default=None)
    amount = models.FloatField(default=0.00)
    tva = models.FloatField(default=0.00)
    mode=models.CharField(max_length=10, default=None)
    factures=models.ManyToManyField(Facture, default=None, blank=True, related_name='reglementsfc')
    # mode: 0 bl, 1 facture
    echance=models.DateField(default=None, null=True, blank=True)
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    # if regl is paid if it has echeaance
    ispaid=models.BooleanField(default=False)
    #refused means impyé
    refused=models.BooleanField(default=False)

class Facturesregle(models.Model):
    payment=models.ForeignKey(PaymentClientfc, on_delete=models.CASCADE, default=None, null=True, blank=True)
    bon=models.ForeignKey(Facture, on_delete=models.CASCADE, default=None, null=True, blank=True)
    amount=models.FloatField(default=0.00)




# price of each product for each salesman
class Salesprice(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    price=models.FloatField()
    salesman=models.ForeignKey(Represent, on_delete=models.CASCADE, default=None)
    date=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.product.ref+'-'+self.id



# signal to set order_no when order is created to be in this format '23-09-00001'

@receiver(post_save, sender=Order)
def set_order_no(sender, instance, created, **kwargs):
    year_month = timezone.now().strftime("%y%m")

    if created:
        instance.order_no = f'{year_month}-{str(instance.id)}'
        instance.save()





# this class is the equivalnt of stockouts for each product
class Orderitem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, default=None, null=True, blank=True)
    bonlivraison=models.ForeignKey('Bonlivraison', on_delete=models.CASCADE, default=None, null=True, blank=True)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    local=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    # this total represents the revenue of this product
    total=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    date=models.DateTimeField(default=datetime.datetime.now, blank=True)
    outprincipal=models.IntegerField(default=0)
    outdepot=models.IntegerField(default=0)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    clientprice=models.FloatField(default=0.00)
    islivraison=models.BooleanField(default=False, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.order} - {self.product.ref}'
class Shippingfees(models.Model):
    city=models.CharField(max_length=20)
    shippingfee=models.FloatField()
    def __str__(self) -> str:
        return f'{self.city} - {self.shippingfee}'




class Pairingcode(models.Model):
    code = models.CharField(max_length=50)
    amount = models.FloatField()




# this class is used to track client prices to be used in bon livraison, last proce the client bought the product with
class Clientprices(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    price=models.FloatField()
    date=models.DateField(auto_now_add=True)




class Outfacture(models.Model):
    facture=models.ForeignKey(Facture, on_delete=models.CASCADE, default=None)
    total=models.FloatField(default=0.00)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    # this total represents the revenue of this product
    price=models.FloatField(default=0.00)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    date=models.DateField(default=None, blank=True, null=True)
    def __str__(self) -> str:
        return self.facture.facture_no
class Livraisonitem(models.Model):
    bon=models.ForeignKey(Bonlivraison, on_delete=models.CASCADE, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    # this total represents the revenue of this product
    price=models.FloatField(default=0.00)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)

    # to track ligns that are generated to facture
    isfacture=models.BooleanField(default=False)
    # to track ligns that will be inventaire (stock stsem 10 stock reel 8, 2 is difference, 2 needs to be inventaire here adfo4nt 4stock)
    isinventaire=models.BooleanField(default=False)
    isavoir=models.BooleanField(default=False)
    clientprice=models.FloatField(default=0.00)
    date=models.DateField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return f' {self.product.ref}'


class Avoirclient(models.Model):
    date=models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    no = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )

    client = models.ForeignKey(
        Client,
        related_name='customer_avoir',
        blank=True, null=True,on_delete=models.CASCADE
    )
    representant= models.ForeignKey(Represent, on_delete=models.CASCADE, default=None, null=True)
    returneditems = models.ManyToManyField(
        'Returned',
        related_name='returned',
        max_length=100, blank=True, default=None
    )
    total = models.FloatField(default=0, blank=True, null=True)
    avoirbl=models.BooleanField(default=False)
    avoirfacture=models.BooleanField(default=False)
    avoirsystem=models.BooleanField(default=True)
    note=models.TextField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.no


class Returned(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    # ref of the article, cause it can be modified
    ref=models.CharField(max_length=500, default='-', null=True, blank=True)
    source=models.CharField(max_length=500, default='', null=True, blank=True)
    # name of the article, cause it can be modified
    name=models.TextField(default='-', null=True, blank=True)
    qty=models.IntegerField()
    remise=models.IntegerField(null=True, blank=True, default=None)
    total=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    avoir=models.ForeignKey(Avoirclient, related_name='returned_invoice', on_delete=models.CASCADE, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.avoir.no

class Avoirsupplier(models.Model):
    date=models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    no = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )

    supplier = models.ForeignKey(
        Supplier,
        related_name='supplier_avoir',
        blank=True, null=True,on_delete=models.CASCADE
    )
    returneditems = models.ManyToManyField(
        'Returnedsupplier',
        related_name='returned_supplier',
        max_length=100, blank=True, default=None
    )
    total = models.FloatField(default=0, blank=True, null=True)
    avoirbl=models.BooleanField(default=False)
    avoirfacture=models.BooleanField(default=False)

class Returnedsupplier(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    # ref of the article, cause it can be modified
    ref=models.CharField(max_length=500, default='-', null=True, blank=True)
    # name of the article, cause it can be modified
    name=models.TextField(default='-', null=True, blank=True)
    qty=models.IntegerField()
    total=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    remise=models.IntegerField(null=True, blank=True, default=None)
    avoir=models.ForeignKey(Avoirsupplier, related_name='avoir_supplier', on_delete=models.CASCADE, default=None, null=True, blank=True)


class Ordersnotif(models.Model):
    length=models.IntegerField(default=0)
    # catch the orders json from server
    orders=models.JSONField(default=list, null=True, blank=True)
    isread=models.BooleanField(default=False)

class Connectedusers(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    activity=models.CharField(max_length=500, default=None, null=True, blank=True)
    lasttime=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.user.username

# this class model for images carousel in catalog
class Promotion(models.Model):
    image=models.ImageField(upload_to='categories_images/', null=True, blank=True)
    info=models.CharField(max_length=500, default=None, null=True, blank=True)

class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username
# his will be refs that clients searched for
class Refstats(models.Model):
    ref=models.CharField(max_length=500, default=None, null=True, blank=True)
    times=models.IntegerField(default=1)
    lastdate=models.DateField(auto_now_add=True, blank=True, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    def __str__(self) -> str:
        if self.user:
            return self.user.username
        return '--'

class Notavailable(models.Model):
    ref=models.CharField(max_length=500, default=None, null=True, blank=True)
    name=models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='products_imags/', null=True, blank=True)
    sellprice=models.FloatField(default=0.00, null=True, blank=True)
    mark=models.ForeignKey(Mark, on_delete=models.CASCADE, default=None, null=True, blank=True)
    equiv=models.TextField(null=True, blank=True, default=None)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total=models.FloatField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        if self.user:
            return self.user.username+' '+str(self.total)
        return '--'
class Cartitems(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, default=None, null=True, blank=True)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    qty=models.IntegerField(default=None, null=True, blank=True)
    total=models.FloatField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.product.ref

class Repcart(models.Model):
    rep=models.ForeignKey(Represent, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.rep.name+' '+str(self.client.name)+' '+str(self.total)

class Repcartitem(models.Model):
    repcart=models.ForeignKey(Repcart, on_delete=models.CASCADE, default=None, null=True, blank=True)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    qty=models.IntegerField(default=None, null=True, blank=True)
    total=models.FloatField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.product.ref

class Wich(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total=models.FloatField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        if self.user:
            return self.user.username
#Wishlist items
class Wishlist(models.Model):
    wich=models.ForeignKey(Wich, on_delete=models.CASCADE, default=None, null=True, blank=True)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    qty=models.IntegerField(default=None, null=True, blank=True)
    total=models.FloatField(default=None, null=True, blank=True)

class Notification(models.Model):
        notification=models.TextField()

class Modifierstock(models.Model):
    date=models.DateField(auto_now_add=True)
    product=models.ForeignKey(Produit, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    stock=models.IntegerField(default=0)
    stockfc=models.BooleanField(default=False)

class Achathistory(models.Model):
    date=models.DateField()
    fournisseur=models.TextField()
    designation=models.TextField()
    ref=models.TextField()
    famille=models.TextField()
    quantity=models.IntegerField()
    prixunitaire=models.TextField()
    mantant=models.TextField()
    devise=models.TextField()
    total=models.FloatField(default=0.00)

class Excelecheances(models.Model):
    #month should be 09/2024
    month=models.CharField(max_length=500, default=None, null=True, blank=True)
    npiece=models.CharField(max_length=500, default=None, null=True, blank=True)
    mode=models.CharField(max_length=500, default=None, null=True, blank=True)
    echeance=models.CharField(max_length=500, default=None, null=True, blank=True)
    # note xill hold anything
    note=models.TextField(max_length=500, default=None, null=True, blank=True)
    client=models.CharField(max_length=500, default=None, null=True, blank=True)
    clientcode=models.CharField(max_length=500, default=None, null=True, blank=True)
    factures=models.TextField(default=None, null=True, blank=True)
    # id is enough # no id is not enqugh cause id cannot be shared between multiple records (2)
    # code is for grouping the lines that will have a total (multiple payments in one total, you whould know which by this code, after user selects the lines that will be grouped in the same total) (1)
    code=models.CharField(max_length=500, default=None, null=True, blank=True)
    ispaid=models.BooleanField(default=False)
    isimpye=models.BooleanField(default=False)
    # it its printed in papres
    isprinted=models.BooleanField(default=False)
    # this will be used to track the factures that exist already before
    iscontable=models.BooleanField(default=False)
    # is empty if npiece has no factures, just got added manually
    isempty=models.BooleanField(default=False)
    #if factures are pointage (zrint 4 lpointaaaage)
    ispointage=models.BooleanField(default=False)
    grandtotal=models.FloatField(default=None, null=True, blank=True)
    amount=models.FloatField(default=None, null=True, blank=True)
    tva=models.FloatField(default=None, null=True, blank=True)
    # if factures in factre input are account (comptabilisé)
    facturesaccount=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.month if self.month else '--'

class Tva(models.Model):
    #month should be 09/2024
    month=models.CharField(max_length=500, default=None, null=True, blank=True)
    tvavente=models.FloatField(max_length=500, default=None, null=True, blank=True)
    tvaachat=models.FloatField(max_length=500, default=None, null=True, blank=True)
    # report means the amount paid
    report=models.FloatField(default=0.00, null=True, blank=True)
    rest=models.FloatField(default=0.00, null=True, blank=True)
    restandtva=models.FloatField(default=0.00, null=True, blank=True)

    # othertva will hold the real tva achat after substracting (-net)
    othertvaachat=models.FloatField(max_length=500, default=None, null=True, blank=True)
    # achat details will hold the tva achat entered
    achatdetails=models.TextField(default=None, null=True, blank=True)
    net=models.FloatField(max_length=500, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.month

class Etude(models.Model):
    facture_no=models.CharField(max_length=500, default=None, null=True, blank=True)
    # created at will be date saisie
    created_at=models.DateField(auto_now_add=True)
    # date will be facture date
    date=models.DateField(default=None, null=True, blank=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    #facturedevise iga facture s $
    facturedevise=models.FloatField()
    tauxChange=models.CharField(max_length=500)
    facturedh=models.FloatField()
    # chargeandfacture will hold charges+facture
    chargeandfacture=models.FloatField(default=0.00, null=True, blank=True)
    cfr=models.FloatField(default=0.00, null=True, blank=True)
    transportInternational=models.FloatField(default=0.00, null=True, blank=True)
    dounane=models.FloatField(default=0.00, null=True, blank=True)
    magazinage=models.FloatField(default=0.00, null=True, blank=True)
    surrestaries=models.FloatField(default=0.00, null=True, blank=True)
    transportCamion=models.FloatField(default=0.00, null=True, blank=True)
    transitaire=models.FloatField(default=0.00, null=True, blank=True)
    autre1=models.FloatField(default=0.00, null=True, blank=True)
    autre2=models.FloatField(default=0.00, null=True, blank=True)
    totalCharges=models.FloatField(default=0.00, null=True, blank=True)
    tauxCharge=models.FloatField(default=0.00, null=True, blank=True)
    # pattc * qty
    pattcQty=models.FloatField(default=0.00, null=True, blank=True)
    tdt=models.FloatField(default=0.00, null=True, blank=True)
    tcharge=models.FloatField(default=0.00, null=True, blank=True)

class EtudeItem(models.Model):
    etude=models.ForeignKey(Etude, on_delete=models.CASCADE)
    ref=models.CharField(max_length=500, default='--', null=True, blank=True)
    name=models.CharField(max_length=1500, default='--', null=True, blank=True)
    qty=models.CharField(max_length=500, default='--', null=True, blank=True)
    devise=models.CharField(max_length=500, default='--', null=True, blank=True)
    amount=models.CharField(max_length=500, default='--', null=True, blank=True)
    dh=models.CharField(max_length=500, default='--', null=True, blank=True)
    hs=models.CharField(max_length=500, default='--', null=True, blank=True)
    dt=models.CharField(max_length=500, default='--', null=True, blank=True)
    pattc=models.CharField(max_length=500, default='--', null=True, blank=True)
    paht=models.CharField(max_length=500, default='--', null=True, blank=True)
    coeff=models.CharField(max_length=500, default='--', null=True, blank=True)
    pbrut=models.CharField(max_length=500, default='--', null=True, blank=True)
    pnet=models.CharField(max_length=500, default='--', null=True, blank=True)
    marge=models.CharField(max_length=500, default='--', null=True, blank=True)
    tdt=models.CharField(max_length=500, default='--', null=True, blank=True)
    tcharges=models.CharField(max_length=500, default='--', null=True, blank=True)

class Setting(models.Model):
    name=models.CharField(max_length=500, default=None, null=True, blank=True)
    ice=models.CharField(max_length=500, default=None, null=True, blank=True)
    rc=models.CharField(max_length=500, default=None, null=True, blank=True)
    idfiscal=models.CharField(max_length=500, default=None, null=True, blank=True)
    cnss=models.CharField(max_length=500, default=None, null=True, blank=True)
    address=models.CharField(max_length=500, default=None, null=True, blank=True)
    phone=models.CharField(max_length=500, default=None, null=True, blank=True)
    fix=models.CharField(max_length=500, default=None, null=True, blank=True)
    # patente
    pt=models.CharField(max_length=500, default=None, null=True, blank=True)
    serverip=models.CharField(max_length=500, default=None, null=True, blank=True)
    logo=models.ImageField(upload_to='logos/', null=True, blank=True)
    logoheadfacture=models.ImageField(upload_to='logos/', null=True, blank=True)
    logobodyfacture=models.ImageField(upload_to='logos/', null=True, blank=True)

# charge turne, eqch ture of representant has charges that need to be stored
class Chargeturne(models.Model):
    represent = models.ForeignKey('Represent', on_delete=models.CASCADE, default=None, null=True)
    startdate = models.DateField(default=None)
    enddate = models.DateField(default=None)
    charge = models.FloatField()