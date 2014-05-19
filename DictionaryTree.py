#Leo Rossignac-Milon
#Auto-Correct Suggestor Implemented in a Tree Dictionary - a Trie

#Very rapidly finds all suggested words within a desired distance of a query
#Distance = # of removals, additions, or character changes need

# (Word, frequency) suggestion pairs are added to the tree
#
#                 ''  (Root node = empty string)
#               /    \
#              h      a ('a', 17)
#            /   \
# ("he",13) e     i ("Hi", 7)
#                /  \
#     ("him",8) m    l
#                     \
#                      l ("hill", 2)

#A query (such as 'hikl') is pushed down the tree
#As we decend the tree, we edit the start of the query to match the chosen path
#Each traversal keeps track of the how many edits have been used so far
#When too many edits were used, that traversal ends
#If we reach the end of a query and arrive at suggestion, we suggest it!

#For example, if query = 'hikl', we could arrive at the "him"-node in multiple ways:

#       add 'm' at query[2]                 ==>     query = 'himkl', edits used = 1
#       change 'k' for 'm'                  ==>     query = 'himl', edits used = 1
#       change 'k' for 'm' AND remove 'l'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)
#       remove 'k' AND change 'l' for 'm'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)

#As we can see, some combinations of actions are equivalent. 
#The findAll() method is implemented to reduce - not eliminate - these repetitions.
#Adding complexity to further reduce repeated work has only resulted in longer overall runtime.



#ACTIONS
REMOVE=-1
ADD=1
SAME=0
CHANGE=2
START=3



#Dictionary Tree as described above
class Trie:
    def __init__(self):
        self.root = LetterNode('')

    #Add a word and its freuquency to dictionary
    def insert(self, recommendation, freq):
        self.root.insert(recommendation, freq , 0)

    #Returns a sorted unique list of all words in the dictionary with a distance to query <= maxDistance
    def findAll(self, query, maxDistance):
        suggestions= self.root.recommend(query.lower(), maxDistance, START) 
        return sorted(set(suggestions), key=lambda x: x.freq)



#A node in a dictionary tree is a letter
#Leaf nodes and some intermediary nodes represent Words
#For speed, all letters are lowercased when inserting a word into a tree
class LetterNode(object):

    def __init__(self, char):
        self.pointers=[] #the list of children nodes (the next chars in a word from the frequency data)
        self.char=char
        self.word=None

    def charIs(self, c):
        return self.char==c

    def insert(self, recommendation, freq, depth):
        if (depth<len(recommendation)):
            #we need to continue down the tree
            c = recommendation[depth].lower()
            for next in self.pointers:
                if (next.charIs(c)):
                    return next.insert(recommendation, freq, depth+1)
            #we havent found the pointer, start a new branch in dictionary tree
            nextNode = LetterNode(c)
            self.pointers.append(nextNode)
            return nextNode.insert(recommendation, freq, depth+1)
        #we've made it to our end node
        else:
            self.word=Word(recommendation,freq)
    
    #Traverse the dictionary tree in 2-step legal manner - keeping track of how many edits we have performed on the query so far
    #If a word is encountered at the end of a traversal, return it!
    #Due to the fact that some combinations of actions are equivalent, this function will lead to few repeated recommendations
    #Optimizing by further reducing equivalent paths has lead to increased complexity and poorer overall runtime
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
class Word(object):
    def __init__(self, word, freq):
        self.word=word #recomendation
        self.freq=freq #frequency