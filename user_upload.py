import streamlit as st
import os
import fitz  # PyMuPDF
from engine.index_document import index_document, remove_document_from_index

UPLOAD_FOLDER = "uploaded"
INDEX_PATH = "index/index_document.json"

# 🧱 Pastikan folder ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def run():
    st.title("📤 Upload PDF & Cari Isi Dokumen Anda")

    col1, col2 = st.columns(2)

    # ==========📁 LAYOUT 1: UPLOAD DAN KELOLA FILE ==========
    with col1:
        st.header("⬆️ Upload & Hapus Dokumen")

        uploaded_file = st.file_uploader("Upload file PDF Anda", type=["pdf"])
        if uploaded_file:
            save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File disimpan: {uploaded_file.name}")

            # Tambahkan ke index
            index_document(save_path, uploaded_file.name)
            st.info(f"📚 Index berhasil diperbarui.")

        # Tampilkan file yang sudah diupload
        st.markdown("### 📂 File yang sudah diupload")
        files = os.listdir(UPLOAD_FOLDER)
        if not files:
            st.info("Belum ada file diunggah.")
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            with st.expander(f"📄 {file}", expanded=False):
                # Tombol download
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    st.download_button(
                        label="⬇️ Download",
                        data=file_bytes,
                        file_name=file,
                        mime="application/pdf",
                        key=f"download_{file}"
                    )

                # Tombol lihat isi dokumen
                try:
                    with fitz.open(file_path) as doc:
                        text = ""
                        for page in doc:
                            text += page.get_text()
                    if text.strip():
                        st.text_area("📖 Isi Dokumen:", text, height=300)
                    else:
                        st.warning("⚠️ PDF ini tidak memiliki teks yang bisa dibaca.")
                except Exception as e:
                    st.error(f"Gagal membuka file: {e}")

                # Tombol hapus
                if st.button(f"🗑️ Hapus {file}", key=f"hapus_{file}"):
                    os.remove(file_path)
                    remove_document_from_index(file)
                    st.success(f"{file} berhasil dihapus.")
                    st.rerun()

    # ==========🔍 LAYOUT 2: PENCARIAN ==========
    with col2:
        st.header("🔍 Cari Dokumen")
        query = st.text_input("Masukkan topik atau kata kunci:")
        if query:
            from engine.search_document import search_documents
            results = search_documents(query, index_path=INDEX_PATH)

            if results:
                st.markdown(f"**Hasil untuk: _{query}_**")
                for i, res in enumerate(results):
                    filename = res.get("filename", f"dokumen_{i}.pdf")
                    snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")
                    file_path = os.path.join(UPLOAD_FOLDER, filename)

                    st.subheader(filename)
                    st.markdown(f"> {snippet}...")

                    # Tombol download
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=file_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                key=f"download_search_{i}"
                            )

                        # Tombol lihat isi dokumen
                        with st.expander("📖 Lihat isi dokumen"):
                            try:
                                with fitz.open(file_path) as doc:
                                    text = ""
                                    for page in doc:
                                        text += page.get_text()
                                if text.strip():
                                    st.text_area("Isi Dokumen:", text, height=300)
                                else:
                                    st.info("PDF tidak memiliki teks yang bisa dibaca.")
                            except Exception as e:
                                st.error(f"Gagal membuka file: {e}")
                    else:
                        st.error("⚠️ File PDF tidak ditemukan.")

                    st.markdown("---")
            else:
                st.warning("Tidak ditemukan dokumen yang relevan.")




# import streamlit as st
# import os
# import fitz
# from engine.search_document import search_documents
# from engine.index_document import index_document, remove_document_from_index


# PDF_FOLDER = "uploaded"

# # Trik untuk "refresh" halaman manual
# if "refresh" in st.session_state:
#     del st.session_state["refresh"]
#     st.query_params.set(dummy=os.urandom(4).hex())  # Ubah query param acak → rerun



# def run():
#     st.title("📤 Upload dan Cari Isi Dokumen PDF Anda")

#     # Layout dibagi dua kolom
#     col1, col2 = st.columns([1, 2])

#     with col1:
#         st.subheader("📁 Upload & Hapus File")
#         uploaded_files = st.file_uploader("Upload beberapa file PDF", type=["pdf"], accept_multiple_files=True)

#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 save_path = os.path.join(PDF_FOLDER, uploaded_file.name)
#                 with open(save_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.success(f"✅ Disimpan: {uploaded_file.name}")
                
