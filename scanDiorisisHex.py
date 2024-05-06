import json, io, sys, os, importlib, itertools, re, platform, pickle
from icecream import ic
ic.configureOutput(includeContext=True)
import prosodyScanner
from utf2beta import convertUTF as utf2beta
from beta2utf import convertBeta as beta2utf
isWindows = 'Windows' in platform.platform()
clear = 'cls' if isWindows else r"clear && printf '\e[3J'"
os.system(clear)
print('Loading files...')
scansions = json.load(open('greekScansions.json', 'r', encoding="utf8"))
solFile = 'prosodyOutput/0012.002.solutions.json'
textFile = 'prosodyInput/0012.002.json'
temporaryScan = 'prosodyOutput/0012.002.scan.p'

document_solutions = json.load(open(solFile,'r')) if os.path.isfile(solFile) else {}

arsis = f"({'|'.join(prosodyScanner.lg)})"
thesis = f"({'|'.join(prosodyScanner.lg.union(prosodyScanner.py))})"
anceps = f"({'|'.join(prosodyScanner.lg.union(prosodyScanner.br))})"
metreRe = re.compile(f"{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{anceps}")
size = 12

def saveTextFile():
	global text, textFile
	with open(textFile,'w') as o:
		o.write('{"tokens": [\n')
		json_lines = ',\n'.join([json.dumps(t,ensure_ascii=False) for t in text['tokens']])
		o.write(json_lines)
		o.write('\n]}')

if not os.path.isfile(temporaryScan):
	print('Scanning...')
	text = json.load(open(textFile,'r'))
	document_stream = io.StringIO()
	newLine = True
	punctuation = ''
	noSpPunct = False
	nlBeg = True
	newScans = False
	corrections = False
	line = '// '
	
	hex_patterns = set()
	tmpH = set()
	for h in [g*2 for g in ['a'+'a'.join(x) for x in itertools.product(['a','bb'],repeat=4)]]:
		for u in range(int(len(h)/2)):
			hex_patterns.add(h[u:u+int(len(h)/2)])

	for e,token in enumerate(text['tokens']):
		nl = False
		for k,v in token['symbol_at'].items():
			if v == '<br/>':
				if k == '0':
					line = '// '
					document_stream.write('\n')
					nl = False
					nlBeg = True
				else: nl = True
		if token['type'] == 'word':
			if not nlBeg and not noSpPunct:
				line += ' '
				document_stream.write(' ')
		if token['type'] == 'punct':
			if token['token'] in '(“«':
				noSpPunct = True
				if not nlBeg:
					line += ' '
					document_stream.write(' ')
			else: noSpPunct = False
		line += token['token']
		document_stream.write(token['token'])
		
		if token['type'] == 'word':
			noSpPunct = False
			while True:
				form = token['token']
				if not scansions.get(utf2beta(form)):
					matching = set()
					prosody = prosodyScanner.doc(form=form)
					if len(prosody.scannedDocument) == 0:
						break	
					prosody = prosody.scannedDocument[0]
					if '?' in prosody[1]['scansion']:
						syllables=prosody[1]['syllables']
						print('\n',line,'\n',f'Form to be scanned: {form}',sep='')
						print('\t','\n\t'.join([f'{e}: {s}' for e,s in enumerate(syllables)]),sep='')
						if input('Type c to correct spelling errors in the form, hit return if there are none: ') == 'c':
							document_stream.seek(document_stream.tell()-len(form))
							document_stream.truncate()
							line = line[:-len(form)]
							form = input('Enter correct form: ')
							token['token'] = form
							corrections = True
							document_stream.write(form)
							line += form
							continue
						if input('If there are errors in the current scansion, enter e to correct them manually: ') == 'e':
							suppletions = []
							while True:
								action = input('Enter index of syllable to edit (return to exit): ')
								if len(action) == 0:
									print()
									break
								elif action.isnumeric():
									suppletions.append([int(action),input(f'Enter scansion of {syllables[int(action)]}: ').replace('lb','⏓').replace('bl','⏒').replace('b','⏑').replace('s','⏑͜').replace('-','–').replace('l','–')])
						else:	
							matchPattern = ''
							matchCombo = ''
							for e,(sy,sc) in enumerate(syllables):
								if sc == '?': matchPattern += '.'
								if sc in prosodyScanner.lg: matchCombo += 'a'
								if sc in prosodyScanner.br: matchCombo += 'b'
								if len(matchCombo) > 1: matchPattern += f'[{matchCombo}]'
								else: matchPattern += matchCombo
								matchCombo = ''
							for h in hex_patterns:
								if (m:=re.search(matchPattern,h)): matching.add(m.group(0))
							matchingSuppletions = []
							for m in matching:
								tmpM = []
								for e,(sy,sc) in enumerate(syllables):
									if sc == '?': tmpM.append((e, sy, {'a':'–','b':'⏑'}[m[e]]))
									else: tmpM.append((e, sy, sc))
								if tmpM not in matchingSuppletions: matchingSuppletions.append(tmpM)
							print('Is any of the following scansions correct?'*bool(matchingSuppletions))
							for e,m in enumerate(matchingSuppletions):
								print(f'    [{e}] {m}')
							if bool(matchingSuppletions) and (m:=input('Enter number of correct scansion or hit return if none is correct: ')).isnumeric():
								suppletions = [[e,q] for e,z,q in matchingSuppletions[int(m)] if syllables[e][1] == '?']
							else:
								suppletions = []
								for e,(sy,sc) in enumerate(syllables):
									if sc != '?': continue
									q = input(f'Enter scansion of {sy}: ').replace('lb','⏓').replace('bl','⏒').replace('b','⏑').replace('s','⏑͜').replace('-','–').replace('l','–')
									if len(q.split(',')) > 1:
										for extra in q.split(',')[1:]:
											suppletions.append([int(x) if x.isnumeric() else x for x in extra.split(':')])
										q = q.split(',')[0]
									suppletions.append([e,q])
						scansions[utf2beta(form)] = list(sorted(suppletions, key=lambda x: x[0]))
						with open('greekScansions.json','w',encoding='utf8') as nf:
							nf.write(json.dumps(scansions, ensure_ascii=False))
						newScans = True
				break
		if nlBeg: nlBeg = False
		if nl:
			line = '// '
			document_stream.write('\n')
			nl = False
			nlBeg = True
	if newScans:
		importlib.reload(prosodyScanner)
	if corrections:
		print('Saving corrections to source file...')
		saveTextFile()
	document_stream.seek(0,0)
	document_scan = prosodyScanner.doc(stream=document_stream,verse=True,metre='hex')
	pickle.dump(document_scan,open(temporaryScan,'wb'))
	document_scan.display(problems=True)
