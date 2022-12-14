# -*- coding: utf-8 -*-
"""Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VOHp77rCrY0gpLYX8WuoHaKaruPd_b5X
"""

import pandas as pd
import numpy as np

import torch
from torch.utils.data import Dataset, DataLoader 

import warnings
warnings.filterwarnings('ignore')

import torch
from torch import cuda
import torch.nn as nn

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import transformers as t
from transformers import AutoModel

import re
import string

!pip install transformers seqeval[gpu] sentencepiece

def get_string_punctuations():
  ans = re.escape(string.punctuation)
  return ans
punctuations = get_string_punctuations()

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.read_csv("drive/MyDrive/hi_train.conll", names = ['word', 'iob_tag'],sep = '_ _',engine = 'python')
# df.
df

def preprocess_train(file_path):
    test = []
    temp = []
    j = 0
    vec = []
    with open(file_path, encoding = 'utf-8') as f:
        data = f.readlines()
    vec = data 

    for i in range(len(vec)):
        if '#' not in vec[i]:
            temp.append(vec[i])


    temp = [w.replace('\n', '') for w in temp]
    res = [list(sub) for ele, sub in groupby(temp, key = bool) if ele]
    for i in range(len(res)):
        string = ''
        labels = ''
        for j in range(len(res[i])):
            temp = []
            temp.append(res[i][j].split(' _ _ '))
            if not string:
                string = string +  temp[0][0]
            else:
                string = string + ' ' + temp[0][0]
            if not labels:
                labels = labels + temp[0][1]
            else:
                labels = labels + ',' + temp[0][1]
            
        test.append([string,labels])
    return test

file_path = "hi_train.conll"
dataset =  preprocessing(file_path)

df = preprocess_train(df)

df

"""## Initializing values to global variables"""

LEARNING_RATE = 1e-03
MAX_GRAD_NORM = 10
TRAIN_BATCH_SIZE = 4
MAX_LEN = 30
VALID_BATCH_SIZE = 2
EPOCHS = 1

"""## Import BERT Tokenizer from ai4bharat"""

tokenizer = t.AutoTokenizer.from_pretrained('ai4bharat/indic-bert')

# Encode our concatenated data
encoded_sent = [tokenizer.encode(sent, add_special_tokens=True) for sent in df.word.values]

# Find the maximum length
max_len = max([len(sent) for sent in encoded_sent])
print('Max length: ', max_len)

# Specify `MAX_LEN`
MAX_LEN = 30

from sklearn.model_selection import train_test_split

df.iob_tag = pd.factorize(df.iob_tag)[0]

X = df.word.values
y = df.iob_tag.values

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=27)

def to_tensor(x):
  ans = torch.tensor(x)
  return ans

input_ids = []
attention_mask = []
for sent in X_train:
    encoded_sent = tokenizer.encode_plus(text=sent,add_special_tokens=True,max_length=MAX_LEN,pad_to_max_length=True,return_attention_mask=True)
    input_ids.append(encoded_sent.get('input_ids'))
    attention_mask.append(encoded_sent.get('attention_mask'))
train_masks = to_tensor(attention_mask)
train_inputs = to_tensor(input_ids)

input_ids = []
attention_mask = []

for sent in X_val:
    encoded_sent = tokenizer.encode_plus(text=sent,add_special_tokens=True,max_length=MAX_LEN,pad_to_max_length=True,return_attention_mask=True)
    input_ids.append(encoded_sent.get('input_ids'))
    attention_mask.append(encoded_sent.get('attention_mask'))

val_inputs = to_tensor(input_ids) 
val_masks = to_tensor(attention_mask)

"""## Import test data into test_df (dataframe)"""

test_df = pd.read_csv("drive/MyDrive/hi_dev.conll", sep = '_ _', names = ['word', 'iob_tag'])

"""## Preprocess test_df """

test_df = preprocess_train(test_df)
test_df.iob_tag = pd.factorize(test_df.iob_tag)[0]

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
# For fine-tuning BERT, the authors recommend a batch size of 16 or 32.
batch_size = 32
# Convert other data types to torch.Tensor
train_labels = torch.tensor(y_train)
val_labels = torch.tensor(y_val)
# Create the DataLoader for our validation set
val_data = TensorDataset(val_inputs, val_masks, val_labels)
val_sampler = SequentialSampler(val_data)
val_dataloader = DataLoader(val_data, sampler=val_sampler, batch_size=batch_size)
# Create the DataLoader for our training set
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

import torch
import torch.nn as nn
from transformers import BertModel

# Create the BertClassfier class
class BertClassifier(nn.Module):
    """Bert Model for Classification Tasks.
    """
    def __init__(self, freeze_bert=True):
        """
        @param    bert: a BertModel object
        @param    classifier: a torch.nn.Module classifier
        @param    freeze_bert (bool): Set `False` to fine-tune the BERT model
        """
        super(BertClassifier, self).__init__()
        # Specify hidden size of BERT, hidden size of our classifier, and number of labels

        # Instantiate BERT model
        self.bert = AutoModel.from_pretrained('ai4bharat/indic-bert')

        # Instantiate an one-layer feed-forward classifier
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(768, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.Dropout(0.2),
            nn.ReLU(),
            #nn.Dropout(0.5),
            nn.Linear(64, 13),
            nn.LogSoftmax(dim=1)
        )

        # Freeze the BERT model
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False
        
    def forward(self, input_ids, attention_mask):
        # Feed input to BERT
        outputs = self.bert(input_ids, attention_mask)
        
        # Extract the last hidden state of the token `[CLS]` for classification task
        last_hidden_state_cls = outputs[0][:, 0, :]

        # Feed input to classifier to compute logits
        logits = self.classifier(last_hidden_state_cls)

        return logits

