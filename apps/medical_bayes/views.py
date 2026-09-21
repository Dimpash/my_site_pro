from django.contrib.staticfiles import finders
from django.http import HttpResponse


def medical_bayes(request):
    path = finders.find("medical_bayes/index.html")

    if not path:
        return HttpResponse(
            "Medical Bayes application not found",
            status=404,
        )

    with open(path, "rb") as f:
        return HttpResponse(
            f.read(),
            content_type="text/html",
        )