#                 # 🔍 Tambahkan file ke index setelah upload
#                 index_document(save_path, uploaded_file.name)
                
#                 # Membaca teks PDF menggunakan PyMuPDF (fitz)
#                 try:
#                     with fitz.open(save_path) as doc:
#                         full_text = ""
#                         for page in doc:
#                             full_text += page.get_text()

#                         # Menambahkan ke index JSON
#                         # Langsung tambahkan ke index
#                         index_document(save_path, uploaded_file.name)
#                         st.info(f"✅ File {uploaded_file.name} berhasil ditambahkan ke index.")

#                 except Exception as e:
#                     st.error(f"❌ Gagal mengindeks {uploaded_file.name}: {e}")

#         st.markdown("### 🗑️ File yang sudah diupload")
        
#         st.markdown(">**Note:** Untuk menghapus file, refresh terlebih dahulu halaman web kemudian hapus data")

#         if os.path.exists(PDF_FOLDER):
#             files = os.listdir(PDF_FOLDER)
#             for file in files:
#                 file_path = os.path.join(PDF_FOLDER, file)
#                 st.markdown(f"- {file}")
#                 if st.button(f"🗑️ Hapus {file}", key=f"hapus_{file}"):
#                     os.remove(file_path)
#                     # 🔍 Hapus dari index juga
#                     remove_document_from_index(file)
#                     st.success(f"{file} berhasil dihapus.")
#                     st.rerun()  # Gunakan ini jika versi Streamlit mendukung
    
#     with col2:
#         st.subheader("🔍 Cari Dokumen")
#         query = st.text_input("Masukkan topik atau kata kunci:")
#         if query:
#             with st.spinner("Mencari dokumen relevan..."):
#                 results = search_documents(query)
#                 if results:
#                     for i, res in enumerate(results):
#                         filename = res.get("filename", f"dokumen_{i}.pdf")
#                         snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")
#                         st.markdown(f"**{filename}**")
#                         st.markdown(f"> {snippet}...")
#                 else:
#                     st.warning("Tidak ditemukan dokumen yang relevan.")





# import streamlit as st
# import os
# import fitz  # PyMuPDF
# from engine.search import search_documents

# UPLOAD_FOLDER = "uploaded"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def run():
#     st.title("📤 Upload PDF Sendiri dan Cari Isi Dokumen")

#     uploaded_files = st.file_uploader("Upload satu atau lebih file PDF", type=["pdf"], accept_multiple_files=True)
#     if uploaded_files:
#         for file in uploaded_files:
#             save_path = os.path.join(UPLOAD_FOLDER, file.name)
#             with open(save_path, "wb") as f:
#                 f.write(file.getbuffer())
#         st.success(f"{len(uploaded_files)} file berhasil diunggah.")

#     st.markdown("---")

#     # Tampilkan daftar file yang sudah di-upload
#     st.subheader("🗂️ File PDF yang Sudah Diupload")
#     files = os.listdir(UPLOAD_FOLDER)
#     if files:
#         for file in files:
#             file_path = os.path.join(UPLOAD_FOLDER, file)
#             with st.expander(f"📄 {file}"):
#                 col1, col2 = st.columns([4, 1])
#                 with col1:
#                     st.write(f"Path: `{file_path}`")
#                 with col2:
#                     if st.button("🗑️ Hapus", key=f"hapus_{file}"):
#                         os.remove(file_path)
#                         st.experimental_rerun()
#     else:
#         st.info("Belum ada file yang diupload.")

#     st.markdown("---")

#     query = st.text_input("Masukkan topik atau kata kunci:")
#     if query:
#         with st.spinner("Mencari dokumen relevan..."):
#             results = search_documents(query, folder=UPLOAD_FOLDER)

#             if results:
#                 for i, res in enumerate(results):
#                     filename = res.get("filename", f"dokumen_{i}.pdf")
#                     snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                     st.subheader(filename)
#                     st.markdown(f"> {snippet}...")

#                     file_path = os.path.join(UPLOAD_FOLDER, filename)

#                     if os.path.exists(file_path):
#                         with open(file_path, "rb") as f:
#                             file_bytes = f.read()
#                             st.download_button(
#                                 label="⬇️ Download PDF",
#                                 data=file_bytes,
#                                 file_name=filename,
#                                 mime="application/pdf",
#                                 key=f"download_{i}"
#                             )

