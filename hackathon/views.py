from django.shortcuts import render
from django.views import View
from shared_lib.hackathon.models import *
from django.contrib import messages
from shared_lib.utils import insertions

from django.conf import settings
import razorpay
from django.utils import timezone

# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


def teams(request):
    return render(request, "hack_team.html")

def challenges(request):
    return render(request, "hack_challenge.html")


class SubmissionView(View):
    def get(self, request):
        return render(request, 'submission.html')
    

    def post(self, request):
        name = request.POST.get('name', '')

        if name:
            HackathonProjects.objects.create(title=name, description="Sample description")
            messages.success(request, "Project submitted successfully!")
        return render(request, 'submission.html')
    


class LogIn(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = HackathonUsers.objects.filter(email=email, password=password).first()
            if user:
                messages.success(request, "Logged in successfully!")
            else:
                messages.error(request, "Invalid credentials!")
        return render(request, 'login.html')
    

class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if name and email and password:
            if HackathonUsers.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
            else:
                user_id = insertions.generate_unique_id()
                HackathonUsers.objects.create(name=name, email=email, password=password, user_id=user_id)
                messages.success(request, "Account created successfully!")
        return render(request, 'signup.html')
    
def home(request):
    return render(request, 'hack_home.html')
    
""" 
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment(request):
    amount = 10000  # Rs. 200 in paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(
        dict(amount=amount, currency=currency, payment_capture='0')
    )
    
    # Save order in database
    # Payment.objects.create(
    #     razorpay_order_id=razorpay_order['id'],
    #     amount=amount,
    #     status='Created'
    # )

    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': '/paymenthandler/'
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # GET THE OBJECT: Fetch the payment record from your DB
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

            # CRITICAL ADDITION: Ensure amount is an integer (Paise)
            # Razorpay will throw an error if this is a float or string
            capture_amount = int(payment.amount)
            
            # CAPTURE THE PAYMENT: This prevents the auto-refund
            razorpay_client.payment.capture(payment_id, capture_amount)
            
            # UPDATE RECORD: Save the IDs and mark as Success
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Success'
            payment.save()

            return render(request, 'paymentsuccess.html')

        except razorpay.errors.SignatureVerificationError:

            Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(status='Failed')
            return render(request, 'paymentfail.html')
            
        except Exception as e:
            
            return HttpResponseBadRequest(f"Payment Processing Error: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method")


 """




client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)

def payment(request):

    order = client.order.create({
        "amount": 10000,
        "currency": "INR"
    })

    context = {
        "order_id": order["id"],
        "razorpay_key": settings.RAZOR_KEY_ID
    }

    return render(request, "payment.html", context)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_payment(request):

    data = json.loads(request.body)

    HackathonPayments.objects.create(
        name=data["email"],
        team=data["team_name"],
        payment=data["payment_id"]
    )

    return JsonResponse({"status":"success"})