from django.shortcuts import render, redirect
from .forms import StockForm
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import numpy as np
import io

def index(request):
    form = StockForm(request.POST)
    return render(request, "stock/index.html", {"form":form}) 

def com(request):
    form = StockForm(request.POST)

    if form.is_valid():
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
        plt.plot(date, df["sma01"], label="sma01", color="#e84a5f")
        plt.plot(date, df["sma02"], label="sma02", color="#ff847c")
        plt.plot(date, df["sma03"], label="sma03", color="#feceab")
        plt.legend()

        plt.subplot(2,1,2)
        plt.bar(date,df["Volume"], label="Volume", color="grey")
        plt.legend()
        return render( request, "stock/index.html", {"form":form} )
        

def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s
        

def get_svg(request):
    com(request) 
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

# Create your views here.
