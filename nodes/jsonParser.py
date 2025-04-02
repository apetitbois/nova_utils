__package__ = "jsonParser"

import folder_paths
import json 
from os import walk
import os
import random

class jsonParser:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        file_list = s.getFileList()
        file_list.insert(0, "None")
        inputs = {
            "required": {
                "seed": ("INT",),
            }
        }
        for i in range (5):
            inputs["required"][f"sourceFile_{i}"] = (file_list,)
        return inputs
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", 'FLOAT',"STRING", 'FLOAT',"STRING", 'FLOAT',"STRING", 'FLOAT',"STRING", 'FLOAT', "STRING")
    RETURN_NAMES = ("positive_prompt","negative_prompt", "lora_name_0", "lora_weight_0","lora_name_1", "lora_weight_1","lora_name_2", "lora_weight_2","lora_name_3", "lora_weight_3","lora_name_4", "lora_weight_4", "prompt_name")
    FUNCTION = "run"
    CATEGORY = "💟NovaUtils/Parsers"
    
    def getFileList():
        prompts = folder_paths.get_input_directory()
        f = []
        for root, dirs, files in os.walk(prompts):
            for name in files:
                if ".json" in name:
                    dirname = root.replace(prompts,'')
                    f.append(str(dirname[1:]+dirname[0]+name))

        return sorted(list(f),)
    
    def parseJson(s, filename):
        if filename != "None":
            full_path=os.path.join(folder_paths.get_input_directory(), filename);
            f = open(full_path, "r")
            blob = json.load(f)
            return blob
        return

    @classmethod
    def parseChunk(s,text):
        final = []
        s1 = text.split("{",1)  					# Split incoming chunk at {
        if len(s1)>1:
            final.append(s1[0])						# Add anything before { to final
            s2 = s1[1].split("}",1)
            if len(s2)>1:
                s3=s2[0].split("|")
                if len(s3) > 1:
                    idx=random.randrange(len(s3))   # Choose one token at random
                    final.append(s3[idx])
                remain = s2[1]						# Add anything after } to remain
        else:
            return (s1[0],"")

        return (final, remain)

    @classmethod
    def parseTokens(s,txt):
        finalChunks, remain = s.parseChunk(txt)
        while remain != "":
            Chunks, remain = s.parseChunk(remain)
            finalChunks+=Chunks

        result = ''.join(finalChunks)
        return result
        

    def run(self, seed, **kwargs ):
        random.seed(seed)
        fName = 'None'
        while fName == 'None':
            idx = random.randrange(0,4)
            fName = kwargs.get(f"sourceFile_{idx}")
        content = self.parseJson(fName)
        p = content['prompt']
        prompt = self.parseTokens(p)
        lora = content['loras']
        loraName = ['','','','','']
        loraWeight = [0.0,0.0,0.0,0.0,0.0]
        for i in range(0,len(lora)):
            if i>4:
                break
            loraName[i] = lora[i]['name']
            loraWeight[i] = random.uniform(lora[i]['weight-range'][0],lora[i]['weight-range'][1])
        negativePrompt = content['negative_prompt']
        prompt_name = os.path.basename(fName)
        prompt_name = prompt_name.replace(".json",'')
        return (prompt,negativePrompt, loraName[0],loraWeight[0], loraName[1],loraWeight[1], loraName[2],loraWeight[2], loraName[3],loraWeight[3], loraName[4],loraWeight[4], prompt_name)
