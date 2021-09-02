
import io
import re
import os
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from mutagen.mp3 import MP3




# проверка длительности мп3 и миди -ok
# проверить наличие темпа больше 250 -ok
# 

# path = '/Volumes/My Passport/Karaoke/new_11.05.2021/audio/'
# path = 'e:\\Karaoke\\new_26.04.2021\\audio\\'
# path = '/Users/Oleg/Downloads/00098806/audio/'
# path = '/Volumes/My Passport/Karaoke/new_07.06.2021/audio/'
# path = 'e:\\Karaoke\\TOP82\\audio\\'
# path = '/Volumes/My Passport/Karaoke/new_26.04.2021/audio/'
# path = '/Volumes/My Passport/Karaoke/new_27.06.2021/audio/'
# path = 'c:\\Kar\\'
# path = '/Users/Oleg/Downloads/new_11.05.2021/audio/send3/'
path = '/Volumes/My Passport/Karaoke/new_27.06.2021/audio/'
path = '/Volumes/My Passport/Karaoke/new_09.07.2021/audio/'
# path = '/Volumes/My Passport/Karaoke/TOP81/audio/'
# path = '/Users/Oleg/Downloads/133816/audio/'
# path = '/Volumes/My Passport/Karaoke/TOP80/audio/'
# path = '/Volumes/My Passport/Karaoke/TOP79/audio/'

path0 = path + ''
message = ''

arr = os.listdir(path)
# print(arr)

arr_midi = [x for x in arr if x.endswith(".mid")]
arr_txt = [x for x in arr if x.endswith(".txt")]
arr_ap = [x for x in arr if x.endswith("_0129.mp3")]

# print("arr_midi", arr_midi)
# print("arr_txt", arr_txt)
# print("arr_ap", arr_ap)

for midiF in arr_txt:
    midiF=midiF.split('.')
    fName=midiF[0]
    print('++++++++++++++++++++++++++++++++++++++++++++')
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
   
    # print (LyricTxt)
    # LyricTxt = LyricTxt.encode(encoding = 'utf-8')
    #LyricTxt = LyricTxt.decode("windows-1251")

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

    # print (LyricSlogi)

    # for slogi in LyricSlogi:
    #     if slogi == '' or slogi == '\n': s4et-=1 #stranno ne wse udaljaet poetomu 2 raza)

    # print (LyricSlogiSchet)
    # print ('LyricSlogi-len', len(LyricSlogiSchet))

    # for n in LyricSlogi:
    #     print (n)

    

    mid = MidiFile(path0 + fName + '.mid', clip=True)

    midLen = mid.length


    def get_tempo(mid):
        tempo = []
        for msg in mid:     # Search for tempo
            if msg.type == 'set_tempo':
                tempo.append (mido.tempo2bpm(msg.tempo))
        return tempo
    overTempo = False
    for tempo in get_tempo(mid):
        if tempo > 250:
            overTempo = True

    # print(mid)

    # for track in mid.tracks:
    #     print(track)

    # print(mid.tracks[0])
    # sna4ala proverit nali4ie not i lyrics v 1 treke
    notes = 0
    lyrics = 0

    for msg in mid.tracks[1]:
        if msg.type == 'note_on' and msg.velocity > 0: 
            # print(msg)
            notes+=1
        if msg.type == 'lyrics' and msg.text != '\n' and msg.text != '\r' and msg.text != ' ' and msg.text != '': 
            # print(msg)
            lyrics+=1
        

    # midiEnd = MidiFile()
    track1 = MidiTrack()
    track2 = MidiTrack()
    # midiEnd.tracks.append(mid.tracks[0])
    

    # mido.merge_tracks(mid)


    lTime=0

    # for msg in mid.tracks[1]:
    #     print (msg)
        
    
    for msg in mid.tracks[1]:
        if lTime!=0:
            msg.time+=lTime
            lTime=0
        if msg.type != 'lyrics':
            track1.append(msg)
        if msg.type == 'lyrics':
            if msg.time > 0:
                lTime = msg.time
            
    mid.tracks.append(track1)    
     

    i=0
    # print (LyricSlogi)
    for msg in mid.tracks[2]:
        if msg.type != 'lyrics':
            track2.append(msg)
        if msg.type == 'note_on' and msg.velocity > 0:
            if LyricSlogi[i] != '*':###
                if (LyricSlogi[i][-1:] == '\n'):
                    track2.append(MetaMessage('lyrics', text=LyricSlogi[i][:-1]+' ', time=0))
                    track2.append(MetaMessage('lyrics', text=LyricSlogi[i][-1:], time=0))
                else:
                    track2.append(MetaMessage('lyrics', text=LyricSlogi[i], time=0))

            if i < len(LyricSlogi)-1:
                if LyricSlogi[i+1]=='\n' or LyricSlogi[i+1]=='\r':
                    i+=1
                    track2.append(MetaMessage('lyrics', text=LyricSlogi[i], time=0))
            i+=1  
            if i == len(LyricSlogi): break




    mid.tracks.append(track2)

    mid.tracks.remove(mid.tracks[1])
    mid.tracks.remove(mid.tracks[1])
    # mid.tracks.remove(mid.tracks[2])

    # print (mid)
    # print (midiEnd)
    


    # f = open('1.txt', 'r+', encoding = 'latin-1')
    # f.write(str(mid))
    # f.close()
    # # f = open('2.txt', 'r+')
    # # f.write(str(midiEnd))
    # # f.close()
    
    # quit()


    # for track in midiEnd.tracks:
    #     print(track)


    # 
    # print('+++++++++++++++++++++++++++++++')
    # print (midiEnd.tracks[1])
    
    if (notes!=s4et):
        print(' || notes v midi:', notes,' || lyrics v midi:', lyrics, ' || Slogov v txt:', s4et)
    if ap.info.length < midLen:
        print ('MIDI lenght more then mp3!!!')
        print("apLen", fName + '_0129.mp3', ap.info.length)
        print("midLen", fName + '.mid', midLen)
    if overTempo:
        print('tempo in midi - OVER!!!')
        print ('changesTempo', get_tempo(mid))
    if message != '':
        print ('MESSAGES: ', message)

    # print('+++++++++++++++++++++++++++++++++++++++++++++++++')

    message = ''

    if notes==s4et:
        mid.save(path0+'render/' + fName + '.mid')
    else:
        mid.save(path0 + fName + '_NOT_OK.mid')



