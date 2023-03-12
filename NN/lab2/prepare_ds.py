# -*- coding: utf-8 -*-

'''
Скрипт позволит переделать датасет из неудобного формата в удобный.

> python3 convert_img_to.py path_to_train_csv path_to_test_csv path_to_test_labels_csv

В итоге появится файл out.csv, который:
Формирует датасет "Toxic Comment Classification" для текущей задачи.
'''

import os
import sys
import pandas as pd
import numpy as np
import json

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

#import torchtext
#from torchtext.data import get_tokenizer
#from torchnlp.encoders.text import StaticTokenizerEncoder, stack_and_pad_tensors, pad_tensor

#from sklearn.feature_extraction.text import TfidfVectorizer


num_words = 10000
max_comment_len = 25

if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc != 4):
        print("Syntax error. Expected: \"> python3 convert_img_to.py path_to_train_csv path_to_test_csv path_to_test_labels_csv\". Exiting...")
        exit()
    path_to_train_csv       = os.path.abspath(sys.argv[1])
    path_to_test_csv        = os.path.abspath(sys.argv[2])
    path_to_test_labels_csv = os.path.abspath(sys.argv[3])

    df_train = pd.read_csv(path_to_train_csv)

    df_test = pd.read_csv(path_to_test_csv)
    df_test_y = pd.read_csv(path_to_test_labels_csv)

    print(f"Check df_test:\n{df_test.head()}\n")
    
    print(f"Check df_test_y:\n{df_test_y.head()}\n")

    print(f"Check df_train:\n{df_train.head()}\n")

    df_test = df_test.merge(df_test_y)

    print(f"Check df_test after merging with df_test_y:\n{df_test.head()}\n")

    df = pd.concat([df_train, df_test])

    print(f"Shape of df_train={df_train.shape}, df_test={df_test.shape}")
    print(f"Shape of df={df.shape}   (159571 + 153164 = 312735)\n")

    print(f"Check row with id \"70d018e543fd49ba\" (in df_test)")
    print(df.loc[ df["id"] == "70d018e543fd49ba" ], end="\n\n")

    # df["id"] = df["id"].astype(str)
    # df["comment_text"] = df["comment_text"].astype(str)
    print(f"Types:\n{df.dtypes}\n")

    df.drop(df.loc[(df["toxic"] == -1) | (df["severe_toxic"] == -1) | (df["obscene"] == -1) | (df["threat"] == -1) | (df["insult"] == -1) | (df["identity_hate"] == -1)].index, inplace=True)

    print(f"Check df after delete rows with -1:\n")
    print(df)
    print(f"df.shape: {df.shape}\n")

    severe_all = []
    #print(df[["toxic", "severe_toxic"]])
    df = df.reset_index()
    for i, row_i in df.iterrows():
        if(row_i["toxic"] == 1 or row_i["severe_toxic"] == 1):
            severe_all.append(1)
        else:
            severe_all.append(0)
    df["toxics"] = severe_all
    #print(df)
    #print(df.loc[df["severe_toxic"] == 1])
    del df["toxic"]
    del df["severe_toxic"]
    df = df[["id", "comment_text", "toxics", "obscene", "threat", "insult", "identity_hate"]]

    print(f"Check df after unite toxic and severe_toxic:\n")
    print(df)

    # vect_word = TfidfVectorizer(max_features=3000, lowercase=True, analyzer="word", 
    #                             stop_words= "english", ngram_range=(1,4), dtype=np.float32)
    # tr_vect = vect_word.fit_transform(df["comment_text"])
    # tfidf_tokens = vect_word.get_feature_names_out()
    # data_points = pd.DataFrame(data=tr_vect.toarray(), 
    #                   columns=tfidf_tokens)
    # X = data_points.to_numpy()
    # np.set_printoptions(threshold=sys.maxsize)
    # print(X)

    #tokenizer = get_tokenizer("basic_english") # get_tokenizer("spacy")
    #loaded_data = df["comment_text"].values.tolist()[:10]
    # https://stackoverflow.com/questions/57767854/keras-preprocessing-text-tokenizer-equivalent-in-pytorch
    #encoder = StaticTokenizerEncoder(loaded_data, tokenize=lambda s: tokenizer(s))
    #encoded_data = [encoder.encode(example) for example in loaded_data]
    #print(encoder.)
    #print(encoded_data)

    tokenizer = Tokenizer(num_words=num_words)

    tokenizer.fit_on_texts(df["comment_text"])

    print(str(tokenizer.word_index)[:1504]) # check word_indexes

    sequences = tokenizer.texts_to_sequences(df["comment_text"])

    print("Check, what tokenazing correct: ")
    print(df["comment_text"].iloc[[0]].values[0])
    print(sequences[0])

    print("First 15 sequences")
    Xs = pad_sequences(sequences, maxlen=max_comment_len)
    print(Xs[:15])

    comments = []
    df = df.reset_index()
    li = 0
    for i, row_i in df.iterrows():
        str_i = str(Xs[li]).replace('\n', '') 
        str_i = str_i[1:len(str_i)-1] # remove "[" and "]"
        comments.append(str_i)
        li-=-1
    df["comment"] = comments

    df_out = df[["id", "comment", "toxics", "obscene", "threat", "insult", "identity_hate"]]
    print(f"Check df_out:\n")
    print(df_out)

    print("Saving \"out.csv\"...", end="")
    df_out.to_csv("out.csv", index=False)
    print("OK! ")

    print("Saving \"word_index_dict.json\"...", end="")
    S = json.dumps(tokenizer.word_index)
    with open("word_index_dict.json", 'w', encoding="utf-8") as temp:
        temp.write(S)
        temp.flush()
    print("OK! ")
