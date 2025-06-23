import streamlit as st
import ollama


model_list = ollama.list()


if "model_name" not in st.session_state:
    st.session_state["model_name"] = "llama3.2:latest"

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Settings")
    # 获取模型名称列表
    model_names = [model.model for model in model_list.models]
    # 防止初始模型名不在本地模型列表时报错
    default_index = model_names.index(st.session_state["model_name"]) if st.session_state["model_name"] in model_names else 0
    option = st.selectbox("Select a Model", model_names, index=default_index)
    st.write("You selected:", option)
    st.session_state["model_name"] = option

st.title(f"Chat with {st.session_state['model_name']}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response =""
        for chunk in ollama.chat(
        model=st.session_state["model_name"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
            if 'message' in chunk and 'content' in chunk['message']:
                full_response += (chunk['message']['content'] or "")
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})