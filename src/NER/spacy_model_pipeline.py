#Creating a Blank spaCy Model

import spacy
import pandas as pd
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher
from spacy import displacy
import en_core_web_lg
from io import StringIO
from collections import Counter
import os
from os import listdir
from os.path import isfile, join

#Bypass error: larger than field limit
import sys
import csv
maxInt= sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt= int(maxInt/10)

def get_entities(x):
    result = {}
    doc = nlp(x)
    for ent in doc.ents:
        result[ent.label_] = ent.text
    return result


#Corpus
emergency = ['conflict', 'violence', 'displacement', 'drought', 'earthquake', 'fire', 'flooding', 'freeze', 'health emergency', 'dengue', 'pneumonic plague', 'measles', 'landslide', 'tropical storm', 'typhoon', 'cyclone', 'hurricane', 'tsunami', 'urban disaster', 'volcanic eruption', 'volcano', 'refugee', 'terrorist attack', 'cold wave', 'complex emergency', 'epidemic', 'extratropical cyclone', 'flash flood', 'flood', 'heat wave', 'insect infestation', 'land slide', 'mud slide', 'severe local storm', 'snow avalanche', 'storm surge', 'technological disaster', 'tropical cyclone', 'volcano', 'wild fire', 'flood crisis', 'victims', 'flood victims', 'flood powerful', 'powerful storms', 'hoisted flood', 'explosion', 'flood cost', 'affected tornado', 'tornado relief', 'photos flood', 'water rises',  'flood waters', 'flood appeal', 'victims explosion', 'bombing suspect', 'massive explosion', 'affected areas','flood relief', 'flood affected', 'tornado victims', 'explosions running', 'evacuated', 'relief', 'flood death', 'deaths confirmed', 'affected flooding', 'people killed', 'dozens', 'footage', 'survivor finds', 'flood worsens', 'flood damage', 'major flood', 'rubble', 'another explosion', 'confirmed dead', 'rescue','flood warnings', 'tornado survivor', 'damage', 'devastating', 'flood toll', 'affected hurricane', 'prayers families', 'crisis', 'text donation', 'redcross give', 'recede', 'bombing', 'massive', 'bombing victims', 'explosion ripped', 'gets donated', 'donated victims', 'relief efforts', 'news flood', 'flood emergency', 'fire flood', 'huge explosion', 'bushfire', 'torrential rains', 'affected explosion', 'disaster', 'tragedy','twister', 'blast', 'fatalities', 'dead explosion', 'survivor', 'death', 'explosion reported', 'evacuees', 'large explosion', 'firefighters', 'morning flood', 'praying', 'public safety', 'destroyed', 'displaced', 'fertilizer explosion', 'donate tornado', 'retweet donate', 'flood tornado', 'casualties', 'climate change', 'financial donations', 'stay strong', 'dead hundreds', 'major explosion', 'bodies recovered', 'waters recede', 'response disasters', 'victims donate','fire fighters', 'explosion victims', 'prayers city', 'torrential', 'bomber', 'explosion registered', 'missing flood', 'brought hurricane', 'relief fund', 'help tornado', 'explosion fire', 'tragic', 'enforcement official', 'dealing hurricane', 'flood recovery', 'dead torrential', 'flood years', 'massive tornado', 'crisis rises', 'flood peak', 'flood ravaged','missing explosion', 'floods kill', 'tornado damage', 'cross tornado', 'facing flood', 'deadly explosion', 'dead missing', 'floods force', 'flood disaster', 'tornado disaster', 'medical examiner', 'fire explosion', 'storm', 'flood hits', 'floodwaters', 'emergency', 'flood alerts', 'crisis unfolds', 'daring rescue', 'tragic events', 'medical office', 'deadly tornado', 'people trapped', 'lives hurricane', 'bombings reports', 'breaking suspect', 'bombing investigation', 'praying affected', 'surging floods', 'explosion injured', 'injured explosion', 'responders killed', 'explosion caught', 'city tornado', 'damaged hurricane', 'suspect bombing', 'massive manhunt', 'releases images', 'shot killed', 'rains severely', 'house flood', 'live coverage', 'devastating tornado', 'lost lives', 'reportedly dead', 'following explosion', 'remember lives', 'tornado flood', 'want help', 'seconds bombing', 'reported dead', 'safe hurricane','dead floods', 'flood threat', 'flood situation', 'thousands homes', 'risk running', 'dying hurricane', 'bombing shot','police people', 'terrible explosion', 'prayers involved', 'reported injured', 'seismic', 'victims waters', 'flood homeowners', 'flood claims', 'homeowners reconnect', 'reconnect power', 'power supplies', 'rescuers help', 'free hotline', 'hotline help', 'saddened loss', 'identified suspect', 'bombings saddened','reported explosion', 'prepare hurricane', 'landfall', 'bombing case','communities damaged', 'destruction', 'levy', 'tornado', 'hurricane coming', 'toxins flood', 'release toxins', 'toxins', 'supplies waters', 'crisis found', 'braces major', 'government negligent', 'terror', 'memorial service', 'terror attack', 'coast hurricane', 'terrified hurricane', 'hurricane category', 'devastating fire', 'disaster area', 'disaster preparedness', 'disaster recovery', 'disaster relief', 'disaster response', 'natural disaster', 'disasters', 'natural disasters', 'disaster site', 'disaster situation', 'emergency response', 'flood control', 'flood damage', 'flood relief', 'flooded', 'flooding', 'heavy rainfall']
emergency_event = ['haiti earthquake', 'earthquake in haiti', 'tropical storm grace', 'coronavirus', 'corona virus', 'coronavirus disease', 'covid-19', 'typhoon goni', 'typhoon rolly', 'typhoon vamco', 'typhoon ulysses', 'beirut port explosions', 'beirut explosion', 'beirut blast', 'cyclone harold', 'hurricane dorian', 'cyclone kenneth', 'cyclone idai', 'indonesia tsunami', 'indian ocean earthquake', 'indian ocean tsunami', 'typhoon manghut']
humanitarian_theme = ['accountability to affected people', 'business continuity', 'civil military coordination', 'climate change', 'community engagement', 'conflict and fragility', 'disaster risk reduction', 'disaster risk', 'early warning', 'early warning system', 'gender', 'humanitarian development index', 'humanitarian development nexus', 'humanitarian development', 'human rights', 'impact measurement', 'innovation and new technologies', 'innovation and technologies', 'forced displacement', 'peace', 'preparedness', 'prevention', 'public private partnership', 'recovery', 'response', 'MSME', 'small and medium sized enterprise', 'small and medium sized enterprises', 'sustainable development', 'sustainable development goals', 'affected families', 'affected regions', 'aid agencies', 'aids', 'collapsed']
humanitarian_action_clusters = ['food security', 'health', 'logistic', 'logistics', 'nutrition', 'protection', 'shelter', 'water sanitation', 'water hygiene', 'hygiene', 'camp coordination', 'early recovery', 'education', 'emergency telecommunication', 'emergency telecommunications']

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 12000000000
ruler = EntityRuler(nlp, overwrite_ents=True)

