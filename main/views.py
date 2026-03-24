
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Category, Client, Order, Orderitem, Produit, Client, Mark, Cart, Connectedusers, Represent, Promotion, Cartitems
import pandas as pd
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import OuterRef, Exists, Count
import uuid
# import csrf_exampt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models import Q
import datetime
from django.utils import timezone
from itertools import chain
import requests as req


def product(request, id):
    product=Produit.objects.get(pk=id)
    regex_pattern = rf'(^|\s){product.ref.upper()}(\s|$)'
    equiv=Produit.objects.filter(equivalent__iregex=regex_pattern)
    return render(request, 'product.html', {'product':product, 'title':product.name, 'equiv':equiv})


def searchref(request):
    ref=request.POST.get('ref').strip().lower()
    search_terms = ref.split('+')
    # search ref first
    productsref=Produit.objects.filter(ref__icontains=ref)
    q_objects = Q()
    for term in ref.split('+'):
        print('>>> ', term)
        q_objects &= (Q(ref__icontains=term) | Q(name__icontains=term) | Q(category__name__icontains=term) |  Q(mark__name__icontains=term) |  Q(equivalent__icontains=term)  |  Q(cars__icontains=term))
    # Perform the broader query, excluding products already in `productsref`
    products_broad = Produit.objects.filter(q_objects).exclude(id__in=productsref)

    # Combine both querysets, prioritizing `productsref`
    products = list(chain(productsref, products_broad))[:50]

    return JsonResponse({
        'data':render(request, 'searchref.html', {'products':products}).content.decode('utf-8')
    })

# users groups
# chack if user's group in accounting
def isaccounting(user):
    return (user.groups.filter(name='accounting').exists() or user.groups.filter(name='admin').exists() )

# chack if user's group in salsemen
def issalsemen(user):
    return user.groups.filter(name='salsemen').exists()

def isclient(user):
    return user.groups.filter(name='clients').exists()

def tocatalog(user):
    return (user.groups.filter(name='salsemen').exists() or user.groups.filter(name='clients').exists() or user.groups.filter(name='admin').exists() )

def bothsalseaccount(user):
    return (user.groups.filter(name='salsemen').exists() or user.groups.filter(name='accounting').exists() or user.groups.filter(name='admin').exists() )

def isadmin(user):
    return user.groups.filter(name='admin').exists()


# Create your views here.
def home(request):
    # print(request.user)
    print(request.user.groups.first())
    if request.user.groups.first():
        if (request.user.groups.first().name=='salsemen'):
            return redirect(catalog)
        if (request.user.groups.first().name=='accounting'):
            return redirect(orders)
        if (request.user.groups.first().name=='admin'):
            return redirect('products:system')
    
    return redirect('main:loginpage')
    
    if request.user.groups.all():
        if request.user.groups.first().name=='admin':
            return redirect('products:system')
    # print(request.user)
    # print(request.user.groups.first())
    # if request.user.groups.first():
    #     if (request.user.groups.first().name=='salsemen'):
    #         return redirect('main:catalog')
    #     if (request.user.groups.first().name=='accounting'):
    #         return redirect('main:''main:orders')
    #     if (request.user.groups.first().name=='admin'):
    #         return redirect('main:''main:orders')
    # return redirect('main:''main:loginpage')
    # return render(request, 'main.html', ctx)
    
    # this is for the front page
    #return render(request, 'main.html')


def about(request):
    return render(request, 'about.html')
def partners(request):
    return render(request, 'marques.html')

def profile(request):
    return render(request, 'profile.html')

