from flask import Flask, request
import random
import os
import json
import pandas as pd

app = Flask(__name__)
filePath = "dataset_new.csv"

if not os.path.exists(filePath): 
    file = pd.DataFrame(columns=["Timestamp", "Value", "Sensor"])
    file.to_csv(filePath,index=False)
    

    
@app.route("/", methods=['POST'])
def server():
    if random.choice([True,False]):
        print(request.data)
        
        file = pd.DataFrame(json.loads(request.data), index=[0])
        file.to_csv(filePath, mode="a",index=None,header=None)
        
        return {"status": "successful"}
    else:
        return {"status": "Failed"}
        
app.run()
