#!/usr/bin/env python

r"""Auto-Correct Suggestor Implemented in a Tree Dictionary - a Trie

The Dictionary Trie stores (word, frequency) pairs in a Trie:

                 ''  (Root node = empty string)
              /    \
              h      a ('a', 17)
            /   \
 ('he',13) e     i ('Hi', 7)
                /  \
     ('him',8) m    l
                     \
                      l ('hill', 2)

It can very rapidly find all the words in the tree within a specified edit distance of a query string.
    Edit Distance = # of edits need to manipulate the query into a word.
    1 Edit = removing/adding a single character from query string OR changing a single character in the string to another character.


A query (such as 'hikl') is pushed down the tree.
As we decend the Trie, we edit the query as needed to match the path of the Trie we are decending.
Each traversal keeps track of the how many edits have been used so far
    If a traversal has used too many edits, that traversal ends
    If we arrive at word and we have matched or edited ALL of the characters in the query, we suggest the word in the Trie.

For example, if query = 'hikl', we could arrive at the "him"-node in multiple ways-

      add 'm' at query[2]                 ==>     query = 'himkl', edits used = 1
      change 'k' for 'm'                  ==>     query = 'himl', edits used = 1
      change 'k' for 'm' AND remove 'l'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)
      remove 'k' AND change 'l' for 'm'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)

As we can see, some combinations of actions are equivalent. 
The DictionaryTree.findAll() method is implemented to reduce - not eliminate - these repetitions.
    Adding complexity to further reduce repeated work has only resulted in longer overall runtime.
    Thus, it is necessary for the Trie to remove any duplicate suggestions.
"""

__author__ = "Leo Rossignac-Milon"
__email__ = "leo.milon@gmail.com"


#ACTIONS
REMOVE=-1
ADD=1
SAME=0
CHANGE=2
START=3



#Dictionary Trie as described above
class Trie:

    def __init__(self):
        self.root = LetterNode('')

    #Add a word and its freuquency to dictionary
    def insert(self, word, freq):
        self.root.insert(word, freq , 0)

    #Returns a sorted unique list of all words in the dictionary with a distance to query <= maxDistance
    def findAll(self, query, maxDistance):
        suggestions= self.root.recommend(query.lower(), maxDistance, START) 
        return sorted(set(suggestions), key=lambda x: x.freq)



#A node in a dictionary tree is a letter
#Leaf nodes and some intermediary nodes represent Words
#For speed, all letters are lowercased when inserting a word into a tree
class LetterNode:

    def __init__(self, char):
        self.pointers=[] #the list of children nodes (the next chars in a word from the frequency data)
        self.char=char
        self.word=None

    def charIs(self, c):
        return self.char==c

    def insert(self, word, freq, depth):
        if (depth<len(word)):
            #we need to continue down the tree
            c = word[depth].lower()
            for next in self.pointers:
                if (next.charIs(c)):
                    return next.insert(word, freq, depth+1)
            #we havent found the pointer, start a new branch in dictionary tree
            nextNode = LetterNode(c)
            self.pointers.append(nextNode)
            return nextNode.insert(word, freq, depth+1)
        #we've made it to our end node
        else:
            self.word=Word(word,freq)

    # As we decend the Trie, we edit the query as needed to match the path of the Trie we are decending.
    # Each traversal keeps track of the how many edits have been used so far
    #     If a traversal has used too many edits, that traversal ends
    #     If we arrive at word and we have matched or edited ALL of the characters in the query, we suggest the word in the Trie.
    #Due to the fact that some combinations of actions are equivalent, this function will lead to few repeated recommendations (which are removed later on)
    def recommend(self, query, movesLeft, lastAction):
        suggestions = []
        length = len(query)

        #BASE CASE (includes pruning tail-end of query)
        if (length>=0 and movesLeft-length>=0 and self.word):
            suggestions.append(self.word)

        #NO MOVES LEFT (just follow trie until no longer possible)
        if (movesLeft==0 and length>0):
            for next in self.pointers:
                if (next.charIs(query[0]) ):
                    suggestions+= next.recommend(query[1:], movesLeft, SAME)
                    break

        #CONTINUE TRAVERSAL
        #To eliminate most commutative pairs of moves:
            #we will not REMOVE after (ADD | CHANGE)
            #we will not ADD after (REMOVE | CHANGE)
        elif (movesLeft>0):
            for next in self.pointers:

                if (length>0):
                #some moves (change, remove, or none) can only be completed if not at end of word

                    if (next.charIs(query[0]) ): 
                    #no action used
                        suggestions+=next.recommend(query[1:], movesLeft, SAME) 
                    
                    else:
                    #the next node is achievable through VARIOUS actions
                        #CHANGE next char to match next node is always an option
                        suggestions+=next.recommend(query[1:], movesLeft-1, CHANGE) 
                        #ADD the missing char to the query if possible
                        if (lastAction!=CHANGE and lastAction!=REMOVE):
                            suggestions+=next.recommend(query, movesLeft-1, ADD)
                        #REMOVE the unmatched char to the query if possible
                        if (lastAction!=ADD and lastAction!=CHANGE):
                            if (length>1 and next.charIs(query[1])):
                                suggestions+=next.recommend(query[2:], movesLeft-1, REMOVE) #removed 1 char
                            elif (length>2 and next.charIs(query[2]) and movesLeft==2):
                                suggestions+=next.recommend(query[3:], movesLeft-2, REMOVE) #removed 2 chars

                else:
                # we have reached the end of the query, but we can still add chars to reach the end of the word
                    if (lastAction!=CHANGE and lastAction!=REMOVE):
                        suggestions+=next.recommend(query, movesLeft-1, ADD) 
        return suggestions



#A word suggestion (with real capitalization) to be held by a node in the dictionary
class Word:

    def __init__(self, word, freq):
        self.word=word #recomendation
        self.freq=freq #frequency