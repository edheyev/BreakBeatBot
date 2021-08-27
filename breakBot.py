from breakFuncs import genOrder, makeBeat

seq, eseq = genOrder(8) # makes a sequence of numbers and letters- n bars of 16th notes

makeBeat(seq, eseq) # convert sequence into audiofile and save
