import os
from os.path import join
import math
import copy

from praatio import tgio
from praatio import audioio

def splitAudioOnTier(wavFN, tgFN, tierName, outputPath,
                     outputTGFlag=False, nameStyle=None,
                     noPartialIntervals=False, silenceLabel=None):
    '''
    Outputs one subwav for each entry in the tier of a textgrid
    
    outputTGFlag: If True, outputs paired, cropped textgrids
                  If is type str (a tier name), outputs a paired, cropped
                  textgrid with only the specified tier
    nameStyle: if 'append': append interval label to output name
               if 'append_no_i': append label but not interval to output name
               if 'label': output name is the same as label
               if None: output name plus the interval number
    noPartialIntervals: if True: intervals in non-target tiers that are
                                  not wholly contained by an interval in
                                  the target tier will not be included in
                                  the output textgrids
    silenceLabel: the label for silent regions.  If silences are unlabeled
                  intervals (i.e. blank) then leave this alone.  If silences
                  are labeled using praat's "annotate >> to silences"
                  then this value should be "silences"
    '''
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    
    if noPartialIntervals is True:
        mode = 'strict'
    else:
        mode = 'truncated'
    
    tg = tgio.openTextgrid(tgFN)
    entryList = tg.tierDict[tierName].entryList
    
    if silenceLabel is not None:
        entryList = [entry for entry in entryList
                     if entry[2] != silenceLabel]
    
    # Build the output name template
    name = os.path.splitext(os.path.split(wavFN)[1])[0]
    orderOfMagnitude = int(math.floor(math.log10(len(entryList))))
    
    # We want one more zero in the output than the order of magnitude
    outputTemplate = "%s_%%0%dd" % (name, orderOfMagnitude + 1)
    
    firstWarning = True
    
    # If we're using the 'label' namestyle for outputs, all of the
    # interval labels have to be unique, or wave files with those
    # labels as names, will be overwritten
    if nameStyle == 'label':
        wordList = [word for _, _, word in entryList]
        multipleInstList = []
        for word in set(wordList):
            if wordList.count(word) > 1:
                multipleInstList.append(word)
        
        if len(multipleInstList) > 0:
            instListTxt = "\n".join(multipleInstList)
            print(("Overwriting wave files in: %s\n" +
                   "Intervals exist with the same name:\n%s")
                  % (outputPath, instListTxt))
            firstWarning = False
    
    # Output wave files
    outputFNList = []
    wavQObj = audioio.WavQueryObj(wavFN)
    for i, entry in enumerate(entryList):
        start, stop, label = entry
        
        # Resolve output name
        outputName = outputTemplate % i
        if nameStyle == "append":
            outputName += "_" + label
        elif nameStyle == "append_no_i":
            outputName = name + "_" + label
        elif nameStyle == "label":
            outputName = label
        
        outputFNFullPath = join(outputPath, outputName + ".wav")

        if os.path.exists(outputFNFullPath) and firstWarning:
            print(("Overwriting wave files in: %s\n" +
                   "Files existed before or intervals exist with " +
                   "the same name:\n%s")
                  % (outputPath, outputName))
        
        frames = wavQObj.getFrames(start, stop)
        wavQObj.outputModifiedWav(frames, outputFNFullPath)
        
        outputFNList.append((start, stop, outputName + ".wav"))
        
        # Output the textgrid if requested
        if outputTGFlag is not False:
            subTG = tg.crop(start, stop, mode, True)
            
            if isinstance(outputTGFlag, str):
                for tierName in subTG.tierNameList:
                    if tierName != outputTGFlag:
                        subTG.removeTier(tierName)
            
            subTG.save(join(outputPath, outputName + ".TextGrid"))
    
    return outputFNList

