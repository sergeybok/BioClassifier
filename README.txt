The program is compiled with the cmd: python hw4.py [corpus.txt] [parameter N]
where N is a number greater than 0.

I used the algorithm Prof Davis suggested in the homework description, so as N increases 
the amount of clusters increases as well, because there's less viable edges. 

The titles of clusters were chosen by choosing the word with the biggest weight 
from the shared words in the cluster. (Ties are broken randomly i.e.first one that 
comes up gets chosen.

Thoughts:
For the sample corpus I get best results with N>10, otherwise I get one huge cluster.
It also doesn't cluster people I think should be clustered and I've tried 
to improve the algorithm by 1) only using the first line of the bio 
(because those seemed like the most important words) and
2) assigning more weight to the first 4 contentive words of the bio 
(for same reason), but my results didn't improve at all so I just reverted 
back to the original algorithm.