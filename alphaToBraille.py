'''
1.) Get the required input to be translated.
2.) Split the words in each sentence and store them in a list.
3.) For each word,
    a.) The word is parsed and if there exists a capital letter then it is represented as ‘@’ to map it with the corresponding braille font in the hasp map.
    b.) If any number exists, precede it with an ‘#’ and return it. Else return the original string.
    c.) The words are trimmed and the punctuations are extracted. Translate the punctuations and the remaining word separately.
    d.) For each substring in the text
        i.) Check whether the entire string is present in the dictionary.
        ii.) If present, replace it with the equivalent braille code and return. 
        iii.) Else, for each substring, check if the substring is present in the dictionary.
        iv.) If the substring is present, check the position code associated with it i.e., (1,2,3,4)
        v.) If the position code matches, replace it with the equivalent braille code and return.
4.) Return the resultant braille code as a string
'''

import mapAlphaToBraille as mab

double_quote=True
single_quote=True

def extract(string):
    words = string.split(" ")
    result = []
    for word in words:
        temp = word.split("\n")
        for item in temp:
            result.append(item)
    return result


def remove_punc(word):
    while len(word) is not 0 and not word[0].isalnum() and word[0]!="#" and word[0]!="@":
        word = word[1:]
    while len(word) is not 0 and not word[-1].isalnum():
        word = word[:-1]
    return word

def numbers(word):
    if word == "":
        return word
    result = word[0]
    if word[0].isdigit():
        result = "#" + word[0]          # '#' associated with number sign in braille
    for i in range(1, len(word)):
        if word[i].isdigit() and not word[i-1].isdigit():
            result += "#" + word[i]
        else:
            result += word[i]
    return result


def capital(word):
    if word == "":
        return word
    result = ""
    for char in word:
        if char.isupper():
            result += "@" + char.lower()    # '@' associated with capital sign in braille
        else:
            result += char
    return result

def process_word(word):
    if word[0]=='@':
        if word[1:] in mab.full_word:
            return word[0]+mab.full_word.get(word[1:])
    elif word in mab.full_word:
        return mab.full_word.get(word)
    start=min(10,len(word))
    for length in range(start,1,-1):
        i=0
        while i+length<=len(word):
            sub=word[i:i+length]
            if sub in mab.word_braille_map[length-2]:
                rep,code=mab.word_braille_map[length-2].get(sub)
                replace=False
                if code==1:
                    replace=True
                elif code==2:
                    if i==0 or (word[0]=="@" and i==1):
                        replace=True
                elif code==3:
                    if i+length==len(word):
                        replace=True
                elif code==4:
                    bool = (i==0 or (word[0]=="@" and i==1)) or i+length==len(word)
                    if not bool:
                        replace=True
                if replace:
                    word=word[0:i]+rep+word[i+length:len(word)]
                    i+=length
                    continue
            i+=1
    return word

def process_punc(word):
    result=""
    i=0
    while i<len(word):
        char=word[i]
        if char == '.':
            if i+2<len(word) and word[i+1]=='.' and word[i+2]=='.':
                result+=mab.punctuation.get('...')
                i+=2
            elif i!=0 and i+1!=len(word) and word[i-1].isdigit and word[i+1]=='#':
                result+=mab.punctuation.get("~")
            else:
                result+=mab.punctuation.get(char)

        elif char=="\"":
            global double_quote
            if double_quote:
                double_quote = not double_quote
                result+=mab.punctuation.get("\u201C")
            else:
                double_quote = not double_quote
                result+=mab.punctuation.get("\u201D")
        elif char=="\'":
            global single_quote
            if single_quote:
                single_quote = not single_quote
                result += mab.punctuation.get("\u2018")
            else:
                single_quote = not single_quote
                result += mab.punctuation.get("\u2019")
        elif char in mab.punctuation:
            result+=mab.punctuation.get(char)
        else:
            result+=char
        i+=1
    return result


def translate(string):
    braille=""
    words=extract(string)
    for word in words:
        word=numbers(word)
        word=capital(word)
        without_punc=remove_punc(word)
        ind=word.find(without_punc)
        punc=word.replace(without_punc,"")
        processed_word=process_word(without_punc)
        processed_punc=process_punc(punc)
        processed_word=process_punc(processed_word)
        if ind==0:
            braille+=processed_word+processed_punc+" "
        else:
            braille+=processed_punc[0:ind+1]+processed_word+processed_punc[ind+1:]+" "
    return braille

if __name__ == '__main__':
    print(translate('Hi, How are you?'))    # to test the code
