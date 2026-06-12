from django.shortcuts import render

# Create your views here.
def termsandpolicy(request):
    return render(request, "privacy.html")

def sfs(request):
    return render(request, "sfs.html")

def krishi_pri(request):
    return render(request, "krishi_pri.html")


def pdfix_pri(request):
    return render(request, "pdf_pri.html")

def sonic_pri(request):
    return render(request, "sonic_pri.html")

def transport_pri(request):
    return render(request, "transport_pri.html")

def skiltrix_pri(request):
    return render(request, "skiltrix_pri.html")

def shop_pri(request):
    return render(request, "shop_pri.html")

def asmail(request):
    return render(request, "asmail_pri.html")

def contact(request):
    return render(request, "contact_1.html")

def disclaimer(request):
    return render(request, "disclaimer.html")

def about(request):
    return render(request, "about.html")