#                         with st.expander("📖 Lihat isi dokumen"):
#                             try:
#                                 doc = fitz.open(file_path)
#                                 text = ""
#                                 for page in doc:
#                                     text += page.get_text()
#                                 if text.strip():
#                                     st.text_area("Isi Dokumen:", text, height=300)
#                                 else:
#                                     st.info("PDF tidak memiliki teks yang bisa dibaca.")
#                             except Exception as e:
#                                 st.error(f"Gagal membaca PDF: {e}")
#                     else:
#                         st.error("⚠️ File tidak ditemukan.")
#                     st.markdown("---")
#             else:
#                 st.warning("Tidak ditemukan dokumen yang relevan.")




# import streamlit as st
# import os
# import fitz  # PyMuPDF
# from engine.search import search_documents

# PDF_FOLDER = "data_pdf"

# def run():
#     st.title("📤 Upload dan Kelola File PDF")

#     # --- Upload Multiple PDF ---
#     uploaded_files = st.file_uploader("Unggah satu atau beberapa file PDF", type=["pdf"], accept_multiple_files=True)

#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             save_path = os.path.join(PDF_FOLDER, uploaded_file.name)
#             with open(save_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.success(f"✅ File berhasil disimpan: {uploaded_file.name}")

#     st.markdown("---")

#     # --- Daftar dan Hapus File ---
#     st.subheader("🗂️ File yang Telah Diupload")
#     existing_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

#     if existing_files:
#         for filename in existing_files:
#             file_path = os.path.join(PDF_FOLDER, filename)
#             col1, col2 = st.columns([6, 1])
#             col1.markdown(f"📄 **{filename}**")
#             if col2.button("🗑️ Hapus", key=f"hapus_{filename}"):
#                 os.remove(file_path)
#                 st.success(f"File {filename} berhasil dihapus.")
#                 st.experimental_rerun()
#     else:
#         st.info("Belum ada file yang diupload.")

#     st.markdown("---")

#     # --- Pencarian PDF ---
#     st.subheader("🔍 Cari Isi Dokumen PDF")
#     query = st.text_input("Masukkan topik atau kata kunci:")
#     if query:
#         with st.spinner("Sedang mencari dokumen relevan..."):
#             results = search_documents(query)

#             if results:
#                 for i, res in enumerate(results):
#                     filename = res.get("filename", f"dokumen_{i}.pdf")
#                     snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                     st.subheader(f"📄 {filename}")
#                     st.markdown(f"> {snippet}...")

#                     file_path = os.path.join(PDF_FOLDER, filename)

#                     if os.path.exists(file_path):
#                         with open(file_path, "rb") as f:
#                             file_bytes = f.read()
#                             st.download_button(
#                                 label="⬇️ Download PDF",
#                                 data=file_bytes,
#                                 file_name=filename,
#                                 mime="application/pdf",
#                                 key=f"download_{i}"
#                             )

#                         with st.expander("📖 Lihat isi dokumen"):
#                             try:
#                                 doc = fitz.open(file_path)
#                                 text = ""
#                                 for page in doc:
#                                     text += page.get_text()
#                                 if text.strip():
#                                     st.text_area("Isi Dokumen:", text, height=300)
#                                 else:
#                                     st.info("PDF tidak memiliki teks yang bisa dibaca.")
#                             except Exception as e:
#                                 st.error(f"Gagal membaca PDF: {e}")
#                     else:
#                         st.error("⚠️ File tidak ditemukan.")
#                     st.markdown("---")
#             else:
#                 st.warning("Tidak ditemukan dokumen yang relevan.")



# import streamlit as st
# import os
# import fitz  # PyMuPDF
# from engine.search import search_documents

# PDF_FOLDER = "data_pdf"

# def run():
#     st.title("📤 Upload Beberapa PDF dan Cari Berdasarkan Isi")

#     uploaded_files = st.file_uploader("Unggah satu atau beberapa file PDF", type=["pdf"], accept_multiple_files=True)

#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             save_path = os.path.join(PDF_FOLDER, uploaded_file.name)
#             with open(save_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.success(f"✅ File berhasil disimpan: {uploaded_file.name}")

#     st.markdown("---")

#     query = st.text_input("🔍 Masukkan topik atau kata kunci untuk pencarian:")
#     if query:
#         with st.spinner("Sedang mencari dokumen relevan..."):
#             results = search_documents(query)

#             if results:
#                 for i, res in enumerate(results):
#                     filename = res.get("filename", f"dokumen_{i}.pdf")
#                     snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                     st.subheader(f"📄 {filename}")
#                     st.markdown(f"> {snippet}...")

#                     file_path = os.path.join(PDF_FOLDER, filename)