# pass the pre-trained BERT to our define architecture
model = BertClassifier()

# push the model to GPU
model = model.to(device)

from transformers.optimization import Adafactor, AdafactorSchedule

optimizer = Adafactor(model.parameters(), scale_parameter=False, relative_step=False, warmup_init=False, lr=1e-4)

loss_fn = nn.CrossEntropyLoss()



import random
import time

# Specify loss function
loss_fn = nn.CrossEntropyLoss()

def set_seed(seed_value=0):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)

def train(model, train_dataloader, val_dataloader=None, epochs=4, evaluation=False):
    print("Start training...\n")
    for epoch_i in range(epochs):
        print(f"{'Epoch':^7} | {'Batch':^7} | {'Train Loss':^12} | {'Val Loss':^10} | {'Val Acc':^9} | {'Elapsed':^9}")
        print("-"*70)

        # Measure the elapsed time of each epoch
        t0_epoch, t0_batch = time.time(), time.time()

        # Reset tracking variables at the beginning of each epoch
        total_loss, batch_loss, batch_counts = 0, 0, 0

        # Put the model into the training mode
        model.train()

        # For each batch of training data...
        for step, batch in enumerate(train_dataloader):
            batch_counts +=1
            # Load batch to GPU
            b_input_ids, b_attn_mask, b_labels = tuple(t.to(device) for t in batch)

            # Zero out any previously calculated gradients
            model.zero_grad()

            # Perform a forward pass. This will return logits.
            logits = model(b_input_ids, b_attn_mask)

            # Compute loss and accumulate the loss values
            loss = loss_fn(logits, b_labels)
            batch_loss += loss.item()
            total_loss += loss.item()

            # Perform a backward pass to calculate gradients
            loss.backward()

            # Clip the norm of the gradients to 1.0 to prevent "exploding gradients"
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            # Update parameters and the learning rate
            optimizer.step()

            # Print the loss values and time elapsed for every 20 batches
            if (step % 100 == 0 and step != 0) or (step == len(train_dataloader) - 1):
                # Calculate time elapsed for 20 batches
                time_elapsed = time.time() - t0_batch

                # Print training results
                print(f"{epoch_i + 1:^7} | {step:^7} | {batch_loss / batch_counts:^12.6f} | {'-':^10} | {'-':^9} | {time_elapsed:^9.2f}")

                # Reset batch tracking variables
                batch_loss, batch_counts = 0, 0
                t0_batch = time.time()

        # Calculate the average loss over the entire training data
        avg_train_loss = total_loss / len(train_dataloader)

        print("-"*70)
        if evaluation == True:
            # After the completion of each training epoch, measure the model's performance
            # on our validation set.
            val_loss, val_accuracy = evaluate(model, val_dataloader)

            # Print performance over the entire training data
            time_elapsed = time.time() - t0_epoch
            
            print(f"{epoch_i + 1:^7} | {'-':^7} | {avg_train_loss:^12.6f} | {val_loss:^10.6f} | {val_accuracy:^9.2f} | {time_elapsed:^9.2f}")
            print("-"*70)
        print("\n")
    
    print("Training complete!")


def evaluate(model, val_dataloader):
    # Put the model into the evaluation mode. The dropout layers are disabled during
    # the test time.
    model.eval()

    # Tracking variables
    val_score = []
    val_loss = []

    # For each batch in our validation set...
    for batch in val_dataloader:
        # Load batch to GPU
        b_input_ids, b_attn_mask, b_labels = tuple(t.to(device) for t in batch)

        # Compute logits
        with torch.no_grad():
            logits = model(b_input_ids, b_attn_mask)

        # Compute loss
        loss = loss_fn(logits, b_labels)
        val_loss.append(loss.item())

        # Get the predictions
        preds = torch.argmax(logits, dim=1).flatten()

        # Calculate the accuracy rate
        score = f1_score(preds.cpu().numpy(), b_labels.cpu().numpy(), zero_division=1, average = 'weighted')
        val_score.append(score)

    # Compute the average accuracy and loss over the validation set.
    val_loss = np.mean(val_loss)
    val_accuracy = np.mean(val_score)

    return val_loss, val_accuracy

import tensorflow
tensorflow.random.set_seed(0)
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

train(model, train_dataloader, val_dataloader, epochs=2, evaluation=True)

import torch.nn.functional as F



def bert_predict(model, test_dataloader):
    test_score = []
    model.eval()
    for batch in test_dataloader:
        b_input_ids, b_attn_mask, b_labels = tuple(t.to(device) for t in batch)

        with torch.no_grad():
            logits = model(b_input_ids, b_attn_mask)
        
        preds = torch.argmax(logits, dim=1).flatten()

        score = f1_score(preds.cpu(), b_labels.cpu(),  average = 'weighted')

        test_score.append(score)

    return np.mean(test_score)

# test_inputs, test_masks = preprocessing_for_bert(test_df.word)
input_ids = []
attention_masks = []

for sent in test_df.word:
  encoded_sent = tokenizer.encode_plus(text=sent,add_special_tokens=True,max_length=MAX_LEN,pad_to_max_length=True,return_attention_mask=True)

  input_ids.append(encoded_sent.get('input_ids'))
  attention_masks.append(encoded_sent.get('attention_mask'))

    # Convert lists to tensors
input_ids = torch.tensor(input_ids)
attention_masks = torch.tensor(attention_masks)

test_inputs  = input_ids 
test_masks = attention_masks

test_labels = torch.tensor(test_df.iob_tag)

# Create the DataLoader for our test set
test_dataset = TensorDataset(test_inputs, test_masks, test_labels)
test_sampler = SequentialSampler(test_dataset)
test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=batch_size)

