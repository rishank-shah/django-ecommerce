import json
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *


def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    orderitems = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        cartItems += cart[i]['quantity']

        product = Product.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product':{
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'thumbnail':product.thumbnail,
            },
            'quantity':cart[i]['quantity'],
            'get_total':total,
        }

        orderitems.append(item)

    return {'cartItems':cartItems, 'order':order, 'orderitems':orderitems}


def cartData(request):

    if request.user.is_authenticated:
        user = request.user
        useraddress = UserAddress.objects.filter(user=user)
        order, created = Order.objects.get_or_create(user=user, completed=False)
        orderitems = OrderItem.objects.filter(
            order=order
        ).order_by('date_added')
        
        cartItems = order.get_cart_items

        return {
            'useraddress':useraddress,
            'orderitems':orderitems,
            'order':order,
            'cartItems':cartItems
        }

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        orderitems = cookieData['orderitems']

        return {
            'orderitems':orderitems,
            'order':order,
            'cartItems':cartItems
        }


def guest_user_cart(request, data):

    #  to call this, define data=json.loads(request.body)
    # then customer, order = guestOrder(request, data)

    print('User is not logged in!')
    print('COOKIES:', request.COOKIES)

    username = data['emailInfo']['username']
    email = data['emailInfo']['email']

    cookieData = cookieCart(request)
    orderitems = cookieData['orderitems']

    user, created = User.objects.get_or_create(
        email=email
    )

    user.username = username
    user.save()

    order = Order.objects.create(
        user=user,
        complete=False,
    )

    for item in orderitems:
        product = Product.objects.get(id=item['product']['id'])

        orderitem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return user, order


def cart_email(request):

    first_name = request.user.first_name
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    orderitems = data['orderitems']

    context = {
        'first_name': first_name,
        'orderitems':orderitems,
        'order':order,
        'cartItems':cartItems
    }
    
    template = render_to_string('product/cart_email_template.html',context)

    email = EmailMultiAlternatives(
        'Hi ' + first_name + ' your shopping cart misses you!',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )

    email.attach_alternative(template,'text/html')
    email.send(fail_silently=False)