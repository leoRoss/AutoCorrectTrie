#Leo Rossignac-Milon

import csv, datetime
from DictionaryTree import Trie

#Builds the tree using all recommended words in a csv file where each line is word,frequency
def buildTrieFromFile(recommendedFilePath, trie):
    start = datetime.datetime.now()
    recommendFile= open(recommendedFilePath, 'r');
    try:
        recommendReader = csv.reader(recommendFile, delimiter=',')
        for row in recommendReader:
            trie.insert(row[0],int(row[1]))
    finally:
        recommendFile.close()
    end = datetime.datetime.now()
    print "\nTime taken to build Dictionary Tree: " + str(end-start) + "\n"
 
#Returns string of a list of unqiue recommendations sorted on frequency
def getSuggestionString(word, trie, maxDistance):
    start = datetime.datetime.now()
    suggestions = trie.findAll(word, maxDistance)
    end = datetime.datetime.now()
    return ''.join(map(lambda x: str(x.word) +' ', suggestions)) + "\nTime Taken: " + str(end-start) + "\n"


#Suggest words based on input till killed
def suggestorIO (trie):
    while (True):
        request = raw_input("Enter word & search distance (ex:'helllo 2'): ")
        try:
            rsplit = request.split(' ')
            print getSuggestionString(rsplit[0], trie, int(rsplit[1]))
        except:
            print "Please try again...\n"

def main():
    #BUILD TREE
    myTrie=Trie()
    buildTrieFromFile('word_frequency.csv', myTrie)
    
    #SUGGEST TILL QUIT
    suggestorIO(myTrie)

if __name__ == "__main__":
    main()