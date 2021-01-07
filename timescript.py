from pathlib import Path
import os
from pymediainfo import MediaInfo
import pandas as pd
import chime
import platform
import magic
import moviepy.editor
from tkinter import filedialog
from tkinter import *
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
fixedfoldername = folder_selected.replace(':','').replace('/','-').replace(' ','_')
print(fixedfoldername)

movielist = []

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 
      
# Driver program 
def getmovieinfo(folder_selected):
    for r,d,f in os.walk(folder_selected):
        #make list ala gitignore for directory to ignore
        if '\\venv' not in r: 
            for file in f:
                if platform.system() == 'Windows':
                    fileInfo = MediaInfo.parse(os.path.join(r,file))
                    for track in fileInfo.tracks:
                            if track.track_type == "Video":
                                print(file,track.duration)
                                #make list of video titles to ignore
                                if track.duration and 'sample' not in file.lower():
                                    movielist.append([file,str(track.other_duration[-2]).replace(';',':'),int(float(track.duration))])
                                    break
                else:
                    mime = magic.Magic(mime=True)
                    isvideo = mime.from_file(os.path.join(r,file)).find('video')
                    if isvideo != -1:
                        video = moviepy.editor.VideoFileClip(os.path.join(r,file))
                        duration = int(video.duration)*1000
                        movielist.append([file,convert(int(video.duration)),duration])




    return movielist
movielist = getmovieinfo(folder_selected)                                
df = pd.DataFrame(movielist,columns=['Movie Name','Duration','MilliSecondsLong'])
pd.set_option('display.max_rows', df.shape[0]+1)
df = df.sort_values('Duration')
print(df.head())
print(f"Average Video length is {convert(df['MilliSecondsLong'].mean()/1000)}")
with open(f'{fixedfoldername}movielength.csv', 'w') as f:
    f.write(df.to_csv(index=False))
print(f"Wrote to {fixedfoldername}movielength.csv name and length of {len(df)} videos")
chime.success(sync=True,raise_error=True)
