# main.py
import streamlit as st

# HARUS di sini, sebelum semua komponen UI
st.set_page_config(page_title="AskMyPDF", layout="wide", page_icon="📚")


from streamlit_option_menu import option_menu
import app_index
import user_upload



# Navigasi menu
selected = option_menu(
    menu_title=None,
    options=["Cari Dokumen", "Upload PDF Sendiri"],
    icons=["search", "upload"],
    orientation="horizontal",
)

if selected == "Cari Dokumen":
    app_index.run()
elif selected == "Upload PDF Sendiri":
    user_upload.run()




# import streamlit as st
# from streamlit_option_menu import option_menu
# import app_index
# import user_upload

# st.set_page_config(page_title="AskMyPDF", layout="wide", page_icon="📚")

# with st.sidebar:
#     selected = option_menu(
#         "Navigasi",
#         ["🔍 Cari dari Index", "📤 Tes PDF Sendiri"],
#         icons=["search", "upload"],
#         default_index=0
#     )

# if selected == "🔍 Cari dari Index":
#     app_index.run()

# elif selected == "📤 Tes PDF Sendiri":
#     user_upload.run()
