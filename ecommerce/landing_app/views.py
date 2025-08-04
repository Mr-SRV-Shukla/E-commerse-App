    """_summary_

    Returns:
        _type_: _description_
    """
#python library
from math import ceil

#django library
from django.shortcuts import render
from django.http import HttpResponse
#current date
from django.utils import timezone
#Caches and radis
from django.core.cache import cache

# local import
#product display
from landing_app.models import Product

"""this is check"""
def check_methods(request):
    """_summary_

    Args:
        request (_type_): _description_
    """    
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)
    product_category = request.POST.get('product_category')

    # If product_category is None or empty, return None (let ShoesProducts handle it)
    if not product_category:
        return None  # Allow ShoesProducts to handle this

    allProds = []
    
    # Handle 'all' and other cases
    if product_category == 'All':
        catprods = Product.objects.all()  # Fetch all products
    elif product_category == 'NewAddedProduct':
        current_date = timezone.now().date()
        catprods = Product.objects.filter(date_field=current_date)
    elif product_category == 'TopBrands':
        catprods = Product.objects.filter(rating_field=int(4))
    else:
        catprods = Product.objects.filter(category=product_category)  # Fetch products randomly
    
    # Calculate slides
    n = len(catprods)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # Prepare context and render the template
    AddedItems=getProductId(request)
    allProds.append([catprods, nSlides,AddedItems,product_category])
    params = {'allProds': allProds}
    return render(request, "products/all_products_iteams.html", params)


def getProductId(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """    
    Product_id=request.POST.get('productId')
    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(Product_id)
        if quantity:
            cart[Product_id]=quantity+1
        else:
            cart[Product_id]=1
    else:
        cart={}
        cart[Product_id]=1
    
    request.session['cart']=cart

    cleaned_data = {int(k): v for k, v in cart.items() if k is not None and k.isdigit()}

    total_sum = sum(cleaned_data.values())
    added_items_info={
        'cart':cart,
        'totalCartItenSum': total_sum
    }
    
    return added_items_info

def home(request):
    """AI is creating summary for home

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    request.user
    allProds=[]
    catprods=Product.objects.values()
    n=len(catprods)
    catprods=Product.objects.values()
    
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([catprods, nSlides,AddedItems,""])
    
    params={'allProds': allProds}
    # cache.set('allProds',allProds)
    # cache.get()
    return render(request, "products/all_products.html", params)


def allProducts(request):
    catprods=cache.get('all_catprods')
    request.user
    allProds=[]
    if catprods is None:
        catprods=Product.objects.values().order_by('?')
        cache.set('all_catprods',catprods,timeout=90)
    n=len(catprods)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([catprods, nSlides,AddedItems," "])
    params={'allProds': allProds}
    return render(request, "products/all_products.html", params)

def allProducts_iteams(request):
    if request.method == 'POST':
        return check_methods(request)  # Return the response from check_methods
    else:
        return HttpResponse(status=405)  # Method Not Allowed

def EachProductDetails(request, product_id):
    if product_id:
        try:
                product=Product.objects.get(id=product_id)
              
                allProds=[]
                AddedItems=getProductId(request)
                allProds.append(["", " ",AddedItems,product])
                params={'allProds': allProds}
                context=params
        except Product.DoesNotExist:
            context={"error":"Product Not Found"}
    else:
        context={"error":"Product id not Fund"}
    return render(request, "products/each_product_details.html", context)


def WinterProducts(request):
    request.user
    
    allProds = []
    prod = Product.objects.filter(category="Winter")
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    AddedItems=getProductId(request)
    allProds.append([prod, nSlides,AddedItems," "])
    params = {'allProds': allProds}
    if request.method == 'POST':
        check_result = check_methods(request)
        if check_result is not None:  # If check_methods returns a valid HttpResponse
            return check_result
        else:
            # Handle the case where check_methods doesn't return an HttpResponse
            return render(request, "products/products.html", params)  # Render the Summer products page
    else:
        return render(request, "products/products.html", params)  # Render the Summer products page


        
def ShoesProducts(request):
    request.user
    
    allProds = []
    prod = Product.objects.filter(category="Shoes")
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    AddedItems=getProductId(request)
    allProds.append([prod, nSlides,AddedItems," "])
    params = {'allProds': allProds}
    if request.method == 'POST':
        check_result = check_methods(request)
        if check_result is not None:  # If check_methods returns a valid HttpResponse
            return check_result
        else:
            # Handle the case where check_methods doesn't return an HttpResponse
            return render(request, "products/products.html", params)  # Render the Summer products page
    else:
        return render(request, "products/products.html", params)  # Render the Summer products page



def MobileProducts(request):
        request.user
        
        allProds = []
        prod = Product.objects.filter(category="Mobile")
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        AddedItems=getProductId(request)
        allProds.append([prod, nSlides,AddedItems," "])
        params = {'allProds': allProds}
        if request.method == 'POST':
            check_result = check_methods(request)
            if check_result is not None:  # If check_methods returns a valid HttpResponse
                return check_result
            else:
            # Handle the case where check_methods doesn't return an HttpResponse
                return render(request, "products/products.html", params)  # Render the Summer products page
        else:
            return render(request, "products/products.html", params)  # Render the Summer products page

def ElectronicsProducts(request):
        request.user
       
        allProds = []
        prod = Product.objects.filter(category="Electronics")
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        AddedItems=getProductId(request)
        allProds.append([prod, nSlides,AddedItems," "])
        params = {'allProds': allProds}
        if request.method == 'POST':
            check_result = check_methods(request)
            if check_result is not None:  # If check_methods returns a valid HttpResponse
                return check_result
            else:
            # Handle the case where check_methods doesn't return an HttpResponse
                return render(request, "products/products.html", params)  # Render the Summer products page
        else:
            return render(request, "products/products.html", params)  # Render the Summer products page


def SummerProducts(request):
    request.user

    allProds = []
    prod = Product.objects.filter(category="Summer")
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    AddedItems=getProductId(request)
    allProds.append([prod, nSlides,AddedItems," "])
    params = {'allProds': allProds}
    if request.method == 'POST':
        check_result = check_methods(request)
        if check_result is not None:  # If check_methods returns a valid HttpResponse
            return check_result
        else:
            # Handle the case where check_methods doesn't return an HttpResponse
            return render(request, "products/products.html", params)  # Render the Summer products page
    else:
        return render(request, "products/products.html", params)  # Render the Summer products page


def NewToCatchProducts(request):
    request.user
    
    allProds=[]
    # Get the current date
    current_date = timezone.now().date()
    prod=Product.objects.filter(date_field=current_date)
    n=len(prod)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([prod, nSlides,AddedItems," "])
    params={'allProds': allProds}
    return render(request, "products/NewToCatchProducts.html", params)

def ToBrandsProducts(request):
    request.user
    allProds=[]
    prod=Product.objects.filter(rating_field =int(4))
    n=len(prod)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([prod,nSlides,AddedItems,"space"])
    params={'allProds': allProds}
    return render(request, "products/ToBrandsProducts.html", params)