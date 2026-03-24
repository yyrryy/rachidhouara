from django.shortcuts import render, redirect
from main.models import Produit, Mark, Category, Supplier, Stockin, Itemsbysupplier, Client, Represent, Order, Orderitem, Clientprices, Bonlivraison, Facture, Outfacture, Livraisonitem, PaymentClientbl, PaymentClientfc,  PaymentSupplier, Bonsregle, Returnedsupplier, Avoirclient, Returned, Avoirsupplier, Orderitem, Carlogos, Ordersnotif, Connectedusers, Promotion, UserSession, Refstats, Notavailable, Cart, Wich, Wishlist, Notification, Modifierstock, Cartitems, Notesrepresentant, Achathistory, Excelecheances, Tva, Damagedproducts, Etude, YearEndStock, Setting
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
import openpyxl
from time import sleep
# import Count
from django.contrib.auth.models import User
from django.db.models import Count, F, Sum, Q, ExpressionWrapper, Func, fields, IntegerField
from django.db.models.functions import Cast
from django.contrib.sessions.models import Session
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
import json
from django.contrib.auth.models import Group
from django.db import transaction
from datetime import datetime, date, timedelta
from django.utils import timezone
import pandas as pd
from itertools import chain, groupby
from django.core.serializers import serialize
import re
from django.contrib.auth import authenticate, login, logout
import requests as req
from collections import defaultdict
import calendar
from django.db.models.functions import TruncDay
import uuid
from dateutil.relativedelta import relativedelta
today = timezone.now().date()
thisyear=timezone.now().year

def checklivraisonno(request):
    no=request.GET.get('no')
    id=request.GET.get('id')
    bl=Bonlivraison.objects.exclude(pk=id).filter(bon_no=no).first()

    return JsonResponse({
        'exist':True if bl else False
    })

def checkfactureno(request):
    no=request.GET.get('no')
    id=request.GET.get('id')
    bl=Facture.objects.exclude(pk=id).filter(facture_no=no).first()

    return JsonResponse({
        'exist':True if bl else False
    })

def downloadfcfromech(request):
    facture='FC'+request.GET.get('facture').strip()
    facture=Facture.objects.get(facture_no=facture)
    print('>>>>>>>>', facture.id)
    return JsonResponse({
    'success':True,
    'factureid':facture.id
    })

def makethisprint(request):
    id=request.GET.get('id')
    facture=request.GET.get('facture').strip()
    thisrow=Excelecheances.objects.get(pk=id)
    rowwithsamefc=Excelecheances.objects.filter(factures=facture).exclude(pk=id)
    thisrow.isprinted=True
    thisrow.save()
    #rowwithsamefc.update(isprinted=True)
    return JsonResponse({
    'success':True
    })

def makethicomptacle(request):
    id=request.GET.get('id')
    thisrow=Excelecheances.objects.get(pk=id)
    thisrow.iscontable=not thisrow.iscontable
    thisrow.save()
    return JsonResponse({
    'success':True
    })

def searchech(request):
    term = request.GET.get('term')
    print('>>>>>>> term: ', term)
    search_terms = term.split('+')

    q_objects = Q()
    for term in search_terms:
        if term:
            q_objects &= (
                Q(client__iregex=term) |
                Q(npiece__iregex=term) |
                Q(mode__iregex=term) |
                Q(amount__iregex=term) |
                Q(grandtotal__iregex=term) |
                Q(month__iregex=term)|
                Q(note__iregex=term)|
                Q(clientcode__iregex=term)|
                Q(factures__iregex=term)
            )
    data = Excelecheances.objects.filter(q_objects).order_by('month')
    print('>>>>>> data: ', data)

    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item.month].append(item)
    print('>>>>>> grouped_data: ', grouped_data)

    return JsonResponse({
        'data': render(request, 'searchresultech.html', {'grouped_data': grouped_data.items}).content.decode('utf-8'),
    })

def getalldatagrouped(request):
    data = Excelecheances.objects.order_by('month')
    print('>>>>>> data: ', data)

    grouped_data = defaultdict(list)
    for item in data:
        grouped_data[item.month].append(item)
    print('>>>>>> grouped_data: ', grouped_data)

    return JsonResponse({
        'data': render(request, 'searchresultech.html', {'grouped_data': grouped_data.items}).content.decode('utf-8'),
    })

def deleterowech(request):
    id=request.GET.get('id')
    row=Excelecheances.objects.get(pk=id)
    row.delete()
    return JsonResponse({
    'success':True
    })

# move to other date
def remplacer(request):
    ids=json.loads(request.GET.get('ids'))
    month=request.GET.get('month')
    print('>>>>>>', ids)
    echeances=Excelecheances.objects.filter(pk__in=ids)

    echeances.update(month=month)

    return JsonResponse({
    'success':True
    })
