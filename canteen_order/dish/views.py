from django.shortcuts import render
from django.contrib import messages
from .forms import DishForm
from .models import Dish, Orders

ordered_dishes = []
ordered_sum = 0
store_id = 0

# Create your views here.
def show_store(request):
    global store_id
    store_id = request.GET.get('store_id')
    context = {
        'store': store_id,
        'dish_list': Dish.objects.filter(store_id=store_id),
    }
    combined_context = {**locals(), **context}
    return render(request, 'dish/store_base.html', combined_context)

def get_order(request):
    global ordered_dishes
    global ordered_sum
    global store_id
    if request.method == "GET":
        dish_id = int(request.GET.get('dish_id'))
        count = int(request.GET.get('count'))
        storage = Dish.objects.get(dish_id=dish_id).dish_store
        if count > storage:
            count = storage
        for i in range(0, count):
            ordered_dishes.append(Dish.objects.get(dish_id=dish_id).dish_name)
            ordered_sum = ordered_sum + Dish.objects.get(dish_id=dish_id).dish_price
        messages.success(request, "操作成功")
        print("[DEBUG][POST][STATE]:ordered_sum : {}", ordered_sum)
    context = {
        'store': store_id,
        'dish_list': Dish.objects.filter(store_id=store_id),
    }
    combined_context = {**locals(), **context}
    return render(request, 'dish/store_base.html', combined_context)

def del_order(request):
    global ordered_dishes
    global ordered_sum
    global store_id
    if request.method == "GET":
        is_success = True
        dish_id = int(request.GET.get('dish_id'))
        count = int(request.GET.get('count'))
        for i in range(0, count):
            if ordered_sum <= 0:
                ordered_sum = 0
                ordered_dishes.clear()
                messages.error(request, "购物车已空")
                is_success = False
                break
            try:
                ordered_dishes.index(Dish.objects.get(dish_id=dish_id).dish_name)
                ordered_dishes.remove(Dish.objects.get(dish_id=dish_id).dish_name)
                ordered_sum = ordered_sum - Dish.objects.get(dish_id=dish_id).dish_price
                print("[DEBUG][POST][STATE]:ordered_sum : {}", ordered_sum)
            except:
                continue
        if is_success:
            messages.success(request, "操作成功")
    context = {
        'store': store_id,
        'dish_list': Dish.objects.filter(store_id=store_id),
    }
    combined_context = {**locals(), **context}
    return render(request, 'dish/store_base.html', combined_context)
    
def submit_order(request):
    global ordered_dishes
    global ordered_sum
    global store_id
    result_string = ";".join(ordered_dishes)
    new_or = Orders.objects.create(user=request.session['user_name'], store=store_id, total=ordered_sum, dish_list=result_string)
    new_or.save()
    for item in ordered_dishes:
        old_store = Dish.objects.get(dish_name = item).dish_store
        old_sales = Dish.objects.get(dish_name = item).dish_sales
        Dish.objects.filter(dish_name=item).update(dish_store=old_store - 1, dish_sales=old_sales + 1)
    ordered_sum = 0
    ordered_dishes.clear()
    return render(request, 'index.html', locals())

def del_dish(request):
    dish_id = request.GET.get('dish_id')
    Dish.objects.filter(dish_id=dish_id).delete()
    context = {
        'dish_list': Dish.objects.filter(store_id=request.session['user_id'])
    }
    combined_context = {**locals(), **context}
    return render(request, 'admin_index.html', combined_context)

def add_dish(request):
    dish_form = DishForm()
    if request.method == "POST":
        dish_form = DishForm(request.POST)
        if dish_form.is_valid():
            Dish.objects.create(dish_name=dish_form.cleaned_data['dish_name'], dish_intro=dish_form.cleaned_data['dish_intro'], dish_price=dish_form.cleaned_data['dish_price'], dish_store=dish_form.cleaned_data['dish_store'], store_id=request.session['user_id'], dish_sales=0)
    context = {
        'dish_list': Dish.objects.filter(store_id=request.session['user_id'])
    }
    combined_context = {**locals(), **context}
    return render(request, 'admin_index.html', combined_context)
    
def receive_order(request):
    order_id = request.GET.get('order_id')
    print("[DEBUG][POST][STATE]:haha")
    if order_id:
        print("[DEBUG][POST][STATE]:id?{}", order_id)
        Orders.objects.filter(order_id=order_id).update(status=1)
    context = {
        'order_list': Orders.objects.filter(store=request.session['user_id'])
    }
    combined_context = {**locals(), **context}
    return render(request, 'dish/show_orders.html', combined_context)