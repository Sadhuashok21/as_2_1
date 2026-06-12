from django.http import JsonResponse
from shared_lib.sfs_core.models import *
from shared_lib.utils.models import *
import hashlib
from sfs.utils import unique_id
from .utils import *
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.db import connection


# Create your views here.
def ip_info_view(request):
    ip = get_client_ip(request)   
    g = GeoIP2(settings.GEOIP_PATH)
    try:
        city_data = g.city(ip)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)


    result = {
        "ip": ip,
        "city": city_data.get("city"),
        "country_name": city_data.get("country_name"),
        "country_code": city_data.get("country_code"),
        "postal_code": city_data.get("postal_code") or city_data.get("postcode"),  # DB may vary
        "latitude": city_data.get("latitude"),
        "longitude": city_data.get("longitude"),
        "region": city_data.get("region"),
    }
    return JsonResponse(result)

def all_insert(request):
    user_id = request.GET.get('user_id', '')
    activity_id = request.GET.get('activity_id', '')
    platform = request.GET.get('platform', '')
    platform_name = request.GET.get('platform_name', '')
    
    data = {
        "status": True,
        "message": "success"
    }

    if activity_id and platform and platform_name:
        ip = request.META.get('REMOTE_ADDR')

        if user_id:

            insert = TotalActivity.objects.create(
                    ip = ip, 
                    user_id = user_id,
                    activity_id = activity_id,
                    platform = platform, 
                    platform_name = platform_name,
                    time=timezone.now(),
                )

            return JsonResponse(data, safe=False)
        else:
            insert = TotalActivity.objects.create(
                    ip = ip, 
                    user_id = 'null',
                    activity_id = activity_id,
                    platform = platform, 
                    platform_name = platform_name,
                    time=timezone.now(),
                )

            return JsonResponse(data, safe=False)
            
    else:
        data.update({"status": False})
        return JsonResponse(data, safe=False)

def error_insert(request):
    error_id = request.GET.get('error_id', '')
    error_msg = request.GET.get('error_msg', '')
    user_id = request.GET.get('user_id', '')
    platform = request.GET.get('platform', '')
    platform_name = request.GET.get('platform_name', '')
    ip = request.META.get('REMOTE_ADDR', '')

    data = {
        "status": True,
        "message": "success"
    }

    if error_id and error_msg and platform and platform_name and ip:

        if user_id:
            insert = Allerrors.objects.create(error_id = error_id, error_msg = error_msg, user_id = user_id, platform_name = platform_name, platform = platform, ip = ip,
                    time=timezone.now())
            return JsonResponse(data, safe=False)
        else:
            insert = Allerrors.objects.create(error_id = error_id, error_msg = error_msg, user_id = 'null', platform_name = platform_name, platform = platform, ip = ip,
                    time=timezone.now())
            return JsonResponse(data, safe=False)
    else:
        data.update({"message": "empty"})
        return JsonResponse(data, safe=False)

def insert_id(request):
    bp_pla_id = request.GET.get('bp_pla_id', '')
    user_id = request.GET.get('user_id', '')
    type = request.GET.get('type', '')
    download_type = request.GET.get('download_type', '')
    platform = request.GET.get('platform', '')
    platform_name = request.GET.get('platform_name', '')

    data = {
        "status": True,
        "message": "success"
    }
    

    if not bp_pla_id or not user_id or not type or not download_type:

        data.update({"user": "missing fields"})
        return JsonResponse(data, safe=False)

    else:
        ip = request.META.get('REMOTE_ADDR')
   
        if type == 'downloads':

            insert = BpDlv.objects.create(
                user_id = user_id, 
                platform=platform, 
                platform_name=platform_name, 
                type=type, 
                download_type=download_type, 
                ip=ip, 
                bp_pla_id=bp_pla_id,
                time=timezone.now())
        else:

            insert = BpDlv.objects.create(
            user_id = user_id, 
            platform=platform, 
            platform_name=platform_name, 
            type=type, 
            download_type="null", 
            ip=ip, 
            bp_pla_id=bp_pla_id,
            time=timezone.now())

        return JsonResponse(data, safe=False)

def home_blueprints(request):
    blueprints = BP.objects.filter(status = "approved", fviews__gte= 1000)[:10].values()
    data = {
        "status": True,
        "message": "success",
        "blueprints": list(blueprints)

    }
    return JsonResponse(data, safe=False)


# sfs blueprints 2_0_87

