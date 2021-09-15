#Creating a Blank spaCy Model

import spacy
import pandas as pd

main_nlp = spacy.blank("en")
en_model = spacy.load("en_core_web_lg")

ruler = nlp.add_pipe("entity_ruler")

patterns = [{"label":"SPORT", "pattern":"basketball"}]

ruler.add_patterns(patterns)

#doc = main_nlp('/src/df_extracted.csv')
df_extracted = pd.read_csv('C:/Users/ohike/PycharmProjects/CBi-MRC-Analytics/src/df_extracted.csv')
doc = nlp(df_extracted)

main_nlp.to_disk("disaster_management_ner")
#save a spaCy Model
#main_nlp.to_disk("sample_spacy_model")
