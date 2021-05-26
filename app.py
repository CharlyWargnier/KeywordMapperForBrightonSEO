import streamlit as st
from polyfuzz import PolyFuzz
import seaborn as sns
import base64
import pandas as pd
import csv

# import matplotlib as plt

st.set_page_config(
    page_title="Keyword Mapper for BrightonSEO", page_icon="✨", layout="wide"
)

c30, c31, c32 = st.beta_columns(3)

with c30:
    st.image("logo.png", width=500)

with c32:
    st.header("")
    st.header("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.markdown(
        "###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://twitter.com/DataChaz) &nbsp [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)"
    )

st.write("")

st.markdown("## **① Upload crawl 🐸**")

c11 = st.beta_container()

c29, c30, c31 = st.beta_columns([1, 6, 1])

with c30:

    c10 = st.beta_container()

########################

st.markdown("## **②  Paste keywords/internal search terms ✨**")

linesDeduped2 = []
MAX_LINES = 200
text = st.text_area("One keyword per line (200 max)", height=200, key=1)
lines = text.split("\n")  # A list of lines
linesList = []
for x in lines:
    linesList.append(x)
linesList = list(dict.fromkeys(linesList))  # Remove dupes
linesList = list(filter(None, linesList))  # Remove empty

if len(linesList) > MAX_LINES:
    st.warning(
        f"⚠️ Only the 200 first keywords will be reviewed. Increased allowance  is coming - Stay tuned! 😊)"
    )
    linesList = linesList[:MAX_LINES]

########################

c = st.beta_container()
c30 = st.beta_container()
c29, c30, c31 = st.beta_columns(3)

with c29:
    start_execution = st.button(" Run model! ✨ ")
    c50 = st.beta_container()

c29, c30, c31 = st.beta_columns([1, 6, 1])

with c30:

    uploaded_file = c10.file_uploader("", key=1)

    if uploaded_file is not None:
        file_container = c10.beta_expander("Check your uploaded CSV")
        GSCDf = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        file_container.write(GSCDf)

    elif start_execution and (uploaded_file is None):
        c30.warning(
            f"""
                👹 **Oh! What the Fuzz!**
                """
        )
        st.stop()

    else:
        st.stop()

GSCDf = GSCDf.fillna(value="")

SFMinimumHeaders = ["Address", "Indexability Status", "Title 1"]
HeadersOK = all(i in GSCDf for i in SFMinimumHeaders)

if not uploaded_file:
    pass
elif (HeadersOK == True) and (uploaded_file):
    pass
else:
    c50.warning(
        f"""
                👹 **Oh! What the Fuzz!** It seems that the crawl you uploaded was not the one I was looking for!                
                Currently, I only accept Screaming Frog's internal_all.csv file, yet  planning to add more crawlers in the future - namely OnCrawl, DeepCrawl and SiteBulb!                
                Check-out here [where to find it](https://i.imgur.com/HavO4d6.png)                
                """
    )

    st.stop()

dfIndexable = GSCDf.loc[GSCDf["Indexability"] == "Indexable"]
col_one_list = GSCDf["Address"].tolist()


model = PolyFuzz("EditDistance")
SCHEMES = ("http://", "https://")

if start_execution and (uploaded_file is None):
    st.wc50.warning("file 1st!")
    st.stop()

else:

    model.match(linesList, col_one_list)
    Polyfuzz = model.get_matches()  # Auto map by Similarity scores
    Polyfuzz.columns = ["URL to map", "URL match", "Similarity"]
    Polyfuzz.index = Polyfuzz.index + 1

    #cmapRed = sns.diverging_palette(10, 133, as_cmap=True)
    #cmapRedBlue = sns.color_palette("vlag", as_cmap=True)
    cmGreen = sns.light_palette("green", as_cmap=True)
    FuzzStyled = Polyfuzz.style.background_gradient(cmap=cmGreen)

    format_dictionary = {
        "Similarity": "{:.1%}",
    }

    FuzzStyled = FuzzStyled.format(format_dictionary)

    c2 = st.beta_container()
    c29, c30, c31 = st.beta_columns([1, 6, 1])

    with c30:
        c = st.beta_container()
        st.table(FuzzStyled)

    csv = Polyfuzz.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    c2.markdown("## **③ Check mapping 📌**")
    with c2.beta_expander("ℹ️ - Tips for better mapping", expanded=False):

        st.write(
            """   
    -   Early beta, still quite some stuff to improve! :)
    -   Use short terms/phrases
    -   (remove that sentence? the longer the less accurate
    -   Do not include branded terms, esp if mapping to URLs
    -   1A - Avoid geo locations terms in the phrase, as it'll bias the mapping.
    -   1B - "FAQs" may be mapped to the FAQ URLs, Whereas the term  FAQ-UK may be directed to an incorrect, Irrelevant URL! 
    -   More NLP processing planned so these biases are catered for automattically in the future

            """
        )

    st.write("")

    c2.subheader("")
    href = f'<a href="data:file/csv;base64,{b64}" download="Mapping_to_URL.csv">** ⯈ Download link 🎁 **</a>'
    c.markdown(href, unsafe_allow_html=True)
