from mido import MidiFile

mid = MidiFile('00005902.mid', clip=True)
# print(mid)

for track in mid.tracks:
    print(track)

# print(mid.tracks[0])

for msg in mid.tracks[1]:
    if msg.time != 0:
        if msg.type == 'lyrics': print(msg)






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