def savetva(request):
    tvaachatval=request.GET.get('tvaachatval')
    othertvaachatval=request.GET.get('othertvaachatval')
    netval=request.GET.get('netval')
    tvavente=request.GET.get('tvavente')
    report=request.GET.get('report')
    rest=request.GET.get('rest')
    restandtva=request.GET.get('restandtva')
    month=request.GET.get('monthyear')
    print(rest, restandtva)
    try:
        already=Tva.objects.get(month=month)
        already.tvaachat=tvaachatval
        already.tvavente=tvavente
        already.report=report
        already.rest=rest
        already.restandtva=restandtva
        already.net=netval
        already.othertvaachat=othertvaachatval
        already.save()
    except:
        Tva.objects.create(month=month, tvaachat=tvaachatval, tvavente=tvavente, net=netval, othertvaachat=othertvaachatval, report=report, rest=rest, restandtva=restandtva)
    return JsonResponse({
    'success':True
    })
def gettvamonthinfo(request):
    month=request.GET.get('month')
    data=Excelecheances.objects.filter(month=month)
    total=data.aggregate(Sum('amount'))['amount__sum'] or 0
    totaltva=round(total-(total/1.2), 2)
    print('>>> total tva', totaltva)
    current_month = datetime.strptime(month, '%m/%Y')
    previous_month = current_month - relativedelta(months=1)
    previous_month_str = previous_month.strftime('%m/%Y')
    thismonth=Tva.objects.filter(month=month).first()
    previousmonth=Tva.objects.filter(month=previous_month_str).first()
    othertvaachat=thismonth.othertvaachat if thismonth else 0.00
    rest=thismonth.net if thismonth else 0.00
    restandtva=thismonth.net if thismonth else 0.00
    net=thismonth.net if thismonth else 0.00
    report=thismonth.report if thismonth else 0
    if previousmonth is not None and previousmonth.net<0:
        print('>>>>>>>> here in if')
        othertvaachat=round(totaltva+previousmonth.net, 2)
        if othertvaachat<0:
            net=-round(thismonth.tvaachat+abs(othertvaachat), 2)
        else:
            net=round(othertvaachat-thismonth.tvaachat, 2)
    else:
        print('>>>>>>>> here in else')
        #othertvaachat=0.00
        #net=round(totaltva-thismonth.tvaachat, 2)
        rest=round(previousmonth.net-previousmonth.report, 2)
        restandtva=round(rest+totaltva, 2)
        if thismonth:
            net=round(restandtva-thismonth.tvaachat, 2)
        else:
            net=restandtva
    rest=round(previousmonth.net-previousmonth.report, 2)
    restandtva=round(rest+totaltva, 2)
    print('>>>>>> rest, othertva, totaltva, net for', rest, month, othertvaachat, totaltva, net)
    return JsonResponse({
        'totaltva':float(totaltva),
        'tvaachat':float(thismonth.tvaachat) if thismonth else 0.00,
        'othertvaachat':float(othertvaachat),
        'net':float(net),
        'rest':rest,
        'restandtva':restandtva,
        'report':report,
    })

