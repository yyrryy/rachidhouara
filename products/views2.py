from django.shortcuts import render, redirect
from main.models import Produit, Mark, Category, Supplier, Stockin, Itemsbysupplier, Client, Represent, Order, Orderitem, Clientprices, Bonlivraison, Facture, Outfacture, Livraisonitem, PaymentClientbl, PaymentClientfc,  PaymentSupplier, Bonsregle, Returnedsupplier, Avoirclient, Returned, Avoirsupplier, Orderitem, Carlogos, Ordersnotif, Connectedusers, Promotion, UserSession, Refstats, Notavailable, Cart, Wich, Wishlist, Notification, Modifierstock, Cartitems, Notesrepresentant, Achathistory, Excelecheances
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
import openpyxl
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
today = timezone.now().date()
thisyear=timezone.now().year
