from ast import arg
from sys import argv


if len(argv) < 2:

    print('----------------------------------------')
    print('               Palindrome               ')
    print('----------------------------------------\n\n')

    infileName = input('Enter .fasta file location: ')

    minLen = int(input('Minimum length of repeat: '))
    maxLen = int(input('Maximum length of repeat: '))
    maxGap = int(input('Maximum gap between repeat pairs: '))
    outfileName = '{a}_palindrome.tsv'.format(a = infileName[:-6])

else:

    infileName = argv[1]
    minLen = int(argv[2])
    maxLen = int(argv[3])
    maxGap = int(argv[4])
    outfileName = argv[5]

mismatches = 0

outfile = open(outfileName,'a')

outfile.write('length\tgap\tstart1\tSequence1\tend1\tstart2\tSequence2\tend2\n')

def getInv(seq):

    inv = []

    for b in seq[::-1]:

        if b == 'A':
            inv.append('T')

        elif b == 'T':
            inv.append('A')

        elif b == 'G':
            inv.append('C')
        
        elif b== 'C':
            inv.append('G')

    return inv

reading = True
t = 0
genome = []

with open(infileName,'r') as infile:

    while reading:

        t += 1

        line = infile.readline()

        if t == 1:

            continue

        elif len(line) == 0:

            reading = False

        else:

            arr = [ i for i in line if i != '\n']

            genome += arr


if len(genome) > 1215606 and len(argv) < 2:
    print('\n\nThis might take a while......\n')


def mainFunction():

    t = 0

    while t < len(genome):

        current_repeat = []

        inc = 1

        current_seq = genome[t:t+minLen]
        current_inv = getInv(current_seq)

        for j in range(t+minLen,t+minLen+maxGap):

            search_seq = genome[j:j+minLen]

            if current_inv == search_seq:

                for k in range(maxLen):

                    current_seq2 = genome[t:t+minLen+k]

                    current_inv2 = getInv(current_seq2)

                    search_seq2 = genome[j-k:j+minLen]


                    if current_inv2 != search_seq2:

                        current_repeat.append(str(len(current_seq2)-1))
                        current_repeat.append(str((j-(k-2)) - (t+minLen+(k-1))))
                        current_repeat.append(str(t+1))
                        current_repeat.append(''.join(genome[t:t+minLen+k-1]))
                        current_repeat.append(str(t+minLen+(k-1)))
                        current_repeat.append(str(j-(k-2)))
                        current_repeat.append(''.join(genome[j-(k-1):j+minLen]))
                        current_repeat.append(str(j+minLen))
                        current_repeat.append('\n')

                        inc += k

                        current_str = '\t'.join(current_repeat)
                        outfile.write(current_str)
                        break

                break
        
        t += inc

mainFunction()

outfile.close()


if len(argv) < 2:

    print('results saves as {a}\n'.format(a = outfileName))

    print('\n\n----------------------------------------')
    print('----------------------------------------')

