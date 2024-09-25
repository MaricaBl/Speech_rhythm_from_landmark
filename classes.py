class VowelPeakLandmark():
    """
    A class to represent a vowel peak landmark.
    It's composed of a start and end time, and a label.
    Example:
    1.06 1.132 V
    1.196 1.277 V
    1.393 1.439 V
    """
    def __init__(self, start:float, end:float, label:str):
        self.start = start
        self.end = end
        self.label = label.strip()
        
class ValAnnotation():
    """
    A class to represent a VAL annotation.
    It's composed of a start sample, an end sample and a label.
    Example:
    26443 28532 ddz
    """
    def __init__(self, start_sample:int, end_sample:int, label:str):
        self.start_sample = start_sample
        self.end_sample = end_sample
        self.label = label.strip()
        
class Landmark():
    """
    A class to represent a landmark.
    It's composed of a start time, a label and a probability.
    Example:
    1.019 +b 0.89316
    1.06 +g 1
    1.06 +p 1
    """
    def __init__(self, timestamp:float, label:str, probability:float):
        self.timestamp = timestamp
        self.label = label.strip()
        self.probability = probability
        
        
class IntervalLandmark():
    """
    A class to represent an interval.
    An interval is defined as a list of landmarks. 
    """        
    def __init__(self, landmarks: list[Landmark]):
        self.landmarks = landmarks
    
    def getStart(self):
        return self.landmarks[0].timestamp
    
    def getEnd(self):
        return self.landmarks[-1].timestamp
    
    def addLandmark(self, landmark: Landmark):
        self.landmarks.append(landmark)
        
class IntervalVowelConsonant():
    """
    A class to represent a VowelConsonant interval.
    It is defined as (start, end, label)
    """
    def __init__(self, start: float, end: float, label: str):
        self.start = start
        self.end = end
        self.label = label.strip()
        
        if self.label not in ['V', 'C', 'S']:
            raise ValueError("The label must be either 'V' or 'C' or 'S'")
        
    def getDuration(self):
        return self.end - self.start
    
    
"""
List of calculated statistics for the rhythm
- percentage_V: percentage of Vowel intervals
- std_V: standard deviation of Vowel intervals
- std_C: standard deviation of Consonant intervals
- Varco_V: variation coefficient of Vowel intervals
- Varco_C: variation coefficient of Consonant intervals
- rPVI: relative PVI (Pairwise Variability Index)
- nPVI: normalized PVI (Pairwise Variability Index)
- VtoV_mean: mean of Vowel to Vowel intervals
- VtoV_std: standard deviation of Vowel to Vowel intervals
- Varco_VC: variation coefficient of Vowel and adjacent Consonant intervals
"""
class RhythmStatistics():
    def __init__(self, percentage_V=None, std_V=None, std_C=None, Varco_V=None, Varco_C=None, rPVI=None, nPVI=None, VtoV_mean=None, VtoV_std=None, Varco_VC=None):
        self.percentage_V = percentage_V
        self.std_V = std_V
        self.std_C = std_C
        self.Varco_V = Varco_V
        self.Varco_C = Varco_C
        self.rPVI = rPVI
        self.nPVI = nPVI
        self.VtoV_mean = VtoV_mean
        self.VtoV_std = VtoV_std
        self.Varco_VC = Varco_VC
    
    def __str__(self):
        return f"Percentage of Vowel intervals: {self.percentage_V}\n" \
                f"Standard deviation of Vowel intervals: {self.std_V}\n" \
                f"Standard deviation of Consonant intervals: {self.std_C}\n" \
                f"Variation coefficient of Vowel intervals: {self.Varco_V}\n" \
                f"Variation coefficient of Consonant intervals: {self.Varco_C}\n" \
                f"Relative PVI: {self.rPVI}\n" \
                f"Normalized PVI: {self.nPVI}\n" \
                f"Mean of Vowel to Vowel intervals: {self.VtoV_mean}\n" \
                f"Standard deviation of Vowel to Vowel intervals: {self.VtoV_std}\n" \
                f"Variation coefficient of Vowel and adjacent Consonant intervals: {self.Varco_VC}"


"""
List of calculated metrics for the evaluation:
- labelling_error: correct boundaries, wrong label
- boundary_error: one of the boundaries is wrong, correct label
- label_boundary_error: one of the boundaries is wrong, wrong label
- deletion: present in annotations but missing in output
- insertion: present in output but missing in annotations 
- correct: correct boundaries, correct label
- error_tot: labelling_error + boundary_error + label_boundary_error + deletion + insertion
- target_tot: total number of boundaries in annotations
"""        
class EvaluationMetrics():
    def __init__(self, labelling_error: int, boundary_error: int, label_boundary_error: int, deletion: int, insertion: int, correct: int, error_tot: int, target_tot: int):
        self.labelling_error = labelling_error
        self.boundary_error = boundary_error
        self.label_boundary_error = label_boundary_error
        self.deletion = deletion
        self.insertion = insertion
        self.correct = correct
        self.error_tot = error_tot
        self.target_tot = target_tot
        
        assert self.error_tot == self.labelling_error + self.boundary_error + self.label_boundary_error + self.deletion + self.insertion
        
    def __str__(self):
        return f"Labelling error: {self.labelling_error}\n" \
                f"Boundary error: {self.boundary_error}\n" \
                f"Label boundary error: {self.label_boundary_error}\n" \
                f"Deletion: {self.deletion}\n" \
                f"Insertion: {self.insertion}\n" \
                f"Correct: {self.correct}\n" \
                f"Error total: {self.error_tot}\n"