#########################################################################
#                           QUICK  REFERENCE                            #
#                                                                       #
# Paths to set up:                                                      #
#                                                                       #
# · textFile: lemmatized Diorisis file (here: the Iliad)                #
#                                                                       #
# · solFile: file containing the solutions to metrical irregularities   #
#            in the text (here: in the Iliad)                           #
#                                                                       #
# · outputFile: the script will produce a file based on the lemmatized  #
#               text plus all metrical information with the following   #
#               structure:                                              #
#                                                                       #
#               - JSON file with dictionary as the root.                #
#               - The dictionary contains the entries 'text',           #
#                 'caesura_stats', and 'irregularities'.                #
#                                                                       #
#               • TEXT (list):                                          #
#                                                                       #
#                 Each item in the list is a dictionary corresponding   #
#                 to a line in the text. The dictionary contains the    #
#                 following entries:                                    #
#                                                                       #
#                 › location: book and line                             #
#                                                                       #
#                 › line: UTF text of the line                          #
#                                                                       #
#                 › scansion: scansion (metrical symbols)               #
#                                                                       #
#                 › analysis: automatically detected metre              #
#                                                                       #
#                 › syllables: a list containing lists for each         #
#                              syllable in the line. For each syllable  #
#                              the UTF representation (with the symbol  #
#                              '#' for word boundaries) and the scan-   #
#                              sion are given.                          #
#                                                                       #
#                 › caesurae: a dictionary containing all caesurae in   #
#                             the line. Keys correspond to the half-    #
#                             foot where the caesura is located (range  #
#                             1–12, e.g. 5 = penthemimeral). If caesu-  #
#                             rae are located after the first breve in  #
#                             a dactyl, their location is represented   #
#                             with a decimal (e.g. 5.5 = κατὰ τὸν       #
#                             τρίτον τροχαῖον). Values contain a        #
#                             dictionary with the following entries:    #
#                             the index of the syllable at which the    #
#                             caesura falls; the half-foot containing   #
#                             the caesura; the Diorisis data for the    #
#                             words immediately preceding and immedia-  #
#                             tely following the caesura.               #
#                                                                       #
#                 › in_scansion: scansion of the line displaying the    #
#                                locations of caesurae (symbol: '|').   #
#                                                                       #
#                 › caesura_combination: specifies if the line displays #
#                                        one of the common caesura pat- #
#                                        terns (see below).             #
#                                                                       #
#                 › irregularities: the index, alteration, form, in-    #
#                                   word location, word form, lemma,    #
#                                   context, and possible explanation   #
#                                   of metrically irregular syllables.  #
#                                   Implemented types of metrical ir-   #
#                                   regularities include: lengthening   #
#                                   before /n/, /m/, and /r/ (<*sr),    #
#                                   digamma in specific lexemes, first- #
#                                   syllable in line, lengthening at    #
#                                   caesura, non-lenghtening before     #
#                                   Σκάμανδρος etc.                     #
#                                                                       #
#               • CAESURA_STATS (dict):                                 #      
#                                                                       #
#                 › combination_frequency: a dictionary containing the  #
#                                      raw frequency of lines that dis- #
#                                      play the following combinations  #
#                                      of caesurae:                     #
#                                      - trith(emimeral) + penth(em.) + #
#                                        hephth(em.)                    #
#                                      - trith + hephth                 #
#                                      - trith + penth                  #
#                                      - trith + bucd (bucolic diaer.)  #
#                                      - penth + hephth                 #
#                                      - penth + bucd                   #
#                                      - katatt (κατὰ τὸν τρίτον τρο-   #
#                                        χαῖον) + hephth                #
#                                      - katatt + bucd                  #
#                                      - trith + katatt                 #
#                                      - trith + penth + bucd           #
#                                      - trith + katatt + bucd          #
#                                                                       #
#                 › caesura_frequency: a dictionary containing the raw  #
#                                      frequencies for caesurae at each #
#                                      location (indicated as above).   #
#                                                                       #
#               • IRREGULARITY_STATS (dict):                            #
#                                                                       #
#                 › post_lengthening_consonants: a list of tuples con-  #
#                                  taining the raw frequency of conso-  #
#                                  nants that follow lenghtened sylla-  #
#                                  bles.                                #
#                                                                       #
#                 › lexemes_lost_sounds: a list containing all lexemes  #
#                                  whose form occur after a lengthened  #
#                                  syllable in the previous form. List  #
#                                  of tuples containing each lexeme,    #
#                                  its frequency following a lengthened #
#                                  syllable, and its total raw frequen- #
#                                  cy in the text.                      #
#                                                                       #
#                 › altered_forms: a list containing all forms that un- #
#                                  dergo metrical lengthening or shor-  #
#                                  tening. Each form is listed as a tu- #
#                                  ple containing the following items:  #
#                                  [0]form; [1] the altered syllable,   #
#                                  [2] its index in the word, [3] the   #
#                                  type of alteration, [4] the raw fre- #
#                                  quency of such alteration in the     #
#                                  text, [5] the total frequency of the #
#                                  form in the text, [6] a list of tu-  #
#                                  ples containing possible explanati-  #
#                                  ons for the alteration and their raw #
#                                  frequencies.                         #
#                                                                       #
#########################################################################


