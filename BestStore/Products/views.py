from .models import Product, Category
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from collections import OrderedDict
from BestStore.settings import PRODUCTS_PER_PAGE, PAGINATION_URL
from django.contrib.auth.models import User
from .models import Wishlist


def home(request):
    """
        This will render the homepage
        :param request: Django's HTTP Request object
        :return: Rendered homepage block to base template
    """
    return render(request, "Products/homepage.html")


def product_listings(request):
    """
        List products via pagination
        :param request: Django's HTTP Request object
        :return: Rendered product list view with pagination
    """
    if request.method == 'GET':
        try:
            # Extract page parameter from page request and try to convert to int
            page = int(request.GET.get('page', 1))
        except ValueError:
            # If page argument is an alphabet this will set the page to 1
            page = 1
        # Grab all categories for filtering purposes on web page
        category = Category.objects.all()
        # Grab all products to paginate
        all_products = Product.objects.all()
        # If no products are in database then we have nothing to show the user
        if len(all_products) == 0:
            return Http404()
        # Set count of products to display for each individual page
        prods_per_page = PRODUCTS_PER_PAGE
        # Calculate total pages based on product count
        total_pages = ((abs(len(all_products)) - 1) // prods_per_page) + 1
        # Override page value if it is not a number in the valid range of pages
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        # Calculate start/end index for all_products list based on page value
        start_index = (page - 1) * prods_per_page
        end_index = start_index + prods_per_page
        # Use index slicing to get the products which are to be displayed on the rendered template
        products = all_products[start_index: end_index]
        # Set context variable for template to use to display the products and paginated navigation
        info = {
            'category': category,
            'product': products,
            'pages': range(1, total_pages + 1),
            'current_page': page,
            'prev': f'{PAGINATION_URL}{page - 1}' if page != 1 else '#',
            'next': f'{PAGINATION_URL}{page + 1}' if page != total_pages else '#',
        }
        # Render template with context containing pagination details
        return render(request, 'Products/products.html', context=info)


def cart_add(request, pk):
    """
       Add products to card
       :param request, pk: Django's HTTP Request object, Primary key of products to be added to cart
       :return: Success message
    """
    if request.method == 'GET':
        sess = request.session
        qty = request.GET.get('qty', 1)

        sess['cart_qty'] = sess.get('cart_qty', 0) + qty
        sess['cart'] = sess.get('cart', OrderedDict())

        if sess['cart'].get(pk, False):
            sess['cart'][pk]['qty'] += qty
        else:
            sess['cart'][pk] = {'qty': qty, 'pk': pk}

        return JsonResponse({'success': True})


def cart_empty(request, pk=0):
    """Empty the cart"""
    if request.method == 'GET':
        if pk == 0:
            sess = request.session
            sess['cart_qty'] = 0
            sess['cart'] = OrderedDict()
            return JsonResponse({'success': True})


def cart_item_remove(request, pk=0):
    """Remove a single item (possible multiple qty) from the cart"""
    if request.method == 'GET' and pk > 0:
        cart = request.session['cart']
        qty = request.GET.get('qty', False)

        cart_item = cart.get(str(pk), False)
        if cart_item:
            cart_item['qty'] -= int(qty)
            if cart_item['qty'] <= 0:
                del cart[str(pk)]
                request.session.modified = True
        
        return JsonResponse({'success': True})


class ProductDetailView(DetailView):
    """
        Product Detail View
        :param:
        :return: A detailed view page for a specific product using slug
    """

    model = Product
    template_name = "Products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding list range to the template context so that user can see dynamic quantity options
        context['qty'] = range(1, context['object'].quantity + 1)
        # Product model object to be used on detail page
        product = kwargs['object']
        context['image'] = product.productimages_set.all()
        return context


@login_required
def wishlist_items(request):
    try:
        user = User.objects.get(email=request.user.email)
        items = Wishlist.objects.filter(customer=request.user)
        if not len(items) == 0:
            context = {'items': items}
        else:
            context = {'no_item_found': True}
    except User.DoesNotExist:
        return redirect('Auth:loginform')
    return render(request, 'Products/wishlist.html', context)


def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        item = Product.objects.get(id=pk)
        try:
            Wishlist.objects.get(item=item)
            return 'Item Already Exists in your Wishlist'
        except Wishlist.DoesNotExist:
            # image = ProductImage.objects.filter(product=product).first()
            Wishlist.objects.create(customer=request.user, item=item)
            return 'Item Added To Wishlist successfully'
    else:
        return 'Login To Save This to your Wishlist'


@login_required
def add_wishlist_to_cart(request, product_id):
    cart_add(request, product_id)
    delete_from_wishlist(request, product_id)
    return HttpResponse(wishlist_items(request))

@login_required
def delete_from_wishlist(request, pk):
    try:
        user = User.objects.get(email=request.user.email)
        item = Wishlist.objects.get(product_id=pk)
        item.delete()
        items = Wishlist.objects.filter(customer=request.user)
        context = {'items': items}
        # import pdb; pdb.set_trace()
        if not len(items) == 0:
            if request.method == 'POST':
                Wishlist.objects.filter(id=pk).delete()
                context = {'items': items}
        else:
            context = {'no_item_found': True}
        return HttpResponse(wishlist_items(request))
    except User.DoesNotExist:
        return redirect('accounts:login_app')

