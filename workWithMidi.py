from midi import myMidi

import io
import re
import os

from mutagen.mp3 import MP3



# path = '/Volumes/My Passport/Karaoke/new_11.05.2021/audio/'
# path = 'e:\\Karaoke\\new_26.04.2021\\audio\\'
# path = '/Users/Oleg/Downloads/00098806/audio/'
# path = '/Volumes/My Passport/Karaoke/new_07.06.2021/audio/'
# path = '/Volumes/My Passport/Karaoke/new_26.04.2021/audio/'
path = '/Volumes/My Passport/Karaoke/new_27.06.2021/audio/'
# path = 'c:\\Kar\\'
# path = '/Users/Oleg/Downloads/new_11.05.2021/audio/send3/'
path0 = path + ''
message = ''

arr = os.listdir(path)

arr_midi = [x for x in arr if x.endswith(".mid")]
arr_txt = [x for x in arr if x.endswith(".txt")]
arr_ap = [x for x in arr if x.endswith("_0129.mp3")]


for midiF in arr_txt:
    midiF=midiF.split('.')
    fName=midiF[0]
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    print(fName) 
    
    ap = MP3(path0 + fName + '_0129.mp3',)
  
    f = open(path0 + fName + '.txt', 'r', encoding = 'utf-8')
    LyricTxt=f.read()
    f.close()
    LyricTxt=LyricTxt.strip()
    LyricTxt=LyricTxt+'\n'

    if LyricTxt.find('- ') != -1:
        LyricTxt=LyricTxt.replace('- ','-')
        message += 'find (- ); '
        # print (LyricTxt)
        
    LyricTxt=LyricTxt.replace('','')
    LyricTxt=LyricTxt.replace('','')
    LyricTxt=LyricTxt.replace('','')
    
    # LyricTxt=LyricTxt.replace('- ','-')??????? нужно ли, и как вызвать лог этого метода

    LyricTxt=LyricTxt.encode('cp1251')
    LyricTxt=LyricTxt.decode('latin-1')
   

    LyricSlogi = LyricTxt.replace (' ', ' |')
    LyricSlogi = LyricSlogi.replace ('-', '|')
    LyricSlogi = LyricSlogi.replace ('\n\n\n', '\n\n')
    LyricSlogi = LyricSlogi.replace ('\n', '\n|')

    LyricSlogi = LyricSlogi.split('|')
  
        
    s4et = len(LyricSlogi)
    for slogi in LyricSlogi:
        if slogi == '\n': s4et-=1
        if slogi == ' ' or slogi == '': 
            #LyricSlogi.remove(slogi)
            s4et-=1


    midi1 = myMidi(path0 + fName + '.mid')
    midi1.findTempo250()
    midi1.coutNotesLyrics()
    midi1.addTrackWithMyFormatLyric(LyricSlogi)

    if (midi1.notes!=s4et):
        print(' || notes v midi:', midi1.notes,' || lyrics v midi:', midi1.lyrics, ' || Slogov v txt:', s4et)
    if ap.info.length < midi1.midLen:
        print ('MIDI lenght more then mp3!!!')
        print("apLen", fName + '_0129.mp3', ap.info.length)
        print("midLen", fName + '.mid', midi1.midLen)
    if message != '':
        print ('MESSAGES: ', message)
        message = ''

    midi1.midiSave(s4et, path0, fName)