#Phrase Matcher
emergency_words = [nlp(text) for text in emergency]
emergency_event_words = [nlp(text) for text in emergency_event]
humanitarian_theme_words = [nlp(text) for text in humanitarian_theme]
humanitarian_action_clusters = [nlp(text) for text in humanitarian_action_clusters]

matcher = PhraseMatcher(nlp.vocab)
matcher.add('EMERGENCY', None, *emergency_words)
matcher.add('EMERGENCY_EVENT', None, *emergency_event_words)
matcher.add('HUMANITARIAN_THEME', None, *humanitarian_theme_words)
matcher.add('HUM_ACTION_CLUSTER', None, *humanitarian_action_clusters)


#Load Dataframe
df_extracted = pd.read_csv('df_extracted_1.csv', engine='python', encoding='utf-8', error_bad_lines=False)
df_extracted['text'] = df_extracted['text'].map(str)
#df_extracted['file_name'] = df_extracted['file_name'].str.replace(r'.txt$', '')
#df_extracted['text'] = df_extracted['text'].str.lower()
#df_extracted['text'] = df_extracted['text'].str.replace("\n","").replace("\t"," ").replace("\x0c"," ").replace(".",". ")
#df_extracted['text'] = df_extracted['text'].str.replace("\r"," ").replace(',',"").replace("\r\n"," ")

d = []
for i in range(len(df_extracted['text'])):
    file_name = df_extracted['file_name'][i]
    text = df_extracted['text'][i]

    doc = nlp(text)
    matches= matcher(doc)
    for match_id, start, end in matches:
        string_ = nlp.vocab.strings[match_id]
        span = doc[start: end]
        first_position = start / len(doc)
        d.append((file_name, string_, span.text, first_position))

df_documentConcepts = pd.DataFrame(d, columns=['file_name', 'concepts.facet', 'concepts.facet_instance', 'first_position'])
df_documentConcepts.to_csv('df_documentConcepts_1.csv')

#save a spaCy Model
nlp.to_disk("disaster_management_ner")