import streamlit as st
import asyncio
from agent import get_agent_response

st.set_page_config(page_title="Zara Customer Support Agent", page_icon="https://logomakerr.ai/blog/wp-content/uploads/2022/08/2019-to-Present-Zara-logo-design.jpg", layout="wide")

st.image("https://logomakerr.ai/blog/wp-content/uploads/2022/08/2019-to-Present-Zara-logo-design.jpg", width=200)
st.markdown("Ask me about products, shipping, returns, or any other questions!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Use threading to avoid event loop conflicts
                import threading
                import concurrent.futures
                
                def run_in_thread():
                    # Create fresh event loop for this thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        return loop.run_until_complete(get_agent_response(prompt))
                    finally:
                        loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    response = future.result()
                
                st.markdown(str(response))
                st.session_state.messages.append({"role": "assistant", "content": str(response)})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

