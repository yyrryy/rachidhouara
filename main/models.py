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



class Caisse(models.Model):
    # this will hold the initial amount of the caisse
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)
    amountinitial=models.FloatField(default=0.00)
    amount=models.FloatField(default=0.00)
    target=models.CharField(max_length=500, default=None, null=True)
# model of money out
class Outcaisse(models.Model):
    date=models.DateField(auto_now_add=True)
    amount=models.FloatField()
    note=models.TextField(default=None, null=True, blank=True)

class Incaisse(models.Model):
    date=models.DateField(auto_now_add=True)
    amount=models.FloatField()
    note=models.TextField(default=None, null=True, blank=True)

class Produit(models.Model):
    # stockinventqire used to know how much qty in bon inventaire #RFF3
    #inventaire in is what needs to be added by inventaire
    #inventaire out is what needs to be out by inventaire
    inventaireinfarah=models.FloatField(default=None, null=True, blank=True)
    inventaireoutfarah=models.FloatField(default=None, null=True, blank=True)
    inventaireinorgh=models.FloatField(default=None, null=True, blank=True)
    inventaireoutorgh=models.FloatField(default=None, null=True, blank=True)
    # negative stock
    replacedby=models.ForeignKey("Produit", on_delete=models.SET_NULL, default=None, null=True, blank=True)
    isnegativeinfr=models.BooleanField(default=False)
    isnegative=models.BooleanField(default=False)
    frnegative=models.TextField(default='[]')
    # sortie items where there is negative
    frsorties=models.TextField(default='[]')
    # negative stock
    negative=models.TextField(default='[]')
    # sortie items where there is negative
    sorties=models.TextField(default='[]')
    #samethis in livraion
    frnegativeliv=models.TextField(default='[]')
    # sortie items where there is negative
    frliv=models.TextField(default='[]')
    # negative stock
    negativeliv=models.TextField(default='[]')
    # sortie items where there is negative
    liv=models.TextField(default='[]')
    # quantity of product in jeu (2, 4)
    qtyjeu=models.IntegerField(default=0, null=True, blank=True)
    name=models.CharField(max_length=500, null=True)
    block=models.CharField(max_length=500, null=True, default=None)
    unite=models.CharField(max_length=500, null=True, default=None)
    # code = classement
    code=models.CharField(max_length=500, null=True)
    coderef=models.CharField(max_length=500, null=True, default=None)
    #price
    buyprice= models.FloatField(default=0.0, null=True, blank=True)
    remise1= models.FloatField(default=0.0, null=True, blank=True)
    remise2= models.FloatField(default=0.0, null=True, blank=True)
    remise3= models.FloatField(default=0.0, null=True, blank=True)
    remise4= models.FloatField(default=0.0, null=True, blank=True)
    netbuyprice= models.FloatField(default=0.0, null=True, blank=True)

    frbuyprice= models.FloatField(default=0.0, null=True, blank=True)
    frremise1= models.FloatField(default=0.0, null=True, blank=True)
    frremise2= models.FloatField(default=0.0, null=True, blank=True)
    frremise3= models.FloatField(default=0.0, null=True, blank=True)
    frremise4= models.FloatField(default=0.0, null=True, blank=True)
    frnetbuyprice= models.FloatField(default=0.0, null=True, blank=True)
    sellpricebrut=models.FloatField(default=0.0, null=True, blank=True)
    supplier=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='supplier')
    coutmoyen=models.FloatField(default=0.0, null=True, blank=True)
    frcoutmoyen=models.FloatField(default=0.0, null=True, blank=True)
    sellprice=models.FloatField(default=0.0, null=True, blank=True)
    remisesell=models.FloatField(default=0.0, null=True, blank=True)
    frsellprice=models.FloatField(default=0.0, null=True, blank=True)
    frremisesell=models.FloatField(default=0.0, null=True, blank=True)
    frstockinitial=models.IntegerField(default=0, null=True, blank=True)
    frpriceinitial=models.FloatField(default=0.0, null=True, blank=True)
    stockinitial=models.IntegerField(default=0, null=True, blank=True)
    priceinitial=models.FloatField(default=0.0, null=True, blank=True)
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
    stocktotalfarah=models.FloatField(default=0.0, null=True, blank=True)
    stockfacturefarah=models.FloatField(default=0.0, null=True, blank=True)
    stocktotalorgh=models.FloatField(default=0.0, null=True, blank=True)
    stockfactureorgh=models.FloatField(default=0.0, null=True, blank=True)
    stockbon=models.IntegerField(default=None, null=True, blank=True)
    # check if product is farah product
    farahproduct=models.BooleanField(default=False)
    orghproduct=models.BooleanField(default=False)
    farahref=models.CharField(max_length=500, default=None, null=True, blank=True)
    orghref=models.CharField(max_length=500, default=None, null=True, blank=True)
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
    carlogos=models.ForeignKey(Carlogos, default=None, blank=True, null=True, on_delete=models.CASCADE)
    # min cmmand
    isnew=models.BooleanField(default=False)
    # use min to indicate the quantity commandé
    min=models.IntegerField(default=1, null=True, blank=True)
    qtycommande=models.FloatField(default=0, null=True, blank=True)
    frqtycommande=models.FloatField(default=0, null=True, blank=True)
    isoffer=models.BooleanField(default=False)
    offre=models.CharField(max_length=500, default=None, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, default=None, null=True, blank=True)
    isactive=models.BooleanField(default=True)
    # commande
    iscommanded=models.BooleanField(default=False)
    suppliercommand=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='suppliercommand')
    friscommanded=models.BooleanField(default=False)
    frsuppliercommand=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='farahsuppliercommand')
    originsupp=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='lastsupplier')
    froriginsupp=models.ForeignKey('Supplier', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='farahlastsupplier')
    near=models.BooleanField(default=False)
    # stock facture
    # stock bon
    def __str__(self) -> str:
        return self.ref
    def code_sort_key(self):
        # Custom sorting key function
        parts = [part.isdigit() and int(part) or part for part in re.split(r'(\d+)', self.code)]
        return parts

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
    def frgetpercentage(self):
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
            return json.loads(self.cars)
        except:
            return []
    # brand=models.CharField(max_length=25, default=None)
    # model=models.CharField(max_length=25, default=None)
    # mark=models.CharField(max_length=25, default=None)
    def qtyachat(self):
        achats=Stockin.objects.filter(product=self, isavoir=False, isfarah=False).aggregate(Sum('quantity'))['quantity__sum'] or 0
        return achats
    def avoirachat(self):
        return Returnedsupplier.objects.filter(product=self, isfarah=False).aggregate(Sum('qty'))['qty__sum'] or 0
    def qtyventes(self):
        return Livraisonitem.objects.filter(product=self, bon__isfarah=False).aggregate(Sum('qty'))['qty__sum'] or 0
    def avoirventes(self):
            return Stockin.objects.filter(
                avoir__isnull=False,
                isorgh=True
            ).aggregate(Sum('quantity'))['quantity__sum']
    def coutmoyenorgh(self):
        stock = self.stocktotalorgh
        if stock <= 0:
            return 0
        entries = (
            Stockin.objects
            .filter(
                product=self,
                isfarah=False,
                issortie=False,
                isavoir=False
            )
            .order_by('-date', '-id')
        )
        remaining = stock
        total_cost = 0.0
        total_qty = 0.0

        for entry in entries:
            if remaining <= 0:
                break

            available_qty = entry.quantity
            if available_qty <= 0:
                continue

            take_qty = min(available_qty, remaining)

            total_cost += take_qty * entry.net
            total_qty += take_qty
            remaining -= take_qty
        cout = round(total_cost / total_qty, 2) if total_qty else 0
        coutttc=round(cout/1.2, 2)
        coutstock=round(cout*self.stocktotalorgh, 2)
        coutstockttc=round(coutttc*self.stocktotalorgh, 2)
        return {
            "cout": cout,
            "coutttc": coutttc,
            "coutstock": coutstock,
            "coutstockttc": coutstockttc,
        }
