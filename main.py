from src import generator, editor

editor.combineAudio(generator.generateFromText("Did you know that the american population is pretty beautiful", "test/trump.pickle"), "test.wav")