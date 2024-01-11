# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Cart, Order, Souhait
from django.contrib.auth.decorators import login_required
from django.utils import timezone 

# Vue pour afficher la page principale avec tous les produits
def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

# Vue pour afficher les détails d'un produit spécifique
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', {'product': product})

# Vue pour ajouter un produit au panier
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    # Récupérer ou créer le panier de l'utilisateur
    cart, _ = Cart.objects.get_or_create(user=user)

    # Récupérer l'article correspondant ou le créer
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product, cart=cart)

    if created:
        cart.orders.add(order)  # Ajouter l'article au panier
        cart.save()
    else:
        order.quantity += 1
        order.save()

    # Rediriger vers la page précédente
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# Vue pour afficher le contenu du panier
def display_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', {'orders': cart.orders.all()})

# Vue pour supprimer le panier de l'utilisateur
def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect('index')

# Vue pour rechercher des produits
def search(request):
    query = request.GET["article"]
    products = Product.objects.filter(name__icontains=query)
    return render(request, "store/search.html", {"products": products})

# Vues pour filtrer les produits par catégorie
def get_ordinateurs(request):
    category_name = 'Ordinateurs'
    products = Product.objects.filter(category__name__icontains=category_name)
    return render(request, "store/ordinateurs.html", {"products": products})

def get_smartphones(request):
    category_name = 'Smartphones'
    products = Product.objects.filter(category__name__icontains=category_name)
    return render(request, "store/smartphones.html", {"products": products})

def get_cameras(request):
    category_name = 'Caméras'
    products = Product.objects.filter(category__name__icontains=category_name)
    return render(request, "store/cameras.html", {"products": products})

def get_accessoires(request):
    category_name = 'Accessoires'
    products = Product.objects.filter(category__name__icontains=category_name)
    return render(request, "store/accessoires.html", {"products": products})

# Vue pour afficher le contenu de la liste de souhaits
def display_souhaits(request):
    souhait = get_object_or_404(Souhait, user=request.user)
    return render(request, 'store/souhaits.html', {'orders': souhait.orders.all()})

# Vue pour ajouter un produit à la liste de souhaits
def add_to_souhaits(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    souhaits, _ = Souhait.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product, souhait=souhaits)

    if created:
        souhaits.orders.add(order)
        souhaits.save()
    else:
        order.quantity += 1
        order.save()

    # Rediriger vers la page précédente
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def display_invoice(request):
    user_orders = Order.objects.filter(user=request.user, ordered=False, cart__isnull=False)

    for order in user_orders:
        order.total_price = order.product.price * order.quantity

    total_price = sum(order.total_price for order in user_orders)
    date = timezone.now().strftime("%d-%m-%Y à %H:%M:%S")

    return render(request, 'store/invoice.html', {'user_orders': user_orders, 'total_price': total_price, 'date': date})

