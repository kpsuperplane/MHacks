import os, wave
# Concats a list of .wav file paths and produces a new .wav file
# Make sure all .wav files have the same params

# i.e. concat(['words/hi/0.wav'])
def concat(wav_file_paths,out_path):
    data = []
    for path in wav_file_paths:
        if os.path.isfile(path):
            w = wave.open(path, 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
    output = wave.open(out_path,'wb')
    output.setparams(data[0][0])
    for datum in data:
        output.writeframes(datum[1])
    output.close()
