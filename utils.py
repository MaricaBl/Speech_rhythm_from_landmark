from classes import Landmark, VowelPeakLandmark, IntervalLandmark, IntervalVowelConsonant, RhythmStatistics, ValAnnotation, EvaluationMetrics
import numpy as np

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
"""
Semplice funzione che legge il file e ritorna la lista con tutte le righe
"""
def leggi_file(filename: str) -> list[str]:
    res=[]
    with open(filename) as f:
        for riga in f:
            res.append(riga)
    return res

"""
Crea la lista a partire dal file appena letto
"""
def create_list(my_data: list[str]) -> tuple[list[VowelPeakLandmark], list[Landmark]]:
    V_LM, l_intervals = [], []
    for riga in my_data:
        l = riga.split()
        if isfloat(l[1]):
            V_LM.append(VowelPeakLandmark(float(l[0]), float(l[1]), l[2]))
        else:
            l_intervals.append(Landmark(float(l[0]), l[1], l[2]))
    return V_LM, l_intervals

"""
Crea gli intervalli a partire dalla lista di Landmark
"""
def create_intervals(l_intervals: list[Landmark]) -> list[IntervalLandmark]:
    res = []
    i = 0
    len_intervals = len(l_intervals)
    while i < len_intervals:
        interval = IntervalLandmark([l_intervals[i]])
        i += 1
        while i < len_intervals and 'g' not in l_intervals[i].label:
            interval.addLandmark(l_intervals[i])
            i += 1
            if i == len_intervals - 1:
                break
        
        if i < len_intervals:
            interval.addLandmark(l_intervals[i])

        res.append(interval)

        if i == len_intervals - 1:
            break
    return res


"""
Controlla se negli intervalli e' contenuto un intervallo in V_LM
Serve per etichettare 'C' o 'V'
"""
def contains_V_LM(intervallo:IntervalLandmark, V_LM:list[VowelPeakLandmark]):
    for V in V_LM:
        if V.start >= intervallo.getStart() and V.end <= intervallo.getEnd():
            return True
    return False


"""
Etichetta l'intervallo come consonante ('C') o vocale ('V')

return: lista di liste con entry (inizio, fine, etichetta)

VOW_CON[i]['fine'] == VOW_CON[i+1]['inizio']
"""
def label_V_or_C(l:list[IntervalLandmark], V_LM:list[VowelPeakLandmark], time_silence:float=0.1) -> list[IntervalVowelConsonant]:
    VOW_CON=[]

    for intervallo in l:
        start = intervallo.getStart()
        end = intervallo.getEnd()
        tag = intervallo.landmarks[0].label  
              
        if tag == '+g':
            if contains_V_LM(intervallo, V_LM):
                isVowel= False
            else:
                isVowel= False
                for i in intervallo.landmarks: # look for an 's' or a 'v', if they are found, label as Consonant, otherwise label as Vowel
                    if 'v' in i.label or 's' in i.label:
                        isVowel= True
            if isVowel:
                VOW_CON.append(IntervalVowelConsonant(start, end, 'C'))
            else:
                VOW_CON.append(IntervalVowelConsonant(start, end, 'V'))
        elif tag == '-g':
            time = end - start
            if time < time_silence:
                VOW_CON.append(IntervalVowelConsonant(start, end, 'C'))
            else:
                VOW_CON.append(IntervalVowelConsonant(start, end, 'S'))
        else:
            VOW_CON.append(IntervalVowelConsonant(start, end, 'C'))
    return VOW_CON



"""
Calcola varie statistiche a partire dai label V or C della funzione label_V_or_C
"""
def calculate_stats(VOW_CON: list[IntervalVowelConsonant]) -> RhythmStatistics:
    stats = RhythmStatistics()
    # Percentuale tempo vocale
    tempo_totale = VOW_CON[-1].end - VOW_CON[0].start # Ultimo - primo
    tempo_vocale = sum([interv.getDuration() for interv in VOW_CON if interv.label == 'V'])
    percentage_V= 100 * tempo_vocale / tempo_totale

    # Deviazione standard di vocale e consonante
    durate_vocali = [interv.getDuration() for interv in VOW_CON if interv.label == 'V']
    durate_consonanti = [interv.getDuration() for interv in VOW_CON if interv.label == 'C']

    std_V = np.nanstd(durate_vocali)
    std_C = np.nanstd(durate_consonanti)

    # Coefficiente di variazione
    Varco_V = std_V / abs(np.nanmean(durate_vocali))
    Varco_C = std_C / abs(np.nanmean(durate_consonanti))


    # Pairwise Variability Index
    rPVI = 0
    nPVI = 0
    for k in range(len(durate_vocali) - 1):
        rPVI += abs(durate_vocali[k] - durate_vocali[k+1]) / (len(durate_vocali) - 1)
        nPVI += abs((durate_vocali[k] - durate_vocali[k+1])/((durate_vocali[k] + durate_vocali[k+1])/2))/(len(durate_vocali) - 1)
    
    i=0
    VtoV=[]
    while i < len(VOW_CON):
        if VOW_CON[i].label == 'V':
            VtoV_durata= VOW_CON[i+1].end - VOW_CON[i].start
            VtoV.append(VtoV_durata)

        i+=1
        if i == len(VOW_CON)-1: 
            break
    VtoV_mean= np.nanmean(VtoV)
    VtoV_std= np.nanstd(VtoV)
    Varco_VC = VtoV_std / abs(VtoV_mean)
    
    # Fill the RhythmStatistics object
    stats.percentage_V = percentage_V
    stats.std_V = std_V
    stats.std_C = std_C
    stats.Varco_V = Varco_V
    stats.Varco_C = Varco_C
    stats.rPVI = rPVI
    stats.nPVI = nPVI
    stats.VtoV_mean = VtoV_mean
    stats.VtoV_std = VtoV_std
    stats.Varco_VC = Varco_VC
    
    return stats


