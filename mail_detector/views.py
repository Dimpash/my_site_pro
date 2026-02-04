# views.py
from django.shortcuts import render
from .mail_detect import detect_provider, extract_domain

def email_check(request):
    context = {}

    if request.method == "POST":
        raw_value = request.POST.get("value", "").strip()

        if "@" in raw_value or "." in raw_value:
            domain = extract_domain(raw_value)
            result = detect_provider(domain)

            context.update({
                "input": raw_value,
                "domain": domain,
                "result": result,
            })
        else:
            context["error"] = "Please enter a valid email or domain."

    return render(request, "mail_detector/email_check.html", context)
