from django.shortcuts import redirect, render
from django.views import View
from shared_lib.hackathon.models import *
from django.contrib import messages
from shared_lib.utils import insertions

from django.conf import settings
import razorpay
from django.utils import timezone
from django.contrib import messages

from .models import Team, Judge, Evaluation


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
    


from django.shortcuts import render, redirect
from django.views import View
from .models import Judge


class LogIn(View):

    def get(self, request):
        return render(request, "hack_signin.html")

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            judge = Judge.objects.get(
                username=username,
                password=password,
                is_active=True
            )

            request.session["judge_id"] = judge.id
            request.session["judge_name"] = judge.full_name

            return redirect("evaluation")

        except Judge.DoesNotExist:
            return render(request, "hack_signin.html", {
                "error": "Invalid username or password."
            })
        


class EvaluationView(View):

    def get(self, request):

        # Check if judge is logged in
        if "judge_id" not in request.session:
            return redirect("login")

        judge = Judge.objects.get(id=request.session["judge_id"])

        evaluated = Evaluation.objects.filter(
        judge=judge
        ).values_list("team_id", flat=True)

        teams = Team.objects.filter(
            judgeassignment__judge=judge
        ).exclude(
            id__in=evaluated
        ).order_by("team_id")

        return render(request, "hack_eval.html", {
            "teams": teams,
            "judge_name": request.session.get("judge_name")
        })

    def post(self, request):

        if "judge_id" not in request.session:
            return redirect("login")

        team_id = request.POST.get("team")

        if not team_id:
            messages.error(request, "Please select a team.")
            return redirect("evaluation")

        try:
            team = Team.objects.get(id=team_id)
            judge = Judge.objects.get(id=request.session["judge_id"])

            # Prevent duplicate evaluation
            if Evaluation.objects.filter(team=team, judge=judge).exists():
                messages.warning(
                    request,
                    f"You have already evaluated Team {team.team_id}. A second evaluation is not allowed."
                )
                return redirect("evaluation")

            innovation = int(request.POST.get("innovation", 0))
            problem = int(request.POST.get("problem", 0))
            technical = int(request.POST.get("technical", 0))
            uiux = int(request.POST.get("uiux", 0))
            completeness = int(request.POST.get("completeness", 0))
            demo = int(request.POST.get("demo", 0))
            presentation = int(request.POST.get("presentation", 0))
            impact = int(request.POST.get("impact", 0))

            # Validate maximum marks
            if (
                innovation > 20 or
                problem > 15 or
                technical > 20 or
                uiux > 10 or
                completeness > 10 or
                demo > 10 or
                presentation > 10 or
                impact > 5
            ):
                messages.error(request, "One or more marks exceed the allowed limit.")
                return redirect("evaluation")

            total = (
                innovation +
                problem +
                technical +
                uiux +
                completeness +
                demo +
                presentation +
                impact
            )

            Evaluation.objects.create(
                team=team,
                judge=judge,
                innovation=innovation,
                problem_understanding=problem,
                technical_implementation=technical,
                ui_ux=uiux,
                completeness=completeness,
                practical_demo=demo,
                presentation=presentation,
                impact=impact,
                total=total
            )

            messages.success(request, "Evaluation submitted successfully.")

        except Team.DoesNotExist:
            messages.error(request, "Selected team does not exist.")

        except Judge.DoesNotExist:
            request.session.flush()
            return redirect("login")

        except ValueError:
            messages.error(request, "Please enter valid marks.")

        except Exception as e:
            messages.error(request, str(e))

        return redirect("evaluation")




from .models import Judge, Team, JudgeAssignment



from django.views import View
from django.shortcuts import render
from django.db.models import Avg, Sum, Count

from .models import Evaluation


class ScoreBoardView(View):

    def get(self, request):

        scores = (
            Evaluation.objects
            .values("team__team_id", "team__team_name")
            .annotate(
                total_score=Sum("total"),
                average_score=Avg("total"),
                judges=Count("judge")
            )
            .order_by("-average_score")
        )

        return render(request, "scoreboard.html", {
            "scores": scores
        })



class AssignJudgeView(View):

    def get(self, request):

        judges = Judge.objects.filter(is_active=True)
        teams = Team.objects.exclude(
            id__in=JudgeAssignment.objects.values_list("team_id", flat=True)
        )

        return render(request, "assign_judge.html", {
            "judges": judges,
            "teams": teams
        })

    def post(self, request):

        judge = Judge.objects.get(id=request.POST.get("judge"))
        team_ids = request.POST.getlist("teams")

        if len(team_ids) == 0:
            messages.error(request, "Please select at least one team.")
            return redirect("assign_judge")

        if len(team_ids) > 10:
            messages.error(request, "A judge can be assigned a maximum of 10 teams.")
            return redirect("assign_judge")

        for team_id in team_ids:

            JudgeAssignment.objects.get_or_create(
                judge=judge,
                team_id=team_id
            )

        messages.success(request, "Teams assigned successfully.")

        return redirect("assign_judge")





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