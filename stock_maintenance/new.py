
def coman(s):
    c = 0
    d = s
    for i in range(len(s)):
        if s[i] in d:
            c = c + 1

        print(c)
        c = 0

s = input('aabbbccde')
coman(s)
