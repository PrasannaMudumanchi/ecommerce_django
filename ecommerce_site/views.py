from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
# Create your views here.
from django.views.generic import ListView, DetailView, View
from django.utils import timezone


def index(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'home/index.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm
        context = {
            'form': form
        }
        return render(self.request, 'home/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print("The form is valid")
            return redirect('ecommerce_site:checkout')

# def checkout1(request):
#     return render(request, 'home/checkout.html')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'home/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect("/")


class Index(ListView):
    model = Item
    paginate_by = 12
    template_name = 'home/index.html'


def product(request):
    return render(request, 'home/products.html')

# def index(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'home/index.html', context)


class HomeView(ListView):
    model = Item
    paginate_by = 2
    template_name = 'home/index.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'home/product.html'


def checkout(request):
    return render(request, "home/checkout.html")


# def products(request):
#     return render(request, "home/product.html")
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
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item quantity was updated")
            return redirect("ecommerce_site:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This Item was added to the cart")
            return redirect("ecommerce_site:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item quantity was updated")
        return redirect("ecommerce_site:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item is removed from the cart")
            print("######")
            return redirect("ecommerce_site:product", slug=slug)
        else:
            # add additional message
            messages.info(request, "This item is not present in cart")
            return redirect("ecommerce_site:product", slug=slug)
    else:
        messages.info(request, "You dont have an Order")
        return redirect("ecommerce_site:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in order
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
            messages.info(request, "This item quantity updated")
            print("######")
            return redirect("ecommerce_site:order-summary")
        else:
            # add additional message
            messages.info(request, "This item is not present in cart")
            return redirect("ecommerce_site:product", slug=slug)
    else:
        messages.info(request, "You dont have an Order")
        return redirect("ecommerce_site:product", slug=slug)
