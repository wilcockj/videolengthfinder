from moviepy.editor import VideoFileClip
from pathlib import Path
import os
from pymediainfo import MediaInfo
import pandas as pd
movielist = []
for r,d,f in os.walk('.'):
    #print(d)
    #make list ala gitignore for directory to ignore
    if '\\venv' not in r: 
        for file in f:
            #print(r,d,f)
            fileInfo = MediaInfo.parse(os.path.join(r,file))
            for track in fileInfo.tracks:
                    if track.track_type == "Video":
                        #print(file,track.duration)
                        #make list of video titles to ignore
                        if track.duration and 'sample' not in file.lower():
                            movielist.append([file,str(track.other_duration[3][:-1])])
df = pd.DataFrame(movielist,columns=['Movie Name','Duration'])
pd.set_option('display.max_rows', df.shape[0]+1)
df = df.sort_values('Duration')
with open('movielength.csv', 'w') as f:
    f.write(df.to_csv(index=False))