else: document_scan = pickle.load(open(temporaryScan,'rb'))


def checkSolutions(scan,solution):
	for problem,solution in solution.items():
		problem = int(problem)
		scan['scansion'] = scan['scansion'].replace('⏑͜', 'a').replace('⏓͜','b').replace('⏒͜','c')
		scan['scansion'] = scan['scansion'][:problem] + solution + scan['scansion'][problem+1:]
		scan['scansion'] = scan['scansion'].replace('a','⏑͜').replace('b','⏓͜').replace('c','⏒͜')
		scan['syllables'] = scan['syllables'][:problem] + [(scan['syllables'][problem][0], solution)] + scan['syllables'][problem+1:]
	if (res:=metreRe.match(scan['scansion'])):
		scan['analysis'] = 'hexameter'
	return scan

saveScan = False
if any([type(f) != list for f in document_scan.scannedDocument]):
	print('Rescan')
	sys.exit()

for e,(line, data) in enumerate(document_scan.scannedDocument):
	sys.stdout.write(f'\r\033[K{e}')
	sys.stdout.flush()
	if data['analysis'] != '?': continue
	if (solutions:=document_solutions.get(str(e))):
		newData = checkSolutions(data,document_solutions[str(e)])
		if newData['analysis'] != '?':
			document_scan.scannedDocument[e][1] = newData
			# ic(document_scan.scannedDocument[e])
			saveScan = True
			continue
	if (solvedScan:=prosodyScanner.doc(form=line,verse=True,metre='hex').scannedDocument[0][1])['analysis'] != '?':
		document_scan.scannedDocument[e][1] = solvedScan
		# ic(document_scan.scannedDocument[e])
		saveScan = True
		continue
	solved = False
	undo = None
	special = {}
		
	if solved: continue
	print(f'\r\033[K[{e}]',line)
	print(data['scansion'])
	print('\n'.join([str([h,d]) for h,d in enumerate(data['syllables'])]))
	print()

	solutionAdded = False
	while True:
		action = input('Edit syllable (enter index) or edit word (type word) (hit return to exit)? ')
		if len(action) == 0:
			print()
			break
		if action == '®':
			importlib.reload(prosodyScanner)
			scansions = json.load(open('greekScansions.json', 'r', encoding="utf8"))
		elif action.isnumeric():
			document_solutions.setdefault(str(e),{})
			document_solutions[str(e)][action] = input(f'Enter scansion of {data["syllables"][int(action)]}: ').replace('lb','⏓').replace('bl','⏒').replace('b','⏑').replace('s','⏑͜').replace('-','–').replace('l','–')
			if document_solutions[str(e)][action] != '':
				with open(solFile,'w',encoding='utf8') as o:
					o.write(json.dumps(document_solutions,ensure_ascii=False,sort_keys=True))
				solutionAdded = True
			else: del document_solutions[str(e)][action]
			print()
		else:
			tmpScan = []
			prosody = prosodyScanner.doc(form=action).scannedDocument[0]
			print([f'{e}: {s}' for e,s in enumerate(prosody[1]['syllables'])])
			suppletions = {}
			while True:
				whichSyll = input('What syllable shall we edit? ')
				if not whichSyll.isnumeric():
					print()
					break
				if (sus:=input(f'Enter scansion for {prosody[1]["syllables"][int(whichSyll)][0]}: ').replace('lb','⏓').replace('bl','⏒').replace('b','⏑').replace('s','⏑͜').replace('-','–')) in list('–⏓⏒⏑⏑͜'):
					suppletions[int(whichSyll)] = sus
			if form:=scansions.get(utf2beta(action)):
				for k,v in suppletions.items():
					already = False
					for g,(sy,sc) in enumerate(form):
						if sy == k:
							scansions[utf2beta(action)][g] = [k,v]
							already = True
					if not already:
						scansions[utf2beta(action)].append([k,v])
				scansions[utf2beta(action)] = list(sorted(scansions[utf2beta(action)], key=lambda x: x[0]))
				with open('greekScansions.json','w',encoding='utf8') as nf:
					nf.write(json.dumps(scansions, ensure_ascii=False))
			else:
				for k,v in sorted(suppletions.items(),key=lambda x: x[0]):
					scansions.setdefault(utf2beta(action).replace('\\','/'),[]).append([k,v])
				with open('greekScansions.json','w',encoding='utf8') as nf:
					nf.write(json.dumps(scansions, ensure_ascii=False))