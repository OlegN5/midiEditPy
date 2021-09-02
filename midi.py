import mido

class myMidi():
    def __init__(self, midiFile):
        self.midiFile = mido.MidiFile(midiFile, clip=True)
        self.notes = 0
        self.lyrics = 0

    def midiLen(self):
        return mido.MidiFile.length
     
    def findTempo250(self):
        for msg in self.midiFile:     # Search for tempo
            if msg.type == 'set_tempo':
                if mido.tempo2bpm(msg.tempo) > 250:
                    print (f'в миди файле темп более чем 250!!!')
    
    def coutNotesLyrics(self):
        for msg in self.midiFile.tracks[1]:
            if msg.type == 'note_on' and msg.velocity > 0: 
                # print(msg)
                self.notes+=1
            if msg.type == 'lyrics' and msg.text != '\n' and msg.text != '\r' and msg.text != ' ' and msg.text != '': 
                # print(msg)
                self.lyrics+=1
        if self.notes != self.lyrics:
            print ("В исходном мидифайле количество нот не совпадает с количеством слогов.")

    def addTrackWithMyFormatLyric(self, LyricSlogi):
        track1 = mido.MidiTrack()
        lTime=0
        for msg in self.midiFile.tracks[1]:
            if lTime!=0:
                msg.time+=lTime
                lTime=0
            if msg.type != 'lyrics':
                track1.append(msg)
            if msg.type == 'lyrics':
                if msg.time > 0:
                    lTime = msg.time      
        self.midiFile.tracks.append(track1)
        self.midiFile.tracks.remove(self.midiFile.tracks[1])    

        track2 = mido.MidiTrack()
        i=0
        # print (LyricSlogi)
        for msg in self.midiFile.tracks[2]:
            if msg.type != 'lyrics':
                track2.append(msg)
            if msg.type == 'note_on' and msg.velocity > 0:
                if LyricSlogi[i] != '*':###
                    if (LyricSlogi[i][-1:] == '\n'):
                        track2.append(mido.MetaMessage('lyrics', text=LyricSlogi[i][:-1]+' ', time=0))
                        track2.append(mido.MetaMessage('lyrics', text=LyricSlogi[i][-1:], time=0))
                    else:
                        track2.append(mido.MetaMessage('lyrics', text=LyricSlogi[i], time=0))

                if i < len(LyricSlogi)-1:
                    if LyricSlogi[i+1]=='\n' or LyricSlogi[i+1]=='\r':
                        i+=1
                        track2.append(mido.MetaMessage('lyrics', text=LyricSlogi[i], time=0))
                i+=1  
                if i == len(LyricSlogi): 

                    break

        self.midiFile.tracks.append(track2)
        self.midiFile.tracks.remove(self.midiFile.tracks[1])

    def midiSave(self, s4et, path0, fName):
        if self.notes==s4et:
            self.midiFile.save(path0 + 'render/' + fName + '_0128.mid')
        else:
            self.midiFile.save(path0 + fName + '_NOT_OK.mid')                
        
   


    
    

