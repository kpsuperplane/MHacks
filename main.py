from src import generator, editor

editor.combineAudio(generator.generateFromText("The vocabulary of this sentence contains an abundance of rarely used words phrases and can paraphrase sentences in a variety of ways that are chosen randomly", "speech/trump.pickle"), "test.wav")