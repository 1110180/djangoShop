from django.shortcuts import render, redirect
from collections.abc import Mapping

from .models import *
from .form import *


# import requests


def index(req):
    items = Tovar.objects.all()
    data = {'tovar': items}
    return render(req, 'index.html', data)


def toCar(req):
    items = Cart.objects.filter(user=req.user)
    forma = OrderForm()
    total = 0
    for i in items:
        total += i.calculateSumma()
    total = round(total, 2)
    # оформление заказа
    if req.POST:
        forma = OrderForm(req.POST)
        k1 = req.POST.get('adres')
        k2 = req.POST.get('tel')
        k3 = req.POST.get('emil')
        print(k1, k2, k3)

        if forma.is_valid():
            print(k1, k2, k3)
            k1 = forma.cleaned_data.get('adres')
            k2 = forma.cleaned_data.get('tel')
            k3 = forma.cleaned_data.get('emil')
            print(k1, k2, k3)
            myzakaz = ''
            for one in items:
                myzakaz += one.tovar.name + ' '
                myzakaz += 'Количество: ' + str(one.count) + ' '
                myzakaz += 'Сумма: ' + str(one.summa) + ' '
                myzakaz += 'Скидка: ' + str(one.tovar.discount) + ' '

            neworder = Order.objects.create(adres=k1,
                                            tel=k2,
                                            emil=k3,
                                            total=total,
                                            myzakaz=myzakaz,
                                            user=req.user)
            items.delete()
            telegram(neworder)

            return render(req, 'sps.html')
    data = {'tovar': items, 'total': total, 'formaorder': forma}
    return render(req, 'cart.html', data)


def buy(req, id):
    item = Tovar.objects.get(id=id)
    curuser = req.user

    if Cart.objects.filter(tovar=item, user=curuser):
        getTovar = Cart.objects.get(tovar_id=id)
        getTovar.count += 1
        getTovar.summa = getTovar.calculateSumma()
        getTovar.save()
    else:
        Cart.objects.create(tovar=item,
                            count=1,
                            user=curuser,
                            summa=item.price)

    return redirect('home')


def delete(req, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('tocart')


def cartCount(req, num, id):
    num = int(num)
    item = Cart.objects.get(id=id)
    item.count += num

    if item.count < 0:
        item.count = 0

    item.summa = item.calculateSumma()
    item.save()

    return redirect('tocart')


import telebot


def telegram(neworder):
    chat = '805774017'
    message = neworder.user.username + ' ' + neworder.tel + ' ' + neworder.myzakaz
    bot = telebot.TeleBot('6293182974:AAHmAzvlIPtnFgaAsBcJ0oES91Dj8uBLMuY')
    bot.send_message(chat, 'новый заказ')
    bot.send_message(chat, message)

# def telegram(neworder):
#     token = '6293182974:AAHmAzvlIPtnFgaAsBcJ0oES91Dj8uBLMuY'
#     # t.me/turtle3000_bot
#     chat = '805774017'
#     message = neworder.user.username + ' ' + neworder.tel + ' ' + neworder.myzakaz
#     url = f"<https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={message}>"
#     requests.get(url)
