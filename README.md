#  🛡️VenomGuard

## Next-Gen Snakebite Management System with AI Expertise, 💊 Medication Recommendations, 🏥 Hospital Locator, and Interactive LLM Companion 🤖
<h3 align="center">
<ins> <b>Project specially developed for UGIP Hackathon by SoftBank & UTokyo</b> </ins>
</h3>
Snakebites are a significant global health issue, particularly in rural and impoverished regions of tropical and subtropical countries. The World Health Organization (WHO) recognizes snakebite envenoming as a neglected tropical disease. Estimates suggest that there are approximately **5.4 million snakebite cases annually, leading to between 81,000 and 138,000 deaths.** Additionally, about <ins> 400,000 survivors suffer from serious sequelae, including amputations, renal failure, and psychological trauma. </ins>

### Regions Most Affected 🐍 
The burden of **snakebites is disproportionately borne by communities in Africa, Asia, and Latin America.** In these regions, access to medical care is limited, and antivenom, the primary treatment, may be scarce, unaffordable, or ineffective against local snake venoms. India, with its diverse snake population, reports the highest number of snakebite deaths. Sub-Saharan Africa also faces a significant snakebite burden, with many cases going unreported.

### Economic and Social Consequences 💸
The impact of snakebites extends beyond health. Survivors often face significant economic hardships due to loss of livelihoods and the cost of treatment. In many cultures, victims may also experience social stigmatization. The economic burden on families and healthcare systems is compounded by the lack of affordable and effective treatment options.

## Objective and Solution:
In **addressing the critical challenges posed by snakebites globally**, our project **"VenomGuard"** proposes an innovative, technology-driven solution designed to **mitigate the impact of snakebites through enhanced detection, identification, and response mechanisms.** 🌟

