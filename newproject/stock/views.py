from django.shortcuts import render, redirect
from .forms import StockForm
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from pandas_datareader import data
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplfinance as mpf
import warnings
import numpy as np
import io
#warnings.simplefilter("ignore")

def index(request):
    form = StockForm(request.POST or None)
    return render(request, "stock/index.html", {"form":form}) 

def pltver(request):
    form = StockForm(request.POST or None)

    if form.is_valid():
        if "button_1" in request.POST:

            company_code = form.cleaned_data["title"]
            start = form.cleaned_data["day_start"]
            end = form.cleaned_data["day_end"]

            df = data.DataReader( company_code , "stooq")
            df = df[(df.index>=start ) & (df.index<=end)]

            date = df.index
            price=df["Close"]

            span01 = 5
            span02 = 25
            span03 = 50

            df["sma01"] = price.rolling(window=span01).mean()
            df["sma02"] = price.rolling(window=span02).mean()
            df["sma03"] = price.rolling(window=span03).mean()

            plt.figure(figsize=(20,10))
            plt.subplot(2,1,1)

            plt.plot(date, price, label = "Close", color="#99b898")
            plt.plot(date, df["sma01"], label="moving average(5days)", color="#e84a5f")
            plt.plot(date, df["sma02"], label="moving average(25days)", color="#ff847c")
            plt.plot(date, df["sma03"], label="moving average(50days)", color="#feceab")
            plt.title( company_code, color="black", size=30)
            plt.ylabel("p\nr\ni\nc\ne", labelpad=15, color="black", size=10, rotation=0, va="center")
            plt.legend()

            plt.subplot(2,1,2)
            plt.bar(date,df["Volume"], label="Volume", color="grey")
            plt.gca().ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
            plt.ylabel("V\no\nl\nu\nm\ne", labelpad=15, color="black", size=10, rotation=0, va="center")
            plt.legend()
        
        elif "button_2" in request.POST:
            company_code = form.cleaned_data["title"]
            start = form.cleaned_data["day_start"]
            end = form.cleaned_data["day_end"]

            df = data.DataReader( company_code , "stooq")
            df = df[(df.index>=start ) & (df.index<=end)]
            df = df.sort_index()
            mpf.plot(df, type="candle", figsize=(20,10), style="mike", volume=True, ylabel="price", title=company_code)


#def mpfver(request):
    #form = StockForm(request.POST or None)

    #if form.is_valid():
        #company_code = form.cleaned_data["title"]
        #start = form.cleaned_data["day_start"]
        #end = form.cleaned_data["day_end"]

        #df = data.DataReader( company_code , "stooq")
        #df = df.sort_index()
        #mpf.plot(df, type="candle", figsize=(20,10), style="mike", volume=True)

def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

#def mpf2svg():
    #buf = io.BytesIO()
    #plt.savefig(buf, format='svg', bbox_inches='tight')
    #s = buf.getvalue()
    #buf.close()
    #return s

def plt_svg(request):
    pltver(request) 
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

#def mpf_svg(request):
    #mpfver(request) 
    #svg = mpf2svg()  #SVG化
    #plt.cla()  # グラフをリセット
    #response = HttpResponse(svg, content_type='image/svg+xml')
    #return response

