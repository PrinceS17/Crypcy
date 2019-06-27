# Crypcy
Crypto Currency Value Maker: A cypoto currency analysis website built with django.

<!--
Crypcy readme:
1. introduction of the whole project
2. framework: django(backend) + react(frontend) + AWS(deployment)
3. functionalities (brief, only advance function here)
  * 1) basic functions: select, sort, insert, etc
  2) advance functions: price prediction, customized recommendations
4. related links: website, demo video, 
  team member
-->

## Overview
Crypcy is a crypto-currency analysis website where people can watch popular crypto-currencies, receive personalized recommendations and make decisions based on the price prediction and future trend estimation. It is built by Team 42 (Fanhui Zeng, Jinhui Song, Ruixin Zou, Yichi Zhang) using Django + React + AWS. Hope you have fun with the thrilling investment and catch the next Bitcoin!

## Features
__1. Predict Future Value__

Though there is actually no 100% accurate prediction in the world, we try to give our user an impression of how the price will behave based on its recent trend. Future price in the next 5 days will be shown in green right after the current price which is in blue in the same price figure on the website. The utility, i.e. estimation of the trend in the recent future, is defined as follows:

Utility = avg(predicted price in 5 days) / price of last day * 100

Therefore, a higher utility to some extent indicates a higher possibility of price increase in the recent future. 

__2. Customized Investment Advice__

While user can add his or her favorite coin into the watchlist, our website will give customized advice for each user according to their preference on risk and their favorites. We evaluate the risk mainly based on the variance of the historical price and each coin has a tag of "high/moderate/low" risk. Then risk along with other attributes such as volume, utility are considered to give 5 recommendations to each user.  

## How to Build
To test the this project in your local host, you can first clone it to your local folder. We recommend use python virtual environment for the following operations. Input the following commands under your directory for the project: 

```
$ pip install -r requirements.txt
$ python manage.py runserver
```

Then visit http://127.0.0.1:8000/ to enjoy Crypcy!

## Related Links
Homepage: http://crypcy.s3-website.us-west-2.amazonaws.com/ (under maintainance to improve the backend)

Demo Video: https://youtu.be/tKva8R8gFb8
