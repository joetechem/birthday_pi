import requests

r = requests.get('https://raw.githubusercontent.com/joetechem/birthday_pi/master/million_pi_digits/million_pi_digits.txt')

pi_string = r.text

for rs in r:
    pi_string += rs.strip()
    
#print(pi_string[:32] + "...")
#print(len(pi_string))

birthday = raw_input("Enter your birthday, in the form mmddyy: ")
if birthday in pi_string:
    print("Your birthday appears in the first million digits of pi!")
else:
    print("Your birthday does not appear in the first million digits of pi.")