import json, os, sys, re, platform, copy
from icecream import ic
import prosodyScanner
from utf2beta import convertUTF as utf2beta
from beta2utf import convertBeta as beta2utf
isWindows = 'Windows' in platform.platform()
clear = 'cls' if isWindows else r"clear && printf '\e[3J'"
os.system(clear)

def isConsonant(_letter):
	return _letter in list('bgdzqklmncprstfxy')

def normalizeForm(_form):
	return beta2utf(re.sub('(.*?[=/].*?)/(.*?)', r'\1\2', utf2beta(_form).replace('\\','/')))

def isPostpositive(_word):
	_form = _word['token'].lower()
	_lemma = str(_word['lemma'])
	return ((not re.search(r'[/\\=\']',utf2beta(_form))) and (_form not in ['εἰ','ὁ','ἡ','οὐ','οὐκ','οὐχ','εἰς','ἐς','ἐξ','ἐκ','ὡς','αἱ', 'ἐν'] or (form == 'οἱ' and  'dat' not in _lemma))) or re.search(r'^(δ[έὲήὴῆ’\'](που|θεν|πουθεν|τα)?|[κγτ][έ’\']|μ[έὲήὴ]ν(τοι)?|γ?οὖν|γ[άὰ]ρ|μ[ήὴ]ν|[ἄἂ][ρν]|πέρ|πού|τοί|ἄρ[’α]|[μσ]έ)$', _form)

def isPrepositive(_word): #maybe add ὅς to stoplist?
	_pos = _word['lemma'][0]['POS']
	return (_pos in ['conjunction', 'preposition', 'article'] and not re.search('(θεν?$|οὕνεκ)', _word['token'].lower())) or _word['lemma'][0]['entry'] == 'o(/s'

def compensateSolutions(_solutions,_index,_procSyllableIndex):
	_compensation = max(len(_solutions.get(str(_index),{}).get(str(_procSyllableIndex-1),'').replace('͜','')) - 1, 0)
	return _procSyllableIndex + _compensation, _compensation

