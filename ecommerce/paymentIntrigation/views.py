from django.shortcuts import render , redirect
from paymentIntrigation import keys
from paymentIntrigation.models import Orders,OrdersUpdate
from django.contrib import messages
from landing_app.views import *

def address(request):
    AddedItems=getProductId(request)
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
    return render(request, 'payment/address.html', context)

def payment(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        number=request.POST.get("number")
        address=request.POST.get("address")
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip')
        if not all([name, email, number, address, state, zip_code]):
            messages.warning(request, "All fields are required!")  # Use error message instead
            return redirect("address")
        
        order=Orders(name=name,email=email,number=number,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update=OrdersUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        AddedItems=getProductId(request)
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
        order_id=order.order_id
        allProds.append([order_id,no_of_items,AddedItems,items_ids])
        
        context={"allProds":allProds}
    return render(request, 'payment/payment.html', context)


def orderStatus(request):
    allProds = []
    message = None

    if request.method == "POST":
        order_id = request.POST.get("order_id")  
        if order_id:
            try:
                AddedItems=getProductId(request)
                new=AddedItems['cart']
                null='null'
                if null in new:
                    AddedItems['cart'].pop('null')
                no_of_items=range(len(AddedItems["cart"]))
                items_ids=list(AddedItems["cart"].keys())
                for i in items_ids:
                    if i == None:
                        items_ids.remove(i)
                allProds.append([order_id,no_of_items,AddedItems,items_ids])  
                
            except Orders.DoesNotExist:
                message = "Order not found."
        else:
            message = "Order ID is required."
    context={"allProds":allProds}
    return render(request, 'payment/order_status.html', context)


    