#! coding:utf-8
import sys,os
razdel = ['_',':',';']
def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def brute_words(words):
    new_words = []

    for i in words:
        new_words.append(i)
        new_words.append(i[0].upper() + i[1:])
        new_words.append(i[0].upper() + i[1:-1] + i[-1].upper())
        new_words.append(i.upper())

    for j in spisok:
        new_words.append(i + j)
    for m in razdel:
        new_words.append(j + m + i)
        new_words.append(j + i)
        new_words.append(i * 2 + j)
        new_words.append(j * 2 + i)
        new_words.append(i[0].upper() + i[1:] + j)
        new_words.append(i[0].upper() + i[1:-1] + i[-1].upper() + j)

   return uniq(new_words)

def generate(words_file):
    o = open(words_file, 'r')

words = o.read().splitlines()
for i in brute_words(words):
    print(i)

def main():
    try:
        argv1 = sys.argv[1]
        generate(argv1)
    except IndexError:
        print("You need to define the file")
    except IOError:
        print("File doesn't exist")

if __name__ == "__main__":
    main()