def loginpage(request):
    print(request.user.groups.all())
    if request.user.groups.all():
        if (request.user.groups.first().name=='salsemen'):
            return redirect('main:catalog')
        if (request.user.groups.first().name=='accounting'):
            return redirect('main:orders')
        if (request.user.groups.first().name=='admin'):
            return redirect('product:system')
        if (request.user.groups.first().name=='clients'):
            return redirect('main:catalog')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group=user.groups.all().first().name
            if group == 'salsemen':
                return redirect('main:catalog')
            elif group=='clients':
                return redirect('main:catalog')
            elif group == 'accounting':
                return redirect('main:orders')
            elif group == 'admin':
                return redirect('products:system')
        else:
            return redirect('main:loginpage')
    ctx={
        'title':'SYSTEM LOGIN'
    }
    return render(request, 'login.html', ctx)


@csrf_exempt
def editinfoclient(request):
    client=Client.objects.get(user_id=request.user.id)
    print(client.name)
    client.name=request.POST.get('name').strip()
    client.phone=request.POST.get('phone').strip()
    client.address=request.POST.get('address').strip()
    client.city=request.POST.get('city').strip()
    client.save()
    return redirect('main:profile')

@login_required(login_url='/login')
@csrf_exempt
def updatepassword(request):
    user=User.objects.get(pk=request.user.id)
    print(request.user.id)
    user.set_password(request.POST.get('cpass'))
    user.save()
    login(request, user)
    return redirect('main:profile')






def filters(request):
    # calls.html will handle the data
    # get call from the request
    category=request.POST.get('category') or None
    brand=request.POST.get('brand') or None
    model=request.POST.get('model') or None
    mark=request.POST.get('mark') or None
    products=''
    # filter logic



    if category and brand and model and mark:
        # get the products from the db
        products=Produit.objects.filter(category=category, brand=brand, model=model, mark=mark)
    elif category and brand:
        # get the products from the db
        products=Produit.objects.filter(category=category, brand=brand)
    elif category and model:
        # get the products from the db
        products=Produit.objects.filter(category=category, model=model)
    elif category and mark:
        products=Produit.objects.filter(category=category, mark=mark)

    elif brand and model:
        # get the products from the db
        products=Produit.objects.filter(brand=brand, model=model)
    elif brand and mark:
        products=Produit.objects.filter(brand=brand, mark=mark)
    elif model and mark:
        products=Produit.objects.filter(model=model, mark=mark)
    elif category:
        # get the products from the db
        products=Produit.objects.filter(category=category)
    elif brand:
        # get the products from the db
        products=Produit.objects.filter(brand=brand)
    elif model:
        # get the products from the db
        products=Produit.objects.filter(model=model)
    elif mark:
        products=Produit.objects.filter(mark=mark)
    return JsonResponse({
        'data':render(request, 'calls.html', {'products':products}).content.decode('utf-8')
    })

@user_passes_test(isadmin, login_url='loginpage')
@login_required(login_url='loginpage')
def create(request):
    # get category from db
    categories=Category.objects.all()
    # get brand from db
    return render(request, 'create.html', {'categories':categories, 'title':'add bulk'})


# add category ajax route
def addcategory(request):
    # get category from request
    category=request.POST.get('category')
    Category(title=category).save()
    return redirect('main:create')

def addbrand(request):
    # get category from request
    brand=request.POST.get('brand')
    print(brand)
    Brand(name=brand).save()
    return redirect('main:create')

def addmark(request):
    # get category from request
    mark=request.POST.get('mark')
    print(mark)
    Mark(name=mark).save()
    return redirect('main:create')