# mid = MidiFile()
# track = MidiTrack()
# mid.tracks.append(track)

# track.append(Message('program_change', program=12, time=0))
# track.append(Message('note_on', note=64, velocity=64, time=32))
# track.append(Message('note_off', note=64, velocity=127, time=32))

# mid.save('new_song.mid')




# mid.save('end.mid')    
    
    # if msg.time != 0:
    #     if msg.type == 'lyrics': print(msg)






# +++++++++++++++++++++++++++
# msg.is_meta

# +++++++++++++++++++++++++++

# >>> msg.type
# 'note_on'
# >>> msg.note
# 60
# >>> msg.velocity
# 64


# mid = MidiFile(type=2)
# mid.type = 1


# ++++++++++++++++++++++++++++++++++++++

# from mido import Message, MidiFile, MidiTrack

# mid = MidiFile()
# track = MidiTrack()
# mid.tracks.append(track)

# track.append(Message('program_change', program=12, time=0))
# track.append(Message('note_on', note=64, velocity=64, time=32))
# track.append(Message('note_off', note=64, velocity=127, time=32))

# mid.save('new_song.mid')


# +++++++++++++++++++++++

# from mido import MidiFile, MidiFile, MidiTrack

# # Opening the original MIDI sequence
# input_midi = MidiFile('./Murundu.mid')

# # Creating the destination file object
# output_midi = MidiFile()

# # Copying the time metrics between both files
# output_midi.ticks_per_beat = input_midi.ticks_per_beat

# note_map = {}
# # Load the mapping file
# with open('note_map.csv') as map_text:
#     for line in map_text:
#         elements = line.replace('\n','').split(',')
#         # Each line in the mapping file will be loaded into a
#         # dictionary with the original MIDI note as key and
#         # another dictionary with target note 
#         # and description as value
#         note_map[int(elements[0])] = { 
#             'target_note': int(elements[1]), 
#             'description': elements[2] }

# # Now, we iterate the source file and insert mapped notes
# # into the destination file

# # Notes are determined by note_on e note_off MIDI messages
# # Other types of messages will be copied directly 
# # Notes that does not exist in the mapping will not be copied

# for original_track in input_midi.tracks:

#     new_track = MidiTrack()

#     for msg in original_track:
#         if msg.type in ['note_on','note_off']:
#             # mido's API allows to copy a MIDI message
#             # changing only some of its parameters
#             # Here, we use the mapping dictionary to create
#             # the mapped note, keeping its properties like
#             # intensity

#             origin_note = msg.note

#             if origin_note in note_map:
#                 new_track.append( 
#                     msg.copy( note = note_map[origin_note]['target_note'] ))
#                 print(note_map[origin_note]['description'])
#             else:
#                 print("Origin note",origin_note,"not mapped")
#         else:
#             print(msg.type)
#             new_track.append(msg)

#     # MIDI files are multitrack. Here we append
#     # the new track with mapped notes to the output file
#     output_midi.tracks.append(new_track)

# # Finally, save the mapped file to disk
# output_midi.save('./Murundu-remap.mid')


