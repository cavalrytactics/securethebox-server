from flask_restplus import Namespace, Resource, fields, reqparse
from .initialize.academy import main
from app_controllers.firestore.firestore_academy import FirestoreAcademy
import json
import os
import stripe

api = Namespace('stripe', description='Stripe related operations')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

@api.route('/public-key')
class StripePublicKey(Resource):
    @api.doc('get_public_key')
    def get(self):
        return {"publicKey": os.getenv('STRIPE_PUBLISHABLE_KEY')}, 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 

@api.route('/create-customer')
class StripeCreateCustomer(Resource):
    @api.doc('create_customer')
    def post(self):
        data = json.loads(request.data)
        paymentMethod = data['payment_method']
        planIds = data['plan_ids']

        # This creates a new Customer and attaches the PaymentMethod in one API call.
        # At this point, associate the ID of the Customer object with your
        # own internal representation of a customer, if you have one.
        customer = stripe.Customer.create(
            payment_method=paymentMethod,
            email=data['email'],
            invoice_settings={
                'default_payment_method': paymentMethod
            }
        )

        # In this example, we apply the coupon if the number of plans purchased
        # meets or exceeds the threshold.
        eligibleForDiscount = len(planIds) >= MIN_PLANS_FOR_DISCOUNT
        coupon = os.getenv('COUPON_ID') if eligibleForDiscount else None

        # Subscribe the user to the subscription created
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": planId} for planId in planIds],
            expand=["latest_invoice.payment_intent"],
            coupon=coupon
        )
        return jsonify(subscription), 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 

@api.route('/subscription')
class StripeGetSubscription(Resource):
    @api.doc('get_subscription')
    def post(self):
        # Reads application/json and returns a response
        data = json.loads(request.data)
        subscription = stripe.Subscription.retrieve(data['subscriptionId'])
        return jsonify(subscription), 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 