# cupppon codes table



class Attribute(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=50)


class Supplier(models.Model):
    name=models.CharField(max_length=500)
    code=models.CharField(max_length=500, default='', null=True)
    personalname=models.CharField(max_length=500, null=True)
    address=models.CharField(max_length=500, default=None, null=True, blank=True)
    ice=models.CharField(max_length=500, default=None, null=True, blank=True)
    rc=models.CharField(max_length=500, default=None, null=True, blank=True)
    suppif=models.CharField(max_length=500, default=None, null=True, blank=True)
    modereglement=models.CharField(max_length=500, default=None, null=True, blank=True)
    phone=models.CharField(max_length=500, default=None, null=True, blank=True)
    phone2=models.CharField(max_length=500, default=None, null=True, blank=True)
    city=models.CharField(max_length=500, default=None, null=True, blank=True)
    address=models.CharField(max_length=500, default=None, null=True, blank=True)
    email=models.CharField(max_length=500, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    plafon=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    image=models.ImageField(upload_to='supplierimages/', null=True, blank=True, default=None)
    note=models.TextField(default=None, null=True)
    def soldfarah(self):
        bons=Itemsbysupplier.objects.filter(supplier=self, isfarah=True).aggregate(Sum('total'))['total__sum'] or 0
        avoirs=Avoirsupplier.objects.filter(supplier=self, isfarah=True, ispaid=False).aggregate(Sum('total'))['total__sum'] or 0
        avancess=Avancesupplier.objects.filter(supplier=self, isfarah=True).aggregate(Sum('amount'))['amount__sum'] or 0
        reglements=PaymentSupplier.objects.filter(supplier=self, isfarah=True,isavoir=False).aggregate(Sum('amount'))['amount__sum'] or 0
        return round(bons-avancess-avoirs-reglements, 2)
    def soldorgh(self):
        bons=Itemsbysupplier.objects.filter(supplier=self, isfarah=False).aggregate(Sum('total'))['total__sum'] or 0
        avoirs=Avoirsupplier.objects.filter(supplier=self, isfarah=False, ispaid=False).aggregate(Sum('total'))['total__sum'] or 0
        avancess=Avancesupplier.objects.filter(supplier=self, isfarah=False).aggregate(Sum('amount'))['amount__sum'] or 0
        reglements=PaymentSupplier.objects.filter(supplier=self, isfarah=False,isavoir=False).aggregate(Sum('amount'))['amount__sum'] or 0
        return round(bons-avancess-avoirs-reglements, 2)
    def __str__(self) -> str:
        return self.name



class Itemsbysupplier(models.Model):
    supplier= models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='provider')
    date = models.DateTimeField(default=None)
    # track bon achat farah
    isfarah=models.BooleanField(default=False)
    # track bon achat orgh
    isorgh=models.BooleanField(default=False)
    #date saisie
    dateentree=models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    items = models.TextField(blank=True, null=True, help_text='Quantity and Product name would save in JSON format')
    total = models.FloatField(default=0.00)
    tva = models.FloatField(default=0.00, null=True, blank=True)
    rest = models.FloatField(default=0.00)
    nbon = models.CharField(max_length=100, blank=True, null=True)
    facture=models.ForeignKey('Factureachat', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='factureofbonachat')
    ispaid=models.BooleanField(default=False)
    isfacture=models.BooleanField(default=False)
    isvalid=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.nbon} - {self.id}'

