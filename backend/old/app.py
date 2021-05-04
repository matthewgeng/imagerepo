import streamlit as st
import pandas as pd
import numpy as np

st.markdown("<h1 style='text-align:center;color:Orange;'>Onboarding Personalization</h1>",unsafe_allow_html=True)


st.write('''

Whether it be Netflix, Apple Music or Domino's Pizza, personalizaiton requires user preferences. Without an understanding of the factors that contribute to a users taste, a recommendation system can never know what is the appropriate next offer. 

Learning user preferences in financial services, appears to be behavior observation, experiment and survey research combined in a statistically significant manner. When utilizing methods that have proven significance, repeatable and increasingly accurate assumtions can be made upon user preferences from the factors we know correlate with our customer base. 

From discussions as well as research into how others in the financial services are capturing user preferences, it appears as if there is an opportunity to offer a better service.

Where others in the industry are viewing customer inteake as an after thought - if we view it as the first touchpoint in a personalizaiton pipeline, we can build onboarding into insights that greatly benefit both the advisor and their customer. 
''')

st.markdown("<h1 style='text-align:center;color:Orange;'>Onboarding Personalization</h1>",unsafe_allow_html=True)

st.write('''
Research has shown that personality factors can provide statistically significant insight into the preferences of wealth customers. 

It has been shown that the Big Five Personality trait metrics "significantly predict financial risk tolerance," and thus can begin to model user prefernce for investment instruments. The applications possible from this base are many: 
''')


st.markdown("<h2 style='text-align:center;color:Orange;'>The Big Five for FI Onboarding</h2>",unsafe_allow_html=True)

st.write('''

Describe yourself as you generally are now, not as you wish to be in the future. 

Describe yourself as you honestly see yourself, in relation to other people you know of the same sex as you are, and roughly your same age. 

So that you can describe yourself in an honest manner, your responses will be kept in absolute confidence. 

Indicate for each statement below how much the statement describes you: 

''')

st.sidebar.markdown('''
#
#
#
#
#
#
#
#
#
#
Values for Survey: 

1. Very Inacurate 

2. Moderately Inacurate 

3. Neither Accurate or Inaccurate 

4. Moderately Accurate 

5. Very Accurate
''')

st.markdown("<h5 style='text-align:center;color:Orange;'>1. Very Inacurate 2.Moderately Inacurate 3. Neither Accurate or Inaccurate 4. Moderately Accurate 5. Very Accurate<h5>",unsafe_allow_html=True)