def irregularity_diagnostics(_irregularity,_currentWord,_syllabifiedWords,_beforeCaesura,_caesuraLocation):
	_diagnosis = []
	_altered_form = None
	_altered_syllable = utf2beta(_irregularity['form'])
	_isFinalSyllable = _irregularity['index'] == sorted(_syllabifiedWords[_currentWord].keys())[-1]
	_hasFinalConsonant = isConsonant(_altered_syllable[-1])
	_nextConsonant = _altered_syllable[-1] if _hasFinalConsonant \
			else _nextWordInitial if _isFinalSyllable and isConsonant(_nextWordInitial:=utf2beta(_irregularity['context']['token'])[0]) \
			else _nextSyllableInitial if not _isFinalSyllable and isConsonant(_nextSyllableInitial:=utf2beta(_syllabifiedWords[_currentWord][_irregularity['index']+1][1])[0]) \
			else None

	_nextLexeme = beta2utf(_irregularity['context']['lemma'][0]['entry']) if _irregularity['context'] else None

	# option -1: resolved -ου
	if _irregularity["alteration"] == 'resolution': _diagnosis.append('resolved diphthong')

	else:

		# option 0: line initial
		if _irregularity['index'] == 0: _diagnosis.append(f'verse initial {_irregularity["alteration"]}')

		# option 1a: before n
		elif _nextConsonant == 'n': _diagnosis.append(f'{_irregularity["alteration"]} before /n/')

		# option 1b: before m-
		elif _nextConsonant == 'm': _diagnosis.append(f'{_irregularity["alteration"]} before /m/')

		# option 1c: before r-
		elif _nextConsonant == 'r': _diagnosis.append(f'{_irregularity["alteration"]} before /r/')

		# option 2: etymological fun
		elif _nextLexeme in ['ὅς','ἔπος','ἑ', 'εἶπον','ἰάχω', 'λίσσομαι', 'ὡς', 'ἐρῶ', 'ἰαχή', 'ὅτε', 'δήν', 'οἶκος', 'οἶδα', 'δεινός', 'δέος', 'δείδω', 'ἔτος', 'Ἑλικών', 'ἐρύω', 'εἰκός', 'ἶφι', 'Ἴλιος', 'Δεῖμος', 'εἶδος', 'ἔργον', 'δειλός', 'οἶνος', 'οἰνίζομαι', 'δηρός', 'Οἰνεύς', 'ἔλπω', 'Ἰλήϊος'] or (_nextLexeme and _nextLexeme[:4] == 'δεισ'): _diagnosis.append(f'{_irregularity["alteration"]} before {_nextLexeme}')

		elif _nextLexeme == 'ὅς' and _irregularity['context']['token'] == 'oi(': _diagnosis.append(f'{_irregularity["alteration"]} before ἑ')

		# option 4: at caesura
		if _beforeCaesura and _caesuraLocation in [3,5,5.5,7,8]: _diagnosis.append(f'before caesura at {_caesuraLocation}')

		if _irregularity['alteration'] == 'shortening' and _nextLexeme and re.search('Σκ[αά]μ', _nextLexeme): _diagnosis.append(f'{_irregularity["alteration"]} before {_nextLexeme}')

		# option 6: whatever
		if len(_diagnosis) == 0:
			_diagnosis.append(f'metrical {_irregularity["alteration"]}')
			_altered_form = True

	# ic(_irregularity['word form'], _irregularity['form'], _diagnosis)

	return (_altered_syllable, _nextConsonant, _diagnosis, _altered_form)

solFile = 'prosodyOutput/0012.001.solutions.json'
textFile = 'prosodyInput/0012.001.json'
outputFile = 'prosodyOutput/0012.001.scanned.json'
metre = 'hex'

print('Loading files...')
scansions = json.load(open('greekScansions.json', 'r', encoding="utf8"))
solutions = json.load(open(solFile,'r'))

if metre == 'hex':
	arsis = f"({'|'.join(prosodyScanner.lg)})"
	thesis = f"({'|'.join(prosodyScanner.lg.union(prosodyScanner.py))})"
	anceps = f"({'|'.join(prosodyScanner.lg.union(prosodyScanner.br))})"
	beatSeq = [arsis,thesis,arsis,thesis,arsis,thesis,arsis,thesis,arsis,thesis,arsis,anceps]
	size = 12

metreRe = re.compile(''.join(beatSeq))

text = json.load(open(textFile,'r'))
textLines = []
parsedText = []
tmpLine = ''
noSpPunct = False
nlBeg = True
lineCounter = 0
tokenTracker = {}
tokenInLineTracker = {}
tokenInLineCounter = 0
formCounter = {}
lexemeCounter = {}

