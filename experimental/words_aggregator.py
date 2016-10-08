# ~ Andrew
from TimeStamp import TimeStamp
import os

# To be called manually to change the database
# Adds the timestamp information to /{person}/{word}.txt
# Please ensure that person contains no spaces (use underscores), and both
# person and word are lowercase
# add_word_to_db("donald_trump", "china", ts)
def add_word_to_db(person, word, timestamp):
    assert type(timestamp) == TimeStamp
    assert person == person.lower() and word == word.lower()
    assert person.find(" ") == -1
    if not os.path.exists("data/"+person+"/"):
        os.makedirs("data/"+person+"/")
    outf = open("data/"+person + "/" + word + ".txt", "a")
    outf.write(timestamp.toString() + "\n")
    outf.close()


