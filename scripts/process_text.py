import os
from docx.api import Document
import pandas as pd
from copy import deepcopy
import pathlib
from unidecode import unidecode
import re

"""
++++++++++++++++
This script processes the text from the google doc and converts it to markdown.
It depends on the order of the columns in the google doc.
So, if the order changes, the legend and artist dictionary should be updated.
++++++++++++++++
"""

mypath = pathlib.Path(__file__).parent.resolve()

url = "https://docs.google.com/document/d/1BCMRd1i1gBC3QLQRgUbdr2NovkSM8K0xoJLwaWkVamc/export?format=docx"

legend = ["author", "title", "year", "statement", "medium_type", "material", "dimension", "id", "qrcode", "status"]
artist = {
    "author": "name",
    "title": "title",
    "year": "year",
    "statement": "statement",
    "medium_type": "type",
    "material": "material",
    "dimension": "dimension",
    "equips": "equips",
    "needs": "needs",
    "status": "status",
}

def process_excerpt(data):
    excerpt = ""
    ar = data.split(". ")
    if len(ar) <= 3:
        excerpt = data.replace('"',"'").replace("\n","")
    else:
        excerpt =  ". ".join(ar[:3]).replace('"',"'").replace("\n","") + "..."
    return excerpt
    

def to_markdown(data):
    md = "---\n"
    md += "type: artist\n"
    for i in range(len(legend)):
        if legend[i] == "author":
            d = data[legend[i]].replace('"',"'")
            d = remove_emojis(d).strip()
            md += f"{legend[i]}: \"{d}\"\n"
            continue
        if legend[i] == "statement": continue
        d = data[legend[i]].replace('"',"'")
        md += f"{legend[i]}: \"{d}\"\n"
    md += f'excerpt: "{process_excerpt(data["statement"])}"\n'
    md += "---\n"
    md += f"{data['statement']}\n"
    return md
    

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

# download file
filename = os.path.join(mypath, 'data.docx')
cmd = f'wget -O "{os.path.join(mypath,filename)}" ' + url
print(os.popen(cmd).read())

data = []
doc = Document(filename)
table = doc.tables[0]

# create dataframe
keys = None
for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)

    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    data.append(row_data)
    # print (data)

df = pd.DataFrame(data)

# iterate over rows
artists = []
for i, row in df.iterrows():
    if i==0: continue
    d = df.iloc[i,:].tolist()[1:]
    item = deepcopy(artist)

    for j in range(len(legend)):
        item[legend[j]] = d[j]
    artists.append(item)
    

os.makedirs(os.path.join(mypath, "artists"), exist_ok=True)

# write to markdown
# clean up the names, very muddy code here
for i in range(len(artists)):
    if artists[i]['status'] == "Out": continue
    md = to_markdown(artists[i])
    name = artists[i]['author']
    name = unidecode(name)
    if name[0] == " ": name = name[1:]
    name = name.replace(' ', '_').lower()
    name = name.replace(',', '') # only one exception
    filename = os.path.join(mypath,
                            "artists",
                            name)+".md"
    
    with open(filename, 'w') as f:
        f.write(md)
        f.close()


# move to the location
cmd = f"mv -v \"{os.path.join(mypath, 'artists')}\"/* \"{os.path.join(mypath, '..', '_texts')}\""
print(os.popen(cmd).read())