print('Preprocessing...')
for e,token in enumerate(text['tokens']):
	# sys.stdout.write('\r\033[KProcessing token '+str(e)+' ...')
	# sys.stdout.flush()
	nl = False
	for k,v in token['symbol_at'].items():
		if v == '<br/>':
			if k == '0':
				textLines.append((currentLocation,tmpLine))
				tokenTracker[lineCounter] = copy.deepcopy(tokenInLineTracker)
				lineCounter += 1
				tokenInLineCounter = 0
				tokenInLineTracker = {}
				tmpLine = ''
				nl = False
				nlBeg = True
			else: nl = True
	currentLocation = token.get('section',e)
	if token['type'] == 'word':
		tokenInLineTracker[tokenInLineCounter] = e
		tokenInLineCounter += 1
		if not nlBeg and not noSpPunct: tmpLine += ' '
	if token['type'] == 'punct':
		if token['token'] in '(“«':
			noSpPunct = True
			if not nlBeg: tmpLine += ' '
		else: noSpPunct = False
	tmpLine += token['token']
	if nlBeg: nlBeg = False
	if nl:
		textLines.append((currentLocation,tmpLine))
		tokenTracker[lineCounter] = copy.deepcopy(tokenInLineTracker)
		lineCounter += 1
		tokenInLineCounter = 0
		tokenInLineTracker = {}
		tmpLine = ''
		nl = False
		nlBeg = True
	if token['type'] == 'word':
		noSpPunct = False
		form = token['token']
		formToCount = normalizeForm(form)
		formCounter.setdefault(formToCount,0)
		formCounter[formToCount] += 1
		lexemeToCount = beta2utf(token['lemma'][0]['entry'])
		lexemeCounter.setdefault(lexemeToCount,0)
		lexemeCounter[lexemeToCount] += 1

print('\nScanning...')
toDelete = []
caesuraStats = {}
caesuraCombinations = {
	'trith+penth+hephth': 0,
	'trith+katatt+hephth': 0,
	'trith+hephth': 0,
	'penth+hephth': 0,
	'katatt+hephth': 0,
	'trith+penth': 0,
	'trith+katatt': 0,
	'trith+penth+bucd': 0,
	'trith+katatt+bucd': 0,
	'trith+bucd': 0,
	'penth+bucd': 0,
	'katatt+bucd': 0
}

_next_consonants = {}
_next_lexemes = {}
_altered_forms = {}

