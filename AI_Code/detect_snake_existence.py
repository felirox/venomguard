from ultralytics import YOLO
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import pandas
from inference_sdk import InferenceHTTPClient
from concurrent.futures import ThreadPoolExecutor
from fuzzywuzzy import process

class DetectSnakeExistence:

    def __init__(self, path_to_image=None):
        self.path_to_image = path_to_image
        self.apiUrl = "https://detect.roboflow.com"
        self.apiKey ="ENTER_YOUR_API_KEY"
        self.CORE_API = "ENTER_YOUR_API_KEY"
        self.snake_df =None
        if __name__ == "__YOLO_main__":
            self.model = YOLO('yolov8n.pt')
        self.snake_existence_check = False
        self.CLIENT = InferenceHTTPClient(
            api_url=self.apiUrl,
            api_key=self.apiKey
        )

    def detect_snake(self,CORE_API=None):
        self.results = self.model(self.path_to_image) 

    def check_snake_existence(self, image = None):
        if image is not None:
            self.path_to_image = image
        print("DEBUG: Checking snake existence")
        
        CLIENT = InferenceHTTPClient(
            api_url=self.apiUrl,
            api_key=self.apiKey
        )
        self.result = CLIENT.infer(self.path_to_image, model_id="project-ai-final/1")
        print("DEBUG: Results obtained: ", self.result)
        
    def print_results(self):
        print(self.result)
    
    def get_results(self):
        return self.result
        
    def get_snake_existence(self, img=None):
        if img is not None:
            self.path_to_image = img
        self.check_snake_existence()
        
        print(self.result['predictions'])
        
        if self.result['predictions'] ==[]:
            print(">> INFO: No snake detected")
            return False
        else:
            print(self.result['predictions'][0]['confidence'])
            print(">> INFO: Snake detected")
            self.snake_existence_check = True
            return True
        
    def check_snake_type_c1(self, snake_existence_mcheck = False):
        if self.snake_existence_check == False or snake_existence_mcheck is True:
            print("WARN: Snake type cannot be deducted before checking snake presence")
            self.get_snake_existence()
        CLIENT = InferenceHTTPClient(
            api_url="https://outline.roboflow.com",
            api_key="ENTER_YOUR_API_KEY"
        )

        self.result_c1 = CLIENT.infer(self.path_to_image, model_id="snakes-calabarzon/2")
        
    def check_snake_type_c2(self, snake_existence_mcheck = False):
        if self.snake_existence_check == False or snake_existence_mcheck is True:
            print("WARN: Snake type cannot be deducted before checking snake presence")
            self.get_snake_existence()
        CLIENT = InferenceHTTPClient(
            self.apiUrl,
            self.apiKey
        )

        self.result_c2 = CLIENT.infer(self.path_to_image, model_id="snakes-calabarzon-pt.-2-2jcgo/2")
        
    def check_snake_types_simultaneously(self):
        with ThreadPoolExecutor() as executor:
            future_c1 = executor.submit(self.check_snake_type_c1)
            future_c2 = executor.submit(self.check_snake_type_c2)
            
            # Wait for both functions to complete and get their results
            result_c1 = future_c1.result()
            result_c2 = future_c2.result()
        print(">> INFO: Snake types checked simultaneously")
   
    def compare_c1_c2(self):
        self.check_snake_types_simultaneously()
        if self.result_c2 is None or self.result_c1 is None:
            print(">> INFO: No snake info detected")
            return False
        try:
            print(">> INFO: Confidence level of c1: ", self.result_c1['predictions'][0]['confidence'])
        except Exception as e:
            pass
        try:
            print(">> INFO: Confidence level of c2: ", self.result_c2['predictions'][0]['confidence'])
        except Exception as e:
            pass
        
        try:
            if self.result_c1['predictions']==[]:
                if self.result_c2['predictions']==[]:
                    print(">> INFO: No snake info detected in either")
                    return False
                else:
                    print(">> INFO: Snake type from 2 is ", self.result_c2['predictions'][0]['class'])
                    return self.result_c2['predictions'][0]['class']
        except Exception as e:
            pass
        try:
            if self.result_c2['predictions']==[]:
                if self.result_c1['predictions']==[]:
                    print(">> INFO: No snake info detected in either")
                    return False
                else:
                    print(">> INFO: Snake type from 1 is ", self.result_c1['predictions'][0]['class'])
                    return self.result_c1['predictions'][0]['class']
        except Exception as e:
            pass
        c2res = c1res = 0.0
        try:
            
            c2res = self.result_c2['predictions'][0]['confidence']
        except Exception as e:  
            pass
        try:
            c1res = self.result_c1['predictions'][0]['confidence']
        except Exception as e:
            pass
        
            
        print(">> INFO: Comparing snake types")   
        if c1res <0.20 and c2res<0.20:
            print(">> INFO: No snake info detected. Low confidence")
            return False
        
        if c1res > c2res:
            print(">> INFO: Snake type is1 ", self.result_c2['predictions'][0]['class'])
            return self.result_c2['predictions'][0]['class']
        else:
            print(">> INFO: Snake type is2 ", self.result_c1['predictions'][0]['class'])
            return self.result_c1['predictions'][0]['class']
   
    def get_snake_type(self,image = None):
        if image is not None:
            self.path_to_image = image  
        self.check_snake_types_simultaneously()
        c2c = self.compare_c1_c2()
        if c2c is False:
            print(">> INFO: No snake info detected")
            return False
        return c2c
    
    
    def load_csv_pandas(self):
        try:
            print(">> INFO: Loading csv file")
            self.snake_df = pandas.read_csv('AI_Code/custom_snakes_data.csv')
        except Exception as e:
            print(">> ERROR: ", e)
            print(">> ERROR: Loading csv file")
            
        # print(self.df)
        return self.snake_df
    
    def get_snake_detailed_info(self, snake_type):
        if self.snake_df is None:
            self.load_csv_pandas()
        #make letters small
        # snake_type = snake_type.lower()
        print(">> INFO: Getting snake info")
        
        snake_info = self.snake_df[self.snake_df['snake_name'].str.lower() == snake_type.lower()]
        if snake_info.empty:
            print(">> WARN: Exact Snake info not found in DB")
            #Attempt fuzzy logic search
            return self.fuzzyLogicSearch(snake_type)
        else:
            return snake_info.values.tolist()[0]
    
    def fuzzyLogicSearch(self,snake_type):
        print(">> INFO: Fuzzy logic search")
        print(">> INFO: Searching for similar snakes")
        # Define a threshold for matching
        threshold = 80  # This means 80% similarity or above
        # Convert the DataFrame column to a list for processing
        names_list = self.snake_df['snake_name'].tolist()

        # Find the best match above a certain threshold
        best_matches = [process.extractOne(snake_type, names_list, score_cutoff=threshold)]

        # Filter the DataFrame based on the matches
        similar_snakes = self.snake_df[self.snake_df['snake_name'].isin([match[0] for match in best_matches if match])]
        print("similar_snakes",similar_snakes.values.tolist())
        return similar_snakes.values.tolist()[0]
    
    def SnakeLLMSearch(self,snake_type):
        print(">> INFO: LLM search")
        print(">> INFO: Searching for snake info using LLM")
        
        
    
        
if __name__ == "__main__":
    path_to_image = r"./AI_Code/Dataset/examples/easternindigosnake-001.webp"
    snake_detector = DetectSnakeExistence(path_to_image)
    result = snake_detector.get_snake_existence()
    # snake_detector.check_snake_types_simultaneously()
    # snake_detector.compare_c1_c2()
    #This below function does what the above functions should do
    val = snake_detector.get_snake_type() 
    op = snake_detector.get_snake_detailed_info(val)
    print(op)