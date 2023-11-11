"""
    @Time    : 2023/11/11 15:25
    @Author  : Chen
    @Description : 主函数
 """
import os
import streamlit as st
import streamlit_authenticator as stauth


def download(file_name, file_path, datatype):
    st.download_button(label="下载", data=open(file_path, 'rb').read(),
                       file_name=file_name, mime=datatype)


def delete(file_name, file_path):
    if st.button("删除" + file_name):
        file_path = os.path.join("uploads", file_name)
        os.remove(file_path)
        st.success(f"已删除文件: {file_path}")


def container(file_name, file_path, datatype):
    with st.container():
        st.subheader(file_name)
        col1, col2 = st.columns(2)
        with col1:
            download(file_name, file_path, datatype)
        with col2:
            delete(file_name, file_path)
    st.divider()


def mainContent():
    # 创建一个文件夹用于保存上传的文件
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # 页面标题和说明文字
    st.header("校园网环境下的文件中转站")
    st.divider()
    msg = "选择文件，允许上传多个文件，支持图片、文本、PDF、Word、PPT、Markdown、MP4、MP3、压缩包等格式"
    uploaded_files = st.file_uploader(msg, accept_multiple_files=True)

    # 保存文件
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"已保存文件: {file_path}")

    st.divider()

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


if __name__ == '__main__':
    # 用户信息
    names = ["管理员"]  # 用户名
    usernames = ['csb']  # 登录名
    passwords = [' bing']  # 登录密码
    # 对密码进行加密操作，后续将这个存放在credentials中
    hashed_passwords = stauth.Hasher(passwords).generate()

    # 定义字典，初始化字典
    credentials = {'usernames': {}}
    # 生成服务器端的用户身份凭证信息
    for i in range(0, len(names)):
        credentials['usernames'][usernames[i]] = {'name': names[i], 'password': hashed_passwords[i]}
    authenticator = stauth.Authenticate(credentials, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=1)
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        with st.container():
            cols1, cols2 = st.columns(2)
            cols1.write('欢迎 *%s*' % (name))
            with cols2.container():
                authenticator.logout('Logout', 'main')

        mainContent()
    elif not authentication_status:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')






