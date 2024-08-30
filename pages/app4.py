import PIL.Image
#from fastapi import FastAPI 
from back_end import gen_text as mg
import time
import requests
import os
import json
import PIL
import streamlit as st
st.title("Content generator")
st.header("Inputs for the story")
genres = [
"Science Fiction",
"Fantasy",
"Mystery",
"Thriller",
"Romance",
"Horror",
"Young Adult (YA)",
"Historical Fiction",
"Western",
"Crime Fiction",
"Comedy",
"Drama",
"Adventure",
"Dystopian",
"Utopian",
"Biography",
"History",
"Science",
"Technology",
"Business",
"Self-Help",
"Philosophy",
"Religion",
"Politics",
"Art",
"Music",
"Literature",
"Education",
"Health",
"Travel",
"Cooking",
"Gardening",
"Sports",
"Space Opera",
"Cyberpunk",
"Dystopian",
"Alternate History",
"Time Travel",
"High Fantasy",
"Low Fantasy",
"Urban Fantasy",
"Dark Fantasy",
"Historical Fantasy",
"Detective Fiction",
"Mystery Thriller",
"Cozy Mystery",
"Psychological Thriller",
"Suspense Thriller",
"Legal Thriller",
"Medical Thriller",
"Contemporary Romance",
"Historical Romance",
"Paranormal Romance",
"Science Fiction Romance",
"Gothic Horror",
"Supernatural Horror",
"Psychological Horror",
"Cosmic Horror",
"Contemporary YA",
"Fantasy YA",
"Science Fiction YA",
]


with st.form("Inputs or login"):
    ugak = os.environ['GOOGLE_NO_KAGI']
    uhfak = os.environ['HUGGINGKAO_NO_KAGI']
    st.write("Enter the type of story you want \nDisclamer No romance before age 22, writing style is only poetic")
    st.write("Enter age of reader")
    Age = st.text_input(label="Age",type="default")
    st.write("Enter prefered reading style of reader")
    rs = st.text_input(label="Reading style",type="default")
    st.write("Enter prefered genre of reader")
    g = st.selectbox(label="genre",options=genres)
    st.write("Enter length of story")
    l = st.slider(label="length of story",min_value=50,max_value=2000)
    st.write("Anything else you want to specify (leave blank if not)")
    extra = st.text_input(label="extra",type="default")
    prompt = 'Write a {} story. Target audience Age: {}. Style: {}. Length: {} words exactly. Suggest very short cover image description. Output in single JSON fromat containing fields: title as "tx", story as "stx"and image description as "ctx". {}'.format(g,Age,rs,l, extra)
    get_story = st.form_submit_button("Generate my story and cover")

if get_story:
    d = {"ugak":ugak,"uhfak": uhfak,"prompt": prompt,"Age":Age,"rs":rs,"g":g,"l":l}
    st.write("Your prompt " ,prompt)
                       
    st.header("Response section")
    
    prog_bar = st.progress(2)
     
    # ... (parse response and update app
    output_dict = mg(d=d)
    #st.write(output_dict)                   # uncomment if you want to print the output dictionary
    try:
        acc = output_dict['keys']
    except:
        try:
            acc = output_dict["keys"]
        except:
            acc = list(output_dict.keys())
    cha =chr(92)
    cha2 = cha + cha
    cha3 = " " + cha
    chan = cha + "n"
    chan2 = chan+chan
    if "Cover Image" in output_dict[acc[0]]:
        if "Title" in output_dict[acc[0]]:
            my_title = str(output_dict[acc[0]]).split("\\n")
            st.write("Your story title is: ")
            st.session_state.title = my_title
            st.write(my_title[0])
        else:    
            st.write( output_dict[acc[1]])
            st.session_state.title = output_dict[acc[1]]
    else:
        txst = output_dict[acc[0]].replace('"','')
        st.session_state.title=txst
        st.write("Your story title is: ")
        st.write(txst )
    content = output_dict[acc[1]].replace(cha2,cha3)
    content = content.replace(chan2,chan)
    st.session_state.story = content
    prog_bar.progress(20)
    #st.write(st.session_state.story)
    from huggingface_hub import login
    login(token=d['uhfak'],add_to_git_credential=True)
    for i in acc:
        if "ctx" in i:
            cov_pr = output_dict[i] + ", no text"
        else:
            if output_dict[acc[1]]=='' or output_dict[acc[1]] == None or "Cover" in output_dict[acc[0]] :
                cov_pr = output_dict[acc[0]] + ", no text"
            else:
                cov_pr = output_dict[acc[1]] + ", no text"
        headers = {"Authorization": f"Bearer {d['uhfak']}"}
    api_list = [ "https://api-inference.huggingface.co/models/prompthero/openjourney",
                "https://api-inference.huggingface.co/models/alvdansen/phantasma-anime",
                "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium-diffusers",
                "https://api-inference.huggingface.co/models/mann-e/Mann-E_Dreams",
                "https://api-inference.huggingface.co/models/fluently/Fluently-XL-Final",
                "https://api-inference.huggingface.co/models/alvdansen/midsommarcartoon",
                "https://api-inference.huggingface.co/models/stabilityai/stable-cascade",
                "https://api-inference.huggingface.co/models/playgroundai/playground-v2.5-1024px-aesthetic",
                "https://api-inference.huggingface.co/models/stablediffusionapi/mklan-xxx-nsfw-pony",
                "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
                "https://api-inference.huggingface.co/models/nerijs/pixel-art-xl",
                ]
    def query(payload, url):
        response = requests.post(url, headers=headers, json=payload)
        return response.content
    image_bytes = bytes()
    # You can access the image with PIL.Image for example
    import io
    from PIL import Image
    err = 1
    while err>0:
        for i in api_list:
            if err==0:
                break
            try:
                print("Trying to generate cover....")
                image_bytes = query(url= i,payload = {"inputs": cov_pr, })
                image = Image.open(io.BytesIO(image_bytes))
            except:
                err +=1
                print("error", image_bytes,)
            else:
                print("Success,", err)
                err = 0
    
    image.save("pages/Cover.png")
    prog_bar.progress(100)
    st.write("Your cover image and story has been generated. You will be redirected automatically or use the button below.")
    
    if "story" in st.session_state:
        if st.button(":material/local_library: Read story"):
            st.switch_page("pages/Stories_page.py" )
    time.sleep(2)
    st.switch_page("pages/Stories_page.py")
