from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect
from .models import User
from django.db import connection
from django.views.decorators.csrf import csrf_protect

from .forms import RegistrationForm


def get_roles(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT role FROM role_user WHERE user=%s', (request.user.id,))
        raw = cursor.fetchall()
        ready = tuple(t[0] for t in raw)
    return ready


def lk(request):
    user_role = {'user_role': get_roles(request)}
    return render(request, 'account/home.html', user_role)


@login_required(login_url='register')
def bought_orders(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT account_email, account_password, '
                       'user_discord_vk, start_rating, stop_rating, price'
                       ' FROM orders '
                       'WHERE id_orders IN '
                       '(SELECT `order` FROM orders_users '
                       'WHERE user = %s)', (request.user.id,))
        ords = cursor.fetchall()
    my_bought_orders = {'ords': ords}
    if my_bought_orders['ords']:
        return render(request, 'account/bought_orders.html', my_bought_orders)
    else:
        return render(request, 'account/bought_orders.html')



@login_required(login_url='register')
@csrf_protect
def see_applications(request):
    if 1 in get_roles(request):
        if request.POST:
            action = request.POST.get('action')
            usid = request.POST.get('usid')
            appid = request.POST.get('appid')
            if action == 'accept':
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO role_user (role, user) values (%s, %s)', (2, usid))
                    cursor.execute('DELETE FROM applications WHERE id_applications=%s', (appid,))
            elif action == 'reject':
                with connection.cursor() as cursor:
                    cursor.execute('DELETE FROM applications WHERE id_applications=%s', (appid,))
    user_role = {'user_role': get_roles(request)}
    print(user_role)
    with connection.cursor() as cursor:
        cursor.execute('SELECT applications.*, role.discription '
                       'FROM applications '
                       'JOIN ( SELECT role_user.user, MIN(role.id_role) '
                       'AS min_role_id FROM role_user JOIN role '
                       'ON role_user.role = role.id_role '
                       'GROUP BY role_user.user) AS min_roles '
                       'ON applications.user = min_roles.user '
                       'JOIN role ON min_roles.min_role_id = role.id_role')
        result = cursor.fetchall()
    applications = {'applications': result}
    if 1 in user_role['user_role']:
        if applications['applications']:
            return render(request, 'account/see_applications.html', applications)
        else:
            return render(request, 'account/see_applications.html')
    return render(request, 'account/home.html')


@login_required(login_url='register')
@csrf_protect
def take_order(request):
    user_role = {'user_role': get_roles(request)}
    if 2 in user_role['user_role']:
        if request.POST:
            with connection.cursor() as cursor:
                post_id = request.POST.get('usid')
                post_ordid = request.POST.get('ordid')
                cursor.execute('INSERT INTO orders_users (user, is_booster, `order`) values (%s, %s, %s)', (post_id, 1, post_ordid))
        with connection.cursor() as cursor:
            cursor.execute('SELECT start_rating, stop_rating, price, date, id_orders '
                           'FROM orders WHERE id_orders '
                           'NOT IN (SELECT `order` '
                           'FROM orders_users WHERE is_booster = 1)')
            raw_ords = cursor.fetchall()
            print(raw_ords)
            orders = {'orders': raw_ords, 'us': request.user.id}
        if orders['orders']:
            return render(request, 'account/take_order.html', orders)
        else:
            return render(request, 'account/take_order.html')
    return render(request, 'account/home.html')


@login_required(login_url='register')
@csrf_protect
def my_orders(request):
    user_role = {'user_role': get_roles(request)}
    if 2 in user_role['user_role']:
        if request.POST:
            with connection.cursor() as cursor:
                post_ordid = request.POST.get('ordid')
                cursor.execute('DELETE FROM orders_users WHERE `order`=%s', (post_ordid,))
    with connection.cursor() as cursor:
        cursor.execute('SELECT account_email, account_password, '
                       'user_discord_vk, start_rating, stop_rating, price, id_orders'
                       ' FROM orders '
                       'WHERE id_orders IN '
                       '(SELECT `order` FROM orders_users '
                       'WHERE user = %s)', (request.user.id,))
        ords = cursor.fetchall()
    ord_process = {'ords': ords}
    if ord_process['ords']:
        return render(request, 'account/myorders.html', ord_process)
    else:
        return render(request, 'account/myorders.html')


@login_required(login_url='register')
@csrf_protect
def applicate(request):
    if request.POST:
        myvalues = (request.POST.get('mmr'), request.POST.get('hours'),
                    '1' if request.POST.get('self_employed') == 'on' else '0',
                    request.POST.get('discord'), request.user.id, request.POST.get('exp'))
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO applications (mmr, hours, self_employed, discord, user, exp)'
                           ' values (%s, %s, %s, %s, %s, %s)', myvalues)
    return render(request, 'account/application.html')


@login_required(login_url='register')
@csrf_protect
def boost(request):
    if request.POST:
        myvalues = (request.POST.get('current'), request.POST.get('future'),
                    request.POST.get('email'), request.POST.get('password'),
                    request.POST.get('discord'), request.POST.get('price'))
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO orders (start_rating, stop_rating, account_email,'
                           'account_password, user_discord_vk, price, date)'
                           ' values (%s, %s, %s, %s, %s, %s, current_timestamp)', myvalues)
            cursor.execute('SELECT LAST_INSERT_ID() FROM orders')
            orid = cursor.fetchone()
            cursor.execute('INSERT INTO orders_users (user, `order`) value (%s, %s)', (request.user.id, orid[0]))
            return redirect('lk')
    return render(request, 'account/boost.html')


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()
            with connection.cursor() as cursor:
                cursor.execute(f'''INSERT INTO role_user (role, user) values (3, {user.id})''')
            if user and user.check_password(password):
                user = authenticate(request, username=username, password=password)
            if user.is_authenticated and user is not None:
                login(request, user)
                print('User authenticated')
                return redirect('lk')
            else:
                print('User is not authenticated')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def mylogout(request):
    logout(request)
    return redirect('index')
