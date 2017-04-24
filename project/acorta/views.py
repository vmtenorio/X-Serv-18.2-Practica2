from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from acorta.models import Page
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def barra(request):
    if request.method == "GET":
        template = get_template("form.html")
        urls=""
        for i in Page.objects.all():
            urls += ("<br/><a href='" + i.url + "'>" + i.url + "</a>: " +
                    "<a href='" + str(i.shortened) + "'>" + str(i.shortened) + "</a>")
        resp = template.render(Context({'urls': urls}))
    elif request.method == "POST":
        try:
            url = request.POST['url']
        except KeyError:
            return HttpResponse("Bad Request", status=400)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            num = len(Page.objects.all())
            page = Page(url=url, shortened=num)
            page.save()
        resp = ("<html><body><h1>Page successfully shortened:</h1>" +
                "<p>URL: <a href='" + url + "'>" + url + "</a></p>" +
                "<p>Shortened URL: <a href='" + str(Page.objects.get(url=url).shortened) + "'>" +
                str(Page.objects.get(url=url).shortened) + "</a></p></body></html>")
    else:
        return HttpResponse("Method not allowed", status=405)

    return HttpResponse(resp)

def pag(request, num):
    url = Page.objects.get(shortened=num).url
    resp = ("<html><head><meta http-equiv='Refresh' " +
            "content='2;url=" + url + "'></head>" +
            "<body><p>Seras redireccionado a " + url + " en 2 segundos o si haces click " +
            "<a href='" + url + "'>aqui</a></p></body></html>")
    return HttpResponse(resp, status=303)
