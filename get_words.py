
word_list = []
count = 0
with open('subjclueslen1-HLTEMNLP05.tff') as f:
    with open('subjectivity.txt', 'w') as v:

        while (True):
            try:
                line = f.readline()
                word = line[line.find("word1")+6:line.find("pos1")-1]
                if word == '':
                    break
                v.write("%s" % word)
                count += 1
                if count%100==0:
                    print(count)
                v.write("," )

            except EOFError:
                break