for e,(location,line) in enumerate(textLines):
	sys.stdout.write('\r\033[KScanning line '+str(e)+'...')
	sys.stdout.flush()
	res = None
	scan = prosodyScanner.doc(form=line,verse=True,metre=metre).scannedDocument[0][1]
	words = [w for w in re.split(r'[,\(\)<>\"“”«»\{\}\[\]—\-– \.··;:]',line) if len(w) > 0]
	potentialSynizesis = False

	#assign syllables to words
	syllablesByWord = []
	tmpSyllables = {}
	lastSet = None
	for j,syllable in enumerate(scan['syllables']):
		for ip,p in enumerate(syllable[0].split('#')):
			if ip > 0:
				syllablesByWord.append(tmpSyllables)
				tmpSyllables = {}
			if re.search('[aeihowu]',utf2beta(p)):
				tmpSyllables.setdefault(j,[len(tmpSyllables),p])
				lastSet = j
			elif len(tmpSyllables) > 0: tmpSyllables[lastSet][-1] += p 
	syllablesByWord.append(tmpSyllables)

	#add solutions
	if solutions.get(str(e)):
		for problem,solution in solutions[str(e)].items():
			problem = int(problem)
			scan['scansion'] = scan['scansion'].replace('⏑͜', 'a').replace('⏓͜','b').replace('⏒͜','c')
			if solution == scan['scansion'][problem]:
				print(line,scan['scansion'],problem,solution)
				print('Deleting',e,problem)
				toDelete.append((str(e),str(problem)))
				scan['scansion'] = scan['scansion'].replace('a','⏑͜').replace('b','⏓͜').replace('c','⏒͜')
				continue
			scan['scansion'] = scan['scansion'][:problem] + solution + scan['scansion'][problem+1:]
			scan['scansion'] = scan['scansion'].replace('a','⏑͜').replace('b','⏓͜').replace('c','⏒͜')
			scan['syllables'] = scan['syllables'][:problem] + [(scan['syllables'][problem][0], solution)] + scan['syllables'][problem+1:]

	#resolve ambiguities
	if (res:=metreRe.match(scan['scansion'])):
		if metre == 'hex':
			correction = ['']*size
			scan['analysis'] = 'hexameter'
			for i in range(1,size+1):
				if i in [1,3,5,7,9,11]: #arsis positions
						correction[i-1] = '–' if len(res.group(i)) <= 2 else re.sub('[⏒⏓]$', '–', res.group(i)) #allow for synizesis
				elif i < 12:
					if res.group(i) in prosodyScanner.py:
						if len(res.group(i)) in (2,3): correction[i-1] = '⏑⏑'
						else: correction[i-1] = re.sub('͜$', '', re.sub('[⏒⏓]','⏑', res.group(i)))
					elif res.group(i) in prosodyScanner.lg: 
						correction[i-1] = re.sub('[⏒⏓]$', '–', re.sub('͜$', '', re.sub('[^⏑]͜[^$]', '⏑͜', res.group(i))))
				else: #final anceps
					correction[i-1] = res.group(i)
					if correction[i-1][-1] == '͜': correction[i-1] = correction[i-1][:-1]
		scan['scansion'] = ''.join(correction)
		res=metreRe.match(scan['scansion'])
	# ic(words)
	wordIndex = 0
	scan['irregularities'] = []
	
	#hexameter analysis
	if metre == 'hex':
		syCount = 0
		syTotalCount = 0
		caesurae = {}
		caesuraeLocations = []
		whatIsInSegment = [None]
		if not res: res = metreRe.match(scan['scansion'])
		resolveSyll = False
		cliticChain = False
		for i in range(1,size+1):
			syCountAugm = False
			syllablesInFoot = []
			foot = ''
			# ic(i, res.group(i), end ='\t')
			if resolveSyll:
				resolveSyll = False
				continue
			try:
				res.group(i)
			except:
				ic(e,line,res,scan)
			tmpSyll = []
			for sy in res.group(i):
				try:
					currSyllable, currScan = scan['syllables'][syCount]
				except:
					ic(e,location,line,res)
					ic(list(enumerate(scan['syllables'])))
					ic(i,res.group(i),sy,syCount)
					input()
				if sy != '͜':
					foot += currSyllable
					tmpSyll.append(currSyllable)
					syCount += 1
					syCountAugm = True
				else: potentialSynizesis = True
				if len(currScan.replace('͜','')) > 1:
					resolveSyll = True

			previousSegment = whatIsInSegment[-1]
			wordSegments = [f.replace('§','#') for f in foot.replace('#','§#').split('#')]
			whatIsInSegment = [2 if s == '' else bool(re.search('[aeihowu]',utf2beta(s))) for s in wordSegments]
			segmentedSyllables = [x for t in tmpSyll for x in t.split('#') if x != '']
			syllInSegments = []

			counter = 0
			tmpSyll = []
			tmpWord = ''

			for ws,segment in enumerate(wordSegments):
				tmpSegment = segment.replace('#','')
				if whatIsInSegment[ws] == 2:
					syllInSegments.append([])
					break
				if tmpSegment == segmentedSyllables[counter]:
					if whatIsInSegment[ws] == 1: tmpSyll = [segmentedSyllables[counter]]
					counter += 1
				else:
					while True:
						if re.search('[aeihowu]',utf2beta(segmentedSyllables[counter])) or len(tmpSyll) == 0: tmpSyll.append(segmentedSyllables[counter])
						else: tmpSyll[-1] += segmentedSyllables[counter]
						tmpWord += segmentedSyllables[counter]
						counter += 1
						if tmpWord == tmpSegment:
							tmpWord = ''
							break
				syllInSegments.append(tmpSyll)
				tmpSyll = []

			segmentData = zip(wordSegments,whatIsInSegment,syllInSegments)
			
			caesuraIndex = None
			processedIrregularities = set()
			processedSyllables = 0
			for sc,(wordSegment, segment, syllablesInSegment) in enumerate(segmentData):
				# print('\n\n')
				currentSequence = res.group(i)[processedSyllables:processedSyllables+len(syllablesInSegment)]
				processedSyllables += len(syllablesInSegment) + ('͜' in currentSequence)
				syTotalCount += len(syllablesInSegment) + ('͜' in currentSequence)
				previousWord = {k:v for k, v in text['tokens'][fwi].items()  if k in ['token','lemma']} if (fwi:=tokenTracker[e].get(wordIndex-1)) is not None else {}
				currentWord = {k:v for k, v in text['tokens'][tokenTracker[e][wordIndex]].items() if k in ['token','lemma']}
				followingWord = {k:v for k, v in text['tokens'][fwi].items()  if k in ['token','lemma']} if (fwi:=tokenTracker[e].get(wordIndex+1)) else None
				if '#' in wordSegment:
					wordIndex += 1

				#find caesurae
				isCaesura = False
				currentPrepositive = isPrepositive(currentWord)
				currentPostpositive = isPostpositive(currentWord)
				followingPostpositive = followingWord and isPostpositive(followingWord)
				followingPrepositive = followingWord and isPrepositive(followingWord)

				if currentWord['token'] == 'σέ' and not followingPostpositive: currentPostpositive = False

				if cliticChain and not currentPostpositive: cliticChain = False

				# ic(i, wordSegment,sc,segment,currentPrepositive,currentPostpositive,cliticChain)
				if '#' in wordSegment and not (currentPrepositive or followingPostpositive or (cliticChain and not followingPrepositive)):
					isCaesura = True
					# ic(isCaesura)
					caesuraSyllable, compensation = compensateSolutions(solutions,e,syTotalCount)
					syTotalCount += compensation
					caesuraIndex = i
					if ((sc == 0 and segment == 1) or\
						(sc == 1 and segment == 1 and not whatIsInSegment[0])) \
						and len([w for w in whatIsInSegment if w == 1]) > 1:
						caesuraIndex -= .5
					elif sc == 0 and segment == 0 or\
					 	(sc == 1 and segment == 1 and not currentPostpositive):
						caesuraIndex -= 1
				# if caesuraIndex == 7.5:
				# 	print()
				# if isCaesura:
				# 	ic(line, caesuraIndex, caesuraSyllable, sc, wordSegments, segmentedSyllables, whatIsInSegment, sc, wordSegment,segment,currentWord['token'],currentPostpositive,currentPrepositive,followingPostpositive,cliticChain,syTotalCount,solutions.get(str(e)))
				# 	input()

				if currentPrepositive: cliticChain = True
				elif not currentPostpositive: cliticChain = False

				if isCaesura:
					# ic(f'{currentWord = }, {followingWord = }', end='\t')
					# ic('Caesura at',caesuraIndex,caesuraSyllable,end='\t')
					if resolveSyll:
						caesuraIndex += 1
					caesuraeLocations.append(caesuraSyllable)
					caesurae.setdefault(caesuraIndex,{}).update({'syllable':caesuraSyllable, 'foot': foot, 'previousWord': currentWord, 'followingWord':followingWord})

				
				# ic(res.group(i), syTotalCount, wordSegments[sc],currentWord,followingWord,isCaesura, caesuraIndex)

				
				#classify metrical irregularities
				if syCount-syCountAugm in processedIrregularities: continue
				if solutions.get(str(e),{}).get(str(syCount-syCountAugm)):
					processedIrregularities.add(syCount-syCountAugm)
					if solutions[str(e)][str(syCount-syCountAugm)] == '⏑͜': continue
					tmpIrregularity = {'index':syCount-syCountAugm}
					currentWordIndex = [h for h,w in enumerate(words) if syllablesByWord[h].get(syCount-syCountAugm)][0]
					currentWord = {k:v for k, v in text['tokens'][tokenTracker[e][currentWordIndex]].items() if k in ['token','lemma']}
					followingWord = {k:v for k, v in text['tokens'][fwi].items()  if k in ['token','lemma']} if (fwi:=tokenTracker[e].get(currentWordIndex+1)) else None
					solvedWord = currentWord['token']
					solvedWord = normalizeForm(solvedWord)
					tmpIrregularity['word form'] = solvedWord
					tmpIrregularity['context'] = followingWord
					solvedSyllableIndex, solvedSyllable = syllablesByWord[currentWordIndex][syCount-syCountAugm]
					tmpIrregularity['form'] = solvedSyllable
					tmpIrregularity['in-word location'] = solvedSyllableIndex
					solvedLexeme = beta2utf(currentWord['lemma'][0]['entry'])
					tmpIrregularity['lemma'] = solvedLexeme
					solDirection = 'lengthening' if solutions[str(e)][str(syCount-syCountAugm)] == '–' else 'shortening' if len(solutions[str(e)][str(syCount-syCountAugm)].replace('͜','')) == 1 else 'resolution'
					tmpIrregularity['alteration'] = solDirection
					if len(solutions[str(e)][str(syCount-syCountAugm)]) > 1: solDirection = 'resolveEnding'
					try:
						diagnostics = irregularity_diagnostics(tmpIrregularity,currentWordIndex,syllablesByWord, isCaesura, caesuraIndex)
					except Exception as ex:
						ic(e,line,tmpIrregularity)
						input(ex)
					_next_consonants.setdefault(diagnostics[1],0)
					_next_consonants[diagnostics[1]] += 1
					try:
						_next_lexemes.setdefault(nextLexeme:=beta2utf(followingWord['lemma'][0]['entry']), 0)
						_next_lexemes[nextLexeme] += 1
						# ic(line,solvedWord,nextLexeme,_next_lexemes[nextLexeme])
					except: pass
					diagnosis = ','.join(diagnostics[2])
					alteredForm = (solvedWord, solvedSyllable, solvedSyllableIndex, solDirection)
					_altered_forms.setdefault(alteredForm,{'count':0,'diagnosis':{}})
					_altered_forms[alteredForm]['count'] += 1
					_altered_forms[alteredForm]['diagnosis'].setdefault(diagnosis,0)
					_altered_forms[alteredForm]['diagnosis'][diagnosis] += 1
					tmpIrregularity['diagnosis'] = diagnostics[2]
					scan['irregularities'].append(tmpIrregularity)
		caesuraeLocations = sorted(list(set(caesuraeLocations)),reverse=True)
		scansionWithCaesurae = scan['scansion']
		for l in caesuraeLocations:
			scansionWithCaesurae = scansionWithCaesurae[:l] + '|' + scansionWithCaesurae[l:]
		scansionWithCaesurae.replace('||','|')
		caesurae['in_scansion'] = scansionWithCaesurae
		# ic(e, line,list[caesurae.keys()],caesuraeLocations,scansionWithCaesurae,[t['previousWord']['token'] for k,t in caesurae.items() if not isinstance(k,str)])
		# input()
		scan['caesurae'] = caesurae

		#caesura stats
		for k in caesurae.keys():
			if isinstance(k,str): continue
			caesuraStats.setdefault(k,0)
			caesuraStats[k] += 1
		if all([c in caesurae.keys() for c in [5,5.5]]): caesuraStats[5.5] -= 1
		if all([c in caesurae.keys() for c in [3,5,7]]): 
			caesuraCombinations['trith+penth+hephth'] += 1
			scan['caesura_combination'] = 'trith+penth+hephth'
		if all([c in caesurae.keys() for c in [3,5.5,7]]):
			caesuraCombinations['trith+katatt+hephth'] += 1
			scan['caesura_combination'] = 'trith+katatt+hephth'
		if all([c in caesurae.keys() for c in [3,7]]) and not caesurae.get(5,caesurae.get(5.5)):
			caesuraCombinations['trith+hephth'] += 1
			scan['caesura_combination'] = 'trith+hephth'
		if all([c in caesurae.keys() for c in [5,7]]) and not caesurae.get(3): 
			caesuraCombinations['penth+hephth'] += 1
			scan['caesura_combination'] = 'penth+hephth'
		if all([c in caesurae.keys() for c in [5.5,7]]) and not caesurae.get(3): 
			caesuraCombinations['katatt+hephth'] += 1
			scan['caesura_combination'] = 'katatt+hephth'
		if all([c in caesurae.keys() for c in [3,5]]) and not caesurae.get(7): 
			caesuraCombinations['trith+penth'] += 1
			scan['caesura_combination'] = 'trith+penth'
		if all([c in caesurae.keys() for c in [3,5.5]]) and not caesurae.get(7): 
			caesuraCombinations['trith+katatt'] += 1
			scan['caesura_combination'] = 'trith+katatt'
		if all([c in caesurae.keys() for c in [3,5,8]]):
			caesuraCombinations['trith+penth+bucd'] += 1
			scan['caesura_combination'] = 'trith+penth+bucd'
		if all([c in caesurae.keys() for c in [3,5.5,8]]):
			caesuraCombinations['trith+katatt+bucd'] += 1
			scan['caesura_combination'] = 'trith+katatt+bucd'
		if all([c in caesurae.keys() for c in [3,8]]) and not caesurae.get(5,caesurae.get(5.5)): 
			caesuraCombinations['trith+bucd'] += 1
			scan['caesura_combination'] = 'trith+bucd'
		if all([c in caesurae.keys() for c in [5,8]]) and not caesurae.get(3): 
			caesuraCombinations['penth+bucd'] += 1
			scan['caesura_combination'] = 'penth+bucd'
		if all([c in caesurae.keys() for c in [5.5,8]]) and not caesurae.get(3): 
			caesuraCombinations['katatt+bucd'] += 1
			scan['caesura_combination'] = 'katatt+bucd'

	parsedText.append({'location':location, 'line':line, **scan})
	if scan['analysis'] != 'hexameter':
		print(e, parsedText[-1])
		ic(list(enumerate(parsedText[-1]['syllables'])))
		input()
