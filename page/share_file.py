import os
import streamlit as st


def download(filename, filepath, datatype):
    st.download_button(label="下载", data=open(filepath, 'rb').read(),
                       file_name=filename, mime=datatype)


def delete(filename):
    if st.button("删除" + filename):
        filepath = os.path.join("uploads", filename)
        os.remove(filepath)
        st.success(f"已删除文件: {filepath}")


def container(filename, filepath, datatype):
    with st.container():
        st.subheader(filename)
        col1, col2 = st.columns(2)
        with col1:
            download(filename, filepath, datatype)
        with col2:
            delete(filename)
    st.divider()


def file_page():
    # 上传文件
    msg = "选择文件，允许上传多个文件，支持图片、文本、PDF、Word、PPT、Markdown、MP4、MP3、压缩包等格式"
    uploaded_files = st.file_uploader(msg, accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"已保存文件: {file_path}")
    st.divider()

    with st.container():
        # 显示文件列表并支持下载
        file_list = os.listdir("uploads")
        if len(file_list) > 0:
            st.write("文件列表:")
            for file_name in file_list:
                file_path = os.path.join("uploads", file_name)
                # 判断文件类型
                suffix = file_name.split(".")[-1]
                # 图片类型
                if suffix == "png" or suffix == "jpg" or suffix == "jpeg":
                    container(file_name, file_path, "image/png")

                # 文本类型
                elif suffix == "txt":
                    container(file_name, file_path, "text/plain")

                # PDF类型
                elif suffix == "pdf":
                    container(file_name, file_path, "application/pdf")

                # Word类型
                elif suffix == "doc" or suffix == "docx":
                    container(file_name, file_path,
                              "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                # PPT类型
                elif suffix == "ppt" or suffix == "pptx":
                    container(file_name, file_path,
                              "application/vnd.openxmlformats-officedocument.presentationml.presentation")

                # Markdown类型
                elif suffix == "md":
                    container(file_name, file_path, "text/markdown")

                # MP4类型
                elif suffix == "mp4":
                    container(file_name, file_path, "video/mp4")

                # MP3类型
                elif suffix == "mp3":
                    container(file_name, file_path, "audio/mp3")

                # zip类型
                elif suffix == "zip" or suffix == "rar" or suffix == "7z":
                    container(file_name, file_path, "application/zip")