def gettvafornewline(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    month=f'{month}/{year}'
    print('>>>>>>>>>', month, year)
    data=Excelecheances.objects.filter(month=month)
    totaltva=round(data.aggregate(Sum('tva'))['tva__sum'] or 0, 2)

    current_month = datetime.strptime(month, '%m/%Y')
    previous_month = current_month - relativedelta(months=1)
    previous_month_str = previous_month.strftime('%m/%Y')
    thismonth=Tva.objects.filter(month=month).first()
    previousmonth=Tva.objects.filter(month=previous_month_str).first()
    othertvaachat=thismonth.othertvaachat if thismonth else 0.00
    net=thismonth.net if thismonth else 0.00
    if previousmonth is not None and previousmonth.net<0:
         othertvaachat=round(totaltva+previousmonth.net, 2)
         net=round(othertvaachat-thismonth.tvaachat, 2)
    print('>>>>> this', (previousmonth is not None and previousmonth.net<0))
    print('>>>>>>', othertvaachat)
    return JsonResponse({
        'totaltva':totaltva,
        'tvaachat':thismonth.tvaachat if thismonth else 0.00,
        'othertvaachat':othertvaachat,
        'net':net
    })

def gettva(request):
    year=request.GET.get('year')
    tvas=Tva.objects.filter(month__icontains=year).order_by('month')
    if tvas:
        ctx={
        'title':'Tva calculations',
        'tvatrs':render(request, 'tvatrs.html', {'tvas':tvas}).content.decode('utf-8'),
        }
        return JsonResponse(ctx)
    else:
        tvas=Tva.objects.create(month=f'01/{year}', tvaachat=0, tvavente=0, net=0, othertvaachat=0, report=0, rest=0, restandtva=0)
        ctx={
        'title':'Tva calculations',
        'tvatrs':render(request, 'tvatrs.html', {'tvas':tvas}).content.decode('utf-8'),
        }
        return JsonResponse(ctx)

# duplicated data in excel exheances
def duplicatedech(request):
    monthyear=request.GET.get('monthyear')
    # Step 1: Find npiece values that are duplicated
    duplicated_npieces = Excelecheances.objects.filter(month=monthyear).values('npiece').annotate(npiece_count=Count('npiece')).filter(npiece_count__gt=1)

    # Step 2: Get the records that have duplicated npiece values
    npiece_values = [item['npiece'] for item in duplicated_npieces]

    # Step 3: Retrieve one record for each duplicated npiece value
    duplicates = Excelecheances.objects.filter(npiece__in=npiece_values).distinct('npiece')

    return JsonResponse({
    'success':True,
    'duplicates':', '.join([i.npiece for i in duplicates])
    })

# this is for comparing the tvas of factures
def tvacomparer(request):
    factures=Facture.objects.all()
    errors=[]
    for i in factures:
        tva=round(i.total-(i.total/1.2), 2)
        if not tva == i.tva:
            print('>>>>', i.facture_no)
            errors.append((i.facture_no, tva, i.tva))
    return JsonResponse({
    'data':errors
    })
# not finished yet
def damagedproducts(request):
    pdctid=request.GET.get('pdctid')
    qty=request.GET.get('qty')
    password=request.GET.get('password')
    product=Produit.objects.get(pk=pdctid)
    print('>>> ', pdctid, qty, password)
    # create a damaged line
    #Damagedproducts.objects.create(product_id=pdctid, qty=qty)
    # update stock (danger: stock cannot be updated)
    #product.stocktotal

    # update stock in server
    return JsonResponse({
        'success':True
    })

def checkfromadashi(request):
    # code=request.GET.get('code')
    ref=request.GET.get('ref').strip()
    assambly=request.GET.get('assambly')
    print('>>> ', ref)
    # get product with the same adashicode
    # products=Produit.objects.filter(adashicode=code)
    print('>>> trying to get the product with the same ref (I should add assambly to get the exact product)')
    try:
        product=Produit.objects.get(ref=ref)
        data=[{
            'id':product.id,
            'ref':product.ref,
            'name':product.name,
            'disponible':'Disponible' if product.stocktotal > 0 else 'Non Disponoble',
            }]
        return JsonResponse({
            'found':True,
            'products':data,
            # if it's the exact product =>> code found in adashi code not in eq
            'exact':True
        })
    except Exception as e:
        print('>>> no products with exact ref, checking refeq1.2.3')
        # make it upper now, cause refeqs and equiv will be in uppercase
        ref=ref.upper()
        regex_pattern = rf'(^|\s|\+){ref}(\s|\+|$)'

        products=Produit.objects.filter(Q(ref=ref)|Q(refeq1=ref)|Q(refeq2=ref)|Q(refeq3=ref)|Q(refeq4=ref))
        # add also equivalents
        products|=Produit.objects.filter(Q(equivalent__regex=regex_pattern))
        if products:
            print('>>> found by ref eq')
            data=[{
                'id':i.id,
                'ref':i.ref,
                'name':i.name,
                'disponible':'Disponible' if i.stocktotal > 0 else 'Non Disponoble',
                } for i in products]
            return JsonResponse({
                'found':True,
                'products':data,
                # if it's the exact product =>> code found in adashi code not in eq
                'exact':False
            })
        else:
            # print('>>> no products with exact refeq1.2.3, checking refeq text')
            # # make it upper now, cause refeqs and equiv will be in uppercase
            # ref=ref.upper()
            # # products=Produit.objects.filter(adashieq=code)
            # regex_pattern = rf'(^|\s|\+){ref}(\s|\+|$)'
            # products=Produit.objects.filter(Q(equivalent__regex=regex_pattern))
            # print('>>> getting regex equiv', products)
            # if products:
            #     print('>>> there is products')
            #     data=[]
            #     for i in products:
            #         p={
            #         'ref':i.ref,
            #         'name':i.name,
            #         'disponible':'Disponible' if i.stocktotal > 0 else 'Non Disponoble',
            #         }
            #         data.append(p)
            #     return JsonResponse({
            #         'found':True,
            #         'products':data,
            #         'exact':False
            #     })
            # else:
            print('>>> there is no products')
            return JsonResponse({
                'found':False,
                'data':'Not found'
            })
def gettvayear(request):
    year=request.GET.get('year')
    tvas=Tva.objects.filter(month__icontains=year)
    if tvas:
        print('there is records')
    else:
        print('there is no records, creating month 01')
        Tva.objects.create(month=f'01/{year}', tvaachat=0, tvavente=0, net=0, othertvaachat=0, report=0, rest=0, restandtva=0)
    return JsonResponse({
    'rr':'rr'
    })

def setdamagedqty(request):
    pdctid=request.GET.get('pdctid')
    qty=request.GET.get('qty')
    password=request.GET.get('password')
    print('>>>', pdctid)
    return JsonResponse({
        'success':True
    })
def reglementech(request):
    thisyear=timezone.now().year
    facture=request.GET.get('facture')
    print('>>> ', facture)
    facture=Facture.objects.get(facture_no=f'FC{facture}')
    client=facture.client
    print('clientid >>', client.id)
    if client.id==3731:
        return JsonResponse({
        'success':False,
        'error':'Diver'
        })
    factures=Facture.objects.filter(client=client).order_by('date')
    trs=''
    for i in factures:
        trs+=f'<tr  class="fcreglrow" style="background: {"rgb(221, 250, 237);" if i.reglementsfc.exists() else ""}" clientid="{client.id}"><td>{i.date.strftime("%d/%m/%Y")}</td><td>{i.facture_no}</td><td>{i.client.name}</td><td>{i.total}</td><td>{"RR" if i.reglementsfc.exists() else "NR"}</td> <td><input type="checkbox" value="{i.id}" name="facturestopay" onchange="checkreglementbox(event)"></td></tr>'
    return JsonResponse({

        'success':True,
        'trs':trs,
        'totalfactures':round(factures.aggregate(Sum('total'))['total__sum']or 0, 2),
        'soldfactureregl':round(client.soldfacture, 2),
        'client':client.name,
        'clientid':client.id
    })

def checktvas(request):
    tvas=Excelecheances.objects.filter(month__icontains='07/2024')
    totalamount=tvas.aggregate(Sum('amount'))['amount__sum'] or 0

    existingtvas=[]
    calc=[]
    for i in tvas:
        existingtvas.append((i.tva, round(i.amount-(i.amount/1.2), 2)))

    return JsonResponse({
    'existingtvas':existingtvas,
    'totalamount':totalamount,
    'tva':totalamount-(totalamount/1.2),
    'tvax':tvas.aggregate(Sum('tva'))['tva__sum'] or 0
    })
def checkoldunpaidbons(request):
    clientid=request.GET.get('clientid')
    three_months_ago = timezone.now() - timedelta(days=90)  # Assuming 30 days per month on average

    # Query for Bonlivraison objects that have a 'date' field earlier than three months ago
    bons = Bonlivraison.objects.filter(date__lt=three_months_ago, ispaid=False, total__gt=0, client_id=clientid).first()
    factures = Facture.objects.filter(date__lt=three_months_ago, ispaid=False, total__gt=0, client_id=clientid).first()
    print('>> bons, factures', bons, factures)
    if bons or factures:
        return JsonResponse({
        'exist':True,
        })
    else:
        return JsonResponse({
        'exist':False,
        })
def getlastcodeclient(request):
    try:
        lastcode = Client.objects.order_by('code').last()
        print('lastcode', lastcode.code)
        if lastcode:

            codecl = f"{int(lastcode.code) + 1:06}"
        else:
            codecl = f"000001"
    except:
        codecl="000001"
    return JsonResponse({
    'lastcode':codecl
    })
# this is temporary just to enter the initial stock for plaquette
def stockinital(request):
    d=[

    ]
    for i in d:
        pass
        # try:
        #     p=Produit.objects.get(ref=i['ref'].lower().strip())
        #     p.stockinitial=int(i['qty'])
        #     p.save()
        #     print('>> ', p.ref, i['qty'])
        # except Exception as e:
        #     print('>>> ', e)
        #     print(i['ref'])
    return JsonResponse({
    'rr':'rr'
    })
# this is to make all bon avoir
def avoirallbon(request):
    # bonid=
    # avoirid=
    # bon=Bonlivraison.objects.get(pk=bonid)
    # bonitems=Livraisonitem.objects.filter(bon=bon, isfacture=False).order_by('product__name')
    # for i in bonitems:
    #     print('>>> ', i.product, i.qty, i.product, i.remise,i.price,i.total)
    #
    #     i.product.stocktotal=int(i.product.stocktotal)+int(i.qty)
    #     i.product.save()
    #     Returned.objects.create(
    #         avoir_id=avoirid,
    #         product=i.product,
    #         qty=i.qty,
    #         remise=i.remise,
    #         price=i.price,
    #         total=i.total
    #     )
    return JsonResponse({
    'bon.total':bon.total,
    'bonitems.count()':bonitems.count()
    })

def rr(request):
    # factures= [
    #     "FC2403296", "FC2403260", "FC2403205", "FC2403156", "FC2403057",
    #     "FC2402984", "FC2402796", "FC2402577", "FC2401706", "FC2401615",
    #     "FC2401593", "FC2401510", "FC2401501", "FC2401480", "FC2401432",
    #     "FC2401390", "FC2401339", "FC2401277", "FC2401260", "FC2401192",
    #     "FC2401189", "FC2401183", "FC2401101", "FC2401085", "FC2401084",
    #     "FC2401017", "FC2401002", "FC2400946", "FC2400936", "FC2400835",
    #     "FC2400821", "FC2400811", "FC2400713", "FC2400662", "FC2400529",
    #     "FC2400488", "FC2400481", "FC2400396", "FC2400357", "FC2400348",
    #     "FC2400334", "FC2400278", "FC2400265", "FC2400254", "FC2400224",
    #     "FC2400004"
    # ]
    # for i in factures:
    #     fac=Facture.objects.get(facture_no=i)
    #     if fac.note:
    #         fac.note='OK R '+fac.note
    #     else:
    #         fac.note='OK R '
    #     fac.save()-
    #     print('>>> ', fac.total)
    #     sleep(3)
    return JsonResponse({
    'rr':'rr'
    })

def stockinitalpdcts(request):
    pdcts=Produit.objects.filter(stocktotal__lte=0)
    refs=[]
    # for i in pdcts:
    #     print('>> ', i)
    #     stockin=Stockin.objects.filter(product=i, nbon__ismanual=False)
    #     outbl=Livraisonitem.objects.filter(product=i, isfacture=False).aggregate(Sum('qty'))['qty__sum'] or 0
    #     outfacture=Outfacture.objects.filter(product=i, facture__bon__isnull=False).aggregate(Sum('qty'))['qty__sum'] or 0
    #     revbl=Livraisonitem.objects.filter(product=i, isfacture=False).aggregate(Sum('total'))['total__sum'] or 0
    #     revfacture=Outfacture.objects.filter(product=i, facture__bon__isnull=False).aggregate(Sum('total'))['total__sum'] or 0
    #     # avoir supplier is needed to be with out items
    #     avoirsupp=Returnedsupplier.objects.filter(product=i)
    #     qtyavoirsupp=avoirsupp.aggregate(Sum('qty'))['qty__sum'] or 0
    #     qtyin=stockin.aggregate(Sum('quantity'))['quantity__sum'] or 0
    #     avoirs=Returned.objects.filter(product=i)
    #     qtyavoir=avoirs.aggregate(Sum('qty'))['qty__sum'] or 0
    #     totalout=outbl+outfacture+qtyavoirsupp
    #     totalin=qtyin+qtyavoir+i.stockinitial
    #     stock=totalin-totalout
    #     realstock=i.stocktotal
    #     if not stock==realstock:
    #         # if i.stocktotal>=0:
    #         print('>> found', i.stocktotal)
    #         refs.append((stock, realstock, i.ref, i.stockinitial, abs(qtyin+qtyavoir-totalout-i.stocktotal)))
    #         i.stockinitial=0
    #         i.save()

    return JsonResponse({
        'rr':refs
    })
# this is to enter the data of facture supp manually
def achatmanual(request):
    ctx={
        'suppliers':Supplier.objects.all(),
        'today':timezone.now().date()
    }
    return render(request, 'achatmanual.html', ctx)
# this is for aachat manual
def createbonmanual(request):
    supplierid=request.GET.get('supplierid')
    nbonachat=request.GET.get('nbonachat')
    if Itemsbysupplier.objects.filter(nbon=nbonachat, supplier__id=supplierid).exists():
        print('>> exists')
        return JsonResponse({
            'success':False,
            'error': 'Facture deja existé'
        })
    datebonachat=datetime.strptime(request.GET.get('datebonachat'), '%Y-%m-%d')
    datefacture=datetime.strptime(request.GET.get('datefacture'), '%Y-%m-%d')
    totalfacture=request.GET.get('totalfacture')
    tvafacture=request.GET.get('tvafacture')
    bon=Itemsbysupplier.objects.create(
        supplier_id=supplierid,
        total=totalfacture,
        date=datefacture,
        nbon=nbonachat,
        isfacture=True,
        ismanual=True,
        tva=tvafacture,
        dateentree=datebonachat
    )

    return JsonResponse({
        'success':True,
        'bonid':bon.id
    })
def excelachatmanual(request):
    myfile = request.FILES['excelFile']
    print(myfile)
    datebonachat=datetime.strptime(request.POST.get('datebonachat'), '%Y-%m-%d')
    bonid=request.POST.get('bonid')
    supplierid=request.POST.get('supplierid')
    print('datebonachat, bonid, supplierid', datebonachat, bonid, supplierid)
    df = pd.read_excel(myfile)
    df = df.fillna(0)
    errorrefs=[]
    for d in df.itertuples():
        try:
            ref = d.ref.lower().strip()
        except:
            ref=d.ref

        try:
            product=Produit.objects.get(ref=ref)

        except Exception as e:
            errorrefs.append(ref)
    print(">>> ", errorrefs)
    if len(errorrefs)>=1:
        print('>>> returning')
        return JsonResponse({
            'success':False,
            'error':errorrefs
        })
    #name=d.name
    for d in df.itertuples():
        try:
            ref = d.ref.lower().strip()
        except:
            ref=d.ref

        product=Produit.objects.get(ref=ref)
        qty=d.qty
        pr=float(d.pr)
        # prixachat 12,0 make it 12,00
        remise=0 if pd.isna(d.remise) else int(d.remise)
        total=d.total
        product.stockfacture+=qty
        product.save()
        # last edit
        Stockin.objects.create(
            date=datebonachat,
            product=product,
            quantity=qty,
            price=pr,
            remise=remise,
            ref=ref,
            name=product.name,
            qtyofprice=qty,
            total=total,
            supplier_id=supplierid,
            nbon_id=bonid,
            facture=True
        )
    return JsonResponse({
    'success':True
    })

# this is to make all bon bon commande
def bontoboncommand(request):
    bonid=''
    clientdiver_id=3731
    bon=Bonlivraison.objects.get(pk=bonid)
    print(f'{str(bon.note)} (bon livraison => boncommande, client {bon.client.name})')
    bonitems=Livraisonitem.objects.filter(bon=bon, isfacture=False)
    print('>> length, totall', len(bonitems), bon.total)
    for i in bonitems:
        # # add qty to stock total
        i.product.stocktotal=int(i.product.stocktotal)+int(i.qty)
        i.product.save()
        # delete livraison item
        i.delete()
    # update note
    # update bon client to diver
    bon.total=0
    # make bon command not dilerverd
    bon.commande.isdelivered=False
    bon.commande.save()
    bon.note=f'{str(bon.note)} (bon livraison => boncommande, client {bon.client.name})'
    bon.client_id=clientdiver_id
    bon.save()

    return JsonResponse({
        'rr':'rr'
    })

def zf(request):
    # duplicated_refs = (
    #     Produit.objects.values('ref')
    #     .annotate(ref_count=Count('ref'))
    #     .filter(ref_count__gt=1)
    # )
    # duplicated_products = Produit.objects.filter(ref__in=[item['ref'] for item in duplicated_refs])
    #
    # ids=[i.id for i in duplicated_products]
    # return JsonResponse({
    # 'data':ids
    # })
    # ids=[611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626,627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642,643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658,659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674,675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690,691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706,707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722,723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738,739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754,755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770,771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786,787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802,803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818,819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834,835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850,851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867]
    # starting=2404628
    # for i in ids:
    #     fc=Facture.objects.get(facture_no='FC2494'+str(i))
    #     print('Fc no', fc.facture_no, 'should have', 'FC'+str(starting))
    #     fc.facture_no='FC'+str(starting)
    #     fc.save()
    #     starting+=1
    #     sleep(2)
    return JsonResponse({
    'rr':'rr'
    })



def make_product_new(request):
    pdcts=["A255V", "A262", "B2010", "B2011", "B2012", "B2015", "B2016", "B2017", "B2018", "B2019", "B2020", "B2021", "B2022", "B2024", "B2025", "B2026", "B2027", "B2028", "B2029", "B2030", "B2031", "B2032", "B2033", "B2034", "B2035", "B2036", "B2037", "B2040", "B2041", "B2042", "B2044", "B2045", "B2046", "B2047", "B2048", "B2049", "B2050", "B2051", "B2052", "B2053", "B2054", "B2055", "B2056", "B2057", "B2058", "B2059", "B2060", "B2061", "B2062", "B2063", "B2064", "B2065", "B2066", "B2067", "B2068", "B2069", "B2070", "B2071", "B2072", "C138", "C147", "GWM67A", "H237", "M188", "M200", "M205", "N143", "N154", "N210", "NF09142", "NF144", "NF332", "NF403-2", "NF545", "NF567", "NF580", "NF632", "NF676", "NF698", "NF699", "NF705", "NF840", "NF876", "O131", "R129", "R179", "S200", "T194", "T195", "T231"]
    notfound=[]
    for i in pdcts:
        try:
            tt=Produit.objects.get(ref=i.lower())
            print('>>', tt.ref)
            tt.isnew=True
            tt.save()

        except Exception as e:
            print('error >>', e)
            notfound.append(i.lower())
    return JsonResponse({
    'rr':notfound
    })

def getbonswhite(request):
    bons=Bonlivraison.objects.filter(isdelivered=False).order_by('-bon_no')
    return JsonResponse({
    'html':render(request, 'bllist.html', {'bons':bons, 'notloading':True}).content.decode('utf-8'),
    })
# make bulk facture compta from excelecheances #uizyerz5
def bulkcompta(request):
    facture=request.GET.get('facture').split(',')
    excelech_id=request.GET.get('excelech_id')
    excelech=Excelecheances.objects.get(pk=excelech_id)
    excelech.facturesaccount=True
    excelech.save()
    print('>> f', excelech.npiece)
    for i in facture:
        try:
            ff=Facture.objects.get(facture_no=f'FC{i.strip()}')
            ff.isaccount=True
            ff.save()
            print('>> no', ff.facture_no)
        except:
            pass
    return JsonResponse({
    'rr':'rr'
    })
def exportinventaire(request):
    # Query the Product model to get only 'ref' values
    print('>> getting articles')
    products = Produit.objects.order_by('category').values('category__name', 'ref', 'stocktotal')

    # Convert to a pandas DataFrame
    df = pd.DataFrame(list(products))

    # Add an empty 'qtt' column for the inventory manager to fill
    df['inventaire'] = ''

    # Create a HTTP response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=INVENTAIRE.xlsx'

    # Write the DataFrame to the Excel file using openpyxl
    print('>> CREATING EXCEL FILE')
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='INVENTAIRE', index=False)
    print('>> returning the file')
    return response