#                     if os.path.exists(file_path):
#                         with open(file_path, "rb") as f:
#                             file_bytes = f.read()
#                             st.download_button(
#                                 label="⬇️ Download PDF",
#                                 data=file_bytes,
#                                 file_name=filename,
#                                 mime="application/pdf",
#                                 key=f"download_{i}"
#                             )

#                         with st.expander("📖 Lihat isi dokumen"):
#                             try:
#                                 doc = fitz.open(file_path)
#                                 text = ""
#                                 for page in doc:
#                                     text += page.get_text()
#                                 if text.strip():
#                                     st.text_area("Isi Dokumen:", text, height=300)
#                                 else:
#                                     st.info("PDF tidak memiliki teks yang bisa dibaca.")
#                             except Exception as e:
#                                 st.error(f"Gagal membaca PDF: {e}")
#                     else:
#                         st.error("⚠️ File tidak ditemukan.")
#                     st.markdown("---")
#             else:
#                 st.warning("Tidak ditemukan dokumen yang relevan.")



# import streamlit as st
# import os
# import fitz  # PyMuPDF
# from engine.search import search_documents

# PDF_FOLDER = "data_pdf"

# def run():
#     st.title("📤 Upload PDF Sendiri dan Cari Isi Dokumen")

#     uploaded_file = st.file_uploader("Upload file PDF Anda", type=["pdf"])
#     if uploaded_file:
#         save_path = os.path.join(PDF_FOLDER, uploaded_file.name)
#         with open(save_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success(f"File berhasil disimpan: {uploaded_file.name}")

#     st.markdown("---")

#     query = st.text_input("Masukkan topik atau kata kunci:")
#     if query:
#         with st.spinner("Mencari dokumen relevan..."):
#             results = search_documents(query)

#             if results:
#                 for i, res in enumerate(results):
#                     filename = res.get("filename", f"dokumen_{i}.pdf")
#                     snippet = res.get("snippet", "[Tidak ada cuplikan tersedia]")

#                     st.subheader(filename)
#                     st.markdown(f"> {snippet}...")

#                     file_path = os.path.join(PDF_FOLDER, filename)

#                     if os.path.exists(file_path):
#                         with open(file_path, "rb") as f:
#                             file_bytes = f.read()
#                             st.download_button(
#                                 label="⬇️ Download PDF",
#                                 data=file_bytes,
#                                 file_name=filename,
#                                 mime="application/pdf",
#                                 key=f"download_{i}"
#                             )

#                         with st.expander("📖 Lihat isi dokumen"):
#                             try:
#                                 doc = fitz.open(file_path)
#                                 text = ""
#                                 for page in doc:
#                                     text += page.get_text()
#                                 if text.strip():
#                                     st.text_area("Isi Dokumen:", text, height=300)
#                                 else:
#                                     st.info("PDF tidak memiliki teks yang bisa dibaca.")
#                             except Exception as e:
#                                 st.error(f"Gagal membaca PDF: {e}")
#                     else:
#                         st.error("⚠️ File tidak ditemukan.")
#                     st.markdown("---")
#             else:
#                 st.warning("Tidak ditemukan dokumen yang relevan.")




# import streamlit as st
# import os
# import fitz  # PyMuPDF

# UPLOAD_FOLDER = "uploaded"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # st.set_page_config(page_title="Upload PDF Sendiri", page_icon="📤")
# st.title("📤 Tes Cari Isi dari PDF Sendiri")

# uploaded_file = st.file_uploader("Unggah file PDF Anda:", type=["pdf"])

# if uploaded_file:
#     file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
#     # Simpan file ke folder
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.read())

#     st.success(f"File '{uploaded_file.name}' berhasil diunggah.")

#     # Ambil query dari user
#     query = st.text_input("Masukkan kata kunci pencarian:")

#     if query:
#         with st.spinner("Mencari..."):
#             try:
#                 doc = fitz.open(file_path)
#                 content = ""
#                 for page in doc:
#                     content += page.get_text()
#                 doc.close()

#                 # Cari semua keyword dalam teks
#                 keywords = query.lower().split()
#                 if all(k in content.lower() for k in keywords):
#                     st.success("✅ Ditemukan!")
#                     st.text_area("Cuplikan Isi Dokumen:", content[:1000], height=300)
#                 else:
#                     st.warning("Tidak ditemukan kata kunci dalam dokumen.")

#             except Exception as e:
#                 st.error(f"Gagal membaca isi PDF: {e}")
