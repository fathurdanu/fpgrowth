import pandas as pd
import numpy as np
import math
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage
UPLOAD_FOLDER = './download'
ALLOWED_EXTENSIONS = {'csv','xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/prepro")
def prepro():
    return render_template('Preprocessing.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/hasil_prepro', methods = ['GET', 'POST'])
def hasil_prepro():
   if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            extension = file.filename.rsplit('.', 1)[1].lower()
            #print("file path panjaaaaaaaangggggggg : ",path)
            # preprocessing
            result = preprocessing(extension,request)
            result.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename),index=False)

            # df = pd.DataFrame([1,2,3,4])
            # print(filename)
            # f=request.files['file']
            # THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            # filename_path = os.path.join(THIS_FOLDER, file.filename)
            # df = pd.read_csv(f, sep=';', header=None, encoding='cp1252')

            # print(df)

            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('prepro'))
        return "error"

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            extension = file.filename.rsplit('.', 1)[1].lower()
            #print("file name panjaaaaaaaangggggggg : ",filename)
            # preprocessing
            result = fpg(extension,request)
            #print("result panjanggggggggggggggggggggg : ", result)
            # print("result === ", result)
            # return redirect(url_for('asosiasi',x=x))
            return render_template(
                'Association_Rule.html',
                transaksi=result["total_transaksi"], 
                produk=result["total_produk_treshold"],
                frekuensi=result["frekuensi"],
                total_baris_frekuensi=len(result["frekuensi"])
            )

    return render_template('Upload.html')

@app.route("/asosiasi")
def asosiasi():
    return render_template('Association_Rule.html')

def preprocessing(extension,request):
    #baca data
    if(extension == 'csv'):
        df = pd.read_csv(request.files['file'], sep=';', encoding='cp1252')
        df.drop(df.columns[[6]], axis=1, inplace=True)
        df.drop(df.columns[[5]], axis=1, inplace=True)
        df.drop(df.columns[[4]], axis=1, inplace=True)
        df.drop(df.columns[[2]], axis=1, inplace=True)
        df.drop(df.columns[[0]], axis=1, inplace=True)
        
        # .groupby('NOMOR')['NAMA ITEM'].apply(list).reset_index()
        return df

def fpg(extension,request):
    if(extension == 'csv'):
        df = pd.read_csv(request.files['file'], sep=',', encoding='cp1252')
        df_itemset = df
        df_dataset = df_itemset['NAMA ITEM'].tolist()

        #frequent pattern
        # dijabarkan = [x for l in df_dataset for x in l]
        # print(dijabarkan)
        df_freq = df_itemset.groupby('NAMA ITEM')['NAMA ITEM'].count().sort_values(ascending=False).to_frame(name='freq').reset_index()
        # print(df_freq)
        # print({x for l in df_dataset for x in l})
        # df_freq = df.groupby(['NAMA ITEM'])['NAMA ITEM'].count().sort_values(ascending=False).to_frame(name='freq').reset_index()
        # print(df_freq)
        #print (df_dataset)
        # #total transaksi

        # for i in range(len(df_freq)):
        #     print(df_freq.loc[i]["NAMA ITEM"])


        result = {
            'total_produk_treshold': str(len(set(df_dataset))),
            'total_transaksi': str(len(df.groupby('NOMOR'))),
            'frekuensi': df_freq
        }



        return (result)

        # #masuk ke preprocessing
        # # instantiate a transaction encoder
        # my_transactionencoder = TransactionEncoder()
        # # fit the transaction encoder using the list of transaction tuples
        # my_transactionencoder.fit(df_dataset)
        # # transform the list of transaction tuples into an array of encoded transactions
        # encoded_transactions = my_transactionencoder.transform(df_dataset)
        # # convert the array of encoded transactions into a dataframe
        # encoded_transactions_df = pd.DataFrame(encoded_transactions, columns=my_transactionencoder.columns_)

        # #frequent itemset
        # # our min support is 3, but it has to be expressed as a percentage for mlxtend
        # min_support = 3/len(df_dataset) 
        # # compute the frequent itemsets using fpgriowth from mlxtend
        # frequent_itemsets = fpgrowth(encoded_transactions_df, min_support=min_support, use_colnames = True)
        # # print the frequent itemsets
        # #frequent_itemsets.sort_values('support', ascending=False)

        # # compute and print the association rules
        # association = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