class Stockin(models.Model):
    # to indicate the stock initial
    isinitial=models.BooleanField(default=False)
    # WE NEED to distinguish between to societies
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    issortie=models.BooleanField(default=False)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    date=models.DateField()
    quantity=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    ref=models.CharField(max_length=500, default='-', null=True, blank=True)
    name=models.CharField(max_length=500, default='-', null=True, blank=True)
    # to delete stock facture is stock in is facture
    isfacture=models.BooleanField(default=False)
    # how much sold in this qty
    soldqty=models.IntegerField(default=0)
    # qtyofprice will be used to track qty of this price
    qtyofprice=models.FloatField(default=0.0)
    remise1=models.FloatField(default=0.00, null=True, blank=
    True)
    remise2=models.FloatField(default=0.00, null=True, blank=
    True)
    remise3=models.FloatField(default=0.00, null=True, blank=
    True)
    remise4=models.FloatField(default=0.00, null=True, blank=
    True)
    total=models.FloatField(default=0.00)
    net=models.FloatField(default=0.00)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True)
    nbon=models.ForeignKey(Itemsbysupplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    isavoir=models.BooleanField(default=False)
    avoir=models.ForeignKey('Avoirclient', on_delete=models.CASCADE, default=None, null=True, blank=True)
    facture=models.ForeignKey('Factureachat', on_delete=models.CASCADE, default=None, null=True, blank=True)
   
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
    # plafont is the maximum sold allowed
    plafon=models.FloatField(default=None, null=True, blank=True)
    clientfarah=models.BooleanField(default=False)
    clientorgh=models.BooleanField(default=False)
    # if client is for both societies
    note=models.TextField(default=None, null=True, blank=True)
    clientsortie=models.BooleanField(default=False)
    represent=models.ForeignKey('Represent', on_delete=models.CASCADE, default=None, null=True, related_name="repclient")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, default=None, null=True)
    name=models.CharField(max_length=200)
    clientname=models.CharField(max_length=200, null=True, default=None, blank=True)
    code=models.CharField(max_length=200, null=True, default=None)
    ice=models.CharField(max_length=200, null=True, default=None)
    clientif=models.CharField(max_length=200, null=True, default=None)
    clientrc=models.CharField(max_length=200, null=True, default=None)
    modereglement=models.CharField(max_length=200, null=True, default=None)
    email=models.CharField(max_length=200, null=True, default=None)
    city=models.CharField(max_length=200, null=True, default=None)
    region=models.CharField(max_length=200, null=True, default=None)
    total=models.FloatField(default=0.00, null=True, blank=True)
    soldtotal=models.FloatField(default=0.00, null=True, blank=True)
    soldbl=models.FloatField(default=0.00, null=True, blank=True)
    soldfacture=models.FloatField(default=0.00, null=True, blank=True)
    soldblorgh=models.FloatField(default=0.00, null=True, blank=True)
    soldfactureorgh=models.FloatField(default=0.00, null=True, blank=True)
    address=models.CharField(max_length=200)
    location=models.TextField(default='', null=True, blank=True)
    phone=models.CharField(max_length=200, default=None, null=True)
    phone2=models.CharField(max_length=200, default=None, null=True)
    diver=models.BooleanField(default=False)
    accesscatalog=models.BooleanField(default=False)
    class SoldblData:
        def __init__(self, sold, bons, avances, avoirs, reglements):
            self.sold = sold
            self.bons = bons
            self.avances = avances
            self.avoirs = avoirs
            self.reglements = reglements

    def sold(self):
        bons = round(Bonlivraison.objects.filter(client=self).aggregate(Sum('total'))['total__sum'] or 0, 2)
        avoirs = round(Avoirclient.objects.filter(client=self).aggregate(Sum('total'))['total__sum'] or 0, 2)
        avances = round(Avanceclient.objects.filter(client=self).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        reglements = round(PaymentClientbl.objects.filter(client=self).aggregate(Sum('amount'))['amount__sum'] or 0, 2)

        sold_value = round(bons - avances - avoirs - reglements, 2)
        return self.SoldblData(sold_value, bons, avances, avoirs, reglements)
    class SoldbsData:
        def __init__(self, sold, bons, avances, avoirs, reglements, remise):
            self.sold = sold
            self.bons = bons
            self.avances = avances
            self.avoirs = avoirs
            self.reglements = reglements
            self.remise = remise

    
    def soldbs(self):
        totalbons=Bonsortie.objects.filter(client_id=self).aggregate(Sum('total')).get('total__sum')or 0
        totalavoirs=Avoirclient.objects.filter(client_id=self).aggregate(Sum('total')).get('total__sum')or 0
        totalavances=Avanceclient.objects.filter(client_id=self).aggregate(Sum('amount')).get('amount__sum')or 0
        totalreglements=PaymentClientbl.objects.filter(client_id=self).aggregate(Sum('amount')).get('amount__sum')or 0
        remise=Bonsortie.objects.filter(client_id=self).aggregate(Sum('remiseamount')).get('remiseamount__sum')or 0
        sold_value = round(totalbons-totalavoirs-totalavances-totalreglements-remise, 2)
        return self.SoldbsData(sold_value, totalbons, totalavances, totalavoirs, totalreglements, remise)
        
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

class Avanceclient(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True)
    date = models.DateTimeField(default=None)
    amount = models.FloatField()
    bon=models.ForeignKey('Bonlivraison', on_delete=models.CASCADE, default=None, null=True)
    facture=models.ForeignKey('Facture', on_delete=models.CASCADE, default=None, null=True)
    mode=models.CharField(max_length=10, default=None, null=True)
    note=models.TextField(default='', null=True)
    echeance=models.DateField(default=None, null=True, blank=True)
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    bank=models.CharField(max_length=50, default=None, null=True, blank=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    issortie=models.BooleanField(default=False)
    bonofavance=models.CharField(max_length=900, default=None, null=True)
    # avance selected in an rglement
    inreglement=models.BooleanField(default=False)
    targetcaisse=models.ForeignKey('Caisse', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    targetbank=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, blank=True)

class Transfer(models.Model):
    date = models.DateTimeField(default=None)
    amount = models.FloatField()
    caissetarget=models.ForeignKey(Caisse, on_delete=models.SET_NULL, default=None, null=True, related_name='fromcaisse')
    caissesource=models.ForeignKey(Caisse, on_delete=models.SET_NULL, default=None, null=True, related_name='tocaisse')
    banksource=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, related_name='frombank')
    banktarget=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, related_name='tobank')
    note=models.TextField(default=None, null=True, blank=True)

