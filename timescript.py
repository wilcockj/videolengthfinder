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
import imghdr
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
fixedfoldername = folder_selected.replace(
    ':', '').replace('/', '-').replace(' ', '_')
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


def getmovieinfo(folder_selected, mintime):
    for r, d, f in os.walk(folder_selected):
        # make list ala gitignore for directory to ignore
        if '\\venv' not in r:
            for file in f:
                if platform.system() == 'Windows':
                    if imghdr.what(os.path.join(r, file)) == "jpeg":
                        continue
                    fileInfo = MediaInfo.parse(os.path.join(r, file))
                    for track in fileInfo.tracks:
                            if track.track_type == "Video":
                                #print(file,track.other_duration,track.other_duration[1].split()[0])
                                # make list of video titles to ignore
                                if "min" not in track.other_duration[0]:
                                    continue
                                else:
                                    if "h" in track.other_duration[0]:
                                        minhr = track.other_duration[0].split("h")
                                        mins = minhr[1].split("min")[0].strip()
                                        mins = int(mins) + 60 * int(minhr[0])
                                    else:
                                        mins = track.other_duration[0].split("min")[0]
                                        mins = int(mins.strip())
                                if track.duration and 'sample' not in file.lower() and mins > mintime:
                                    print(file)
                                    print("added to list")
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
mintime = int(input("How many minutes long should the shortest video be?"))
movielist = getmovieinfo(folder_selected,mintime)                                
df = pd.DataFrame(movielist,columns=['Movie Name','Duration','MilliSecondsLong'])
pd.set_option('display.max_rows', df.shape[0]+1)
df = df.sort_values('Duration')
print(df.head(20))
print(f"Average Video length is {convert(df['MilliSecondsLong'].mean()/1000)}")
with open(f'{fixedfoldername}movielength.csv', 'w') as f:
    f.write(df.to_csv(index=False))
print(f"Wrote to {fixedfoldername}movielength.csv name and length of {len(df)} videos")
chime.success(sync=True,raise_error=True)
