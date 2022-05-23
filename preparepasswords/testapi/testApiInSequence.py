import requests


first = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]
second = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]
third = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]


start = "00"
count = 0
api = "https://knowyourpassword.pythonanywhere.com/api/v1/haveibeenpwned/"
sec = 0


for i in first:
    for j in second:
        for k in third:
            url = api + str(start) + str(i) + str(j) + str(k)
            r = requests.get(url)
            if r.status_code == 200:

                print("\033[1;32;40m" + url + " : " + str(r.status_code) + " : " + str(r.elapsed.total_seconds()) + "\n")
            else:
                print("\033[1;31;40m" + url + " : " + str(r.status_code) + " : " + str(r.elapsed.total_seconds()) + "\n")
            sec += r.elapsed.total_seconds()
            count += 1

print("\n\nTotal api request : ",count)
print("Total Time taken : ","%.4f" % sec)
print("Average time taken : ","%.4f" % (sec/count))
print("\n")
