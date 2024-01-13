from django.shortcuts import render


def index(req):
    data = {}
    return render(req, 'index.html', data)


