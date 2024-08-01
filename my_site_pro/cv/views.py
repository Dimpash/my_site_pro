from django.shortcuts import render, redirect
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import json
from os import listdir
from os.path import isfile, join


# data = {
    #     'app1': {
    #     'Category': 'Web app', 'Client': 'ASU Company', 'Period': '01 March, 2020', 'Project URL': 'www.example.com', 'Filter': 'App'},
    #     'simba': {
    #     'Category': 'Web app, Databases', 'Client': 'RUE "Vitebskenergo"', 'Period': '2023', 'Project URL': '', 'Filter': 'App'}, 
    #     'bars': {
    #     'Category': 'Desktop app, Databases', 'Client': 'RUE "Vitebskenergo"', 'Period': '2015-2024', 'Project URL': '', 'Filter': 'App'}
    #     }
    # # e.g. file = './data.json' 
    # with open('media/cv/portfolio_detail.json', 'w') as f: 
    #     json.dump(data, f)


def read_portfolio_detail():
    with open('media/cv/portfolio_detail.json', 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

# Create your views here.
########################################
# Main page for CV 
########################################
def cv_start(request, lang='en'):
    portfolio_items = read_portfolio_detail()
    # select filters fo portfolio
    filters = []
    for key, value in portfolio_items.items():
        if not value['Filter'] in filters:
            filters.append(value['Filter'])
    filters.sort()
    context = {
        'my_age': relativedelta(dt.today(), dt.strptime('21.09.1976', '%d.%m.%Y')).years,
        'portfolio_items': portfolio_items,
        'filters': filters
        }
    return render(request, f'cv/{lang}/index.html', context=context)


########################################
# Main page for CV 
########################################
def cv_index(request, lang='en'):
    return redirect('cv-start', lang=lang)


########################################
# Portfolio details
########################################
def portfolio_details(request, lang, portfolio_name):
    portfolio_items = read_portfolio_detail()
    pf_item = portfolio_items[portfolio_name]
    img_dir = f'cv/static/cv/img/portfolio/{portfolio_name}/'
    images = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
    context = {
        'pf_name': portfolio_name,
        'pf_item': pf_item,
        'images': images
        }
    return render(request, f'cv/{lang}/portfolio-details.html', context=context)