@login_required(login_url='loginpage')
def addbulk(request):
    myfile = request.FILES['fileinaddbulk']
    categoryid=request.POST.get('categoryinaddbulk')
    df = pd.read_excel(myfile)
    df = df.fillna('')
    for d in df.itertuples():
        pr=Produit.objects.create(
            ref=str(d.ref).lower(),
            name=d.name.lower(),
            category_id=categoryid,
            sellprice=round(d.price, 2),
            mark_id=None if pd.isna(d.mark) else d.mark,
        )
        # try:
        #     pr = Produit.objects.get(ref=str(d.ref).lower(), category_id=None if pd.isna(d.category) else d.category)
        #     pr.name = d.name.lower()
        #     pr.price = round(d.price, 2)
        #     pr.image.name=None if pd.isna(d.image) else d.image
        #     pr.save()
        # except:
        #     # Create a new Produit object if it doesn't exist
        #     pr=Produit.objects.create(
        #         ref=str(d.ref).lower(),
        #         name=d.name.lower(),
        #         category_id=None if pd.isna(d.category) else d.category,
        #         price=round(d.price, 2),
        #         mark_id=None if pd.isna(d.mark) else d.mark,
        #     )
        #     # if image is not empty assign it
        pr.image.name=None if pd.isna(d.image) else d.image
        pr.save()
    return redirect('products:addproductspage')
    # return JsonResponse({
    #     'success':True
    # })

@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def commande(request):
    # clientname=request.POST.get('clientname')
    # clientaddress=request.POST.get('clientaddress')
    # clientphone=request.POST.get('clientphone')
    #total=request.POST.get('total') 
    modpymnt=request.POST.get('modpymnt')
    modlvrsn=request.POST.get('modlvrsn')
    clientid=request.POST.get('clientid')
    
    #to know if the client is the one placed the order
    isclient=request.POST.get('isclient')=='true' 
    #totalremise=request.POST.get('totalremise', 0)
    cart=Cart.objects.filter(user=request.user).first()
    if cart:
        cartitems=Cartitems.objects.filter(cart=cart)
        if isclient:
            order=Order.objects.create(client_id=clientid,total=cart.total, modpymnt=modpymnt, modlvrsn=modlvrsn, code=str(uuid.uuid4()), isclient=isclient)
        else:
            # add salesman
            order=Order.objects.create(client_id=clientid, salseman=request.user.represent, total=cart.total, modpymnt=modpymnt, modlvrsn=modlvrsn, code=str(uuid.uuid4()), isclient=isclient)
        
        for i in cartitems:
            Orderitem.objects.create(order=order, product=i.product, ref=i.product.ref, name=i.product.name, qty=i.qty, total=i.total)
        # return a json res
        cart.delete()
        # send_mail(message='Nouveau commande.', subject=f'Nouveau commande. #{order.id}')
        #threading.Thread(target=send_mail, args=('Nouveau commande.', f'Nouveau commande. #{order.id}', 'abdelwahedaitali@gmail.com', ['aitaliabdelwahed@gmail.com'], False)).start()
        return JsonResponse({
            'valid':True,
            'message':'Commande enregistrée avec succès',
            'id':order.code
        })
    return JsonResponse({
        'valid':False,
        'message':'Panier vide'
    })






@user_passes_test(isaccounting, login_url='loginpage')
@login_required(login_url='loginpage')
def orders(request):
    # get orders from db and order them by date ascendant
    orders=Order.objects.all()
    delivered=len(Order.objects.all().filter(isdelivered=True))
    paied=len(Order.objects.all().filter(ispaied=True))

    return render(request, 'orders.html', {'orders':orders, 'delivered':delivered, 'title':'Commandes', 'notdel':len(orders)-delivered, 'paied':paied})


def orderitems(request, id):
    orderitems=Orderitem.objects.filter(order=id)
    order=Order.objects.get(pk=id)
    return JsonResponse({
        'data':render(request, 'orderitems.html', {'orderitems':orderitems, 'order':order}).content.decode('utf-8')
    })


def dilevered(request, id):
    order=Order.objects.get(pk=id)
    order.isdelivered=True
    order.save()
    return JsonResponse({
        'success':True
    })
def excel(request):
    # Get the order ID from the query parameters
    order_id = request.GET.get('id')
    
    # Fetch the order and its related items
    order = Order.objects.get(pk=order_id)
    orderitems = Orderitem.objects.filter(order=order)

    # Extract only the required fields: ref, name, qty
    data = orderitems.values('ref', 'name', 'qty')

    # Convert the filtered data to a pandas DataFrame
    df = pd.DataFrame(list(data))

    # Prepare the HttpResponse with the Excel file content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.xlsx"'

    # Write the DataFrame to the Excel file and send it as a response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response


