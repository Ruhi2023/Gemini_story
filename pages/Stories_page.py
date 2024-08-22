import streamlit as st 
import os
import streamlit.components.v1 as cpm


@st.dialog("Share Story")
def share_story():
    if st.button("Download_cover"):
        with open("pages/Cover.png","rb") as img:
            st.download_button("Download",data =img,mime="image/png",file_name="Cover.png")
    if st.button("Download_story"):
        st.download_button("Download story",data =st.session_state["story"],mime="text/plain",file_name="story.txt")
    if st.button("Share"):
        c1,c2,c3,c5,c4 = st.columns(5)

        twitter=  """
        <a href="https://twitter.com">
        <img src="https://img.icons8.com/color/48/000000/twitter.png" />
        </a>    """
        if "story" in st.session_state:
                    the_message = st.session_state["story"][100]+"... checkout the link for more https://streamlit.io"
        else:
             the_message = "Check out this story generator https://streamlit.io"
        whatsapp = """
        <a href="https://api.whatsapp.com/send?text={}" data-action="share/whatsapp/share">
        <img src="https://img.icons8.com/color/48/000000/whatsapp.png" />
        </a>
        """.format( the_message )
        facebook = """
        <a href="https://www.facebook.com/" >
        <img src="https://img.icons8.com/color/48/000000/facebook-new.png" />
        </a>
        """
        instagram = """
        <a href="https://www.instagram.com/">
        <img src="https://img.icons8.com/color/48/000000/instagram-new.png" />
        </a>
        """
        pinterest = """
        <a href="http://pinterest.com/pin/create" >
        <img src="https://img.icons8.com/color/48/000000/pinterest.png" />
        </a>"""

        c1.html(twitter)
        c2.html(whatsapp)
        c3.html(facebook)
        c5.html(instagram)
        c4.html(pinterest)







col_not_img1,col_not_img2,col_not_img3 = st.columns([3,2,1])

if col_not_img3.button("""Download 
                       and 
                       Share"""):
    share_story()
col1,col2,col3 = st.columns(3)
if "story" in st.session_state:
    st.header("Response Stories")

    col2.image("pages/Cover.png")
    st.write(st.session_state["title"])

    stor = st.session_state["story"]
    chan =chr(92) +"n"
    stor = stor.replace(chan, "<br>")
    st.write(stor, unsafe_allow_html=True)
         
         
else:
    st.write("Go to generate stories")
    if st.button("Go home"):
        st.switch_page("app4.py")

