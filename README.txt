AUTO-CORRECT SUGGESTOR --- IMPLEMENTED IN A TREE DICTIONARY


WHAT?

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


HOW?

A query (such as 'hikl') is pushed down the tree.
As we decend the Trie, we edit the query as needed to match the path of the Trie we are decending.
Each traversal keeps track of the how many edits have been used so far
    If a traversal has used too many edits, that traversal ends
    If we arrive at word and we have matched or edited ALL of the characters in the query, we suggest the word in the Trie!

For example, if query = 'hikl', we could arrive at the "him"-node in multiple ways-

      add 'm' at query[2]                 ==>     query = 'himkl', edits used = 1
      change 'k' for 'm'                  ==>     query = 'himl', edits used = 1
      change 'k' for 'm' AND remove 'l'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)
      remove 'k' AND change 'l' for 'm'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)

As we can see, some combinations of actions are equivalent. 
The DictionaryTree.findAll() method is implemented to reduce - not eliminate - these repetitions.
    Adding complexity to further reduce repeated work has only resulted in longer overall runtime.
    Thus, it is necessary for the Trie to remove any duplicate suggestions.


TO RUN:

      cd DictionaryTree
      python main.py