def paied(request, id):
    order=Order.objects.get(pk=id)
    order.ispaied=True
    order.save()
    return redirect('main:orders')


# gets products after clicking on a category
@user_passes_test(tocatalog, login_url='loginpage')
@login_required(login_url='loginpage')
def products(request, id):
    # get the products from the db
    c=Mark.objects.get(pk=id)
    products=Produit.objects.filter(mark_id=id, isactive=True)
    return render(request, 'products.html', {'products':products, 'title':'Produits de '+str(c), 'category':c})


def productscategories(request, id):
    # get the products from the db
    c=Category.objects.get(pk=id)
    products=Produit.objects.filter(category_id=id, isactive=True).order_by('code')
    return render(request, 'products.html', {'products':products, 'title':'Produits de '+str(c), 'category':c})

@user_passes_test(isadmin, login_url='loginpage')
@login_required(login_url='loginpage')
def dashboard(request):
    ctx={
        'title':'Dashboard',
        'orders':Order.objects.filter(date__date=datetime.date.today()).count(),
        'monthorders':Order.objects.filter(date__month=datetime.date.today().month).count(),
        'clientscount':Client.objects.all().count(),
        'products':Produit.objects.all().count(),
        'productthismonth':Orderitem.objects.filter(order__date__month=datetime.date.today().month).order_by('-qty')[:20],

    }
    return render(request, 'dashboard.html', ctx)

#@user_passes_test(tocatalog, login_url='loginpage')
#@login_required(login_url='loginpage')
def catalog(request):
    # categories = Category.objects.annotate(
    #     has_promotion=Exists(Produit.objects.filter(category_id=OuterRef('pk'), isoffer=True)),
    #     total_products=Count('produit')
    # )
    constraction=False
    if constraction:
        return render(request, 'constraction.html', {'title':'Under Constraction'})
    promotions=Promotion.objects.filter(info='active')
    marks = Mark.objects.annotate(
        has_promotion=Exists(Produit.objects.filter(mark_id=OuterRef('pk'), isoffer=True)),
        total_products=Count('produit')
    )
    categories = Category.objects.order_by('code').annotate(
        has_promotion=Exists(Produit.objects.filter(mark_id=OuterRef('pk'), isoffer=True, isactive=True)),
        total_products=Count('produit')
    )
    ctx={
            'categories': categories,
            'clients':Client.objects.all(),
            'title':'Catalog',
            'cc':marks,
            'promotions':promotions
        }
    return render(request, 'catalog.html', ctx)

#@user_passes_test(bothsalseaccount, login_url='loginpage')
@login_required(login_url='loginpage')
def ordersforeach(request):
    # get id of request user
    if request.user.groups.filter(name='salsemen').exists():
        orders=Order.objects.filter(salseman=request.user.represent)
    else:
        orders=Order.objects.filter(client=request.user.client)
    delivered=len(orders.filter(isdelivered=True))
    #paied=len(orders.filter(ispaied=True))

    return render(request, 'orders.html', {'orders':orders, 'delivered':delivered, 'title':'Commandes', 'notdel':len(orders)-delivered, 'paied':paied})
@user_passes_test(bothsalseaccount, login_url='loginpage')
@login_required(login_url='loginpage')
def salsemanorders(request, str_id):
    orders=Order.objects.get(code=str_id)
    items=Orderitem.objects.filter(order=orders.id)
    return render(request, 'salsemanorders.html', {'order':orders, 'items':items, 'title':'Commande #'+str(orders.id)})




