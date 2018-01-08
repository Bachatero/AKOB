def anti_vowel(text):
    strln = len(text)
    #lst = list()
    #lst.append(text)
    anttext = ""
    vowel="aeiou"
    #for index, item in enumerate(lst):
    for i in range(0, strln):
        if text[i].lower() not in vowel:
           anttext += text[i]
        #print index, item
    return anttext
            


print anti_vowel("Hey, basmeg!")