def inventaire(request):
    return render(request, 'inventaire.html')

def updatestockinv(request):
    today = timezone.now().date()
    try:
        myfile = request.FILES['excelFile']
    except:
        return JsonResponse({
        'success':False,
        'error':'no excel fichier'
        })
    df = pd.read_excel(myfile)
    entries=0
    referrors=[]
    difftracker=[]
    isinvCellEmpty=False
    for i, d in enumerate(df.itertuples()):
        if isinvCellEmpty:
            return JsonResponse({
            'success':False,
            'error':'inventaire cell vide N° '+str(i)
            })
        if pd.isna(d.inventaire) or int(d.inventaire)<0:
            print('cell is empty')
            isinvCellEmpty=True
    if isinvCellEmpty:
        return JsonResponse({
        'success':False,
        'error':'inventaire cell vide'
        })
    for d in df.itertuples():
        try:
            ref = d.ref.lower().strip()
        except:
            ref=d.ref
        inventaire = d.inventaire

        try:
            print('entering', ref)
            product=Produit.objects.get(ref=ref)
            diff=int(product.stocktotal)-int(inventaire)
            # system stock - what was found in inventaire, if the stock system is more than inventaire, the difference will be positive, means, the real stock is less than system stock, we need to deduct the diff from stock system by creating livaison items line with inventair is True, or if we have the diff is negatice, means
            print('>> diff, systemstock, inv', diff, product.stocktotal, inventaire)
            # case1: diff is negative, means that system stock is less than real stock,  systemstock 10 real stock 12 diff -2, here we willadd the 2 as a stockin kchmnd dar forurnisseur
            if diff<0:
                print('>> negative diff, creating stockin', abs(diff))
                #create a stockin line
                Stockin.objects.create(
                date=today,
                product=product,
                quantity=abs(diff),
                price=0,
                remise=0,
                qtyofprice=abs(diff),
                total=0,
                isinventaire=True
                )
                # add to stocktotal
                product.stocktotal=int(inventaire)
                # add to diff tracker
                difftracker.append(f'<tr><td>{product.ref}</td><td>{product.stocktotal}</td><td>{inventaire}</td><td>{diff}</td></tr>')
                # save product
                product.save()
            # case2: diff is more than 0, means that system stock is more than real stock,  systemstock 12 real stock 10 diff 2, here we will add the 2 as a stockout i5ssa adfo4nt 4 stock
            elif diff>0:
                print('>> positive diff, creating livraisonitem')
                #create a livraisonitem line (stockout)
                Livraisonitem.objects.create(
                    remise=0,
                    product=product,
                    qty=diff,
                    price=0,
                    total=0,
                    date=today,
                    isinventaire=True
                )
                # deduct from stock total
                product.stocktotal=int(inventaire)
                # add to diff tracker
                difftracker.append(f'<tr><td>{product.ref}</td><td>{product.stocktotal}</td><td>{inventaire}</td><td>{diff}</td></tr>')
                # save product
                product.save()
            entries+=1
        except Exception as e:
            print('>> ref not found')
            referrors.append(f">> {ref}: {e} n'existe pas dans la base de donnée")
    print('>>> enteries', entries)
    return JsonResponse({
        'success':True,
        'entries':entries,
        'referrors':referrors,
        'difftracker':difftracker
    })

