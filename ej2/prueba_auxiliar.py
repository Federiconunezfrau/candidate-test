
import re

with open('memdump0.mem','rt') as file_input:
    text = file_input.read()

    #pattern = re.compile(r'  reg \[(.*)\] (\S*) \[(.*)\];\n')

    #match = pattern.search(text)
    #out = match.group()
    #out = match.end()
    #print(text[24:])

    # pattern_2 = re.compile(r' \S*;')
    # pattern_2 = re.compile(r'[\d\s]*\'[s\s]*[\w]*')
    # match_2 = pattern_2.search(text)
    # out = match_2.group()
    # print(out)

    # out = text.split('initial begin')

    # line_0 = out[0]
    # print(line_0)
    #line_2 = out[1]
    #text_2 = line_2.split(';')
    # out_2 = pattern_2.search(out[1])
    # line_2 = out_2.group()
    # print(line_2)
    #print(text_2)
    #pattern = re.compile(r'(?<=[\d\s]\'s?[\w])[\S]*;')
    pattern = re.compile(r'(?<=[\d\s]\'[\w])[\w]*')
    match = pattern.findall(text)
    #out = match.group()
    print(match)