def blueprint_2_0_87(request):
    bp_id = request.GET.get('blueprint_id', '')
    data = {
        "status": True,
        "message": "success",

    }
    if bp_id:
        bp = BP.objects.filter(status="approved", bp_id=bp_id).first()

        if bp:

            bp = BP.objects.filter(status="approved", bp_id=bp_id).values()
            data.update({"blueprints": list(bp)})
            return JsonResponse(data, safe=False)

        else:
            data.update({"message": "null"})
            return JsonResponse(data, safe=False)


    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def rand_blueprints_2_0_87(request):
    blueprints = BP.objects.filter(status="approved", type="blueprint").order_by('?')[:10].values()
    data = {
        "status": True,
        "message": "success",
        "blueprints": list(blueprints)

    }
    return JsonResponse(data, safe=False)



#sfs blueprints 2_0_9

def blueprints_2_0_9(request):
    off = request.GET.get('off', '')

    data = {
        "status": True,
        "message": "success",
    }


    try:
        off = int(off) if off else 0

    except ValueError:
        off = 0

    if off:
        blueprints = BP.objects.filter(status="approved", type="blueprint").order_by('-id')[off*10:off*10+10].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)

    else:
        blueprints = BP.objects.filter(status="approved", type="blueprint").order_by('-id')[:10].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)

def pla_2_0_9(request):
    off = request.GET.get('off', '')
    data = {
        "status": True,
        "message": "success",
    }


    try:
        off = int(off) if off else 0

    except ValueError:
        off = 0

    if off:
        blueprints = BP.objects.filter(status="approved", type="planet").order_by('-id')[off*10:off*10+10].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)

    else:
        blueprints = BP.objects.filter(status="approved", type="planet").order_by('-id')[:10].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)


def category_2_0_9(request):
    category_id = request.GET.get('category_id', '')

    data = {
        "status": True,
        "message": "success",
    }

    if category_id:
        category = BP.objects.filter(status="approved", category=category_id).values()
        data.update({"category": list(category)})
        return JsonResponse(data, safe=False)
    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def blueprint_2_0_9(request):
    bp_id = request.GET.get('bp_id', '')

    data = {
        "status": True,
        "message": "success",
    }

    if bp_id:
        bp = BP.objects.filter(status="approved", bp_id= bp_id).first()

        if bp:
            blueprint = BP.objects.filter(status="approved", bp_id= bp_id).values()

            data.update({"blueprint": list(blueprint)})
            return JsonResponse(data, safe=False)
        else:
            data.update({"message": "empty"})
            return JsonResponse(data, safe=False)

    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def blueprints(request):
    off = request.GET.get('off', '')

    data = {
        "status": True,
        "message": "success",
    }

    try:
        off = int(off) if off else 0

    except ValueError:
        off = 0

    limit = 5
    start = off * limit
    
    end = start + limit
    if off:
         
        blueprints = BP.objects.filter(status="approved").order_by('-id')[start:end].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)
    else:
        blueprints = BP.objects.filter(status="approved").order_by('-id')[:end].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)

def blueprints_off(request):
    off = request.GET.get('off', '')

    try:
        off = int(off) if off else 0

    except ValueError:
        off = 0

    off = int(off*10) +5

    data = {
        "status": True,
        "message": "success",
    }
    if off:
        
        blueprints = BP.objects.filter(status="approved").order_by('-id')[off:off+5].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)
    else:
        blueprints = BP.objects.filter(status="approved").order_by('-id')[:off+5].values()
        data.update({"blueprints": list(blueprints)})
        return JsonResponse(data, safe=False)

def page(request):
    off = request.GET.get('off')

    if off is not None and off.isnumeric():
        off = int(off)

        # Run SQL query (same as PHP)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sfs_BP WHERE status = 'approved' and type='blueprint'")
            rows = cursor.fetchone()[0]  # get total rows

        total_pages = rows // 10  # equivalent to floor division

        # Handle boundaries
        if off < 1:
            off = 1

        if off >= total_pages:
            next_page = off
            back_page = off - 1
        else:
            next_page = off + 1
            back_page = off - 1

        # Page dictionary
        if off <= 1:
            pages = {
                "first": 0,
                "empty": 0,
                "back": 0,
                "current": off,
                "next": next_page,
                "empty1": 0,
                "last": total_pages
            }
        else:
            pages = {
                "first": 1,
                "empty": 0,
                "back": back_page,
                "current": off,
                "next": next_page,
                "empty1": 0,
                "last": total_pages
            }

        return JsonResponse({
            "status": True,
            "message": "success",
            "pages": pages
        })

    else:
        return JsonResponse({
            "status": False,
            "message": "empty"
        })