def getconnected(request):
    serverip = Setting.objects.only('serverip').first()
    serverip = serverip.serverip if serverip else None
    if serverip:
        res=req.get(f'http://{serverip}/products/getconnectedusers')
        return JsonResponse(json.loads(res.text))
    return JsonResponse([], safe=False)
def getusercart(request):
    userid=request.GET.get('userid')
    serverip = Setting.objects.only('serverip').first()
    serverip = serverip.serverip if serverip else None
    if serverip:
        res=req.get(f'http://{serverip}/getitemsincart?userid='+userid)
        return JsonResponse(json.loads(res.text))
    return JsonResponse([], safe=False)
    
def getitemsinWishlist(request):
    userid=request.GET.get('userid')
    serverip = Setting.objects.only('serverip').first()
    serverip = serverip.serverip if serverip else None
    if serverip:
        res=req.get(f'http://{serverip}/getitemsinWishlist?userid='+userid)
        return JsonResponse(json.loads(res.text))
    return JsonResponse([], safe=False)
def initpage(request):
    setting=Setting.objects.first()
    ctx={
        'title':'Configuration'
    }
    if setting:
        ctx['setting']=setting
    return render(request, 'initpage.html', ctx)

def getetudesofyear(request):
    year=request.GET.get('year')
    etudes=Etude.objects.filter(created_at__year=year).order_by('-created_at')
    return JsonResponse({
    'trs':render(request, 'etudetrs.html', {"etudes":etudes}).content.decode('utf-8')
    })