class Avancesupplier(models.Model):
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True)
    date = models.DateTimeField(default=None)
    bon=models.ForeignKey(Itemsbysupplier, on_delete=models.CASCADE, default=None, null=True)
    facture=models.ForeignKey("Factureachat", on_delete=models.CASCADE, default=None, null=True)
    amount = models.FloatField()
    mode=models.CharField(max_length=10, default=None, null=True, blank=True)
    echeance=models.DateField(default=None, null=True, blank=True)
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    bank=models.CharField(max_length=50, default=None, null=True, blank=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    inreglement=models.BooleanField(default=False)
    targetcaisse=models.ForeignKey('Caisse', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    targetbank=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, blank=True)


class Bonlivraison(models.Model):
    # track history prices whenavoir or modifier bon, restore qty of qtyprice
    pricesofout=models.TextField(default=None, blank=True, null=True)
    isvalid=models.BooleanField(default=False)
    iscanceled=models.BooleanField(default=False)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    #bon command
    command=models.ForeignKey('Command', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofcommand')
    facture=models.ForeignKey('Facture', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='factureofthisbon')
    devi=models.ForeignKey('Devi', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='deviofbon')
    bonsortie=models.ForeignKey('Bonsortie', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonsortie')
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
    # track farah bons
    isfarah=models.BooleanField(default=False)
    # track orgh bons
    isorgh=models.BooleanField(default=False)
    # true when the bon is DELIVERED
    isdelivered=models.BooleanField(default=False)
    # true when its paid
    ispaid=models.BooleanField(default=False)
    # this will hold bon sortie numbers
    note=models.TextField(default=None, null=True, blank=True)
    # this will hold notes related only to bon
    notebon=models.TextField(default=None, null=True, blank=True)
    #statud if regl == r0
    statusreg=models.CharField(max_length=50, null=True, default='n1', blank=True)
    #statud if factur == f1
    statusfc=models.CharField(max_length=50, null=True, default='b1', blank=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    # payments of this bon
    payment=models.FloatField(default=0.00)
    benifice=models.FloatField(default=0.00)
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.bon_no
    def totalht(self):
        return round(self.total/1.2, 2)
    def tva(self):
        return round((self.total/1.2)*.2, 2)

class Facture(models.Model):
    isvalid=models.BooleanField(default=False)
    iscaceled=models.BooleanField(default=False)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    bon=models.ForeignKey(Bonlivraison, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name='bonofthisfacture')
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
    # if we have more than one bon for the same facture
    bons=models.ManyToManyField(Bonlivraison, default=None, blank=True, related_name='bonsoffactures')
    def ht(self):
        return round(self.total/1.2, 2)
    def thistva(self):
        return round((self.total/1.2)*.2, 2)
    def reglements(self):
        return PaymentClientbl.objects.filter(factures__in=[self])
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)



class PaymentSupplier(models.Model):
    # date dyal nhar tvalida f lbanka
    dateregl = models.DateTimeField(default=None, null=True, blank=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=None)
    amount = models.FloatField(default=0.00)
    mode=models.CharField(max_length=10, default=None)
    echeance=models.DateField(default=None, null=True, blank=True)
    bon=models.ForeignKey(Itemsbysupplier, on_delete=models.CASCADE, null=True, default=None, blank=True, related_name="bonofreglement")
    #factures reglé onetomanys
    bons=models.ManyToManyField(Itemsbysupplier, default=None, blank=True, related_name="reglementssupp")
    avoirs=models.ManyToManyField("Avoirsupplier", default=None, blank=True, related_name="avoirsofreglement")
    avances=models.ManyToManyField(Avancesupplier, default=None, blank=True, related_name="avancesofreglement")
    factures=models.ManyToManyField("Factureachat", default=None, blank=True, related_name="factureofreglement")
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    #bankname
    bank=models.CharField(max_length=500, default=None, null=True, blank=True)
    nrecu=models.CharField(max_length=500, default=None, null=True, blank=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    usedinfacture=models.BooleanField(default=False)
    # avoir fornisseur I5lls i bo lmahal
    isavoir=models.BooleanField(default=False)
    targetcaisse=models.ForeignKey('Caisse', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    targetbank=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    # if regl is paid if it has echeaance
    ispaid=models.BooleanField(default=False)
    #refused means impyé
    refused=models.BooleanField(default=False)
    source=models.CharField(max_length=500, default=None, null=True, blank=True)

    # we need somthin to track if the reglement
class Notesrepresentant(models.Model):
    represent=models.ForeignKey('Represent', on_delete=models.SET_NULL, default=None, null=True)
    note=models.TextField()
    def __str__(self) -> str:
        return self.represent.name





class PaymentClientbl(models.Model):
    code=models.CharField(max_length=100, default=None, null=True, blank=True)
    dateregl = models.DateTimeField(default=None, null=True, blank=True)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    date = models.DateTimeField(default=None)
    amount = models.FloatField(default=0.00)
    mode=models.CharField(max_length=10, default=None)
    # the name of the bank
    bank=models.CharField(max_length=100000, default=None, null=True, blank=True)
    nrecu=models.CharField(max_length=100000, default=None, null=True, blank=True)
    amountofeachbon=models.CharField(max_length=100000, default=None, null=True, blank=True)
    bons=models.ManyToManyField(Bonlivraison, default=None, blank=True, related_name="reglements")
    factures=models.ManyToManyField(Facture, default=None, blank=True, related_name="fcreglements")
    bonsortie=models.ManyToManyField('Bonsortie', default=None, blank=True, related_name="reglementsortie")
    avoirs=models.ManyToManyField('Avoirclient', default=None, blank=True, related_name="avoirsofreglement")
    avances=models.ManyToManyField(Avanceclient, default=None, blank=True, related_name="avancesofreglement")
    # mode: 0 bl, 1 facture
    echance=models.DateField(default=None, null=True, blank=True)
    npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
    # if the regelement is used to regle facture
    usedinfacture=models.BooleanField(default=False)
    # if regl is paid if it has echeaance
    ispaid=models.BooleanField(default=False)
    #refused means impyé
    refused=models.BooleanField(default=False)
    bon=models.ForeignKey(Bonlivraison, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='bonofreglement')
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    issortie=models.BooleanField(default=False)
    # payment given to client when avoir
    isavoir=models.BooleanField(default=False)
    targetcaisse=models.ForeignKey('Caisse', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    targetbank=models.ForeignKey('Bank', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    source=models.CharField(max_length=500, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.mode+'-'+str(self.amount)


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
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    livraison=models.ForeignKey('Livraisonitem', on_delete=models.SET_NULL, default=None, null=True)
class Livraisonitem(models.Model):
    coutmoyen=models.FloatField(default=0.00, null=True, blank=True)
    achatids=models.TextField(default=None, null=True, blank=True)
    remainqties=models.TextField(default=None, null=True, blank=True)
    oldqties=models.TextField(default=None, null=True, blank=True)
    pricesofout=models.TextField(default=None, blank=True, null=True)
    qtyofout=models.TextField(default=None, blank=True, null=True)
    bon=models.ForeignKey(Bonlivraison, on_delete=models.CASCADE, default=None, null=True)
    total=models.FloatField(default=0.00)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=9000, null=True, default=None)
    qty=models.FloatField(default=0.00)
    # this total represents the revenue of this product
    price=models.FloatField(default=0.00)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    bonsortie=models.ForeignKey('Bonsortie', on_delete=models.CASCADE, default=None, null=True, blank=True)
    
    # t o track ligns that are facture
    isfacture=models.BooleanField(default=False)
    #track farah
    isfarah=models.BooleanField(default=False)
    #track orgh
    isorgh=models.BooleanField(default=False)
    isavoir=models.BooleanField(default=False)
    clientprice=models.FloatField(default=0.00)
    date=models.DateField(default=None, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    def priceht(self):
        return round(self.price/1.2, 2)
    def totalht(self):
        return round(self.total/1.2, 2)
    

class Avoirclient(models.Model):
    iscaceled=models.BooleanField(default=False)
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
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    issortie=models.BooleanField(default=False)

    # avoir selected in an rglement
    inreglement=models.BooleanField(default=False)
    # avoir can be paid to the client
    ispaid=models.BooleanField(default=False)
    rest= models.FloatField(default=0, blank=True, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

# class Paymentavcl(models.Model):
#     client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
#     date = models.DateTimeField(default=None)
#     amount = models.FloatField(default=0.00)
#     mode=models.CharField(max_length=10, default=None)
#     # the name of the bank
#     bank=models.CharField(max_length=100000, default=None, null=True, blank=True)
#     amountofeachbon=models.CharField(max_length=100000, default=None, null=True, blank=True)
#     bons=models.ManyToManyField(Bonlivraison, default=None, blank=True, related_name="reglements")
#     factures=models.ManyToManyField(Facture, default=None, blank=True, related_name="fcreglements")
#     bonsortie=models.ManyToManyField('Bonsortie', default=None, blank=True, related_name="reglementsortie")
#     avoirs=models.ManyToManyField('Avoirclient', default=None, blank=True, related_name="avoirsofreglement")
#     avances=models.ManyToManyField(Avanceclient, default=None, blank=True, related_name="avancesofreglement")
#     # mode: 0 bl, 1 facture
#     echance=models.DateField(default=None, null=True, blank=True)
#     npiece=models.CharField(max_length=50, default=None, null=True, blank=True)
#     # if the regelement is used to regle facture
#     usedinfacture=models.BooleanField(default=False)
#     # if regl is paid if it has echeaance
#     ispaid=models.BooleanField(default=False)
#     #refused means impyé
#     refused=models.BooleanField(default=False)
#     bon=models.ForeignKey(Bonlivraison, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='bonofreglement')
#     isfarah=models.BooleanField(default=False)
#     isorgh=models.BooleanField(default=False)
#     issortie=models.BooleanField(default=False)

class Returned(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    qty=models.FloatField(default=0.00)
    remise=models.IntegerField(null=True, blank=True, default=None)
    total=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    avoir=models.ForeignKey(Avoirclient, related_name='returned_invoice', on_delete=models.CASCADE, default=None, null=True, blank=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    bon=models.ForeignKey(Bonlivraison, on_delete=models.CASCADE, default=None, null=True, blank=True)
class Avoirsupplier(models.Model):
    iscaceled=models.BooleanField(default=False)
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
    note=models.TextField(default=None, null=True, blank=True)
    total = models.FloatField(default=0, blank=True, null=True)
    avoirbl=models.BooleanField(default=False)
    avoirfacture=models.BooleanField(default=False)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    inreglement=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # avoir can be paid to the client
    ispaid=models.BooleanField(default=False)
    rest= models.FloatField(default=0, blank=True, null=True)
class Returnedsupplier(models.Model):
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None)
    qty=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    price=models.FloatField(default=0.00)
    avoir=models.ForeignKey(Avoirsupplier, related_name='avoir_supplier', on_delete=models.CASCADE, default=None, null=True, blank=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    remise1=models.CharField(max_length=100, null=True, default=None)
    remise2=models.CharField(max_length=100, null=True, default=None)
    remise3=models.CharField(max_length=100, null=True, default=None)
    remise4=models.CharField(max_length=100, null=True, default=None)
    
class Ordersnotif(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
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
#wishlist items
class wishlist(models.Model):
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
    # is empty if npiece has no factures, just got added manually
    isempty=models.BooleanField(default=False)
    grandtotal=models.FloatField(default=None, null=True, blank=True)
    amount=models.FloatField(default=None, null=True, blank=True)
    tva=models.FloatField(default=None, null=True, blank=True)
class Command(models.Model):
    devi=models.ForeignKey('Devi', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='deviofcommand')
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    amountpaid=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    note=models.CharField(max_length=5500, null=True, default=None)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    generatedbl=models.BooleanField(default=False)
    bl=models.ForeignKey(Bonlivraison, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofcommand')
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    #bc=models.ForeignKey(Boncommande, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    forsupplier=models.BooleanField(default=False)

class CommandItem(models.Model):
    command=models.ForeignKey(Command, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    price=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    # this total represents the revenue of this product
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # track farah products in sortie items
    isfarah=models.BooleanField(default=False)
    # to track ligns that are facture
    isorgh=models.BooleanField(default=False)
    date=models.DateField(default=None, null=True, blank=True)


# devi becom bonsorie, then bl
class Devi(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    amountpaid=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    note=models.CharField(max_length=5500, null=True, default=None)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    generatedbl=models.BooleanField(default=False)
    bl=models.ForeignKey(Bonlivraison, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofdevi')
    generatedbc=models.BooleanField(default=False)
    bc=models.ForeignKey(Command, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='commandofdevi')
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    forsupplier=models.BooleanField(default=False)
class DeviItem(models.Model):
    devi=models.ForeignKey(Devi, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    price=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    # this total represents the revenue of this product
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # track farah products in sortie items
    isfarah=models.BooleanField(default=False)
    # to track ligns that are facture
    isorgh=models.BooleanField(default=False)
    date=models.DateField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.devi.bon_no} - {self.product.ref}'

# devi becom bonsorie, then bl

class Commandsupplier(models.Model):
    devi=models.ForeignKey('Devisupplier', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='devisupplierofcommand')
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    amountpaid=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    note=models.CharField(max_length=5500, null=True, default=None)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    generatedbl=models.BooleanField(default=False)
    bl=models.ForeignKey(Itemsbysupplier, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofcommandsupplier')
    facture=models.ForeignKey("Factureachat", on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofcommandsupplier')
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    #bc=models.ForeignKey(Boncommande, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    forsupplier=models.BooleanField(default=False)

class CommandItemsupplier(models.Model):
    command=models.ForeignKey(Commandsupplier, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    price=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    # this total represents the revenue of this product
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # track farah products in sortie items
    isfarah=models.BooleanField(default=False)
    # to track ligns that are facture
    isorgh=models.BooleanField(default=False)
    date=models.DateField(default=None, null=True, blank=True)

# devi becom bonsorie, then bl
class Devisupplier(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    amountpaid=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    note=models.CharField(max_length=5500, null=True, default=None)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    generatedbl=models.BooleanField(default=False)
    bl=models.ForeignKey(Itemsbysupplier, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofdevisupplier')
    # can be generated to be facture
    facture=models.ForeignKey('Factureachat', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='bonofdevisupplier')
    generatedbc=models.BooleanField(default=False)
    bc=models.ForeignKey(Commandsupplier, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='commandofdevisupplier')
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    forsupplier=models.BooleanField(default=False)
class DeviItemsupplier(models.Model):
    devi=models.ForeignKey(Devisupplier, on_delete=models.CASCADE, default=None)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    price=models.FloatField(default=0.00)
    total=models.FloatField(default=0.00)
    # this total represents the revenue of this product
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # track farah products in sortie items
    isfarah=models.BooleanField(default=False)
    # to track ligns that are facture
    isorgh=models.BooleanField(default=False)
    date=models.DateField(default=None, null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.devi.bon_no} - {self.product.ref}'

# devi becom bonsorie, then bl


class Bonsortie(models.Model):
    pricesofout=models.TextField(default=None, blank=True, null=True)
    remise=models.BooleanField(default=False)
    paidamount=models.FloatField(default=0.00)
    remiseamount=models.FloatField(default=0.00)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    bonlivraison=models.ForeignKey(Bonlivraison, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='blofbon')
    devi=models.ForeignKey(Devi, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    client=models.ForeignKey(Client, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    total=models.FloatField(default=0.00)
    amountpaid=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    bon_no=models.CharField(max_length=50, null=True, default=None)
    # true when the bon is generated to be a bon liv
    generated=models.BooleanField(default=False)
    # true when the bon is generated to be a facture
    ispaid=models.BooleanField(default=False)
    note=models.TextField(default=None, null=True, blank=True)
    #statud if regl == r0
    statusreg=models.CharField(max_length=50, null=True, default='n1', blank=True)
    car=models.CharField(max_length=500, null=True, default='n1', blank=True)
    #statud if factur == f1
    statusfc=models.CharField(max_length=50, null=True, default='b1', blank=True)
    def save(self, *args, **kwargs):
        self.code = str(uuid.uuid4())
        super().save(*args, **kwargs)
    def hasavance(self):
        return Avanceclient.objects.filter(bonofavance=self.bon_no).exists()
    def __str__(self) -> str:
        return self.bon_no
# lines in bon sorie
class Sortieitem(models.Model):
    pricesofout=models.TextField(default=None, blank=True, null=True)
    qtyofout=models.TextField(default=None, blank=True, null=True)
    bon=models.ForeignKey(Bonsortie, on_delete=models.CASCADE, default=None)
    total=models.FloatField(default=0.00)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=9000, null=True, default=None)
    qty=models.FloatField(default=0.00)
    coutmoyen=models.FloatField(default=0.00, null=True, blank=True)
    achatids=models.TextField(default=None, null=True, blank=True)
    remainqties=models.TextField(default=None, null=True, blank=True)
    oldqties=models.TextField(default=None, null=True, blank=True)
    
    # this total represents the revenue of this product
    price=models.FloatField(default=0.00)
    client=models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True, blank=True)
    # track farah products in sortie items
    isfarah=models.BooleanField(default=False)
    # to track ligns that are facture
    isfacture=models.BooleanField(default=False)
    isavoir=models.BooleanField(default=False)
    date=models.DateField(default=None, null=True, blank=True)
    
class Factureachat(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    iscaceled=models.BooleanField(default=False)
    isvalid=models.BooleanField(default=False)
    facture_no=models.CharField(max_length=500, null=True, default=None)
    date = models.DateTimeField(default=None, blank=True, null=True)
    bons=models.ManyToManyField(Itemsbysupplier, default=None, blank=True, related_name='facturebons')
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    total=models.FloatField(default=0.00)
    tva=models.FloatField(default=0.00)
    rest=models.FloatField(default=0.00)
    ispaid=models.BooleanField(default=False)
    isvalid=models.BooleanField(default=False)
    bon=models.ForeignKey(Itemsbysupplier, default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='facturebon')
    supplier=models.ForeignKey(Supplier, default=None, blank=True, on_delete=models.CASCADE, related_name='supplieroffacture')
    def ht(self):
        return round(self.total/1.2, 2)
    def thistva(self):
        return round((self.total/1.2)*.2, 2)
    def reglements(self):
        return PaymentSupplier.objects.filter(factures__in=[self])
class Outfactureachat(models.Model):
    facture=models.ForeignKey(Factureachat, on_delete=models.CASCADE, default=None)
    total=models.FloatField(default=0.00)
    product=models.ForeignKey(Produit, on_delete=models.CASCADE, default=None, null=True)
    remise1=models.CharField(max_length=100, null=True, default=None)
    remise2=models.CharField(max_length=100, null=True, default=None)
    remise3=models.CharField(max_length=100, null=True, default=None)
    remise4=models.CharField(max_length=100, null=True, default=None)
    ref=models.CharField(max_length=100, null=True, default=None)
    name=models.CharField(max_length=100, null=True, default=None)
    qty=models.IntegerField()
    # this total represents the revenue of this product
    price=models.FloatField(default=0.00)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None, null=True, blank=True)
    date=models.DateField(default=None, blank=True, null=True)
    isfarah=models.BooleanField(default=False)
    isorgh=models.BooleanField(default=False)
    stockin=models.ForeignKey(Stockin, on_delete=models.SET_NULL, default=None, null=True)

class Bank(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    rib=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)
    initialamount=models.FloatField(default=0.0)
    target=models.CharField(max_length=500, default='', null=True)


# caisse farah
class Caissefarah(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)

class Caisseorgh(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)

class Caissepos(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)

class Bankfarah(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)

class Bankorgh(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)

class Bankpos(models.Model):
    name=models.CharField(max_length=500, default='', null=True)
    total=models.FloatField(default=0.0)



class Config(models.Model):
    caissesortie=models.FloatField(default=0.00)
    banksortie=models.FloatField(default=0.00)
    caissefarah=models.FloatField(default=0.00)
    caisseorgh=models.FloatField(default=0.00)
    bankfarah=models.FloatField(default=0.00)
    bankorgh=models.FloatField(default=0.00)
    