def pla_page(request):
    off = request.GET.get('off')

    # Check if `off` is provided and numeric
    if off and off.isnumeric():
        off = int(off)

        # Count approved rows (like mysqli_num_rows)
        rows = BP.objects.filter(status='approved', type='planet').count()

        # Calculate total pages (floor division)
        total_pages = rows // 10

        # Boundaries
        if off < 1:
            off = 1

        if off >= total_pages:
            next_page = off
            back_page = off - 1
        else:
            next_page = off + 1
            back_page = off - 1

        # Build page dictionary
        if off <= 1:
            pages = {
                "first": 0,
                "empty": 0,
                "back": 0,
                "current": off,
                "next": next_page,
                "empty1": 0,
                "last": total_pages
            }
        else:
            pages = {
                "first": 1,
                "empty": 0,
                "back": back_page,
                "current": off,
                "next": next_page,
                "empty1": 0,
                "last": total_pages
            }

        # JSON Response (like echo json_encode)
        return JsonResponse({
            "status": True,
            "message": "success",
            "pages": pages
        })
    
    # If 'off' not provided or invalid
    return JsonResponse({
        "status": False,
        "message": "empty"
    })



def profile(request):
    user_id = request.GET.get['user_id', '']

    if user_id is not None:
        profile = AllUsers.objects.filter(user_id = user_id, status = 'approved')

        data = {
            "status": True,
            "message": "success"
        }

        return JsonResponse(data, safe= False)


def inner_bp(request):
    blueprint_id = request.GET.get('blueprint_id', '')

    data = {
            "status": True,
            "message": "success",
            }

    if blueprint_id:
        
        blueprints = BP.objects.filter(blueprint_id = blueprint_id, status = 'approved').values()[:5]

        data.update({"blueprints": list(blueprints)})

        return JsonResponse(data, safe = False)
    else:
        return JsonResponse(data, safe=False)


def inner_pla(request):
    pla_id = request.GET.get('pla_id')
    pass

def home_plawor(request):
    blueprints = BP.objects.filter(status = "approved", type="planet", fviews__gte= 10)[:10].values()
    data = {
        "status": True,
        "message": "success",
        "blueprints": list(blueprints)
    }
    return JsonResponse(data, safe=False)

def home_category(request):
    blueprints = BpCat.objects.filter(status = "approved").values()[:4]
    data = {
        "status": True,
        "message": "success",
        "category": list(blueprints)

    }
    return JsonResponse(data, safe=False)

def home_category_off(request):
    blueprints = BpCat.objects.filter(status = "approved").values()[5:]
    data = {
        "status": True,
        "message": "success",
        "category": list(blueprints)

    }
    return JsonResponse(data, safe=False)

def signin(request):
    email = request.GET.get('email', '')
    password = request.GET.get('password', '')

    data = {
        "status": True,
        "message": "success",
    }

    if not email or not password:
        
        data.update({"user_id": "missing fields", "ip": request.META.get('REMOTE_ADDR')})
        return JsonResponse(data, safe=False)
    else:

        md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()

        user_ = AllUsers.objects.filter(email=email, password=md5_pass, status='approved')
        user = user_.first()

        if user is None:
            data.update({"user": "no data"})
            return JsonResponse(data, safe=False)
        else:
            data.update({"user_id": user.user_id})
            return JsonResponse(data, safe=False)

def create_account(request):
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    user_id = request.GET.get('user_id', '')
    profile = request.GET.get('profile', '')
    type = request.GET.get('type')
    password = request.GET.get('password')
    platform = request.GET.get('platform')
    platform_name = request.GET.get('platform_name')

    data = {
        "status": True,
        "message": "success"
        }

    if name and email and user_id and profile and  type and platform and platform_name:
        
        user_exist = AllUsers.objects.filter(email = email).first()
        if user_exist:
            data.update({"message": "existed"})
            return JsonResponse(data, safe=False)
        else:

            if password:
                md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
                user_id = unique_id()
                data.update({"message": "inserted"})
                insert = AllUsers.objects.create(name= name, email=email, password=md5_pass, user_id=user_id, profile="null", user_type='user', platform=platform, platform_name=platform_name, type=type, status='approved', time=timezone.now())
                return JsonResponse(data, safe=False)
            else:
                data.update({"message": "inserted"})
                insert = AllUsers.objects.create(name= name, email=email, user_id=user_id, profile="null", user_type='user', platform=platform, platform_name=platform_name, type=type, status='approved', time=timezone.now())
                return JsonResponse(data, safe=False)

        if user_id == 'manual':
            pass


        return JsonResponse(data, safe=False)

    else:
        data.update({"message": "empty"})
        return JsonResponse(data, safe=False)
  

    if all_users > 0:
        data.update({
            "user": "email exists",
        })
        return JsonResponse(data)
    else:
        md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        user_id = unique_id()
        data.update({"user": user_id})
        insert = AllUsers.objects.create(name= name, email=email, password=md5_pass, user_id=user_id, profile="null", user_type='user', platform=platform, platform_name=platform_name, type=type, status='approved', time=timezone.now())
        return JsonResponse(data)

