#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:14:05 2018

@author: huyu
"""

# A.List
# create a list containing 4 strings.
l1 = ['This','is','a','list']
# print the 3rd item of l1
print (l1[2])
#print the 1st and 2nd item in the list using [:]
print (l1[0:2])
#Add a new string with text “last” to the end
l1.append('last')
print (l1)
# get list length
print (len(l1))
#Replace the last item in the list with the string “new”
l1[-1] = 'new'
print (l1)



# B.Strings
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
# convert the list into a string
s = ' '.join(sentence_words)
print (s)
# reverse sentence_words
sentence_words_v2 = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
sentence_words_v2.reverse()
print (sentence_words_v2)
# sort the list using .sort()
# .sort() method sort this list in place and returns None
# while sorted() does not sort the list in place but returns a sorted list.
sentence_words_v3 = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
sentence_words_v3.sort()
sentence_words_v4 = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
store = sorted(sentence_words_v4)
print (sentence_words_v3)
print (store)



# C. Random Function
def your_randnum (h,l = 0):
    '''
    Function takes a lower bound l, and an upper bound h,
    and returns an integer between l and h
    '''
    from random import randint
    num = randint (l,h)
    print (num)

# function called
your_randnum (100,10)
your_randnum (50)



# D.String Formatting Function
def bestseller ():
    '''
    returns a string that shows the rank and title
    of the bestseller
    '''
    import re
    def titlecase(s):
        '''
        a sub function that titlecases the inputed title
        '''
        return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                      lambda mo: mo.group(0)[0].upper() +
                              mo.group(0)[1:].lower(),
                      s)
    # get the rank and title from user
    n = int(input("give me rank: "))
    t = str(input("give me the title: "))
    # title case the inputed title
    T= titlecase(t)
    a = f"The number {n} bestseller today is: {T}"
    print (a)
# function bestseller called
bestseller ()



# E. Password validation
def is_pwd_valid(s):
    '''
    function checks if an inputed string meets validation criteria
    '''
    # check if len(s) is between 8-14 char
    if len(s)>=8 and len(s)<=14:
        # contiue check if it includes at least 2 numbers
        count_num = 0
        numbers = "0123456789"
        for e in s:
            for n in numbers:
                if e == n:
                    count_num += 1
                    if count_num >= 2:
                        break
            if count_num >= 2:
                break
        if count_num >= 2: # meaning s has has at least 2 digits
            # continue check if s has at least 1 upper case
            count_cap = 0
            cap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for E in s:
                for L in cap:
                    if E == L:
                        count_cap +=1
                        if count_cap >= 1:
                            break
                if count_cap >= 1:
                    break
            if count_cap >= 1: # meaning s indeed has at least 1 uppercase
                # continue check special char
                count_schar = 0
                schar = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
                for x in s:
                    for y in schar:
                        if x == y:
                            count_schar += 1
                            if count_schar >= 1:
                                break
                        if count_schar >= 1:
                            break
                if count_schar >= 1: # Final Test Passed!!!
                    print ("Your password is valid, congratulations!")
                else: # meaning there is no special char
                    print ("error")
            else: # meaning s has less than 1 uppercase
                print ("error")

        else: # meaning s has less than 2 digits
            print ("error")

    else: # meaning s is either too short or too long
        print ("error")
pwd = str(input("enter your intended password for validation: "))
# Function called
is_pwd_valid (pwd)


# F. Exponentiation Function
# using recursion method
def e(a,b):
    if b == 0:
        return 1
    elif b == 1:
        return a
    else:
        return (a*e(a,b-1))
# test case 2 to the power of 4:
print (e(2,4))


# G.Max function
def max(L):
    '''
    function takes in a list L containing numbers, and finds the max
    '''
    max = L[0] # assume the L[0] is the max
    for i in range(1,len(L)): # starting from the 2nd item
        if L[i]>=max: # if any later item is larger than max
            max = L[i] # update max
    return max
# function called
print (max([11,20,8,55,55,6]))
