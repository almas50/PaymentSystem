import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item, OrderItem, Order, Tax, Discount
from django.shortcuts import get_object_or_404, render

stripe.api_key = settings.STRIPE_SECRET_KEY


class BuyItemApiView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price * 100),  # Stripe expects cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success/',
                cancel_url='https://example.com/cancel/',
            )
            return Response({'id': session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def item_page_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_page.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })



def get_stripe_discount_coupon(discount: Discount):
    return discount.name

def get_stripe_tax_rate(tax: Tax):
    return tax.name

class BuyOrderApiView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        line_items = []

        for order_item in order.orderitem_set.all():
            line_item = {
                "price_data": {
                    "currency": 'usd',
                    "unit_amount": int(order_item.item.price * 100),
                    "product_data": {
                        "name": order_item.item.name,
                        "description": order_item.item.description,
                    },
                },
                "quantity": order_item.quantity,
            }
            if order.tax:
                tax_rate_id = get_stripe_tax_rate(order.tax)
                line_item["tax_rates"] = [tax_rate_id]
            line_items.append(line_item)

        checkout_session_params = {
            "payment_method_types": ["card"],
            "line_items": line_items,
            "mode": "payment",
            "success_url": "https://example.com/success/",
            "cancel_url": "https://example.com/cancel/",
        }

        if order.discount:
            coupon_id = get_stripe_discount_coupon(order.discount)
            checkout_session_params["discounts"] = [{"coupon": coupon_id}]

        try:
            session = stripe.checkout.Session.create(**checkout_session_params)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"id": session.id})
def order_page_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'order_page.html', {
        'order': order,
        'total_amount': order.total_amount(),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })