# Film Color Search Engine
*(Separate instance of Bucknell film color search. Will merge when product is closer to completion)*

### Steps to complete the search engine
**1. Scene detect** 

A python scene detect package is used to slice film or videos into a series of scenes. 
Each scene contains 

    1.1 One picture representing the color distribution of this scene
    1.2 The basic film info
    1.3 Time period of this scene

**2. K-Mean Cluster**

Pre-process pictures with `sklearn`, `opencv` with K-mean cluster method. (Considering using AWS).
Each output of a picture is a list of dominant colors contains
    
    2.1 RGB color
    2.2 Percentage this RGB

**3. N-Array Tree**

Color-distribution-oriented N-array tree will be used as the main data structure for the search.
Factors under consideration:

    3.1 Color dominance ranking
    3.2 

**4. Pictures for search** 

Basic steps for searching:

1. Users are allowed to upload one pictures. 
2. We will use the same machine learning method in pre-processing step to process the image.
(use `sklearn` and `opencv` package) 
3. Search the image in our database
4. Generate the clips and relevant film information according to the search result.