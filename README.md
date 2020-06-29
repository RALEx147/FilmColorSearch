# Film Color Search Engine
*(Separate instance of Bucknell film color search. Will merge when product is closer to completion)*

## 1. Scene detect

#### What does it do?
A python scene detect package is used to slice film or videos into a series of scenes. 

Each scene contains:
1. One picture representing the color distribution of this scene
2. The basic film info
3. Time period of this scene

#### When to use?

Originally, we have a film database. Now, we use scene detect to process each film into 
pieces of scenes and generate a picture represent this scene's color distribution.

## 2. K-Mean Cluster

#### What does it do?
Pre-process pictures with `sklearn`, `opencv` with K-mean cluster method. (Considering using AWS).

Each output of a picture is a list of dominant colors contains
    
1. RGB color
2. Percentage this RGB

#### When to use?
K-mean cluster will be used in 2 places:
1. It will be used to analyze pictures representing scenes of the film and generate the color distribution.
The color distribution of these pictures will stored as an object pickled locally and the pickle file 
will be the database for the search engine.
2. It will be used to process image uploaded by users. It will generate the color distribution information 
so that engine will compare with other images information in our database.

## 3. Parallel Search

#### What does it do?
Parallel search uses the python multi-thread library `Pool` to process the image search quickly

#### When to use?
Parallel search is used after we obtain the color distribution information from user, we use it to compare
those images in our database.

## 4. General steps for searching:

1. Users are allowed to upload one pictures. 
2. We will use the same machine learning method in pre-processing step to process the image.
(use `sklearn` and `opencv` package) 
3. Search the image in our database
4. Generate the clips and relevant film information according to the search result.