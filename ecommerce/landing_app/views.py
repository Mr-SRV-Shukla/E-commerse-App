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

    request.user
    allProds=[]
    # If catprods cache the return it 
    catprods=cache.get('Home_catprods')
    # if catprods is none the set catprods in cache
    if catprods is None:
        catprods=Product.objects.values()
        cache.set('Home_catprods',catprods,timeout=60)

    n=len(catprods)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([catprods, nSlides,AddedItems,""])
    
    params={'allProds': allProds}
    # cache.set('allProds',allProds)
    # cache.get()
    return render(request, "products/all_products.html", params)


def allProducts(request):
     # If catprods cache the return it 
    catprods=cache.get('all_catprods')
    request.user
    allProds=[]
     # if catprods is none the set catprods in cache
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
                # if product cached the return it from cache
                product=cache.get('EachProductDetails')
                # if prduct is not cache them cached it
                if product is None:
                    product=Product.objects.get(id=product_id)
                    cache.set('EachProductDetails',product,timeout=90)
                
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
    prod=cache.get("WinterProducts")
    if prod is None:
        prod = Product.objects.filter(category="Winter")
        cache.set("WinterProducts",prod,timeout=90)
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
    prod=cache.get("ShoesProducts")
    if prod is None:
        prod = Product.objects.filter(category="Shoes")
        cache.set("ShoesProducts",prod,timeout=90)
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
        prod=cache.get("MobileProducts")
        if prod is None:
            prod = Product.objects.filter(category="Mobile")
            cache.set("MobileProducts",prod,timeout=90)
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
        prod=cache.get("ElectronicsProducts")
        if prod is None:
            prod = Product.objects.filter(category="Electronics")
            cache.set("ElectronicsProducts",prod,timeout=90)
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
    prod=cache.get("SummerProducts")
    if prod is None:
        prod = Product.objects.filter(category="Summer")
        cache.set("SummerProducts",prod,timeout=90)
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
    prod=cache.get("NewToCatchProducts")
    if prod is None:
        prod=Product.objects.filter(date_field=current_date)
        cache.set("NewToCatchProducts",prod,timeout=90)
    n=len(prod)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([prod, nSlides,AddedItems," "])
    params={'allProds': allProds}
    return render(request, "products/NewToCatchProducts.html", params)

def ToBrandsProducts(request):
    request.user
    allProds=[]
    prod=cache.get("ToBrandsProducts")
    if prod is None:
        prod=Product.objects.filter(rating_field =int(4))
        cache.set("ToBrandsProducts",prod,timeout=90)
    n=len(prod)
    nSlides=n // 4 + ceil((n/4) - (n//4))
    AddedItems=getProductId(request)
    allProds.append([prod,nSlides,AddedItems,"space"])
    params={'allProds': allProds}
    return render(request, "products/ToBrandsProducts.html", params)