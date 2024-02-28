import streamlit as st
from PIL import Image

def home_page():
    # Catchphrase
    st.markdown("<h2 style='font-size: 40px; text-align: center; color: white;'>Know About the Snake, Stay Safe </h2>", unsafe_allow_html=True)
    st.write("##")
    st.write("##")
    
    # Greetings
    st.markdown("<h2 style='font-size: 24px; color: white;'>Greetings </h2>", unsafe_allow_html=True)

    st.markdown("<p style='color: white;'>Welcome to 🛡️VenomGuard, where you can learn about everything you need to know when confronting a snake. All you need to have to get started is the device that you are looking at! Click on the 'Detect' button in the sidebar to identify the snake or the 'Chat' button to get an assistance about the snake. </p>", unsafe_allow_html=True)

    st.write("##")
    st.write("##")
    
    # Top 3 Deadliest Snakes in the World
    st.markdown("<h2 style='font-size: 24px; color: white;'>Top 3 Deadliest Snakes in the World </h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    # left column
    with col1:
        inland_taipan_img = Image.open("./snake/Inland-Taipan.jpeg")
        resized_it_img = inland_taipan_img.resize((600, 400))
        st.image(resized_it_img, use_column_width=True)
        st.markdown("<h3 style='font-size: 18px; text-align: center; color: white;'>&#129351; Inland Taipan </h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white;'> The inland taipan is considered the most venomous snake in the world. The inland taipan's venom has the potency to kill 100 humans in a single bite. It lives in central east Australia. Despite its potency, it is rarely encountered by humans due to its elusive nature and remote habitat. </p>", unsafe_allow_html=True)
        
    # middle column
    with col2:
        coastal_taipan_img = Image.open("./snake/Coastal-Taipan.jpeg")
        resized_ct_img = coastal_taipan_img.resize((600, 400))
        st.image(resized_ct_img, use_column_width=True)
        st.markdown("<h3 style='font-size: 18px; text-align: center; color: white;'>&#129352; Coastal Taipan </h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white;'>You could be bitten multiple times before becoming aware of the coastal taipan, thanks to its incredible speed. The coastal taipan is found in the Australian outback and it ranges from light olive to dark brown in colour but has reddish eyes. The coastal taipan has a long, slender body.</p>", unsafe_allow_html=True)
        
    # right column
    with col3:
        king_cobra_img = Image.open("./snake/King-Cobra.jpeg")
        resized_kc_img = king_cobra_img.resize((600, 400))
        st.image(resized_kc_img, use_column_width=True)
        st.markdown("<h3 style='font-size: 18px; text-align: center; color: white;'>&#129353; King Cobra </h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: white;'>Native to South Asia, the king cobra is the longest venomous snake in the world. A single king cobra bite can kill a human in 15 minutes due to its large amount of venom injection. King Cobra is one of the few creatures in the animal kingdom that eat their own kind. </p>", unsafe_allow_html=True)
        
    return
    