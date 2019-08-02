import json, requests
import pandas as pd
from hatebase import HatebaseAPI

hatebase = HatebaseAPI({"key": '4UyMTCENrNkmsYgPZiRneBVbVJYHDY7F'})
filters = {"language": "eng"}
format = "json"
# initialize list for all vocabulary entry dictionaries
ara_vocab = []
response = hatebase.getVocabulary(filters=filters, format=format)
pages = response["number_of_pages"]
# fill the vocabulary list with all entries of all pages
# this might take some time...
for page in range(1, pages+1):
    filters["page"] = str(page)
    response = hatebase.getVocabulary(filters=filters, format=format)
    ara_vocab.append(response["result"])

# create empty pandas df for all vocabulary entries
df_ara_vocab = pd.DataFrame()
# fill df
for elem in ara_vocab:
    df_ara_vocab = df_ara_vocab.append(elem)
# reset the df index
df_ara_vocab.reset_index(drop=True, inplace=True)
df_ara_vocab.to_csv('hatebase_eng.csv')
