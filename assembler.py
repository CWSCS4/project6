#!/usr/bin/env python

import sys

compTranslate={
    ''    : '000000',
    '0'   : '101010',
    '1'   : '111111',
    '-1'  : '111010',
    'D'   : '001100',
    'A'   : '110000',
    '!D'  : '001101',
    '!A'  : '110001',
    '-D'  : '001111',
    '-A'  : '110011',
    'D+1' : '011111',
    'A+1' : '110111',
    'D-1' : '001110',
    'A-1' : '110010',
    'D+A' : '000010',
    'D-A' : '010011',
    'A-D' : '000111',
    'D&A' : '000000',
    'D|A' : '010101',
    'M'   : '110000',
    '!M'  : '110001',
    '-M'  : '110011',
    'M+1' : '110111',
    'M-1' : '110010',
    'D+M' : '000010',
    'D-M' : '010011',
    'M-D' : '000111',
    'D&M' : '000000',
    'D|M' : '010101'
}

destTranslate={
    ''    :'000',
    'M'   :'001',
    'D'   :'010',
    'MD'  :'011',
    'A'   :'100',
    'AM'  :'101',
    'AD'  :'110',
    'AMD' :'111'
}

jumpTranslate={
    ''    : '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
}

storedValues = {
    'SP'    :'0',
    'LCL'   :'1',
    'ARG'   :'2',
    'THIS'  :'3',
    'THAT'  :'4',
    'R0'    :'0',
    'R1'    :'1',
    'R2'    :'2',
    'R3'    :'3',
    'R4'    :'4',
    'R5'    :'5',
    'R6'    :'6',
    'R7'    :'7',
    'R8'    :'8',
    'R9'    :'9',
    'R10'   :'10',
    'R11'   :'11',
    'R12'   :'12',
    'R13'   :'13',
    'R14'   :'14',
    'R15'   :'15',
    'SCREEN':'16384',
    'KBD'   :'24576'
}

def translateComp(comp1):
    comp = ''.join(comp1)
    if comp=="A+D":
        comp=comp[::-1]
    if comp=="A&D":
        comp=comp[::-1]
    if comp=="A|D":
        comp=comp[::-1]
    if comp=="M+D":
        comp=comp[::-1]
    if comp=="M&D":
        comp=comp[::-1]
    if comp=="M|D":
        comp=comp[::-1]
    return compTranslate[comp]
def aInstruct(inputvalue):
    return format(inputvalue,'016b').decode('ascii')
def cInstruct(inputvalue):
    temp = sys.maxint
    try:
        if inputvalue.index("=") < temp:
            temp=inputvalue.index("=")
    except:
        pass
    try:
        if inputvalue.index(";") < temp:
            temp=inputvalue.index(";")
    except:
        pass
    typesel = inputvalue[temp]
    comp = ""
    dest = ""
    jump = ""
    if typesel=="=":
        inputvalue.replace(";","=")
        ivlist = inputvalue.split("=")
        if len(ivlist) == 3:
            dest=ivlist[0]
            comp=ivlist[1]
            jump=ivlist[2]
        else:
            dest=ivlist[0]
            comp=ivlist[1]
    if typesel==";":
        ivlist = inputvalue.split(";")
        comp=ivlist[0]
        jump=ivlist[1]

    compT=translateComp(comp)
    destT=destTranslate[dest]
    jumpT=jumpTranslate[jump]
    abit="0"
    if "M" in comp:
        abit="1"
    return "111"+abit+compT+destT+jumpT

def symbolFormat(inputL):
    toRemove = 0
    current = 16
    for i in range(len(inputL)):
        inputL[i]=inputL[i].replace(" ","")
        if inputL[i][0] == '(':
            toRemove+=1
            temp = inputL[i][1:-1]
            if not (temp in storedValues):
                storedValues[temp]=str(i-toRemove+1)

    for i in range(len(inputL)):
        inputL[i]=inputL[i].replace(" ","")
        if inputL[i][0] == "@":
            if not inputL[i][1:].isdigit() and not inputL[i][1:] in storedValues:
                storedValues[inputL[i][1:]]=str(current)
                current+=1
            if not inputL[i][1:].isdigit():
                inputL[i]=inputL[i].replace(inputL[i][1:],storedValues[inputL[i][1:]])
    inputL = filter(lambda x:x[0]!="(",inputL)
    return inputL

masterlist = ""
instructions = ""
for line in sys.stdin:
    instructions+=line
ilist = instructions.splitlines()
ilist = filter(lambda x:(x!='' and  x[:2]!="//"),ilist)
ilist=symbolFormat(ilist)
ilist = filter(lambda x:x!="(",ilist)
for i in range(len(ilist)):
    ilist[i]=ilist[i].replace(" ","")
    try:
        ilist[i]=ilist[i][:ilist[i].index("//")]
    except:
        pass
    
    if ilist[i][0]=='@':
        masterlist=masterlist+'\n'+(aInstruct(int(ilist[i][1:])))
    else:
        masterlist=masterlist+'\n'+(cInstruct(ilist[i]))
print masterlist[1:]
