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
    
    if request.method=='GET':
        params = {'dieStrings':'2d6;1d12','check':8}
    if request.method=='POST':
        params = {'dieStrings':request.form['dieString'].encode('utf8'),
                  'check':request.form['check'].encode('utf8')}
#        print params
    return(render_template('page.html',graph=pathfinder.Analyze(**params),curr_die=params['dieStrings'],curr_check=params['check']))

app.run(host='0.0.0.0',port=5001)
