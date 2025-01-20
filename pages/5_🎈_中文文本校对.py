import streamlit as st
import jieba
import mammoth
import save
import time
import jieba.posseg as pseg
from LAC import LAC

st.set_page_config(page_title="中文文本校对", page_icon="🎈", layout="wide")


def remove_duplicates(lst):
    return list(dict.fromkeys(lst))


def processing():
    st.sidebar.header("中文人名识别进度")
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    for i in range(1, 101):
        status_text.text("人名标注进度%i%%" % i)
        progress_bar.progress(i)
        time.sleep(0.01)
    # progress_bar.empty()


def show_detail(detail_text, list):
    # 使用Markdown语法设置字体颜色
    for i in range(len(list)):
        colored_text = f"<span style='color:red'>{list[i]}</span>"
        detail_text = detail_text.replace(list[i], colored_text)
    st.markdown(detail_text, unsafe_allow_html=True)
    return detail_text

def stream_text(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)  # 使用 flush=True 立即输出每个字符
        time.sleep(delay)  # 每个字符之间的延迟


st.title("中文文本校对")
st.markdown("""**请上传需处理的DOCX或者TXT文件：**""")
uploaded = st.file_uploader("请上传需处理的DOCX或者TXT文件", type=['docx', 'txt'], label_visibility="collapsed")
if uploaded is not None:
    if uploaded.name.split('.')[-1] == 'docx':
        text = mammoth.convert_to_markdown(uploaded).value
    elif uploaded.name.split('.')[-1] == 'txt':
        text = uploaded.read().decode("utf-8")
    docx_file = uploaded.name

    show_detail = text
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("原文：")
        st.text_area(label='原文', value=show_detail, height=300, label_visibility="collapsed")
    with col2:
        st.header("校对后文章：")
        st.text_area(label='校对后文章', value=show_detail, height=300, label_visibility="collapsed")
# Main interface
st.title("有什么可以帮忙的？")
user_input = st.text_input("给ChatGPT发送消息")
for chunk in user_input:
    st.header("你输入的内容：")
    st.text_area(label='你输入的内容:', value=user_input, height=300, label_visibility="collapsed")
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")