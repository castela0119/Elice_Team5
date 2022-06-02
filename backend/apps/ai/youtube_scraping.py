# TODO: 코드 옮겨오긴 했는데, page_rank에 다 있어서 안써도 되는 것 같다. -> 여쭤보기!

import pytube
import pandas as pd
import re
from youtube_transcript_api import YouTubeTranscriptApi

url = "https://www.youtube.com/watch?v=mc02IZhouEg" #= input()
yt = pytube.YouTube(url)

# videoId = url의 (v=) 다음에 오는 11개 문자열 compile
pat = re.compile("(v=)([a-zA-Z0-9-_]{11})")
video_id = pat.search(url).group(2)

#list화
temp = YouTubeTranscriptApi.get_transcript(video_id, languages = {'ko'})
dic = {"timestamp" : [], "script" : []}

for i in temp:
    minute = int(i['start']) // 60
    second = int(i['start']) - minute * 60

    if (len(str(minute)) == 1) and (len(str(second)) == 1):
        #초와 분 둘 다 한자리 숫자이면
        dic['timestamp'].append("0" + str(minute) + ":0" + str(second))
    elif len(str(minute)) == 1:
        #분이 한자리 숫자이면
        dic['timestamp'].append("0" + str(minute) + ":" + str(second))
    elif len(str(second)) == 1:
        #초가 한자리 숫자이면
        dic['timestamp'].append(str(minute) + ":0" + str(second)) 
    else:
        dic['timestamp'].append(str(minute) + ":" + str(second)) 
     
    dic['script'].append(str(i['text']))

# df = pd.DataFrame(dic)
# print(df)
# #df.to_csv("test.csv", index = False)
# df.to_csv('test.txt', sep = '\t', index = False)