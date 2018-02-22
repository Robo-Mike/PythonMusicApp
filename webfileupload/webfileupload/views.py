from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def testdb(request):
    try:
        count = 0
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            data =  cursor.fetchall()
            count = len(data)
    except:
        raise Http404("Cannot connect to default db")
    return HttpResponse("%s database tables found" % count )