def deletebonachatmanual(request):
    bon=Itemsbysupplier.objects.get(pk=request.GET.get('id'))
    bontotal=bon.total
    bonsupplier=bon.supplier
    print(bontotal, bon.supplier, bon.nbon)
    items=Stockin.objects.filter(nbon=bon)
    for i in items:
        print(i.product.ref, int(i.product.stockfacture)-int(i.quantity))
        print('>> bon is facture')
        i.product.stockfacture=int(i.product.stockfacture)-int(i.quantity)
        i.product.save()

    items.delete()
    bon.delete()
    return JsonResponse({
        'success':True
    })

def cleararrivage(request):
    categoryid=request.GET.get('categoryid')
    products=Produit.objects.filter(category_id=categoryid)
    print('>>', products[0].category)
    products.update(minstock=0)
    products.update(qtycommande=0)
    return JsonResponse({
        'success':True
    })
def yearstock(request):
    print('>> rrtttrrtt')
    today = timezone.now().date()
    date=request.GET.get('date')
    # if today.month != 12 or today.day != 31:
    #     return JsonResponse({'success': False, 'message': 'Year-end stock can only be captured on December 31.'}, status=403)
    data=YearEndStock.objects.last()
    if data and data.date == date:
        return JsonResponse({'success': False, 'message': 'les donneés deja existé'}, status=403)
    print('>>> looping')
    products = Produit.objects.all()
    for product in products:
        YearEndStock.objects.create(
        product=product,
        stocktotal=product.stocktotal,
        stockfacture=product.stockfacture,
        ref=product.ref,
        name=product.name,
        buyprice=product.buyprice,
        coutmoyen=product.coutmoyen,
        remise=product.remise,
        prixnet=product.prixnet,
        devise=product.devise,
        sellprice=product.sellprice,
        date=date
        )
    return JsonResponse({'success': True, 'message': 'Year-end stock captured successfully'})

