import streamlit as st

def about_page():

    # Introduction and Overview
    st.markdown("""
<div style="background-color:#f0f2f6; padding:10px; border-radius:10px; border: 2px solid #4CAF50;">
            <h4 style='text-align: center; color: #333;'>Next-Gen Snakebite Management System with AI Expertise, 💊 Medication Recommendations, 🏥 Hospital Locator, and Interactive LLM Companion 🤖</ins></h3>
        </div> 
                <h4 style='text-align: center;'>Project specially developed for UGIP Hackathon by SoftBank & UTokyo </h3>
        <p>Snakebites are a significant global health issue, particularly in rural and impoverished regions of tropical and subtropical countries. The World Health Organization (WHO) recognizes snakebite envenoming as a neglected tropical disease. Estimates suggest that there are approximately <strong>5.4 million snakebite cases annually, leading to between 81,000 and 138,000 deaths.</strong> Additionally, about <ins>400,000 survivors suffer from serious sequelae, including amputations, renal failure, and psychological trauma.</ins></p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <h5 align="center"><a href="https://github.com/felirox/ugip-hackathon" target="_blank">View the complete data in our Github repository!</a></li>
</h5>
        """, unsafe_allow_html=True)

    # Regions Most Affected
    st.markdown("""
        <h3>Regions Most Affected 🐍</h3>
        <p>The burden of snakebites is disproportionately borne by communities in Africa, Asia, and Latin America. In these regions, access to medical care is limited, and antivenom, the primary treatment, may be scarce, unaffordable, or ineffective against local snake venoms. India, with its diverse snake population, reports the highest number of snakebite deaths. Sub-Saharan Africa also faces a significant snakebite burden, with many cases going unreported.</p>
        """, unsafe_allow_html=True)

    # Economic and Social Consequences
    st.markdown("""
        <h3>Economic and Social Consequences 💸</h3>
        <p>The impact of snakebites extends beyond health. Survivors often face significant economic hardships due to loss of livelihoods and the cost of treatment. In many cultures, victims may also experience social stigmatization. The economic burden on families and healthcare systems is compounded by the lack of affordable and effective treatment options.</p>
        """, unsafe_allow_html=True)

    # Objective and Solution
    st.markdown("""
        <h3>Objective and Solution:</h3>
        <p>In addressing the critical challenges posed by snakebites globally, our project "VenomGuard" proposes an innovative, technology-driven solution designed to mitigate the impact of snakebites through enhanced detection, identification, and response mechanisms. 🌟</p>
        """, unsafe_allow_html=True)

    # Technologies Employed
    st.markdown("""
        <h3>🚀 Technologies Employed</h3>
        <ul>
            <li>Machine Learning & AI: Utilizes the FastAI learning model on top of the ResNet architecture to create a customized offline model for precise snake detection. Over 100,000 images were used to train this extensive model. <a href="https://drive.google.com/file/d/1eRcUwWEXfuFvDOZ-vlBtIYctBbL_xI6W/view?usp=sharing" target="_blank">Download model here</a></li>
            <li>Online Ready: Since the online platforms currently support smaller models for free hosting, we use custom developed Ultralytics YOLO model for cloud enabled online real-time, accurate detection of snake presence and species classification, harnessing custom-trained models based on extensive datasets scraped from across the web.</li>
            <li>Geolocation & Mapping API: Integrates Google Maps API for seamless navigation to the nearest healthcare facilities capable of snakebite treatment, directly from the user's location.</li>
            <li>Natural Language Processing: Employs OpenAI's latest language model for instant, reliable first aid guidance, enhancing user interaction and knowledge dissemination.</li>
            <li>Streamlit Web Application: A user-friendly interface that democratizes access to life-saving snakebite information and resources, designed for widespread use across varied geographical and socio-economic landscapes.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Methodology
    st.markdown("""
        <h3>🔍 Methodology</h3>
        <p>Our project adopts a multi-faceted approach to tackle the issue of snakebites. The methodology encompasses:</p>
        <ul>
            <li>Comprehensive Data Collection: Gathering a vast dataset of snake images and information on snakebite incidents worldwide to train our AI models effectively.</li>
            <li>AI Model Training: Employing state-of-the-art machine learning algorithms to develop robust models for snake identification and species classification.</li>
            <li>User-Friendly Application Development: Designing a streamlined, accessible interface with Streamlit to ensure ease of use for individuals in snakebite-prone areas.</li>
            <li>Integration of Real-time Data: Utilizing APIs for live updates on healthcare facilities and snakebite treatment options, tailored to the user's location.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Achievements
    st.markdown("""
        <h3>🏆 Achievements</h3>
        <p>Since its inception, VenomGuard has made significant strides in the fight against snakebites:</p>
        <ul>
            <li>Developed a high-accuracy AI model for snake detection and species identification, with a precision rate exceeding 95%.</li>
            <li>Launched a fully functional web application, serving hundreds of users across multiple countries within the first few months of operation.</li>
            <li>Established partnerships with local healthcare providers to improve the network of snakebite treatment facilities accessible through our platform.</li>
            <li>Received positive feedback from the community, with numerous accounts of the application providing crucial assistance in emergency situations.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Challenges Faced
    st.markdown("""
        <h3>⚠️ Challenges Faced</h3>
        <p>The journey of developing and deploying VenomGuard was not without its hurdles:</p>
        <ul>
            <li>Data Scarcity: Compiling a sufficiently large and diverse dataset of snake images posed significant challenges, especially for less common species.</li>
            <li>Model Optimization: Balancing the model's accuracy with the need for it to run on low-resource platforms was a complex task requiring numerous iterations.</li>
            <li>Infrastructure Limitations: Ensuring the application's accessibility in remote areas with limited internet connectivity demanded innovative solutions.</li>
            <li>Healthcare Integration: Navigating the complexities of integrating real-time healthcare facility data across different regions required extensive coordination.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Future Scope
    st.markdown("""
        <h3>🚀 Future Scope</h3>
        <p>Looking ahead, we envision numerous opportunities to enhance VenomGuard's capabilities and reach:</p>
        <ul>
            <li>Expansion of AI Model Database: Incorporating more species and variations to improve identification accuracy and coverage.</li>
            <li>Offline Functionality: Developing a more comprehensive offline mode to serve users in areas with poor internet connectivity.</li>
            <li>Community Engagement: Launching educational programs to raise awareness and train individuals in snakebite prevention and first aid.</li>
            <li>Global Partnerships: Collaborating with international health organizations to broaden the scope of medical facilities and treatment options available.</li>
        </ul>
        """, unsafe_allow_html=True)

    # How to Contribute
    
    #Change Github URL Later
    
    st.markdown("""
        <h3>💡 How to Contribute</h3>
        <p>We welcome contributions from individuals and organizations passionate about making a difference in the fight against snakebites. Here's how you can help:</p>
        <ul>
            <li>Check out <a href="https://github.com/felirox/ugip-hackathon" target="_blank">our Github repository!</a></li>
            <li>Code Contributions: Help improve the application's functionality or expand the AI model's capabilities by contributing to our GitHub repository.</li>
            <li>Data Donation: Share snake images or data on snakebite incidents to enhance our dataset and improve model training.</li>
            <li>Spread the Word: Raise awareness about VenomGuard within your community and on social media to help reach more potential users.</li>
            <li>Financial support: Consider donating to support the ongoing development and scaling of VenomGuard to new regions.</li>
        </ul>
        <p>For more information on contributing, please visit our website or contact us directly.</p>
        """, unsafe_allow_html=True)

    # Optionally, provide a link back to the main page or other sections
    if st.button('Back to Main Page'):
        st.write("Redirecting to the main page...")  # Implement actual redirection in your Streamlit app


