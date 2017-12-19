#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:42:38 2017

@author: acoth
"""

from flask import Flask, request, render_template
import pathfinder
from io import BytesIO
import re


app = Flask(__name__)
#@app.route('/odds')
def drawGraph(d='3d6',c='9'):
    si = BytesIO()
    pathfinder.Analyze(d,c,si)
#    return(send_file(si,mimetype='image/svg'))
    return(re.search(r'<svg.*',si.getvalue(),re.DOTALL).group(0))
    
@app.route('/',methods=['GET','POST'])
def page():
    
#    retPage = '<html><head><title>Pathfinder Odds Calculator</title></head>\n<body><img src="%s"></body></html>'%'odds.svg'
    if request.method=='GET':
        params = ['2d6;1d12',8]
    if request.method=='POST':
        params = [request.form['dieString'].encode('utf8'),request.form['check'].encode('utf8')]
#        print params
    return(render_template('page.html',svg=drawGraph(*params),curr_die=params[0],curr_check=params[1]))

app.run(host='0.0.0.0',port=5001)
