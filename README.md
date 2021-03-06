Forecasting_Mutual_Funds
=====================

This Project gives you an overall idea for Forecasting Mutual Funds.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![License](https://img.shields.io/pypi/l/selenium-wire.svg)
<!--- ![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)--->

Introduction
============
* Project performs forecasting by using different Time Series algorithms.
* This gives you an overall idea about how each algorithm forecast same mutual fund.
* Performs Next 30 days forecasting.
  

Installation
=============
Clone this repository and install the requirements.


Pre-Requisite
==============
Project required Mutual fund scheme code, *[here](https://raw.githubusercontent.com/NayakwadiS/mftool/master/Scheme_codes.txt)* you can get those. 


Steps to Run from Terminal
=================
1. Direct to cloned repository path in CMD or Terminal
2. Run main.py 
```shell
  >>D:\Forecasting_Mutual_Funds> python main.py
```
3. Enter Mutual Fund Scheme code you want to Forecast
```shell
  >>Enter the MF Scheme code:- MF code
```
4. Wait a minute to get the result as 

<img src="./images/forecasting_cmd.JPG" >
<img src="./images/forecasting_plot.jpg" >


Steps to Run as Web App
=================
1. Direct to cloned repository path and Run app.py
2. Navigate to http://localhost:5000/
3. Enter Scheme code, select Algorithm and click Submit

<img src="./images/web_app.jpg" >


Disclaimer
================
This project gives an idea about MF forecasting and should not be considered as investment advice.


To Do
================
Creation of Advance Webapp 


