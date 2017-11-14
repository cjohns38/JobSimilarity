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

def riasecSplit(data): 
    """ Takes a RIASEC code and returns a series with the First, Second, and Third RIASEC code letters.
    
        Keyword arguments: 
        data : Pandas ROW (series)
    """
    dataOut = [True  if x in data['riasec'] else False for x in riasecCode]
    return pd.Series(dataOut)


def preprocessText(txt, stopwords): 
    """Use gensim simple preprocess and remove stopwords"""
    stopwords = stopwords
    txt = gensim.utils.simple_preprocess(txt)
    return  [word for word in txt if word not in stopwords]

def average_word_embedding(data, model, keyed = False): 
    """Return the average word embedding"""
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
    """Determine the cosine similarity"""
    job1 = target_vector
    job2 = row.loc['d0':].values
    numerator = np.dot(job1,job2)
    denominator = np.sqrt(np.sum(job1**2)) * np.sqrt(np.sum(job2**2))
    return pd.Series([numerator/denominator])

def find_jobs(data, soc, topN, bottomN): 
    """ Given the ONET job DF and a SOC code find the top and bottom similar jobs """

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
    top = df[['title', 'similarity']].head(topN).values.tolist()

    # Print the bottom N 
    bottom = df[['title', 'similarity']].tail(bottomN).values.tolist()

    # Print results 
    print("For the job of {0}...".format(target['title'].values[0]))

    # Top 
    print("The most similiar jobs are...".format(target['title'].values[0]))
    for job in top: 
        print("\t {0}".format(job[0]))

    # Bottom 
    print("The least similar jobs are...")
    for job in bottom: 
        print('\t {0}'.format(job[0]))


def model_comparison(data1, data2, soc): 
    """ Given two dataframes using diffferent modesl see show similar they are """
    
    def calc(data, soc):
        """ Return the top and bottom most similiar jobs"""
        # Create a DF of the target and non-target jobs
        target = data[data['soc'] == soc]
        df = data[data['soc'] != soc]

        # Create target vector 
        target_vector = data[data['soc'] == soc].loc[:, 'd0':].values[0]

        # Run similarities 
        s = df.apply(lambda x: cosine_similarity(target_vector, x), axis = 1)
        df = df.assign(similarity = s)

        # Sort the values 
        df.sort_values(by = 'similarity', ascending = False, inplace = True)

        return df
    
    out = {'data1':calc(data1, soc), 'data2':calc(data2, soc)}
    
    return out

def listcomparision(list1, list2): 
    """ Determine the similarity between two lists"""
    return len(set(list1) & set(list2)) / float(len(set(list1) | set(list2))) * 100
