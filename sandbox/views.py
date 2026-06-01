from django.shortcuts import render


def fb_privacy(request): 
    return render(request, "sandbox/fb_privacy.html")


def fb_terms(request): 
    return render(request, "sandbox/fb_terms.html")


def fb_data_deletion(request): 
    return render(request, "sandbox/fb_data-deletion.html")