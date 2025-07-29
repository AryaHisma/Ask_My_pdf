# app_index.py

import streamlit as st
from engine.search import search_documents
import os
import fitz  # PyMuPDF

PDF_FOLDER = "data_pdf"

def run():
    st.title("🔍 Cari File PDF Berdasarkan Isi (Index JSON)")
    
    st.markdown("""
    Selamat datang di halaman pencarian dokumen!  
    Di sini, Anda dapat mencari file PDF berdasarkan **isi teksnya**, bukan hanya dari nama file.

    > **Note:**  
    Dokumen yang tersedia di halaman ini merupakan **data contoh** yang telah diunggah sebelumnya.  
    Anda bisa mencoba mencari berdasarkan topik atau kata kunci yang relevan untuk melihat hasilnya.
    
    Kata kunci contoh : kucing, laut, marah, obat, bosan
    """)

    query = st.text_input("Masukkan topik atau kata kunci:")

    if query:
        with st.spinner("Sedang mencari dokumen relevan..."):
            results = search_documents(query)

            if results:
                for i, res in enumerate(results):
                    filename = res.get("filename", f"dokumen_{i}.pdf")
                    snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

                    st.subheader(filename)
                    st.markdown(f"> {snippet}...")

                    file_path = os.path.join(PDF_FOLDER, filename)

                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=file_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                key=f"download_{i}"
                            )

                        with st.expander("📖 Lihat isi dokumen"):
                            try:
                                doc = fitz.open(file_path)
                                text = ""
                                for page in doc:
                                    text += page.get_text()
                                if text.strip():
                                    st.text_area("Isi Dokumen:", text, height=300)
                                else:
                                    st.info("PDF tidak memiliki teks yang bisa dibaca.")
                            except Exception as e:
                                st.error(f"Gagal membaca PDF: {e}")
                    else:
                        st.error("⚠️ File tidak ditemukan di direktori.")
                    st.markdown("---")
            else:
                st.warning("Tidak ditemukan dokumen yang relevan.")




# import streamlit as st
# from engine.search import search_documents
# import os
# import fitz  # PyMuPDF untuk membaca isi PDF

# PDF_FOLDER = "data_pdf"

# # st.set_page_config(page_title="Cari File PDF", page_icon="🔍")
# st.title("🔍 Cari File PDF Berdasarkan Isi (Index JSON)")

# query = st.text_input("Masukkan topik atau kata kunci:")

# if query:
#     with st.spinner("Sedang mencari dokumen relevan..."):
#         results = search_documents(query)

#         if results:
#             for i, res in enumerate(results):
#                 filename = res.get("filename", f"dokumen_{i}.pdf")
#                 snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                 st.subheader(filename)
#                 st.markdown(f"> {snippet}...")

#                 file_path = os.path.join(PDF_FOLDER, filename)

#                 if os.path.exists(file_path):
#                     with open(file_path, "rb") as f:
#                         file_bytes = f.read()
#                         st.download_button(
#                             label="⬇️ Download PDF",
#                             data=file_bytes,
#                             file_name=filename,
#                             mime="application/pdf",
#                             key=f"download_{i}"
#                         )

#                     # Tombol untuk menampilkan isi PDF
#                     with st.expander("📖 Lihat isi dokumen"):
#                         try:
#                             doc = fitz.open(file_path)
#                             text = ""
#                             for page in doc:
#                                 text += page.get_text()
#                             if text.strip():
#                                 st.text_area("Isi Dokumen:", text, height=300)
#                             else:
#                                 st.info("PDF tidak memiliki teks yang bisa dibaca.")
#                         except Exception as e:
#                             st.error(f"Gagal membaca PDF: {e}")
#                 else:
#                     st.error("⚠️ File tidak ditemukan di direktori.")

#                 st.markdown("---")
#         else:
#             st.warning("Tidak ditemukan dokumen yang relevan.")





# import streamlit as st
# from engine.search import search_documents
# import os

# # Konfigurasi dasar
# PDF_FOLDER = "data_pdf"

# st.set_page_config(page_title="Cari File PDF", page_icon="🔍")
# st.title("🔍 Cari File PDF Berdasarkan Isi (Index JSON)")

# query = st.text_input("Masukkan topik atau kata kunci:")

# if query:
#     with st.spinner("Sedang mencari dokumen relevan..."):
#         results = search_documents(query)

#         if results:
#             for res in results:
#                 filename = res.get("filename", "dokumen_tidak_bernama.pdf")
#                 snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                 st.subheader(filename)
#                 st.markdown(f"> {snippet}...")

#                 # Path lengkap ke file PDF
#                 file_path = os.path.join(PDF_FOLDER, filename)

#                 # Tampilkan tombol download jika file tersedia
#                 if os.path.exists(file_path):
#                     with open(file_path, "rb") as f:
#                         file_bytes = f.read()
#                         st.download_button(
#                             label="⬇️ Download PDF",
#                             data=file_bytes,
#                             file_name=filename,
#                             mime="application/pdf"
#                         )
#                 else:
#                     st.error("⚠️ File tidak ditemukan di direktori.")

#                 st.markdown("---")
#         else:
#             st.warning("Tidak ditemukan dokumen yang relevan.")





# import streamlit as st
# from engine.search import search_documents

# st.set_page_config(page_title="Cari File PDF", page_icon="🔍")
# st.title("🔍 Cari File PDF Berdasarkan Isi (Index JSON)")

# query = st.text_input("Masukkan topik atau kata kunci:")

# if query:
#     with st.spinner("Sedang mencari dokumen relevan..."):
#         results = search_documents(query)

#         if results:
#             for res in results:
#                 st.subheader(res.get("filename", "📄 (Tanpa Nama)"))
#                 st.markdown(f"> {res.get('snippet', '[Tidak ada cuplikan tersedia]')}...")
#                 st.markdown("---")
#         else:
#             st.warning("Tidak ditemukan dokumen yang relevan.")



# import streamlit as st
# from engine.search import search_documents

# st.title("🔍 Cari File PDF Berdasarkan Datanya (Pakai Index JSON)")

# query = st.text_input("Masukkan topik atau kata:")
# if query:
#     with st.spinner("Mencari..."):
#         results = search_documents(query)
#         if results:
#             for res in results:
#                 st.subheader(res["filename"])
#                 st.markdown("> " + res["snippet"] + "...")
#                 st.markdown("---")
#         else:
#             st.warning("Tidak ditemukan dokumen yang relevan.")