altering_lexemes = sorted(_next_lexemes.items(), key=lambda x: x[1], reverse=True)
altering_lexemes = [(a,b,lexemeCounter[a]) for (a,b) in altering_lexemes]
altering_consonants = sorted(_next_consonants.items(), key=lambda x: x[1], reverse=True)
altered_forms = sorted([(k,v) for k,v in _altered_forms.items()],key=lambda x:x[1]['count'],reverse=True)
altered_forms = [(a,b,c,d,data["count"],formCounter[a],sorted(data["diagnosis"].items(), key=lambda x: x[1],reverse=True)) for (a,b,c,d),data in altered_forms]

# print(parsedText)
finalOutput = {'text':parsedText,'irregularity_stats':{'lexemes_lost_sounds':altering_lexemes,'post_lengthening_consonants':altering_consonants, 'altered_forms':altered_forms},'caesura_stats':{'combination_frequency':caesuraCombinations,'caesura_frequency':caesuraStats}}
for (solution,problem) in toDelete:
	del solutions[solution][problem]
redundant_solutions = []
for solution,s in solutions.items():
	if len(s) == 0: redundant_solutions.append(solution)
with open(solFile,'w') as w:
	json.dump(solutions,w,ensure_ascii=False)
with open(outputFile,'w') as w:
	json.dump(finalOutput,w,ensure_ascii=False)
