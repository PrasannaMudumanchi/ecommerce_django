from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item,Order,OrderItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
def index(request):
    context ={
        "items" :Item.objects.all()
    }
    return render(request, 'home/index.html',context)
def checkout1(request):  
    return render(request,'home/checkout.html')
class Index(ListView):
    model = Item
    paginate_by = 12
    template_name = 'home/index.html'

def product(request):
    return render(request,'home/products.html')

class ItemDetailedView(DetailView):
    model = Item
    template_name = 'home/products.html'
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("ecommerce_site:order_summery")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("ecommerce_site:order_summery" )
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("ecommerce_site:product",slug =slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            # return redirect("ecommerce_site:order_summary") 
            return redirect("ecommerce_site:product",slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            # return redirect("ecommerce_site:product", slug=slug)
            return redirect("ecommerce_site:product",slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        # return redirect("ecommerce_site:product", slug=slug)
        return redirect("ecommerce_site:product",slug=slug)
@login_required  
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("ecommerce_site:order_summery" )
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("ecommerce_site:order_summery" )
    else:
        messages.info(request, "You do not have an active order")
        return redirect("ecommerce_site:order_summery" )


class OrderSummery(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered =False)
        context = {
            "object":order 
        }
        return render(self.request,'home/order_summery.html',context)