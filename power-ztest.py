# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 23:09:12 2021

@author: Carlos
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
from load_css import local_css

st.set_page_config(layout="centered")
st.title("Power of z.test")
st.write("Author: Carlos Pérez González (ULL)")
local_css("styles.css") 



col = st.beta_columns(4)

with col[0]:        
    tail=st.radio(
    'Select test type:',  
    ('Two tails', 'Left tail', 'Right tail'),
    index=0)

    #if tail == 'Two tails':
    #     st.write('You selected Two tails.')
    #else:
    #    st.write("You didn't select Two tails.")
        
    #if tail == 'Two tails':
    #     st.markdown('<p class="big-font">You selected Two tails.</p>', unsafe_allow_html=True)
    #else:
    #    st.markdown("<p class='big-font'>You didn't selected Two tails.</p>", unsafe_allow_html=True)
        
       
with col[1]:   
    effect_size=st.slider('effect size d', -0.15, 0.15, 0.15, 0.01)
    #st.write("effect size:", effect_size)

with col[2]:   
    alpha=st.slider('alfa \u03B1', 0.01, 0.15, 0.05, 0.01)
    #st.write("alfa \u03B1:", alpha)

with col[3]:   
    sample_size=st.slider('sample size n', 300, 500, 350)
    #st.write("sample size n:", sample_size)



def f_make(tail,effect_size,alpha,sample_size):
    
    def critical_z(alpha=0.05, tail="two"):
      """
      Given significance level, compute critical value.
      """
      if tail == "two":
        p = 1 - alpha / 2
      else:
        p = 1 - alpha        
      return norm.ppf(p)

    fig=plt.figure(figsize=(12,6))
    ax=plt.gca()
    #fig, ax = plt.subplots(figsize=(16, 8))
    #fig, ax = plt.subplots()
    #ax.cla()

    # one-tailed z-test
    h_0 = 0.8
    h_1 = h_0+effect_size
    
    #alpha = 0.05 
    #alpha = list(np.arange(0.05,0.45,0.4/1000))[frame]
    
    #n = list(range(1, 1000)) [frame]
    #n=300
    
    #tail = "two"
    se = np.sqrt(h_0 * (1 - h_0) / sample_size)

    z = critical_z(alpha=alpha, tail=tail)
    
    lower = h_0 - z * se
    upper = h_0 + z * se
    
    lower_a = norm.cdf(lower, h_1, se)
    upper_a = 1 - norm.cdf(upper, h_1, se)
    
    x = np.linspace(0.6, 0.9, 10000)
    norm_0 = norm.pdf(x, loc=h_0, scale=se)
    norm_1 = norm.pdf(x, loc=h_1, scale=se)
    ax.plot(x, norm_0, label='$H_0$')
    ax.plot(x, norm_1, label='$H_1$')
    ax.set_ylabel("Density")
    ax.set_xlabel("Sampling statistic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    #ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)  
          
    
    if tail == "Two tails":
        ax.axvline(lower, linestyle="--")
        ax.axvline(upper, linestyle="--")

        ax.annotate("\u03B1/2",  xy=(upper+0.15*(alpha-0.01), 0.05+10*(alpha-0.01)), xycoords='data',
                           xytext=(0.87, 5), textcoords='data', 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3") )
    
        ax.annotate("\u03B1/2",  xy=(lower-0.15*(alpha-0.01), 0.05+10*(alpha-0.01)), xycoords='data',
                           xytext=(0.72, 5), textcoords='data', 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3") )
        
        
        ax.fill_between(x, [0], norm_0, where=x > upper, facecolor='none', hatch='///', interpolate=True, alpha=0.3)
        ax.fill_between(x, [0], norm_0, where=x < lower, facecolor='none', hatch='///', interpolate=True, alpha=0.3, label="\u03B1: Type I error")
    
        ax.fill_between(x, [0], norm_1, where=x > upper, facecolor='C9', interpolate=True, alpha=0.3)        
        ax.fill_between(x, [0], norm_1, where=(x > lower) & (x < upper), facecolor='C3', interpolate=True, alpha=0.3, label="\u03B2: Type II error")
        ax.fill_between(x, [0], norm_1, where=x < lower, facecolor='C9', interpolate=True, alpha=0.3, label="1 - \u03B2: power")
        power = lower_a + upper_a
    
    elif tail == "Left tail":
        ax.axvline(lower, linestyle="--")
        
   
        ax.annotate("\u03B1",  xy=(lower-0.15*(alpha-0.01), 0.05+10*(alpha-0.01)), xycoords='data',
                           xytext=(0.72, 5), textcoords='data', 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3") )
        
        ax.fill_between(x, [0], norm_0, where=x < lower, facecolor='none', hatch='///', interpolate=True, alpha=0.3, label="\u03B1: Type I error")
    
            
        ax.fill_between(x, [0], norm_1, where=x > lower, facecolor='C3', interpolate=True, alpha=0.3, label="\u03B2: Type II error")
        ax.fill_between(x, [0], norm_1, where=x < lower, facecolor='C9', interpolate=True, alpha=0.3, label="1 - \u03B2: power")
        power = lower_a
    
    elif tail == "Right tail":
        ax.axvline(upper, linestyle="--")

        ax.annotate("\u03B1",  xy=(upper+0.15*(alpha-0.01), 0.05+10*(alpha-0.01)), xycoords='data',
                           xytext=(0.87, 5), textcoords='data', 
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3") )

        ax.fill_between(x, [0], norm_0, where=x > upper, facecolor='none', hatch='///', interpolate=True, alpha=0.3, label="\u03B1: Type I error")
 
        ax.fill_between(x, [0], norm_1, where=x < upper, facecolor='C3', interpolate=True, alpha=0.3, label="\u03B2: Type II error")
        ax.fill_between(x, [0], norm_1, where=x > upper, facecolor='C9', interpolate=True, alpha=0.3, label="1 - \u03B2: power")
        power = upper_a

    ax.legend(frameon=False, loc="upper left", prop={'size': 15})
    ax.set_ylim(-0.01, 35)
    ax.set_xlim(0.6, 0.9)    
    
    html="<p style='font-size:20px'> When the effect_size=%.2f, for \u03B1=%.2f and sample_size=%i"\
        " then the type II-error is <span class='highlight red'>\u03B2=<b>%.3f</b></span> and the test power"\
        " is <span class='highlight blue'>1-\u03B2=<b>%.3f</b></span> </p>" % (h_1-h_0, alpha, sample_size, 1-power, power)
    st.markdown(html, unsafe_allow_html=True)


    st.pyplot(fig, use_container_width=True)




f_make(tail,effect_size,alpha,sample_size)