print('\nScansion completed.')

def showData():
	while True:
		print('Show: [1] Lexemes that determine metrical irregularities due to sound changes\n      [2] Consonants occurring after metrically lengthened syllables\n      [3] All metrically irregular forms\n      [4] Violations of Hermann\'s bridge\n      [5] Raw and relative frequency (percent) of caesurae at metrical locations\nor [e]xit: ' ,end="")
		command = input()
		print()
		if command == '1':
			for a,b,c in altering_lexemes:
				print(a,b,c,sep=',')
		if command == '2':
			for a,b in sorted(altering_consonants, key=lambda x: x[1],reverse = True):
				if a: print(a,b)
		if command == '3':
			for (a,b,c,d,e,f,g) in altered_forms:
				print(f'{a},{"‑"*(c>0)}{b}{"‑"*(b!=a[-len(b):])},{"–" if d == "lengthening" else "⏑"},{e},{f},{"; ".join([":".join([str(j) for j in h]) for h in g])}')
		if command == '4':
			counter = 0
			for line in parsedText:
				if line['caesurae'].get(7.5):
					context = line['caesurae'][7.5]['previousWord']['token']
					if '’' in context: continue
					if len(re.findall('[aehiowu]',utf2beta(context))) > 1:
						counter += 1
						print(f'[{counter}]')
						print(line)
						input()
		if command == '5':
			for location, number in sorted(caesuraStats.items(),key=lambda x: x[0]):
				print(location,number,number*100/len(parsedText),sep=',')
		if command == 'e': return
		print()