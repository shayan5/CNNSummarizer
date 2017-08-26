import requests
import re
import math

        
def removeTags(sentence):
  pattern = re.compile('<.*?>')
  newText = re.sub(pattern, '', sentence)
  return newText

def fixBrokenTags(sentence):
  pattern = re.compile('zn-body__paragraph.*?>')
  newText = re.sub(pattern, '<div>', sentence)
  return newText

def getSentences(text):
  sentences = []
  word = ""
  lst = ["Mr.", "mr.", "Mrs.", "mrs.", "Ms.", "ms.", "Dr.", "dr."]
  sentenceEnd = [".", "!", "?"]
  if len(text)>=3:
    for i in range(0, len(text)):
      word += text[i]
      if (text[i] in sentenceEnd) and (len(word) >= 3) and (word[-3:] not in lst):
        sentences.append(word)
        word=""
  return fixQuotes(sentences)

def fixQuotes(sentences):
  result = []
  for i in range(0, len(sentences)):
    result.append(sentences[i])
    if result[i][0]==" ":
      result[i]=result[i][1:]
    if len(result[i]) >= 2 and result[i][0:2]=="\" ":
      if i - 1 >= 0:
        result[i]=result[i][2:]
        result[i-1]=result[i-1]+"\""
  return result

def countWord(sentenceList):
  result = {}
  for sentence in sentenceList:
    for word in sentence.split(" "):
      if word not in result:
        word=normalizeWord(word)
        result[word]=1
      else:
        result[word]=result[word]+1
  return result

def rankSentences(sentenceList, wordOccurance):
  result=[]
  ignoreWords=["he", "she", "it", "has", "will", "to", "a", "of", "the"]
  score = 0
  for sentence in sentenceList:
    for word in sentence.split(" "):
      word=normalizeWord(word)
      if word in ignoreWords:
        score=0
      else:
        score += wordOccurance[word]
    result.append((sentence, score))
    score=0
  return result

def normalizeWord(word):
  word=word.lower()
  word=word.replace("\"", "");
  word=word.replace(".", "");
  word=word.replace(",", "");
  word=word.replace("!", "");
  word=word.replace("!", "");
  word=word.replace("?", "");
  return word

def getScoreOrder(rankedSentences, num):
  numScores=[]
  for sentence in rankedSentences:
    numScores.append(sentence[1])
  numScores.sort()
  return (numScores[num*-1:])
  
def getTopSentences(rankedSentences, num):
  result = []
  order = getScoreOrder(rankedSentences, num)
  for sentence in rankedSentences:
    if sentence[1] in order:
      result.append(sentence[0])
  return result

def printSentences(sentences):
  for sentence in sentences:
    print(sentence)

def getNumSentences(percentReduced, numSentences):
  return (math.floor(numSentences*(100-percentReduced)/100))
  
def executeProgram(link, percentReduced):
  r=requests.get(link)
  if r.status_code==200:
      article=""
      result = re.findall("zn-body__paragraph.*?<\/div>", r.text)
      for item in result:
          article += fixBrokenTags(item) + " "
      article = removeTags(article)
      sentences = getSentences(article)
      countedWords = countWord(sentences)
      rankedSentences = rankSentences(sentences, countedWords)
      numSentences = getNumSentences(percentReduced, len(rankedSentences))
      orderedSentence = getTopSentences(rankedSentences, numSentences)
      printSentences(orderedSentence)  

if __name__=="__main__":
    #ONLY WORKS ON cnn.com articles, not money.cnn or videos etc
    link = input("Enter a cnn article link: ")
    percentReduced = input("Enter how much % you would like reduced (60-85 recommended): ")
    percentReduced = int(percentReduced)
    while(percentReduced > 100 or percentReduced < 0):
      percentReduced = input("Enter how much % you would like reduced: ")
    percentReduced = int(percentReduced)
    executeProgram(link, percentReduced)

