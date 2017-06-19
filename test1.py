from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter
from nltk import ngrams
import nltk
from nltk.corpus import stopwords
from informationRetrieval import feature_names


def makeArray():
    corpus = [];
    
    sentence1 = "Narrator: What was I doing? Your Uncle Marshall was taking the biggest step of his life, and me-I'm calling your Uncle, Barney."
    sentence2 = "[Cut to Later: Barney's in the barber shop, Ted's talking from home]"
    sentence3 = "Barney: (on the phone) hey, so you know how I've always had a thing for half-Asian girls? Well, now I've got a new favorite: Lebanese girls! Lebanese girls are the new half-Asians."
    sentence4 = "Barney: Okay, meet me at the bar in fifteen minutes, and Suit up!"
    sentence5 = "The gentlemen's dress is called suit, and girls like it"
    
    corpus.append(sentence1)
    corpus.append(sentence2)
    corpus.append(sentence3)
    corpus.append(sentence4)
    corpus.append(sentence5)    
    
    return corpus



    
def calculateTFIDF(corpus):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
    
    X = tf.fit_transform(corpus)
    idf = tf.idf_
    feature_names = tf.get_feature_names()
    print (feature_names);

    print (type(X))
    
    dense = X.todense()
    print (dense)
    print (dense[0].tolist()[0])    

    return dense, feature_names
    
    
#Note: For each query term scoreArray should be mutually shared among all the the query terms.    
def applyQuery1(query, dense, feature_names):
    indexInFeature = None
    try:
        indexInFeature = feature_names.index(query)
    except:
        print ("Some error")
        
    numberOfDocuments = (dense.shape)[0]
    
    #Max number of documents to store with highest score
    numberOfTopDocuments = 2
    scoreArray = []
    for i in range(0, numberOfDocuments):
        if not indexInFeature:
            break
        
        print (i, indexInFeature)

        score = (dense[i].tolist()[0])[indexInFeature]
        
        #checking whether scoreArray is empty and storing top N score documents
        lenScoreArray = len(scoreArray)
        
        if lenScoreArray < numberOfTopDocuments:
            scoreArray.append((i, score))
        else:
            if scoreArray[0][1] < score:
                scoreArray[0] = (i, score)
                
        #sorting the scoreArray in ascending order
        scoreArray = sorted(scoreArray, key=itemgetter(1), reverse = False)
        
    print (scoreArray)
    



#Note: For each query term scoreArray should be mutually shared among all the the query terms.    
def applyQuery(query, dense, feature_names): 
    numberOfDocuments = (dense.shape)[0]
    
    #Max number of documents to store with highest score
    numberOfTopDocuments = 2
    scoreArray = []

    #This checks whether the query term is present in feature list    
    indexArray = list()
    for queryTerm in query:
        try:
            indexInFeature = feature_names.index(queryTerm)
            indexArray.append(indexInFeature)
            print (queryTerm)
        except:
            print ("Some error")
          
       
        
        
    for i in range(0, numberOfDocuments):        
                
        netScore = 0.0
        for indexInFeature in indexArray:        
            print (i, indexInFeature)
            netScore = netScore + (dense[i].tolist()[0])[indexInFeature]
        
        print (netScore)
        #checking whether scoreArray is empty and storing top N score documents
        lenScoreArray = len(scoreArray)
        
        if lenScoreArray < numberOfTopDocuments:
            scoreArray.append((i, netScore))
        else:
            if scoreArray[0][1] < netScore:
                scoreArray[0] = (i, netScore)
                
        #sorting the scoreArray in ascending order
        scoreArray = sorted(scoreArray, key=itemgetter(1), reverse = False)
        
    print (scoreArray)




def generateTokens(query, dense, feature_names):
    two_grams = ngram_helper(query, 2)
    three_grams = ngram_helper(query, 3)    
    
    word_list = nltk.word_tokenize(query)
    #removing stop words
    filtered_words = [word for word in word_list if word not in stopwords.words('english') and word.isalnum()]
               
    #Adding ngrams
    filtered_words = filtered_words + two_grams
    filtered_words = filtered_words + three_grams
    
    #calling applyQuery for all terms
    print (filtered_words)
    applyQuery(filtered_words, dense, feature_names)




def generateTokens1(query, dense, feature_names):
    two_grams = ngram_helper(query, 2)
    three_grams = ngram_helper(query, 3)    
    
    word_list = nltk.word_tokenize(query)
    #removing stop words
    filtered_words = [word for word in word_list if word not in stopwords.words('english') and word.isalnum()]
               
    #Adding ngrams
    filtered_words = filtered_words + two_grams
    filtered_words = filtered_words + three_grams
    
    #calling applyQuery for all terms
    for queryTerm in filtered_words:
        applyQuery(queryTerm, dense, feature_names)
                    

    
#This function helps in calculating ngrams           
def ngram_helper(query, n):    
    query = query.lower()
    
    sixgrams = ngrams(query.split(), n)
    ngram_list = list()
    
    for grams in sixgrams:
        if n == 2:
            ngram_list.append(grams[0] + " " +grams[1])
        elif n == 3:    
            ngram_list.append(grams[0] + " " +grams[1] + " " +grams[2])
        elif n == 4:    
            ngram_list.append(grams[0] + " " +grams[1] + " " +grams[2] + " " +grams[3])                   
 
                
    #print ngram_list    
    return ngram_list     
        
    
    
    
def main():
    corpus = makeArray()
    dense, feature_names = calculateTFIDF(corpus)
    #applyQuery("girls", dense, feature_names)
    generateTokens("girls favorite", dense, feature_names)   
    
main()