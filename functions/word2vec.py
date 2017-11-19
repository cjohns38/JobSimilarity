import gensim
import pandas as pd
import numpy as np

def createRIASEC(data): 
    """ Returns a RIASEC code with up to three letters. Example: RIA  
        RIASEC code created by taking the first letter of the First, Second, and Third High-Point code.
        
        NOTES: 
            * Reqiures O*NET Database Column Names 'First Interest High-Point', 'Second Interest High-Point', 
              'Third Interest High-Point'
            * The actual RIASEC code length will vary between one and three letters depending on if the 
              job had codes which reached the threshold.  
        
        Keyword arguments:
        data : Pandas ROW (series)
    """
    columns = [data['First Interest High-Point'], 
               data['Second Interest High-Point'], 
               data['Third Interest High-Point']
              ]
    
    dataOut = [x[0] for x in columns if x != None]
    return ''.join(dataOut)


def preprocessText(txt, stopwords): 
    """Returns a list of words after running text string through gensims simple preprocess and removing stopwords. 
    
    Keyword arguments:
    txt : String of text you wish to preprocess
    stopwords: List of words you wish to remove from string
    
    """
    
    stopwords = stopwords
    txt = gensim.utils.simple_preprocess(txt)
    return  [word for word in txt if word not in stopwords]

def average_word_embedding(data, model, keyed = False): 
    """Return a series of the average word embedding
    
    Keyword arguments: 
    data : Pandas or numpy series 
    model: gensim model 
    keyed: If True the function will use a KeyedVectors instance common for 
           other training such as Fastext, WordRank, or VarEmbed. If False 
           the function will use a keyed format.   
           
    NOTE: Returned variables are labled starting with d0 and running through the length of the dimentions 
    """
    
    out = []
    
    # Handle keyed vectors 
    if keyed == True: 
        find_vector = lambda word: model.word_vec(word)
    else: 
        find_vector = lambda word: model.wv[word]
        
    # Loop through 
    for word in data: 
        if word in model:
            out.append(find_vector(word))
    
    # calculate average 
    avg = np.average(np.array(out), axis = 0)
    return pd.Series({'d' + str(idx):x for idx, x in enumerate(avg)})

def cosine_similarity(target_vector, row): 
    """Returns the cosine similarity 
       Reference: https://en.wikipedia.org/wiki/Cosine_similarity
       
       Keyword arguments
       target_vector: A Pandas or numpy series representing a single case of interest 
       row: row of interest 
   
    """
    
    job1 = target_vector
    job2 = row.loc['d0':].values
    numerator = np.dot(job1,job2)
    denominator = np.sqrt(np.sum(job1**2)) * np.sqrt(np.sum(job2**2))
    return pd.Series([numerator/denominator])

def find_jobs(data, soc, topN, bottomN): 
    """ Given the O*NET code print the most and least similar jobs
    
        Keyword arguments
        data: Pandas dataframe 
        soc: O*NET SOC code 
        topN: Number of top results you wish returned
        bottomN: Number of bottom results you wish returned 
    
    """

    # Create a DF of the target and non-target jobs
    target = data[data['onetsoc_code'] == soc]
    df = data[data['onetsoc_code'] != soc]

    # Create target vector 
    target_vector = data[data['onetsoc_code'] == soc].loc[:, 'd0':].values[0]

    # Run similarities 
    s = df.apply(lambda x: cosine_similarity(target_vector, x), axis = 1)
    df = df.assign(similarity = s)

    # Sort the values 
    df.sort_values(by = 'similarity', ascending = False, inplace = True)

    # Print the top N 
    top = df[['title', 'similarity', 'riasec', 'onetsoc_code']].head(topN).values.tolist()

    # Print the bottom N 
    bottom = df[['title', 'similarity', 'riasec', 'onetsoc_code']].tail(bottomN).values.tolist()

    # Top 
    print("The most similiar jobs are...".format(target['title'].values[0]))
    for job in top: 
        print("\t {0}; cosine:{1:.2f}; O*NET:{2}; Holland code:{3}".format(job[0], job[1], job[3], job[2]))

    # Bottom 
    print("The least similar jobs are...")
    for job in bottom: 
        print("\t {0}; cosine:{1:.2f}; O*NET:{2}; Holland code:{3}".format(job[0], job[1], job[3], job[2]))


def model_comparison(data1, data2, soc): 
    """ Returns a dictionary of data frames after calculating the cosine similarity.  
        
        Keyword arguments
        data1: Pandas dataframe 1
        data2: Pandas dataframe 2 
        soc: O*NET soc code of interest 
    
    """
    
        
    
    def calc(data, soc):
        """ Return a dataframe of sorted jobs 
            
            Keyword arguments
            data: Pandas dataframe of interest
            soc: O*NET soc code of interest 
        
        """
        # Create a DF of the target and non-target jobs
        target = data[data['onetsoc_code'] == soc]
        df = data[data['onetsoc_code'] != soc]

        # Create target vector 
        target_vector = data[data['onetsoc_code'] == soc].loc[:, 'd0':].values[0]

        # Run similarities 
        s = df.apply(lambda x: cosine_similarity(target_vector, x), axis = 1)
        df = df.assign(similarity = s)

        # Sort the values 
        df.sort_values(by = 'similarity', ascending = False, inplace = True)

        return df
    
    out = {'data1':calc(data1, soc), 'data2':calc(data2, soc)}
    
    return out

def listcomparision(l1, l2): 
    """ Return the percentage of similar items between two lists 
    
        Keyword arguements 
        l1: List1 for comparison 
        l2: List2 for comparison
    
    """
    total_common_elements = len(set(l1) & set(l2)) * 2
    total_elements = len(l1) + len(l2)
    percent_agreement = total_common_elements / total_elements * 100
    return percent_agreement
