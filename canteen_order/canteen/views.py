from django.shortcuts import render
from django.contrib import messages
from .models import Canteen, Store

def index(request):
    context = {
        'canteen_list': Canteen.objects.all(),
        'store_list': Store.objects.all(),
    }
    combined_context = {**locals(), **context}
    return render(request, 'canteen/canteen_base.html', combined_context)