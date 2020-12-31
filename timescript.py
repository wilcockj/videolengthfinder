from pathlib import Path
import os
from pymediainfo import MediaInfo
import pandas as pd

from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
fixedfoldername = folder_selected.replace(':','').replace('/','-')
print(fixedfoldername)

movielist = []

for r,d,f in os.walk(folder_selected):
    #make list ala gitignore for directory to ignore
    if '\\venv' not in r: 
        for file in f:
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
print(df.head())

with open(f'{fixedfoldername}movielength.csv', 'w') as f:
    f.write(df.to_csv(index=False))

print(f"Wrote to {fixedfoldername}movielength.csv name and length of {len(df)} videos")
