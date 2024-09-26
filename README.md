The present project's aim is to derive speech rhythm metrics directly from speech samples. In doing so a specilised software based on acoustic landmarks was used. 
 The original concept of acoustic landmark was theorised by the Speech and Communication Group at MIT back in th 90's (Stevens 1989, 2002).
 Acoustic landmarks are timestamp boundaries denoting sharp changes in speech articulation. 
 In fact, to the abrupt changes in the articulatory configuration correspond specific transitions between different types of sounds in the signal. 
 The landmarks are acoustic correlate of distinctive articulatory features. 

The patterns of acoustic landmarks therefore represent systematic effects of coarticulation, i.e., 
the timing among several articulatory movements to create a single constriction and overlapping moments that occur during sequences of constrictions.

The acoustic landmarks were extracted directly from the audio recordings by using a specilised software, SpeechMark (free toolbox on MATLAB). 
The python script available here derives the sequence of vocalic and consonantal intervals from the list of landmarks (extracted by SpeechMark). 
The rhythm metrics were the computed usign the vocalic and consonantal intervals duration. The rhyhtm metrics computed are the most used in the cross-linguistic studies and in the clinical literature.
The script performance was evaluated with the eval algorithm which is also available here. Data from an italian general speech corpus (CLIPS) was employed for the eval. 
The data in the eval-files folder is extracted from the same opensource corpus (CLIPS), which provides manual phonetic annotation. 
Thus, the manual annotation was used as a benchmark to test the landmark pipeline results.
