import streamlit as st
from annotated_text import annotated_text as st_annotated_text
import tiktoken as tk
from st_keyup import st_keyup

import random
get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]

if 'supported_encodings' not in st.session_state:
    st.session_state.supported_encodings = tk.list_encoding_names()

if 'supported_model' not in st.session_state:
    st.session_state.supported_models = list(tk.model.MODEL_TO_ENCODING.keys())

if 'selected_encoding' not in st.session_state:
    st.session_state.selected_encoding = ''

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = ''

if 'input_text' not in st.session_state:
    st.session_state.input_text = ''

if 'annotated_tkns' not in st.session_state:
    st.session_state.annotated_tkns = []

if 'annotated_idxs' not in st.session_state:
    st.session_state.annotated_idxs = []

if 'totalTkns' not in st.session_state:
    st.session_state.totalTkns = 0

if 'includeWS' not in st.session_state:
    st.session_state.includeWS = False

def isEncodingSelected():
    if st.session_state.selected_encoding != '':
        return True
    else:
        return False

def returnTkns(ids, encoding):
    t = {}
    for i in ids:
        t[i] = encoding.decode_single_token_bytes(i).decode('utf-8', errors='replace')
    return t

def returnWSasNeeded(t: str):
    #print(f'Entering WS with string {t}')
    if st.session_state.includeWS:
        t = t.replace(' ', '␣')
        t = t.replace('\n', '⏎')
        #print(f'Replaced string {t}')
    return t

def tknvisualize():
    # print('Entering tknVisualize')
    st.session_state.annotated_tkns = []
    st.session_state.annotated_idxs = []
    st.session_state.totalTkns = 0

    encoding = None
    if isEncodingSelected():
        encoding = tk.get_encoding(st.session_state.selected_encoding)
    else:
        encoding = tk.encoding_for_model(st.session_state.selected_model)
    
    idxs = encoding.encode(st.session_state.input_text)
    if len(idxs) >= 1:
        tkns = returnTkns(idxs, encoding)
        tknColors = get_colors(len(idxs))
        tknColorsMap = dict(zip(idxs, tknColors))
        
        for k,v in tkns.items():
            st.session_state.annotated_tkns.append((returnWSasNeeded(v), str(k), tknColorsMap[k]))
            st.session_state.annotated_idxs.append((str(k),'',tknColorsMap[k]))
        
        st.session_state.totalTkns = len(st.session_state.annotated_idxs)

with st.sidebar:
    st.markdown('## Settings ⚙️')
    choice = st.radio(label='Choose between Encoding scheme or a Language Model', options=('Encoding Scheme', 'Language Model'))
    match choice:
        case 'Encoding Scheme':
            st.session_state.selected_encoding = st.selectbox(label='Select Encoding Scheme', options=st.session_state.supported_encodings)
            st.session_state.selected_model = ''
        case 'Language Model':
            st.session_state.selected_model = st.selectbox(label='Select Encoding by Model', options=st.session_state.supported_models)
            st.session_state.selected_encoding = ''
    
    input_choice = st.radio(label='Choose between simple and advanced', options=('simple', 'advanced'))

    match input_choice:
        case 'simple':
            st.session_state.input_text = st_keyup('Enter your text to visualize tokens', max_chars=100)
        case 'advanced':
            advanced_text = st.text_area('Enter your text to visualize tokens', height=30)
            if st.button('submit'):
                st.session_state.input_text = advanced_text
    
    st.session_state.includeWS = st.toggle('Show ␣ and ⏎ ')

    if st.session_state.input_text != '':
        tknvisualize()

st.title(':rainbow[TikTokenViewer] 🫣')
st.subheader(':rainbow[Visualize] your tokens 🤩🤩🤩')

st.markdown('## Annotated Tokens')
st_annotated_text(st.session_state.annotated_tkns)

st.markdown('## Annotated embeddings')
st_annotated_text(st.session_state.annotated_idxs)

# st_card(title='Total Tokens', text=st.session_state.totalTkns, image='https://htmlcolorcodes.com/assets/images/html-color-codes-color-tutorials-hero.jpg', styles= {"card" : {
#     "font-size" : "10px"
# }, "text" : {
#     "font-size" : "50px"
# }})

st.markdown('#### Total Tokens')
st.markdown(f'# :rainbow[{st.session_state.totalTkns}]')
