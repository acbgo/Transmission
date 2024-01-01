import streamlit as st
import os
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from page import *


def main_content():
    pages = {
        "文本共享": {
            "icon": "📝",
            "func": text_page,
        },
        "文件共享": {
            "icon": "📂",
            "func": file_page,
        },
    }
    with st.sidebar:
        st.title("导航栏")
        options = list(pages)
        icons = ['📝', '📂']
        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            default_index=default_index,
        )

    if selected_page in pages:
        pages[selected_page]["func"]()


if __name__ == '__main__':
    st.set_page_config(
        page_title="我的中转站",
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': f"""欢迎使用我的中转站1.0！"""
        }
    )

    # 创建一个文件夹用于保存上传的文件
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if not os.path.exists("text.txt"):
        with open("text.txt", "w") as f:
            f.write("")

    import streamlit as st

    st.markdown("<h1 style='text-align: center; color: black;'>😎欢迎使用我的中转站😎</h1>", unsafe_allow_html=True)
    st.divider()

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
    authenticator = stauth.Authenticate(credentials, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=10)
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        with st.container():
            cols1, cols2 = st.columns(2)
            cols1.write('欢迎 *%s*' % name)
            with cols2.container():
                authenticator.logout('Logout', 'main')
        main_content()
    elif not authentication_status:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')
