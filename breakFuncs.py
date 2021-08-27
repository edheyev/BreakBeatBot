import random, os
from pydub import AudioSegment

def genOrder(bars): # makes 2 sequences of length bars * 16, seq = order and eseq = effects
    seq = []#int numbers to choose file names must be 0-15
    eseq = []# types to add effects
    seqLen = 15 # breaks are cut into 16 parts
    for j in range(bars):
        for i in range(seqLen):
            ordering = random.randint(0,6) # this value chooses which  cut will be selected
            effect = random.randint(0,15)
            if ordering == 0: #repeat last
                seq.append(i-1);
            elif ordering == 1:# totally random
                seq.append(random.randint(0, seqLen));
    #        elif type == 2:# short burst of faster
    #            seq.append('s');
            else: # carry on with correct sequence
                seq.append(i);
            if effect == 0:
                eseq.append("slow")
            elif effect == 1:
                eseq.append("fast")
            elif effect == 2:
                eseq.append("stut")
            elif effect == 3:
                eseq.append("shot") # one shot
            else:
                eseq.append("_")

    return seq, eseq;


def makeBeat(seq, eseq): # converts sequence into sound by choosing folders and files
      speedFactor = 2.75
      print(seq);
      print(eseq);
      #get all sample folders
      breakFolders = fn("samples")
      #print(breakFolders)
      sFolder =  breakFolders[random.randint(0,len(breakFolders))-1] # choose random sample folder
      path = "samples/" + sFolder
      samples = fn(path)
      sPath = "samples/" + sFolder + "/" + samples[seq[0]];# initial sample
      combined_sounds = AudioSegment.from_wav(sPath) # manually initialise sound

      for i in range(len(seq)-1): # loop over sequence and choose audio files to splice
          if(random.uniform(0, 1)<0.01): # change sample folders - unlikely
              sFolder =  breakFolders[random.randint(0,len(breakFolders))-1]
              print(sFolder)
          sPath = "samples/" + sFolder + "/" + samples[seq[i]];
          thisSound = AudioSegment.from_wav(sPath)
          #apply effects
          if(eseq[i]=="slow"):
              thisSound = speed_change(thisSound, 1/2)
              i= i + 1
          elif(eseq[i]=="fast"):
              thisSound = speed_change(thisSound, 2)
              combined_sounds = combined_sounds + thisSound
          elif(eseq[i]=="stut"):
              thisSound = speed_change(thisSound, 4)
              combined_sounds = combined_sounds + thisSound
              combined_sounds = combined_sounds + thisSound
              combined_sounds = combined_sounds + thisSound
          elif(eseq[i] == "shot"):
              tpath = "OneShots/"
              tsamples = fn(tpath)
              tsPath = "OneShots/"+ tsamples[0]
              thisSound = AudioSegment.from_wav(tsPath)
              i=i+1


              #thisSound = speed_change(thisSound, speedFactor)

          combined_sounds = combined_sounds + thisSound # combine samples
      fast_sound = speed_change(combined_sounds, speedFactor)# change speed for DnB
      fast_sound.export("joinedFile.wav", format="wav")#export as wav




def fn(path):       # Get file names from directory
    return os.listdir(path)

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. They often only
     # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