def stockperyear(request):
    return render(request, 'stockperyear.html')

def getstockyear(request):
    date=request.GET.get('date')
    date=datetime.strptime(date, '%Y-%m-%d')
    print('>>', date.year)
    pdcts=YearEndStock.objects.filter(date__year=date.year)
    return render(request, 'stockyeartrs.html', {'products':pdcts})
def addmark(request):
    name=request.POST.get('marque')
    if Mark.objects.filter(name=name).exists():
        return JsonResponse({
            'exist':True,
            'error':'deja exist'
        })
    m=Mark.objects.create(name=name)
    serverip = Setting.objects.only('serverip').first()
    serverip = serverip.serverip if serverip else None
    mrq=Mark.objects.create(name=name)
    if serverip:
        req.post(f'http://{serverip}/products/createmarque', {
            'name':name,
        })
    return JsonResponse({
        'success':True,
        'id':m.id,
        'name':name
    })

def addcategory(request):
    name=request.POST.get('category')
    if Category.objects.filter(name=name).exists():
        return JsonResponse({
            'exist':True,
            'error':'deja exist'
        })
    m=Category.objects.create(name=name)
    serverip = Setting.objects.only('serverip').first()
    serverip = serverip.serverip if serverip else None
    if serverip:
        try:
            res=req.post(f'http://{serverip}/products/createcategory', {
                'name':name,
                # get image file
            })
            res.raise_for_status()
        except Exception as e:
            return JsonResponse({
                'success':False,
                'error':'Error in request to the server'
            })
        
    return JsonResponse({
        'success':True,
        'id':m.id,
        'name':name
    })

