import operator
def compactCode(input='',groupLines=None,changeIndents=4,indentLevel=4,**kwargs):
    if groupLines not in(False, None)and type(groupLines)not in(int, float): groupLines=50
    try:maxEfficiency=kwargs["max"]
    except:pass
    else:
        if maxEfficiency:groupLines=-1;changeIndents=1
    input=input.replace('"""',"'''").split("'''");input=''.join(input[::2]);
    #Loops that may have the contents on the same line
    ifNames=set(i+j for i in ('if','else','elif','try','except','finally','for','with') for j in (" ","(",":"))
    #Things that may not be grouped on above lines
    loopNames=set(i+j for i in ('while','return','class','def') for j in (" ","(",":"))|ifNames
    input = input.replace('\\','\\\\').replace('\r\n','\\r\\n')
    removeSpace=list('+-*/=!<>%,.()[]{}:');outputList=[];inLineTextMarker=";txt.{};";textSymbols=["'",'"']
    indentMultiplier=float(changeIndents)/indentLevel
    for line in str(input).split('\n')+['end']:
        #Remove comments
        line=line.split("#")[0]
        #Don't affect text
        textStorage={}
        lastSymbolFail=None
        while True:
            #Find the earliest symbol
            symbolOccurrances={}
            for symbol in textSymbols:
                placeOfOccurrance = line.find(symbol)
                if placeOfOccurrance >= 0 and line.count(symbol)>1:
                    symbolOccurrances[symbol]=placeOfOccurrance
            try:symbol=sorted(symbolOccurrances.items(),key=operator.itemgetter(1))[0][0]
            except:break
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
        leadingSpace=int((len(line)-len(stripLine))*indentMultiplier)
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
                        if lastLineStrippedLength+len(line)<groupLines or groupLines<0:
                            if all(x not in line[:8] for x in loopNames) and all(x not in line for x in ('@staticmethod','@classmethod')):
                                line=lastLineStripped+';'+line
                                outputList.pop(-1)
                #Group the if, else, try and except statements
                oneLineAgo,twoLinesAgo=None,None
                try:
                    twoLinesAgo,oneLineAgo=outputList[-2:]
                except:
                    pass
                if oneLineAgo and twoLinesAgo:
                    oneLineAgoStrip=oneLineAgo.lstrip()
                    twoLinesAgoStrip=twoLinesAgo.lstrip()
                    oneLineAgoIndentLevel = len(oneLineAgo)-len(oneLineAgoStrip)
                    #Check the current indent is less than the last line, and the last line indent is greater than the 2nd last line
                    if leadingSpace<oneLineAgoIndentLevel:
                        if int(oneLineAgoIndentLevel-indentLevel*indentMultiplier)==len(twoLinesAgo)-len(twoLinesAgoStrip):
                            #Make sure 2 lines ago was a statement, but the latest line wasn't
                            if any(x in twoLinesAgoStrip[:7] for x in ifNames) and all(x not in oneLineAgoStrip[:7] for x in ifNames):
                                outputList[-2] = twoLinesAgo+oneLineAgoStrip
                                outputList.pop(-1)
            line=' '*leadingSpace+line
            outputList.append(line.rstrip())
    return '\r\n'.join(outputList[:-1])