#change boundaries accordingly
for i in range(106,151):	
    try:
        #tg = tgio.openTextgrid(str(i)+".TextGrid")
        tg = tgio.openTextgrid("nur"+str(i)+".TextGrid")
    except Exception:
        continue
    
    try:
        entryList = tg.tierDict["sentences"].entryList
    except Exception:
        try:
            entryList = tg.tierDict["Sentences"].entryList
        except Exception:
            try:
                entryList = tg.tierDict["sentenses"].entryList
            except Exception:
                try:
                    entryList = tg.tierDict["Sentenses"].entryList
                except Exception:
                    try:
                        entryList = tg.tierDict["sentseces"].entryList
                    except Exception:
                        try:
                            entryList = tg.tierDict["sentsences"].entryList
                        except Exception:
                            try:
                                entryList = tg.tierDict["senyences"].entryList
                            except Exception:
                                try:
                                    entryList = tg.tierDict["Sentence"].entryList
                                except Exception:
                                    try:
                                        entryList = tg.tierDict["sentence"].entryList
                                    except Exception:
                                        try:
                                            entryList = tg.tierDict["sentience"].entryList
                                        except Exception:
                                            try:
                                                entryList = tg.tierDict["sebtebces"].entryList
                                            except Exception:
                                                print(j)
                                                continue
    print(entryList)
    x = len(entryList)

    for j in range(0,len(entryList)):
#         f = open("tengrinews_blog"+str(i) + "_" + str(j) + ".txt", "w")
        if x > 99:
            if j < 10:
                f = open("nur"+str(i)+"_00" + str(j) + ".txt", "w")
            elif j < 100:
                f = open("nur"+str(i)+ "_0" + str(j) + ".txt", "w")
            else: 
                f = open("nur"+str(i)+"_" + str(j) + ".txt", "w")
            f.write(entryList[j].label)
            f.close()
        elif x > 9:
            if j < 10:
                f = open("nur"+str(i) + "_0" + str(j) + ".txt", "w")
            else: 
                f = open("nur"+str(i) +"_" + str(j) + ".txt", "w")
            f.write(entryList[j].label)
            f.close()
        else:
            if j < 10:
                f = open("nur"+str(i)+ "_" + str(j) + ".txt", "w")
            else:
                f = open("nur"+str(i) +"_" + str(j) + ".txt", "w")
            f.write(entryList[j].label)
            f.close()
        
#         f.write(entryList[j].label)
#         f.close()

    try:
        splitAudioOnTier("nur"+str(i) + '.wav',"nur"+str(i) + '.TextGrid', 'sentences', 'splitted_audio')
    except Exception:
        try:
            splitAudioOnTier("nur"+str(i) + '.wav',"nur"+str(i) + '.TextGrid', 'Sentences', 'splitted_audio')
        except Exception:
            try:
                splitAudioOnTier("nur"+str(i)+ '.wav',"nur"+str(i)+ '.TextGrid', 'sentenses', 'splitted_audio')
            except Exception:
                try:
                    splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i) + '.TextGrid', 'Sentenses', 'splitted_audio')
                except Exception:
                    try:
                        splitAudioOnTier("nur"+str(i) + '.wav',"nur"+str(i) + '.TextGrid', 'sentseces', 'splitted_audio')
                    except Exception:
                        try:
                            splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i) + '.TextGrid', 'sentsences', 'splitted_audio')
                        except Exception:
                            try:
                                splitAudioOnTier("nur"+str(i)+ '.wav', "nur"+str(i) + '.TextGrid', 'senyences', 'splitted_audio')
                            except Exception:
                                try:
                                    splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i) + '.TextGrid', 'Sentence', 'splitted_audio')
                                except Exception:
                                    try:
                                        splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i)+ '.TextGrid', 'sentence', 'splitted_audio')
                                    except Exception:
                                        try:
                                            splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i) + '.TextGrid', 'sentience', 'splitted_audio')
                                        except Exception:
                                            try:
                                                splitAudioOnTier("nur"+str(i) + '.wav', "nur"+str(i) + '.TextGrid', 'sebtebces', 'splitted_audio')
                                            except Exception:
                                                print("Error", i)
                                                continue
                                            
                                            