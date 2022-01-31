import cv2
import json
import re
import pafy
import time

'''
Set API key
'''
pafy.set_api_key("AIzaSyAUE8vMgamLLrGXO7686mmE71CW_ucb6qk")


'''
Get List of Videos and pop first 520 vids
'''
f = open("videos.json" ,encoding="utf8")
data = json.load(f)
print(len(data["messages"]))
f.close()
inital_pop = 794
for i in range(inital_pop):
    data["messages"].pop(0)


with open("base_array.json") as f:
    base_array = json.load(f)["arr"]
print(len(base_array))

'''
Loop over all videos
'''
for i,vid in enumerate(data["messages"]):
    '''
    Get video url
    '''
    url = re.findall('https[\s\S]+',vid["content"])[0]
    try: 

        '''
        Get video info
        '''
        video = pafy.new(url)
        des = video.description
        '''
        Get all base links
        '''
        bases = re.findall("[1]{1,2}[:][\s\S]+https:\/\/link\.clashofclans\.com\/en\?action=OpenLayout&id=TH14[\S]+[\n]" , des)
        '''
        Getting All time Stamps
        '''
        timestamps = re.findall("[0-9]{1,2}[:][0-9]{2}", des)
        timestamps = [float(int(x.split(":")[0])*60 + int(x.split(":")[1])) for x in timestamps]
        timestamps.pop(0)
        timestamps.pop()

        print(video.title)
        print("Video : ",inital_pop+i)

        if len(timestamps) >= 0:
            if(len(bases) >= 1):
                '''
                If there is a base link and timestamps exists
                '''
                print("Base found with timestamps : ", len(timestamps), " and bases : ", len(bases))   
                best = video.getbest()

                cap = cv2.VideoCapture(best.url)
                fps = cap.get(cv2.CAP_PROP_FPS)
                cur = 0
                js = {
                    "title" : video.title,
                    "url" : best.url,
                    "bases" : bases,
                    "timestamps" : timestamps,
                    "imgs" : []
                }
                for j in timestamps: 
                    cap.set(cv2.CAP_PROP_POS_FRAMES, (j - cur)*fps)
                    success,image = cap.read()
                    cv2.imwrite(f"images/base{inital_pop+i}{j}.jpg", image)
                    js["imgs"].append(f"base{inital_pop+i}{j}.jpg")
                

                base_array.append(js)
                print("Base added")
                # save base array in a json file
                with open('base_array.json', 'w') as outfile:
                    json.dump({"arr" : base_array}, outfile)
                time.sleep(10)
    except:
        print("Error")