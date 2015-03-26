import operator
def compactCode(input='',groupLines=None,changeIndents=4,indentLevel=4):
    if groupLines not in(False, None)and type(groupLines)not in(int, float): groupLines=50
    input=input.replace('"""',"'''").split("'''");input=''.join(input[::2]);
    loopNames=set(i+j for i in ('for','if','while','return','try','except','else','finally','elif','class','def','with') for j in (" ","(",":"))
    input = input.replace('\\','\\\\').replace('\r\n','\\r\\n')
    removeSpace=list('+-*/=!<>%,.()[]{}:');outputList=[];inLineTextMarker=";txt.{};";textSymbols=["'",'"']
    indentMultiplier=float(changeIndents)/indentLevel
    for line in str(input).split('\n'):
        #Remove comments
        line=line.split("#")[0]
        #Don't affect text
        textStorage={}
        while True:
            #Find the earliest symbol
            symbolOccurrances={}
            for symbol in textSymbols:
                numOccurrances = line.find(symbol)
                if numOccurrances >= 0:
                    symbolOccurrances[symbol]=numOccurrances
            try:symbol=sorted(symbolOccurrances.items(),key=operator.itemgetter(1))[0][0]
            except:break
            if len(symbolOccurrances.items())==1 and line.count(symbol)==1:break
            textStorage[symbol]=[]
            ignoreSymbol=False
            #Make sure there is not only 1 of those symbols left
            if line.count(symbol)%2==1:
                ignoreSymbol=True
            #Replace the text so it won't be cut down later
            while symbol in line and (not ignoreSymbol or line.count(symbol)>1):
                splitByText=line.split(symbol,1)
                line=splitByText[0]+inLineTextMarker
                if symbol in splitByText[1]:
                    textSplit=splitByText[1].split(symbol,1)
                    line+=textSplit[1]
                    textStorage[symbol].append(textSplit[0])
                else:
                    line+=splitByText[1]
                    break
            line=line.replace(inLineTextMarker,inLineTextMarker.format(ord(symbol)))
        #Remove double spaces
        stripLine=line.lstrip(' ')
        leadingSpace=len(line)-len(stripLine)
        while '  ' in stripLine:
            stripLine=stripLine.replace('  ',' ')
        line = stripLine
        if stripLine:
            #Remove unnecessary spaces
            for i in removeSpace:
                line=line.replace(' '+i,i).replace(i+' ',i)
            #Replace the text
            while True:
                resultsExist={symbol:True for symbol in textSymbols}
                for symbol in textSymbols:
                    currentTextMarker=inLineTextMarker.format(ord(symbol))
                    while currentTextMarker in line:
                        line=line.replace(currentTextMarker,symbol+textStorage[symbol].pop(0)+symbol,1)
                    if currentTextMarker not in line:
                        resultsExist[symbol]=False
                if not any(x in line for x in (inLineTextMarker.format(ord(symbol)) for symbol in textSymbols)):
                    break
            #Group together lines
            if groupLines:
                lastLine=None
                try:
                    lastLine = outputList[-1]
                except:
                    pass
                if lastLine:
                    lastLineLength = len(lastLine)
                    lastLineStripped = lastLine.lstrip()
                    lastLineStrippedLength = len(lastLineStripped)
                    lastIndent = lastLineLength-lastLineStrippedLength
                    lastLength = lastLineStrippedLength
                    #Make sure it is of the same indent, and doesn't mark the start of a loop
                    if leadingSpace == lastIndent:
                        if lastLineStrippedLength+len(line)<groupLines:
                            if all(x not in line[:8] for x in loopNames) and all(x not in line for x in ('@staticmethod','@classmethod')):
                                line=lastLineStripped+';'+line
                                outputList.pop(-1)
            line=' '*int(leadingSpace*indentMultiplier)+line
            outputList.append(line.rstrip())
    return '\r\n'.join(outputList)
