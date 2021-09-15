#Creating a Blank spaCy Model

import spacy
import pandas as pd

text = "Martha, a senior, moved to Spain where she will be playing basketball until 05 June 2022 or until she can't play any longer."

nlp = spacy.blank("en")
#en_model = spacy.load("en_core_web_lg")

ruler = nlp.add_pipe("entity_ruler")

patterns = [{"label":"SPORT", "pattern":"basketball"},
            {"label":"SPORT", "pattern":"Spain"}]

ruler.add_patterns(patterns)

#doc = main_nlp('/src/df_extracted.csv')
df_extracted = pd.read_csv('C:/Users/ohike/PycharmProjects/CBi-MRC-Analytics/src/df_extracted.csv')
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)

#save a spaCy Model
#main_nlp.to_disk("disaster_management_ner")