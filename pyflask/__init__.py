from log import logger_pyflask
from flask import Flask, render_template, request, redirect, url_for
from process.buySellProcess import buySellProcess
import sys
from pymongo import MongoClient
from process.autoLogin import autoLogin
from process.autoLogin import autoLoginCheck
from process.realTimeForeign import  realTimeForeign
from PyQt5.QtWidgets import QApplication
from process.show_order_history import show_order_history
from process.buySellModify import buySellModify
import os
import datetime
import time
from analysis.common_data import common_min_shortTime
from analysis.monitoring import  monitoring
from analysis.monitoring2 import  monitoring2
from analysis.monitoring3 import  monitoring3
from analysis.common_data import common_min_timeline
from process.realTimeProgram import realTimeProgram
from process.realTimePrice import realTimePrice
from data.TR_1206 import TR_1206
from data.TR_1314_3 import TR_1314_3
from process.realTimeConclusion import realTimeConclusion