def survey():
    a = st.slider("I am the life of the party",min_value=1,max_value=5)
    b = st.slider("Feel little concern for others", min_value=1,max_value=5)
    c = st.slider("Am always prepared", min_value=1,max_value=5)
    d = st.slider("Get stressed out easily",min_value=1,max_value=5)
    e = st.slider("Have a rich vocabularly",min_value=1,max_value=5)
    f = st.slider("Dont talk a lot", min_value=1,max_value=5)
    g = st.slider("Am interested in people",min_value=1,max_value=5)
    h = st.slider("Leave my belongings around",min_value=1,max_value=5)
    i = st.slider("Am relaxed most of the time",min_value=1,max_value=5)
    j = st.slider("Have difficulty understanding abstract ideas",min_value=1,max_value=5)
    k = st.slider("Feel comfortable around people",min_value=1,max_value=5)
    l = st.slider("Insult people",min_value=1,max_value=5)
    m = st.slider("Pay attention to details",min_value=1,max_value=5)
    n = st.slider("Worry about things",min_value=1,max_value=5)
    o = st.slider("Have a vivid imagination",min_value=1,max_value=5)
    p = st.slider("Keep in the background",min_value=1,max_value=5)
    q = st.slider("Symathize with others feelings",min_value=1,max_value=5)
    r = st.slider("Make a mess of things",min_value=1,max_value=5)
    s = st.slider("Seldom feel blue",min_value=1,max_value=5)
    t = st.slider("Am not interested in abstract ideas",min_value=1,max_value=5)
    u = st.slider("Start conversations.",min_value=1,max_value=5)
    v = st.slider("Am not interested in other people's problems",min_value=1,max_value=5)
    w = st.slider("Get chores done right away",min_value=1,max_value=5)
    x = st.slider("Am easily disturbed",min_value=1,max_value=5)
    y = st.slider("Have excellent ideas",min_value=1,max_value=5)
    z = st.slider("Have little to say.",min_value=1,max_value=5)
    aa = st.slider("Have a soft heart.",min_value=1,max_value=5)
    bb = st.slider("Often forget to put things back in their proper place",min_value=1,max_value=5)
    cc = st.slider("Get upset easily",min_value=1,max_value=5)
    dd = st.slider("Do not have a good imagination.",min_value=1,max_value=5)
    ee = st.slider("Talk to a lot of different people at parties",min_value=1,max_value=5)
    ff = st.slider("Am not really interested in others",min_value=1,max_value=5)
    gg = st.slider("Like order",min_value=1,max_value=5)
    hh = st.slider("Change my mood a lot",min_value=1,max_value=5)
    ii = st.slider("Am quick to understand things",min_value=1,max_value=5)
    jj = st.slider("Dont like to draw attention to myself.",min_value=1,max_value=5)
    kk = st.slider("Take time out for others.",min_value=1,max_value=5)
    ll = st.slider("Shirk my duties.",min_value=1,max_value=5)
    mm = st.slider("Have frequent mood swings",min_value=1,max_value=5)
    nn = st.slider("Use difficult words.",min_value=1,max_value=5)
    oo = st.slider("Don't mind being the center of attention",min_value=1,max_value=5)
    pp = st.slider("Feel others' emotions",min_value=1,max_value=5)
    qq = st.slider("Follow a schedule",min_value=1,max_value=5)
    rr = st.slider("Get irritated easily.",min_value=1,max_value=5)
    ss = st.slider("Spend time reflecting on things.",min_value=1,max_value=5)
    tt = st.slider("Am quiet around strangers",min_value=1,max_value=5)
    uu = st.slider("Make people feel at ease",min_value=1,max_value=5)
    vv = st.slider("Am exacting in my work.",min_value=1,max_value=5)
    ww = st.slider("Often feel blue.",min_value=1,max_value=5)
    xx = st.slider("Am full of ideas",min_value=1,max_value=5)
    if st.button("Submit"):
        features = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo,pp,qq,rr,ss,tt,uu,vv,ww,xx]
        #extraversion factors 
        positive_extraversion = [a,k,u,ee,oo]
        negative_extraversion = [f,p,z,jj,tt]
        neg_extra_convert = []
        for factor in negative_extraversion:
            if factor == 5:
                 factor = factor - 4 
            elif factor == 4:
                factor = factor - 2
            elif factor == 2:
                factor = factor + 2
            elif factor == 1:
                factor = factor + 4
            neg_extra_convert.append(factor)
        extraversion = positive_extraversion + neg_extra_convert
        extraversion = sum(extraversion) / 10
        
        #agreeableness factors
        positive_agree = [g,q,aa,kk,pp,uu]
        negative_agree = [b,l,v,ff]
        negative_agree_convert = []
        for factor in negative_agree:
             if factor == 5:
                 factor = factor - 4 
             elif factor == 4:
                factor = factor - 2
             elif factor == 2:
                factor = factor + 2
             elif factor == 1:
                factor = factor + 4
             negative_agree_convert.append(factor)
        agreeableness = positive_agree + negative_agree_convert
        agreeableness = sum(agreeableness) / 10

        #conscientiousness factors
        positive_consc = [c,m,w,gg,qq,vv]
        negative_consc = [h,r,bb,ll]
        negative_consc_convert = []
        for factor in negative_consc:
            if factor == 5:
                factor = factor - 4 
            elif factor == 4:
                factor = factor - 2
            elif factor == 2:
                factor = factor + 2
            elif factor == 1:
                factor = factor + 4
            negative_consc_convert.append(factor)
        conscientiousness = positive_consc + negative_consc_convert
        conscientiousness = sum(conscientiousness) / 10

        #emotional stability factors
        positive_emotion = [i,s]
        negative_emotion = [d,n,x,cc,hh,mm,rr,ww]
        negative_emotion_convert = []
        for factor in negative_emotion:
            if factor == 5:
                factor = factor - 4 
            elif factor == 4:
                factor = factor - 2
            elif factor == 2:
                factor = factor + 2
            elif factor == 1:
                factor = factor + 4
            negative_emotion_convert.append(factor)
        emotional_stability = positive_emotion + negative_emotion_convert
        emotional_stability = sum(emotional_stability) / 10

        #imagination factors
        positive_imagination = [e,o,y,ii,nn,ss,xx]
        negative_imagination = [j,t,dd]
        negative_imagination_convert = []
        for factor in negative_imagination:
            if factor == 5:
                factor = factor - 4 
            elif factor == 4:
                factor = factor - 2
            elif factor == 2:
                factor = factor + 2
            elif factor == 1:
                factor = factor + 4
            negative_imagination_convert.append(factor)
        imagination = positive_imagination + negative_imagination_convert
        imagination = sum(imagination) / 10
        st.write(extraversion)
        st.write(agreeableness)
        st.write(conscientiousness)
        st.write(emotional_stability)
        st.write(imagination)

        df = pd.DataFrame({'Extraversion':extraversion,'Extra_Mean':3.03,'Agreeableness':agreeableness,'Agree_Mean':3.16,'Conscientiousness':conscientiousness,'Consc_Mean':3.12,'Emotion':emotional_stability,'Emotion_Mean':3.01,'Imagination':imagination,'Imagine_Mean':3.28},index=[0])
        st.write(df)
        st.vega_lite_chart(df,{
            'width': 600,
            'height': 400,
            'mark': {'type': 'bar', 'tooltip': True},
            'encoding':{
                'x': {'field': 'extraversion', 'type':'nominal'},
                'y': {'field': 'value', 'type': 'quantitative'}
        }})


survey()


