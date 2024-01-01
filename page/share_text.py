import streamlit as st


def text_page():
    # 获取text.txt文件中的内容
    with open("text.txt", "r", encoding="utf-8") as f:
        text = f.read()
        f.close()
    # 显示文本内容
    txt = st.text_area("共享文本", text, height=300)
    st.write(f'You wrote {len(txt)} characters.')
    # 以UTF-8编码写入文件
    if st.button("保存"):
        with open("text.txt", "w", encoding="utf-8") as f:
            f.write(txt)
            f.close()
        st.success(f"已保存文本")