def clients(request):
    clients=Client.objects.all()
    # Convert the QuerySet to a list of dictionaries
    data = list(clients.values())

    # Serialize the list as JSON
    json_data = json.dumps(data)
    # return a json response with clients as clients
    return JsonResponse({
        'clients':json_data
    })


def addclient(request):
    name=request.POST.get('name')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    city=request.POST.get('city')
    Client.objects.create(name=name, phone=phone, address=address, city=city)
    options=['<option value="'+str(i.id)+'">'+i.name+' | '+i.city+'</option>' for i in Client.objects.all().order_by('-id')]
    print(options)
    return JsonResponse({
        'options':options,
    })

def logoutuser(request):
    logout(request)
    return redirect('main:loginpage')


def aboutus(request):
    return render(request, 'aboutus.html', {'title':'A propos de nous'})

def create_product(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    offre=request.POST.get('offre')
    min=request.POST.get('min')
    ref=request.POST.get('ref')
    category=request.POST.get('category')
    print(name, price, offre, min, ref, category)
    # Create the product object
    product = Produit(name=name, price=price
    , offre=offre, min=min, ref=ref, category=Category.objects.get(pk=category))


    product.save()
    return redirect('main:create')

@user_passes_test(tocatalog, login_url='loginpage')
def cart(request):
    cartitems=Cartitems.objects.filter(cart__user=request.user)
    print('>>>>>', cartitems)
    ctx={
        'title':'Panier',
        'cartitems':cartitems
    }
    if request.user.groups.all().first().name=="salsemen":
        clients=Client.objects.all()
        ctx['clients']=clients
    
    return render(request, 'cart.html', ctx)

def developer(request):
    return render(request, 'me.html', {'title':'Develper - abdelwahed ait ali'})

# def signup(request):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         usename=request.POST.get('usename')
        
#         return redirect('loginpage')


def sitemap(request):
    # Get the base URL for the sitemap
    host_base = request.build_absolute_uri(reverse("home"))

    # Static routes with static content
    static_urls = []
    for url in ["aboutus", "#contactus", "partners", "catalog"]:
        static_urls.append({"loc": f"{host_base}{url}"})

    # Render the sitemap template
    context = {"static_urls": static_urls}
    sitemap_xml = render(request, "sitemap.xml", context, content_type="application/xml")

    # Return the sitemap as an HTTP response with the appropriate content type
    return HttpResponse(sitemap_xml, content_type="application/xml")
def getcartitems(request):
    length=0
    item=[]
    cart=Cart.objects.filter(user=request.user).first()
    if cart:
        length=len(Cartitems.objects.filter(cart=cart))
        item=list(Cartitems.objects.filter(cart=cart).values())
    return JsonResponse({
        'length':length,
        'items':item
    })

def addtocart(request):
    productid=request.GET.get('productid')
    qty=request.GET.get('qty')
    product=Produit.objects.get(pk=productid)
    print(qty, product)
    total=round(float(qty)*float(product.sellprice), 2)
    print(total, product)
    user=request.user
    cart=Cart.objects.filter(user=user).first()
    
    if cart:
        print('>>>>cart already')
        cartitem=Cartitems.objects.filter(cart=cart, product=product).first()
        if cartitem:
            return JsonResponse({
                'success':False
            })
        else:
            Cartitems.objects.create(cart=cart, product=product, qty=qty, total=total)
            cart.total+=total
        cart.save()
        
    else:
        cart=Cart.objects.create(user=user, total=total)
        Cartitems.objects.create(cart=cart, product=product, qty=qty, total=total)
    return JsonResponse({
        'success':True
    })
    
def edititemincart(request):
    cartitem=Cartitems.objects.get(pk=request.GET.get('cartitemid'))
    qty=request.GET.get('qty')
    total=round(float(cartitem.product.price)*float(qty), 2)
    cart=cartitem.cart
    # new cart total
    newtotal=cart.total-cartitem.total+total
    cart.total=newtotal
    cart.save()
    cartitem.total=total
    cartitem.qty=qty
    cartitem.save()
    return JsonResponse({
        'total':cart.total
    })

def removeitemincart(request):
    cartitem=Cartitems.objects.get(pk=request.GET.get('cartitemid'))
    cart=cartitem.cart
    cart.total-=cartitem.total
    cart.save()
    cartitem.delete()
    return JsonResponse({
        'total':cart.total
    })


def makeuserconnected(request):
    if not (request.user.groups.all()[0].name=='admin'):
        try:
            useralready=Connectedusers.objects.get(user=request.user)
            useralready.activity=request.GET.get('activity')
            useralready.lasttime=timezone.now()
            useralready.save()
        except:
            Connectedusers.objects.create(user=request.user, activity=request.GET.get('activity'))
        print('user connecte')
    return JsonResponse({
        'success':True
    })

def getpdctfordash(request):
    ref=request.GET.get('ref').lower()
    print('>>> ref', ref)
    res=[]
    
    products=Produit.objects.filter(ref__icontains=ref)
    print('>> pdcts', products)
    # for i in products:
    #     data={
    #         'image':i.image.url if i.image else '',
    #         'ref':i.ref.upper(),
    #         'price':i.sellprice,
    #         'id':i.id,
    #         'equivalent':i.equivalent.upper(),
    #     }
    #     res.append(data)
    ctx={
        'products':products,
        'categories':Category.objects.all(),
        'marks':Mark.objects.all(),
    }
    return JsonResponse({
        'products':render(request, 'pdctsdash.html', ctx).content.decode('utf-8'),
        'success':True
    })
    
    
def updateproduct(request):
    pdctid=request.POST.get('pdctid')
    price=request.POST.get('price')
    activation=request.POST.get('activation')
    category=request.POST.get('category')
    mark=request.POST.get('mark')
    print('activation', activation)
    # offre=request.POST.get('offre')
    # isoffer=request.POST.get('isoffer')=='true'
    image=request.FILES.get('image', None)
    equivalent=request.POST.get('equivalent').strip().upper()
    # cars=request.POST.get('cars').strip().upper()
    ref=request.POST.get('ref').lower()
    print('>>> dctid, ref', pdctid, ref)
    if Produit.objects.filter(ref=ref).exclude(pk=int(pdctid)).exists():
        return JsonResponse({
            'success':False,
            'error':'Ref deja existe'
        })
    product=Produit.objects.get(pk=pdctid)
    product.sellprice=price
    product.equivalent=equivalent
    # product.cars=cars
    product.ref=ref
    product.category_id=category
    product.mark_id=mark
    product.active=activation=="on"
    # product.isoffer=isoffer
    # product.offre=offre
    if image:
        product.image=image
    product.save()
    return JsonResponse({
        'success':True,
        'error':'Ref deja existe'
    })
    
def listsamesmen(request):
    reps=Commercial.objects.all()
    ctx={
        'title':'List commeciaux',
        'reps':reps
    }
    return render(request, 'listsamesmen.html', ctx)
    
def listclients(request):
    try:
        lastcode = Client.objects.order_by('code').last()
        print('lastcode', lastcode.code)
        if lastcode:

            codecl = f"{int(lastcode.code) + 1:07}"
        else:
            codecl = f"0000001"
    except:
        codecl="0000001"
    ctx={
        'title':'List clients',
        'clients':Client.objects.all(),
        'commerciaux':Represent.objects.all(),
        'lastcode':codecl
    }
    return render(request, 'listclients.html', ctx)

def getsimilar(request):
    ref=request.GET.get('ref').lower()
    regex_pattern = rf'(^|\s){ref.upper()}(\s|$)'
    products=Produit.objects.filter(isactive=True, equivalent__iregex=regex_pattern)
    return JsonResponse({
        'products':render(request, 'similarproducts.html', {'products':products, 'ref':ref.upper()}).content.decode('utf-8'),
        
    })