def updateid(request):
    email = request.GET.get('email', '')
    user_id = request.GET.get('user_id', '')

    data = {
        "status": True,
        "message": "updated"
    }
    if email and user_id:
        user = AllUsers.objects.filter(email=email).first()
        if user:
            user.user_id = user_id
            return JsonResponse(data, safe=False)
        else:
            data.update({"message": "noRecord"})
            return JsonResponse(data, safe=False)
    else:
        data.update({"message": "empty"})
        return JsonResponse(data, safe=False)










""" 


def products(request):
    products = FreshBasketProducts.objects.filter(status="approved").order_by('?').values()

    data = {
        "products": list(products)
    }
    return JsonResponse(data, safe=False)


def upload_product(request):
    name = request.GET.get('name', '')
    price = request.GET.get('price', '')
    img = request.GET.get('img', '')
    quantity = request.GET.get('quantity', '')
    price_del = request.GET.get('price_del', '')
    user_id = request.GET.get('user_id', '')

    data = {
        "status": True,
        "message": "success",
    }


    if name and price and img and quantity and price_del and user_id:

        product = FreshBasketProducts.objects.create(
            name = name,
            price = price,
            img = img,
            quantity = quantity,
            price_del = pricde_del,
            user_id = user_id,
            status = approved,
            time = timezone.now(),
            product_id = unique_id()
        )

        return JsonResponse(data, safe=False)
    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def edit_product(request):
    name = request.GET.get('name', '')
    price = request.GET.get('price', '')
    img = request.GET.get('img', '')
    quantity = request.GET.get('quantity', '')
    price_del = request.GET.get('price_del', '')
    user_id = request.GET.get('user_id', '')
    product_id = request.GET.get('product_id', '')

    data = {
        "status": True,
        "message": "success",
    }


    if name and price and img and quantity and price_del and user_id:

        product = FreshBasketProducts.objects.filter(product_id).first()

        if product:
            product.name = name
            product.price = price
            product.quantity = quantity
            product.img = img
            product.price_del = price_del

            return JsonResponse(data, safe=False)

        else:
            data.update({"message": "notUpdated"})
            return JsonResponse(data, safe=False)
    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def orders(request):
    user_id = request.GET.get('user_id', '')

    data = {
        "status": True,
        "message": "success",
    }

    if not user_id:
        product = FreshBasketOrders.objects.filter(status="approved", user_id =user_id)

        if product.count > 0:
            
            data.update({"orders": list(products)})
            return JsonResponse(data, safe=False)
        else:
            data.update({"message": "no orders"})
            return JsonResponse(data, safe=False)
     

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status": False, "message": "notSet"}, safe=False)

def fb_create_account(request):
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    password = request.GET.get('password', '')
    profile = request.GET.get('profile', '')
    address = request.GET.get('address', '')
    phone = request.GET.get('phone', '')

    data = {
            "status": True,
            "message": "success"
        }

    if name and email and password and profile and address and phone:

        md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
        user = FreshBasketUsers.objects.create(
            name=name,
            email=email,
            password=md5_pass,
            profile=profile,
            address=address,
            phone=phone,
            user_type='user',
            user_id=unique_id(),
            type='manual',
            status='approved',
            time=timezone.now()
            )

        
        return JsonResponse(data, safe=False)
    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False)


def delete_product(request):
    user_id = request.GET.get('user_id', '')
    data = {
        "status": True,
        "message": "success",
    }

    if user_id:

        user = FreshBasketUsers.objects.filter(user_id=user_id).first()

        if user:
            user.delete()
            return JsonResponse(data, safe=False)
        else:
            user.update({"message": "notDeleted"})
            return JsonResponse(data, safe=False)
    
 
    return JsonResponse(data, safe=False)


def fb_sign_in(request):
    email = request.GET.get('email', '')
    password = request.GET.get('password', '')

    data = {
        "status": True,
        "message": "success"
    }
    if email and password:
        
        md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()

        exists = FreshBasketUsers.objects.filter(email=email, password=md5_pass).first()
        if exists:
            
            data.update({"user_id": exists.user_id})
            
            return JsonResponse(data, safe=False)
        else:

            data.update({"message": "no_user"})
            return JsonResponse(data, safe=False)
    else:
        data.update({"message": "notSet"})
        return JsonResponse(data, safe=False) """