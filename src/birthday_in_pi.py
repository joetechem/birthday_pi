""" 
Testing functionality locally (not in AWS)
    A simple program returning a response to user from an api call
    to a GitHub gist. Lets the user know if their birthday is found
    in pi.
"""

import requests

r = requests.get('https://raw.githubusercontent.com/ehmatthes/pcc/master/chapter_10/pi_million_digits.txt')

pi_string = r.text

for rs in r:
    pi_string += rs.strip()
    
print(pi_string[:32] + "...")
print(len(pi_string))

##birthday = raw_input("Enter your birthday, in the form mmddyy: ")
##if birthday in r:
##    print("Your birthday appears in the first million digits of pi!")
##else:
##    print("Your birthday does not appear in the first million digits of pi.")
