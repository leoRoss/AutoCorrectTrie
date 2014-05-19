AUTO-CORRECT SUGGESTOR --- IMPLEMENTED IN A TREE DICTIONARY

WHAT?

Store (word, frequency) pairs in a Trie:

                 ''  (Root node = empty string)
               /    \
              h      a ('a', 17)
            /   \
 ("he",13) e     i ("Hi", 7)
                /  \
     ("him",8) m    l
                     \
                      l ("hill", 2)

Very rapidly finds all words in the tree within a specified edit distance of a query
Distance =  of removals, additions, or character changes need to manipulate the word into the query

HOW?

A query (such as 'hikl') is pushed down the tree
As we decend the tree, we edit the start of the query to match the chosen path
Each traversal keeps track of the how many edits have been used so far
When too many edits were used, that traversal ends
If we reach the end of a query and arrive at suggestion, we suggest it!

For example, if query = 'hikl', we could arrive at the "him"-node in multiple ways:

       add 'm' at query[2]                 ==>     query = 'himkl', edits used = 1
       change 'k' for 'm'                  ==>     query = 'himl', edits used = 1
       change 'k' for 'm' AND remove 'l'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)
       remove 'k' AND change 'l' for 'm'   ==>     query = 'him', edit used = 2 (Return "him" as a suggestion)

As we can see, some combinations of actions are equivalent. The findAll() method is implemented to reduce - not eliminate - these repetitions.Adding complexity to further reduce repeated work has only resulted in longer overall runtime.


TO RUN:
cd DictionaryTree
python main.py