"""
Prende in input il file valutazione creato con leggi_file
"""
def create_list_VAL(my_data: list[str]) -> list[ValAnnotation]:
    result: list[ValAnnotation] = []
    for riga in my_data:
        l=riga.split()
        result.append(ValAnnotation(int(l[0]), int(l[1]), l[2]))
    return result


"""
Prende in input le annotazioni lette e il sampling rate e le trasforma in lista di oggetti IntervalVowelConsonant
"""
def label_intervals_VAL(annotations: list[ValAnnotation], sampling_rate: int = 22050) -> list[IntervalVowelConsonant]:
    result=[]

    for item in annotations:
        start = round(item.start_sample/sampling_rate, 4)
        end = round(item.end_sample/sampling_rate, 4)
        
        VOWELS = "AEIOUJWaeioujw" #in vowels we include semivowels: j, w
        found = False
        label = ''
        for v in VOWELS:
            if v in item.label:
                label = 'V'
                found = True
                break
        
        if not found:
            if '__' in item.label:
                label = 'S'
            else:
                label = 'C'
        
        result.append(IntervalVowelConsonant(start, end, label))
    
    return result


def merge_equal_interval(labels: list[IntervalVowelConsonant]) -> list[IntervalVowelConsonant]:   
    #merge adiacent intervals with the same label: 'C' 'C' or 'V' 'V' --> questa parte è da testare 
    res: list[IntervalVowelConsonant]=[]
    i = 0
    while i < len(labels)-1:         
        k = 0
        # Skips all the labels that are equals to the next one
        while  i+k+1 < len(labels) and labels[i].label == labels[i+k+1].label:
            k += 1
        if k > 0:
            res.append(IntervalVowelConsonant(labels[i].start, labels[i+k].end, labels[i].label))
            i += k
        else:
            res.append(IntervalVowelConsonant(labels[i].start, labels[i+k].end, labels[i].label))

        i += 1   
    return res 


"""
Differenzia i casi in cui c'è match solamente da un lato
"""
def get_matches(intervallo: IntervalVowelConsonant, labels: list[IntervalVowelConsonant], threshold: float = 0.02) -> tuple[bool, bool, IntervalVowelConsonant]:
    for i in labels:
        left_match = abs(i.start-intervallo.start) <= threshold
        right_match = abs(i.end-intervallo.end) <= threshold
        if left_match or right_match:
            return left_match, right_match, i
    
    return False, False, None

"""
Prende in input due liste di oggetti IntervalVowelConsonant e 
calcola le metriche di valutazione
"""
def evaluation_match(labels: list[IntervalVowelConsonant],
                     annotazioni: list[IntervalVowelConsonant],
                     threshold: float = 0.02) -> EvaluationMetrics:
    labelling_error = 0
    boundary_error = 0
    label_boundary_error = 0
    deletion = 0
    correct = 0

    for i in annotazioni:
        
        left_match, right_match, interval= get_matches(i, labels, threshold=threshold)
        
        # Both match
        if left_match and right_match:
            if i.label == interval.label:
                correct += 1
            else:
                labelling_error += 1
        elif right_match or left_match:
            # Only one match
            if i.label == interval.label:
                boundary_error += 1
            else:
                label_boundary_error += 1
        else:
            # No match
            deletion += 1

        # Delete interval from labels
        if not interval is None:
            labels.remove(interval)

         
    # I valori rimasti/non rimossi li conto come insertion
    insertion=len(labels) 
    error_tot=labelling_error+boundary_error+label_boundary_error+deletion+insertion
    target_tot=len(annotazioni)
    
    return EvaluationMetrics(labelling_error=labelling_error,
                             boundary_error=boundary_error,
                             label_boundary_error=label_boundary_error,
                             deletion=deletion,
                             insertion=insertion,
                             correct=correct,
                             error_tot=error_tot,
                             target_tot=target_tot)
