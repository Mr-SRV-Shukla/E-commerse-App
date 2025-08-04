from django.shortcuts import render
from landing_app.models import Product
from landing_app.views import *
# from landing_app.signals import session_update_singal
# Create your views here.

def cart_summery(request):
    AddedItems=getProductId(request)
    # remove the null value form the dict
    new=AddedItems['cart']
    null='null'
    if null in new:
        AddedItems['cart'].pop('null')
    no_of_items=range(len(AddedItems["cart"]))
    items_ids=list(AddedItems["cart"].keys())
    for i in items_ids:
        if i == None:
            items_ids.remove(i)
    allProds = []
    allProds.append(["",no_of_items,AddedItems,items_ids])
    context={"allProds":allProds}
    #session_update_singal.send(sender=request.user,request=request)
    return render(request, "cart/cart_summery.html", context)

def cart_delete(request, product_id):
    cart = request.session.get('cart')
    if cart and str(product_id) in cart:
        del cart[str(product_id)]
        
        request.session['cart'] = cart  # Fixed the assignment issue

    # Avoid popping 'null' if it doesn't exist in the dictionary
    if 'null' in cart:
        cart.pop('null')
        

    no_of_items = range(len(cart))
    items_ids = list(cart.keys())
    
    # Remove invalid or None entries from the list
    items_ids = [i for i in items_ids if i is not None]
    if str(product_id) in items_ids:
        items_ids.remove(str(product_id))

    cleaned_data = {int(k): v for k, v in cart.items() if k is not None and k.isdigit()}
    total_sum = sum(cleaned_data.values())
    AddedItems={
        'cart':cart,
        'totalCartItenSum':total_sum
    }
    
    allProds = []
    allProds.append(["", no_of_items, AddedItems, items_ids])
    context = {"allProds": allProds}
    #session_update_singal.send(sender=request.user,request=request)
    return render(request, "cart/cart_summery.html", context)

def quntity_add(request,product_id):
    print("started adding product")
    cart = request.session.get('cart', {})

    # If the cart contains the product, increment the quantity
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        # If the product doesn't exist in the cart, add it with a quantity of 1
        cart[str(product_id)] = 1

    # Update the session with the modified cart
    request.session['cart'] = cart

    # Avoid popping 'null' if it doesn't exist in the dictionary
    if 'null' in cart:
        cart.pop('null')

    # Get the number of items and the product ids
    no_of_items = range(len(cart))
    items_ids = list(cart.keys())
    
    # Remove invalid or None entries from the list
    items_ids = [i for i in items_ids if i is not None]

    # Clean the cart data by ensuring the keys are digits
    cleaned_data = {int(k): v for k, v in cart.items() if k.isdigit()}

    # Calculate the total sum of the cart
    total_sum = sum(cleaned_data.values())

    # Prepare the data to pass to the template
    AddedItems = {
        'cart': cart,
        'totalCartItemSum': total_sum
    }

    # Prepare the list of all products to pass to the context
    allProds = []
    allProds.append(["", no_of_items, AddedItems, items_ids])

    context = {"allProds": allProds}
    # session_update_singal.send(sender=request.user,request=request)
    # Render the cart summary page
    return render(request, "cart/cart_summery.html", context)

def quntity_remove(request,product_id):
    cart = request.session.get('cart', {})

    if cart and str(product_id) in cart:
        # Decrease the quantity of the given product by 1
        cart[str(product_id)] -= 1

        # If the quantity becomes 0, remove the product from the cart
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]

        # Update the session with the modified cart
        request.session['cart'] = cart

    # Avoid popping 'null' if it doesn't exist in the dictionary
    if 'null' in cart:
        cart.pop('null')

    # Get the number of items and the product ids
    no_of_items = range(len(cart))
    items_ids = list(cart.keys())
    
    # Remove invalid or None entries from the list
    items_ids = [i for i in items_ids if i is not None]

    # Clean the cart data by ensuring the keys are digits
    cleaned_data = {int(k): v for k, v in cart.items() if k.isdigit()}

    # Calculate the total sum of the cart
    total_sum = sum(cleaned_data.values())

    # Prepare the data to pass to the template
    AddedItems = {
        'cart': cart,
        'totalCartItemSum': total_sum
    }

    # Prepare the list of all products to pass to the context
    allProds = []
    allProds.append(["", no_of_items, AddedItems, items_ids])

    context = {"allProds": allProds}
    #session_update_singal.send(sender=request.user,request=request)
    # Render the cart summary page
    return render(request, "cart/cart_summery.html", context)

def Checkout(request):
    AddedItems=getProductId(request)
    # remove the null value form the dict
    new=AddedItems['cart']
    null='null'
    if null in new:
        AddedItems['cart'].pop('null')
    no_of_items=range(len(AddedItems["cart"]))
    items_ids=list(AddedItems["cart"].keys())
    for i in items_ids:
        if i == None:
            items_ids.remove(i)
    allProds = []
    allProds.append(["",no_of_items,AddedItems,items_ids])
    context={"allProds":allProds}
    return render(request, 'cart/checkout.html', context)

    
