import operator
def compactCode(input='',groupMaxSpaces=None,changeIndents=4,indentLevel=4,**kwargs):
    
    #Check that grouping is not disabled, and set to 50 if it is not a number
    if groupMaxSpaces not in (False, None) and type(groupMaxSpaces) not in (int, float): 
        groupMaxSpaces=50
        
    #Auto set variables to the best efficiency if 'max' is given
    try:
        maxEfficiency=kwargs["max"]
    except:
        pass
    else:
        if maxEfficiency:
            groupMaxSpaces=-1
            changeIndents=1
    
    #If text should also be affected
    ignoreText = False
    try:
        ignoreText=kwargs["ignoreText"]
    except:
        pass
    
    #Remove all triple quoted comments
    input=input.replace('"""',"'''").split("'''");input=''.join(input[::2]);
    
    possibleSuffixes=list("( :")
    #Conditions that may have their contents on the same line
    groupableNames=set(i+j for i in ('if','else','elif','try','except','finally','for','with','while') for j in possibleSuffixes)
    #Conditions which can't be moved up a line
    fixedNames={x:len(x) for x in set(i+j for i in ('class','def') for j in possibleSuffixes)|groupableNames|{'@staticmethod','@classmethod'}}
    
    input = input.replace('\\','\\\\').replace('\r\n','\\r\\n')
    removeSpace=list('+-*/=!<>%,.()[]{}:')        #These items will have all spaces next to them removed
    inLineTextMarker=";txt.{};"
    textSymbols=["'",'"']        #Add to this to preserve text if text is defined by anything other than quotation marks and speech marks
    if ignoreText: 
        removeSpace+=textSymbols
        textSymbols=[]
    indentMultiplier=float(changeIndents)/indentLevel
    outputList=[]
    
    for line in str(input).split('\n')+[';endoflist;']:
        
        #Remove comments
        line=line.split("#")[0]
        
        #Replace text as to avoid it being affected
        textStorage={}
        lastSymbolFail=None
        
        #Loop until all text is replaced
        while True:
            
            #Find the first symbol
            symbolOccurrances={}
            for symbol in textSymbols:
                placeOfOccurrance = line.find(symbol)
                #Only add to dictionary if there is more than one symbol
                if placeOfOccurrance >= 0 and line.count(symbol)>1:
                    symbolOccurrances[symbol]=placeOfOccurrance
                    
            #Get the first occurance, or break loop if there is none
            try:
                symbol=sorted(symbolOccurrances.items(),key=operator.itemgetter(1))[0][0]
            except:
                break
            textStorage[symbol]=[]
            
            #Replace the text so it won't be cut down later
            while symbol in line:
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
        
        if stripLine:
            
            #Remove unnecessary spaces
            for i in removeSpace:
                stripLine=stripLine.replace(' '+i,i).replace(i+' ',i)
                
            #Replace the text markers with the actual text again
            while True:
                resultsExist={symbol:True for symbol in textSymbols}
                for symbol in textSymbols:
                    currentTextMarker=inLineTextMarker.format(ord(symbol))
                    while currentTextMarker in stripLine:
                        stripLine=stripLine.replace(currentTextMarker,symbol+textStorage[symbol].pop(0)+symbol,1)
                    if currentTextMarker not in stripLine:
                        resultsExist[symbol]=False
                if not any(x in stripLine for x in (inLineTextMarker.format(ord(symbol)) for symbol in textSymbols)):
                    break
                    
            #Group together lines
            if groupMaxSpaces:
                lastLine=None
                try:
                    lastLine = outputList[-1]
                except:
                    pass
                if lastLine and stripLine!=';endoflist;':
                    lastLineLength = len(lastLine)
                    lastLineStripped = lastLine.lstrip()
                    lastLineStrippedLength = len(lastLineStripped)
                    lastIndent = lastLineLength-lastLineStrippedLength
                    lastLength = lastLineStrippedLength
                    #Make sure the last space is of the same indent, and doesn't mark the start of a loop
                    if leadingSpace == lastIndent:
                        if lastLineStrippedLength+len(stripLine)<groupMaxSpaces or groupMaxSpaces<0:
                            if all(x not in stripLine[:y] for x, y in fixedNames.iteritems()):
                                stripLine=lastLineStripped+';'+stripLine
                                outputList.pop(-1)
                                
                #Group to the conditional statements
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
                            if any(x in twoLinesAgoStrip[:7] for x in groupableNames) and all(x not in oneLineAgoStrip[:7] for x in groupableNames):
                                outputList[-2] = twoLinesAgo+oneLineAgoStrip
                                outputList.pop(-1)
            
            #Add the indent and repeat
            line=' '*leadingSpace+stripLine
            outputList.append(line.rstrip())
    
    return '\r\n'.join(outputList[:-1])
