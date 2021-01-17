# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:19:48 2020

@author: zainab fathima kz
"""

import cv2
import numpy as np
import image_diff as diff

def messageToBinary(message):
    if type(message)==str:
        return ''.join([format(ord(i),"08b") for i in message])
    elif type(message)==bytes or type(message)==np.ndarray:
        return [format(i,"08b")for i in message]
    elif type(message) == int or type(message) == np.util8:
        return format(message,"08b")
    else:
        raise TypeError("Input type not supported")
        

#function to hide the secret message into the image
def hideData(image, secret_message):
    
    #calculate the maximum bytes to encode
    n_bytes=image.shape[0]*image.shape[1]+3//8
    print("Maximum bytes to encode",n_bytes)
    
    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError('Error encountered insufficient bytes, need bigger image or less data ||')
        
    secret_message+="#####"
    
    data_index=0
    #convert input data to binary format using messageToBinary() function
    binary_secret_msg=messageToBinary(secret_message)
    
    data_len=len(binary_secret_msg)
    for values in image:
       for pixel in values:
           #convert RGB values to binary format
           r, g, b=messageToBinary(pixel)
           #modify the least significant bit only if there is still data to store
           if data_index < data_len:
               #hide the data into least significant bit of red pixel
               pixel[0]=int(r[:-1]+binary_secret_msg[data_index],2)
               data_index+=1
          
           if data_index < data_len:
               #hide the data into least significant bit of red pixel
               pixel[1]=int(g[:-1]+binary_secret_msg[data_index],2)
               data_index+=1
             
           if data_index < data_len:
               #hide the data into least significant bit of red pixel
               pixel[2]=int(b[:-1]+binary_secret_msg[data_index],2)
               data_index+=1
               
           #if data is encoded, just break out of the loop
           if data_index > data_len:
               break
           
    return image


def showData(image):
    
    binary_data=""
    for values in image:
        for pixel in values:
            r, g, b=messageToBinary(pixel)
            binary_data+=r[-1]
            binary_data+=g[-1]
            binary_data+=b[-1]
    #split by 8-bits
    all_bytes=[binary_data[i: i+8] for i in range(0,len(binary_data),8)]
    #convert from bits to characters
    decoded_data=""
    for byte in all_bytes:
        #byte=chr(byte)
        #print(byte)
        decoded_data+=chr(int(byte,2))
        if decoded_data[-5:]=="#####":
            break
    #print(decoded_data)
    return decoded_data[:-5]#remove the delimiter to show the original hidden message

#Encode data into image
def encode_text():
    image_name=input("Enter image name(with extension): ")
    image=cv2.imread(image_name)
    #img = np.full((300, 300, 3), 255).astype(np.uint8)
    
    print("The shape of the image is: ",image.shape)
    print("The original image is as shown below: ")
    resized_image=cv2.resize(image,(500,500))
    cv2.imshow("Encoded image",resized_image)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image
    data=input("Enter data to be encoded: ")
    if(len(data)==0):
        raise ValueError('Data is empty')
        
    filename=input("Enter the name of new encoded image(with extension): ")
    encoded_image=hideData(image,data)
    cv2.imwrite(filename,encoded_image)
    
        
#Decode the data in the image
def decode_text():
    #read the image that contains the hidden image
    image_name=input("Enter the name of the steganographed image that you want to decode (with extension):")
    image=cv2.imread(image_name)

    print("The Steganographed image is as shown below: ")
    resized_image=cv2.resize(image,(500,500))
    cv2.imshow("Decoded image",resized_image)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image
    
    text=showData(image)
    return text

def showDifference():
    image_name=input("Enter the name of the original image that was encoded (with extension):")
    imageA=cv2.imread(image_name)
    image_name1=input("Enter the name of the steganographed image that was decoded (with extension):")
    imageB=cv2.imread(image_name1)
    diff.differentiation(imageA,imageB)
    #plt.hist(imageA.ravel(),256,[0,256])
    #plt.show()
    #plt.hist(imageB.ravel(),256,[0,256]) 
    #plt.show() 

def Steganography():
    ch='y'
    
    while ch == 'y':
        a=input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n 3. Image Difference \n Your input is: ")
        userinput=int(a)
        if(userinput==1):
            print("\n Encoding...")
            encode_text()
            
        elif(userinput==2):
            print("\n Decoding...")
            print("Decoded message is: "+decode_text())
            
        elif(userinput==3):
            print("-----------Image Difference-------------")
            showDifference()
            
        else:
            raise Exception('Enter correct input')
            
        ch=input("Do you want to continue press y for yes and n for no")
        ch=ch.lower()
    
        
Steganography()
        
        
        
        
        
        
        
        
        
        
    
    