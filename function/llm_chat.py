from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, \
    MessagesPlaceholder, \
    PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler
import os
import openai
import streamlit as st
from dotenv import load_dotenv

# set env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_for_chat_structure = PromptTemplate(
    input_variables=["snake_type"],
    template="""
    # variables
    [Types of the snake] = ```{snake_type}```

    # instruction
    Please provide first aid and necessary measures for a user who has been bitten by a snake.
    
    # context
    The user has been bitten by a venomous snake.
    """)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate(prompt=prompt_for_chat_structure),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}"),
])

def first_aid_chat(snake_type, first_aid, hospitals):
    # nearby hospital
    st.markdown('### Nearby hospital')
    
    if len(hospitals) > 5:
        for i in range(5):
            st.write(f"{i+1}. {hospitals[i]}")
        
        if st.button('さらに表示'):
            for i in range(5, len(hospitals)):
                st.write(f"{i+1}. {hospitals[i]}")
    else:
        for i, hospital in enumerate(hospitals):
            st.write(f"{i+1}. {hospital}")
    st.markdown('### How to administor first aid.')

    # first aid
    llm_memory = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    memory = ConversationSummaryBufferMemory(llm=llm_memory, memory_key="chat_history", input_key="human_input",
                                             return_messages=True, max_token_limit=200)

    # chatを行う準備（各chatごとに行う）
    llm_key = f'llm_greetings'
    if llm_key not in st.session_state:
        llm = ChatOpenAI(model_name="gpt-4", temperature=0, streaming=True)

        chat_llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            verbose=True,
        )
        st.session_state[llm_key] = chat_llm_chain
    else:
        chat_llm_chain = st.session_state[llm_key]

    # 初めてのchatの場合
    if f"chat_first_aid" not in st.session_state:
        st.session_state[f"chat_first_aid"] = [{"role": "assistant", "content": first_aid}]
    # 過去のmessageを全て表示する & chat_contextを更新
    for message in st.session_state[f"chat_first_aid"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 今回のmessageのinputと表示
    if user_input := st.chat_input("Please input the text", key=f"chat_first_aid_input"):
        st.session_state[f"chat_first_aid"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # LLMの回答の表示
        with st.chat_message("assistant"):
            st_callback = StreamlitCallbackHandler(st.container())  # この行も必要に応じて修正または削除する
            response = chat_llm_chain.predict(snake_type = snake_type,
                                              human_input=user_input,
                                              callbacks=[st_callback])
        st.session_state[f"chat_first_aid"].append({"role": "assistant", "content": response})