### 🚀 Technologies Employed
* **Machine Learning & AI:** Utilizes the FastAI learning model on top of the ResNet architecture to create a customized offline model for precise snake detection. Over 100,000 images were used to train this extensive model. [Download model here](https://drive.google.com/file/d/1eRcUwWEXfuFvDOZ-vlBtIYctBbL_xI6W/view?usp=sharing)
* **Online Ready:** Since the online platforms currently support smaller models for free hosting, we use custom developed Ultralytics YOLO model for cloud enabled online real-time, accurate detection of snake presence and species classification, harnessing custom-trained models based on extensive datasets scraped from across the web.
* **Geolocation & Mapping API:** Integrates Google Maps API for seamless navigation to the nearest healthcare facilities capable of snakebite treatment, directly from the user's location.
* **Natural Language Processing:** Employs OpenAI's latest language model for instant, reliable first aid guidance, enhancing user interaction and knowledge dissemination.
* **Streamlit Web Application:** A user-friendly interface that democratizes access to life-saving snakebite information and resources, designed for widespread use across varied geographical and socio-economic landscapes.

### 💡 Key Features
* **AI-Driven Identification:** Advanced algorithms instantly recognize and classify snakes, discerning venomous from non-venomous species with unparalleled accuracy.
* **Critical Medical Resources:** An interactive map guides affected individuals to the closest medical facilities equipped for snakebite emergencies, informed by real-time geolocation data.
* **Immediate First Aid Assistance:** The integration of an AI-powered conversational agent provides users with immediate, actionable first aid advice, tailored to the specific snakebite incident.
* **Comprehensive Educational Outreach:** A vast, accessible knowledge base educates communities on snakebite prevention, first aid, and the importance of timely medical intervention.

### 🌍 Impact and Innovation
This project stands at the forefront of global health innovation, addressing the WHO's call to action on snakebite envenoming with a multifaceted technology-first approach. By combining AI, geo-location, and LLM technologies, we're setting new standards in public health response mechanisms, educational outreach, and community empowerment against snakebites.

* **Elevates Global Health Standards:** Our solutions directly contribute to reducing the annual incidence of snakebite fatalities and long-term disabilities, particularly in under-resourced regions.
* **Democratizes Medical Knowledge:** By providing immediate, accessible guidance on snakebite treatment and first aid, we bridge critical gaps in public health education.
* **Supports Sustainable Healthcare Practices:** Our project aids in the optimization of antivenom distribution and use, supporting more sustainable healthcare practices worldwide.

### 🛠️ Behind the Scenes: Technical Brilliance
* **Custom AI Models** - Developed three bespoke AI models: one for detecting snake presence and two for detailed species classification, trained on a vast corpus of data, showcasing a significant leap in machine learning applications for public health.
* **Comprehensive Data Aggregation** - Conducted exhaustive internet-wide scraping efforts to compile a comprehensive database on global snake species, supplemented by a sophisticated fuzzy logic algorithm for nuanced species differentiation.
* **Streamlit & Google Maps Integration** - Crafted an intuitive Streamlit web application, integrating Google Maps API for automated user location detection and nearby hospital listings, culminating in a seamless end-to-end user experience.

# Setup

## Prerequisites

Before installing and running this application, ensure you have the following installed on your system:
- Python 3.9
- Conda (recommended for managing environments)
- Pytorch, CUDA (check reuirements.txt)

## Installation & Environment Setup

1. **Create and Activate a Conda Environment**

   To isolate and manage the project's dependencies, create a new Conda environment:

   ```bash
   conda create -n snakeenv python=3.9
   conda activate snakeenv
   ```

2. **Install Required Libraries**

   Install the necessary Python libraries within your active environment:

   ```bash
   pip install -y ultralytics opencv-python-headless pillow matplotlib pandas fuzzywuzzy python-Levenshtein requests concurrent futures
   ```

   Note: The `ultralytics[all]` package is a comprehensive installation that includes YOLOv5 and other utilities for deep learning-based object detection.

3. **Additional Dependencies**

   Depending on your system, you might need additional libraries or tools. Ensure all dependencies are resolved before proceeding.

## Application Setup

1. **Clone the Repository**

   Ensure you have the application code on your local machine. If provided, clone the repository using Git or download the source code directly.

2. **Prepare the Dataset**

   Place your dataset images in the specified directory structure (e.g., `./AI_Code/Dataset/examples/`) to ensure the application can process them.

3. **API Keys and Endpoints**

   Update the `DetectSnakeExistence` class with the correct API keys and endpoints for the inference services you are using. These are critical for connecting to external AI models for snake detection and type identification.

## Dataset

* For training of the snake models, use the dataset sourced from [Microsoft and AI Crowd](https://www.aicrowd.com/challenges/snakeclef2021-snake-species-identification-challenge).
* We custom scrape the "snake deadliness" information from [SnakeDB](http://snakedb.org/)
*  You can find complete information of our novel crowdsourced data [here](AI_Code/custom_snakes_data.csv)

## Running the Application

To execute the snake detection application, navigate to the project directory and run the main script:

```bash
python main.py
```

Replace `main.py` with the actual name of your Python script if different.

To run the model detections in isolation, run the `DetectSnakeExistence` class from [here](AI_Code/detect_snake_existence.py)
```bash
python './AI_Code/detect_snake_existence.py' 
```
## Example Usage

After running the application, it will process the image specified in the `path_to_image` variable, detect if a snake is present, identify its type, and fetch detailed information about the snake. The results will be printed to the console.

## Troubleshooting

- **Environment Issues**: Ensure the Conda environment is activated before installing dependencies or running the application.
- **Dependency Conflicts**: If you encounter conflicts, verify the installed versions of the libraries and consult their official documentation for compatibility information.
- **API Connectivity**: Ensure your API keys are valid and endpoints are correctly configured in the application code.


## Authors
<!-- Add your information here! -->
- [@Miyuki]()
- [@Niran](https://niran.dev/)
- [@Yuki]()


