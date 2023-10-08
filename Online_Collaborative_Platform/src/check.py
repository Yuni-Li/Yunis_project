#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:34:57 2020

@author: z5237308
"""
import re 
  

# Make a regular expression 
# for validating an Email 
regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
      
# Define a function for 
# for validating an Email 
def check_email(email):  
  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return "Valid Email"
          
    else:  
        return "Invalid Email"
    
def check_password(password):
    if(len(password) >= 6):
        return "Valid Password"
    else:
        return "Invalid Password"
    
def check_name(name_first, name_last):
    if(len(name_first) < 1 or len(name_first) > 50) or name_first.isalpha() is not True:
        return "Invalid First Name"
    
    elif(len(name_last) < 1 or len(name_last) > 50) or name_last.isalpha() is not True:
        return "Invalid Last Name"
    else:
        return "Valid Name"
'''
# Driver Code  
if __name__ == '__main__' :  
      
    # Enter the email  
    email = "ankitrai326@gmail.com"
      
    # calling run function  
    check(email) 
  
    email = "my.ownsite@ourearth.org"
    check(email) 
  
    email = "ankitrai326.com"
    check(email)    
'''