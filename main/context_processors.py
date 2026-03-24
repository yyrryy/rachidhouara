from .models import Shippingfees

# inject cities in the base template
def cities(request):
    return {
        'cities': Shippingfees.objects.all()
    }