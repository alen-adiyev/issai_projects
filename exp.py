import librosa

import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
%matplotlib inline

import glob
import re
speechFileList = []

for i in range (119, 137):
    speechFileList.append(str(i) + '.wav')
print(speechFileList)

# x, sr = librosa.load('interview_2.wav')
# plt.figure(figsize=(15, 5))
# librosa.display.waveplot(x, sr)


for speechFile in speechFileList:
    y, sr = librosa.load(speechFile,sr=None)
    m = re.match(r'\./C/(.+)\.wav', speechFile)
    filename = "alen"
    print(filename)
      #file.write(filename + '\n')
    path = 'segment/{}'.format(filename)
    print(path)
    if not os.path.isdir(path):
        os.makedirs(path)
#     librosa.display.waveplot(y,sr)
#     plt.savefig('{}/waveform_origin.png'.format(path))
#     plt.clf()
    m = re.match(r'\./C/(.+)\.wav', speechFile)  
    ts = librosa.effects.split(y,top_db=27, ref=np.max)
    i = 1
    log_file = '{}/log.txt'.format(path)
    with open(log_file,'w') as file:
        for start_i, end_i in ts:
            print(sr)
            print(start_i, end_i)
            print('chunk {} in file {}'.format(i, filename))
            if (float(end_i-start_i+1)/sr) <= 3.00:
                continue
            if (float(end_i-start_i+1)/sr) >= 10.00: 
                continue
            file.write('chunk {}:'.format(i, filename))
            print('time: {}s'.format(float(end_i-start_i+1)/sr))
            file.write('time: {}s\n'.format(float(end_i-start_i+1)/sr))
#             file.write('{}\n'.format(start_i/sr))
#             file.write('{}\n'.format((end_i)/sr))
            
#             plt.subplot(len(ts),1,i)
#             librosa.display.waveplot(y[start_i:end_i],sr)
            librosa.output.write_wav('{}/{}.wav'.format(path,speechFile[:-4]+"_"+str(i)),y[start_i:end_i],sr)
            i = i+1
        print(i)
            
    #work with log.txt (concatenate files if some length is not exceeded then ...)