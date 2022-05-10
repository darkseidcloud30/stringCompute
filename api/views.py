from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework import status
import json

import math
import scipy
import nltk
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import time
start_time = time.time()

print("\nLoading Model...\n")

try: 
    glove_file = datapath('glove.840B.300d.txt')
    tmp_file = get_tmpfile("word2vec.txt")
    # _ = glove2word2vec(glove_file, tmp_file)
    model = KeyedVectors.load_word2vec_format(glove_file, binary=False, no_header=True)
    # print("21")
except:
    print("error")

# glove_file2 = datapath('glove.6B.300d.txt')
# tmp_file2 = get_tmpfile("word2vec.txt")
# _ = glove2word2vec(glove_file2, tmp_file2)
# model2 = KeyedVectors.load_word2vec_format(tmp_file2)


    print("\nModel Initialized in ","{:.10f}".format(float(time.time() - start_time)),"seconds\n")


@api_view(['GET'])  
def overview(request):
    code = {

        'codeBody':'dadsadasd',
        'classname':'dasdsad'   

    }
    return Response(code)



@api_view(['POST'])
@parser_classes([JSONParser])
def similarity(request, format=None):
    if request.META['HTTP_X_TOKEN'] == "1234":



        start_time = time.time()

        simRate=cosine(request.query_params['entry1'],request.query_params['entry2'],model)
        simRate2=cosine(request.query_params['entry1'],request.query_params['entry2'],model)

        fetch=(time.time() - start_time)

        fetch="{:.10f}".format(float(fetch))

        corpus={'entry1':request.query_params["entry1"],'entry2': request.query_params["entry2"]}

        body = {'corpus':corpus,'similarityRate': simRate,'simrate2':simRate2
        ,'fetchTime':fetch+"s",'status':status.HTTP_200_OK,'description':'HTTP_200_OK'}

        stringComputeApi=body

        print("\n"+json.dumps(stringComputeApi),"\n")

        return JsonResponse(stringComputeApi)
    else:   
        return JsonResponse({'error': status.HTTP_401_UNAUTHORIZED,'description':'HTTP_401_UNAUTHORIZED'})
 
def cosine(s1, s2,theModel):
    stopWords = stopwords.words('english')  
    tokenizer = RegexpTokenizer(r'\w+')
    # word1=word_tokenize(s1)
    # word2=word_tokenize(s2)
    token1=tokenizer.tokenize(s1)
    token2=tokenizer.tokenize(s2)

    xWord= {w.lower() for w in token1 if not w in stopWords}
    yWord= {w.lower() for w in token2 if not w in stopWords}


    xvec=[]
    yvec=[]
    
    for xw in xWord:
        try:
            xvec.append(theModel[xw])
        except:
            a=0
    
    for yw in yWord:
        try:
            yvec.append(theModel[yw])
        except:
            a=0

        
    meanx=np.mean(xvec,axis=0)
    meany=np.mean(yvec,axis=0)


    t=0
    normX=0
    normY=0
    for x in range(len(meanx)):
#         print(x)
        t+=meanx[x]*meany[x]
        normX+=meanx[x]**2
        normY+=meany[x]**2
    normX=math.sqrt(normX)
    normY=math.sqrt(normY)
    cos=t/(normX*normY)
    return cos



# def cosine2(s1, s2):
#     stopWords = stopwords.words('english')  
#     tokenizer = RegexpTokenizer(r'\w+')
#     # word1=word_tokenize(s1)
#     # word2=word_tokenize(s2)
#     token1=tokenizer.tokenize(s1)
#     token2=tokenizer.tokenize(s2)

#     xWord= {w.lower() for w in token1 if not w in stopWords}
#     yWord= {w.lower() for w in token2 if not w in stopWords}

#     # print(word1)u
#     # print(word2)

#     meanx=np.mean([model2[word] for word in xWord],axis=0)
#     meany=np.mean([model2[word] for word in yWord],axis=0)
#     t=0
#     normX=0
#     normY=0
#     for x in range(len(meanx)):
# #         print(x)
#         t+=meanx[x]*meany[x]
#         normX+=meanx[x]**2
#         normY+=meany[x]**2
#     normX=math.sqrt(normX)
#     normY=math.sqrt(normY)
#     cos=t/(normX*normY)
#     return cos