#Diorisis Scan

import re, sys, json, os, string, platform, io, itertools
dt = True
mCl = False
try:
	import datrie
except:
	if not os.path.isfile('dt'):
		dt = os.system('pip3 install datrie')
		if dt == 0:
			import datrie
		else:
			open('dt','w+')
			dt = False
			print('\nWarning: the Python module "datrie" cannot be installed on your system. Please refer to the above error message for a possible solution and contact the administator of this system if necessary.')
	else:
		dt = False
	if not dt:
		input('DiorisisScan is running without the module "datrie". Part of the algorithm will be disabled and it might happen that certain syllables will not be scanned.')
else:
	if os.path.isfile('dt'):
		os.remove('dt')
			
from utf2beta import convertUTF as utf2beta
from beta2utf import convertBeta as beta2utf
if len(os.path.dirname(__file__)) > 0: os.chdir(os.path.dirname(__file__))

scanTrie = None
dictionary ={}

isWindows = 'Windows' in platform.platform()

if isWindows:
	import ctypes
	from ctypes.wintypes import *
	from ctypes import *
	pw = True
	try:
		import win32gui
	except:
		pw = os.system('pip3 install pywin32')
		if pw == 0: pw = False


	#flags
	LF_FACESIZE = 32
	STD_OUTPUT_HANDLE = -11
	handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
	_WriteFile = ctypes.windll.kernel32.WriteFile
	_SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute

	class COORD(ctypes.Structure):
		_fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

	class CONSOLE_FONT_INFOEX(ctypes.Structure):
		_fields_ = [("cbSize", ctypes.c_ulong),
					("nFont", ctypes.c_ulong),
					("dwFontSize", COORD),
					("FontFamily", ctypes.c_uint),
					("FontWeight", ctypes.c_uint),
					("FaceName", ctypes.c_wchar * LF_FACESIZE)]
			
	#Get console font
	currentFont = CONSOLE_FONT_INFOEX()
	currentFont.cbSize = sizeof(CONSOLE_FONT_INFOEX)
	if not ctypes.windll.kernel32.GetCurrentConsoleFontEx(handle, c_long(False), ctypes.pointer(currentFont)):
		print("Failed to fetch font.")

	#Check if font is installed
	def callback(font, tm, fonttype, names):
		names.append(font.lfFaceName)
		return True

	fontnames = []
	if pw:
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, callback, fontnames)

	if not "DJVSM  Metrical" in fontnames:
		#Temporarily load font
		from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
		import win32print
		import win32ui
		file = ctypes.byref(ctypes.create_unicode_buffer("DJVSMM.ttf"))
		font_count = ctypes.windll.gdi32.AddFontResourceExW("DJVSMM.ttf", 0, 0)
		if(font_count == 0):
			print("Error loading font.")
		else:
			#Notify running programmes
			try:
				user32 = ctypes.windll('user32', use_last_error=True)		
			except:
				user32 = ctypes.WinDLL('user32', use_last_error=True)		
			user32.SendMessageTimeoutW.restype = wintypes.LPVOID
			user32.SendMessageTimeoutW.argtypes = (
				wintypes.HWND,   # hWnd
				wintypes.UINT,   # Msg
				wintypes.LPVOID, # wParam
				wintypes.LPVOID, # lParam
				wintypes.UINT,   # fuFlags
				wintypes.UINT,   # uTimeout
				wintypes.LPVOID) # lpdwResult

			HWND_BROADCAST   = 0xFFFF
			SMTO_ABORTIFHUNG = 0x0002
			WM_FONTCHANGE	= 0x001D
			GFRI_DESCRIPTION = 1
			GFRI_ISTRUETYPE  = 3
			user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, None)

	#Set metrical font
	font = CONSOLE_FONT_INFOEX()
	font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
	font.nFont = 12
	font.dwFontSize.X = 11
	font.dwFontSize.Y = 18
	font.FontFamily = 54
	font.FontWeight = 400
	font.FaceName = "DJVSM  Metrical"
	ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

	def restoreFont():
		ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(currentFont))
		ctypes.windll.gdi32.RemoveFontResourceExW("DJVSMM.ttf", 0, 0)

def loadDictionary():
	global dictionary, scanTrie
	dictionary = json.load(open('greekScansions.json', 'r', encoding="utf8"))
	if dt:
		scanTrie = datrie.Trie(string.printable)
		for k,v in dictionary.items():
			scanTrie[k] = v

if __name__ != '__main__': loadDictionary()
		
long_vowels = ['h','w']
short_vowels = ['e','o']
ancipites = ['a','i','u']
diphthongs = ['ai','ei','oi','ui','au','eu','ou','a|','hi','h|','wi','w|','hu','wu']
scans = {'long':'–','short':'⏑','inv_anceps':'⏓','eli/syn':'⏑͜'}
verbose = True
verse = True
width = 15

#metrical elements
py = {'⏒͜⏓', '⏓͜⏑͜', '⏓͜⏓͜', '⏓⏓͜', '⏒͜⏒', '⏑⏓͜', '⏑͜⏑͜', '⏓⏑͜', '⏑⏓', '⏒͜⏑͜', '⏑⏑͜', '⏑͜⏑', '⏑⏒', '⏒⏑', '⏓⏒͜', '⏓͜⏑', '⏑͜⏓͜', '⏓⏒', '⏒⏑͜', '⏒⏓', '⏒⏒', '⏒⏒͜', '⏒͜⏑', '⏑͜⏒', '⏓͜⏒͜', '⏒⏓͜', '⏒͜⏒͜', '⏓⏑', '⏑⏑', '⏓͜⏓', '⏑⏒͜', '⏓͜⏒', '⏓⏓', '⏒͜⏓͜', '⏑͜⏓', '⏑͜⏒͜'}
br = {'⏑', '⏑͜', '⏓','⏒','⏓͜','⏒͜'}
lg = {'⏑͜–', '⏓', '⏑͜⏒', '⏑͜⏓', '⏒', '–','⏓͜','⏒͜'}

metreCycle = ['4anap^','hex','pent','4tr^','3ia','3ia/s','gl','ph','sapph','adon'] #longer first


class _externalFile:
	def __init__(self, filename, *args):
		if os.path.isfile(filename):
			self.verse = args[0] if args else False
			self.text = open(filename,'r',encoding='utf-8').read()
			self.text = self.text.replace('\n',' @ ') if self.verse else self.text.replace('\n', ' ')
		else:
			print('File not found.')
			sys.exit()

class _word:
	def __init__(self, form):
		self._form = form
		self.parse = [(character,self.type(character)) for character in re.sub('([^A-Za-z]+)\|',r'|\1',utf2beta(beta2utf(form).lower()))]
	def type(self,character):
		if character in long_vowels + short_vowels + ancipites: return 'vowel'
		if re.match('[A-Za-z]',character) and character not in long_vowels + short_vowels + ancipites: return 'consonant'
		if character == '#': return 'break'
		return 'diacritic'
	def isLastSyllable(self, index):
		for i in range(1,len(self.parse)-index):
			if self.parse[index+i][1] == 'vowel' or self.parse[index+i][0] == "'": return False
		return True
	def whereIsAccent(self):
		revSearch = self.parse[::-1]
		count = 0
		activeVowel = ''
		activeDiacritics = []
		diacritics = []
		for i in range(0,len(revSearch)):
			if revSearch[i][1] == 'diacritic' and revSearch[i][0] != "'": activeDiacritics.append(revSearch[i][0])
			if revSearch[i][1] == 'consonant': activeVowel = ''
			if revSearch[i][1] == 'vowel' or revSearch[i][0] == "'":
				count += 1
				diacritics.append(activeDiacritics)
				activeDiacritics = []
				if revSearch[i][0] in ['a','e','o','h','w'] and revSearch[i-1][0] in ['i','u'] and i > 0:
					if '+' not in diacritics[count-2] : count -=1
				if revSearch[i][0] in 'u' and activeVowel == 'i':
					if '+' not in diacritics[count-2]: count -=1
				if '/' in diacritics[-1]: return ('/', count)
				if '\\' in diacritics[-1]: return ('\\', count)
				if '=' in diacritics[-1]: return ('=', count)
				activeVowel = revSearch[i][0]
	def previous_vowel(self, index):
		revSearch = self.parse[:index+1][::-1]
		for i in range(1,len(revSearch)):
			if revSearch[i][1] == 'consonant': break
			if revSearch[i][1] == 'vowel': return revSearch[i][0]
		return False
	def next_vowel(self, index):
		for i in range(1,len(self.parse)-index):
			if self.parse[index+i][1] == 'consonant': break
			if self.parse[index+i][1] == 'vowel': return self.parse[index+i][0]
		return False
	def next_consonant(self, index):
		self.nextConsonantLocation = False
		for i in range(1,len(self.parse)-index):
			if self.parse[index+i][1] == 'vowel': break
			if self.parse[index+i][1] == 'consonant':
				self.nextConsonantLocation = index + i
				return self.parse[index+i][0]
		return False
	def letter_diacritics(self, index):
		diacritics = []
		for i in range(1,len(self.parse)-index):
			if self.parse[index+i][1] == 'diacritic': diacritics.append(self.parse[index+i][0])
			else: break
		return diacritics
	def shortToLong(self,index):
		if next_consonant := self.next_consonant(index):
			if next_consonant in ['c','y','z']: return 'long' #double consonant
			if self.nextConsonantLocation == len(self.parse) -1: 
				return 'anceps' #word-final consonant
			if consonant_cluster:=self.next_consonant(self.nextConsonantLocation):
				if consonant_cluster in ['l','r'] and not next_consonant in ['l','r'] and mCl: return 'short' #positio debilis
				if consonant_cluster in ['l','r'] and not next_consonant in ['l','r']: return 'anceps' #muta cum liquida
				return 'long'
		return False
	def add_before_coda(self,form,addition):
		if self.type(form[0][-1]) == 'consonant':
			return form[0][:-1] + addition + form[0][-1]
		else: return form[0] + addition
	def syllabify(self):
		TMPsyll = []
		index = 0
		toParse = []
		for e,c in enumerate(self.parse):
			if c[0] == '|': toParse.append(('i','vowel'))
			elif c[0] in ['r','l']: toParse.append((c[0],'liquid consonant'))
			elif c[0] not in ['#',"'",'’']: toParse.append(c)
			elif len(toParse) > 0: toParse[-1] = (toParse[-1][0]+c[0],toParse[-1][1])
		for e,x in enumerate(toParse):
			x = list(x)
			if e == len(toParse) -1 and 'consonant' in x[1]:
				index += 1
				TMPsyll.append([index, x])
				break
			if x[1] == 'vowel':
				if e> 0 and ((x[0][0] not in ['i','u'] and toParse[e-1][1] in ['vowel','diacritic']) or (x[0][0] in ['i','u'] and (toParse[e-1][1] == 'diacritic' or toParse[e-1][0][0] in ['i','u']))):
					index += 1
					TMPsyll.append([index, ('','boundary')])
				index += 1
				TMPsyll.append([index, x])
			if x[0] == '+':
				index -= .4
				TMPsyll.append([index, ('','boundary')])
				index += 1
			if x[1] == 'diacritic':
				index += .3
				TMPsyll.append([index, x])
			if 'consonant' in x[1]:
				if toParse[e+1][1] == 'consonant' or ('consonant' in toParse[e+1][1] and (not mCl or 'liquid' in x[1])):
					index += 1
					TMPsyll.append([index, x])
					if e-1 >= 0:
						if 'consonant' not in toParse[e-1][1]:
							index += 1
							TMPsyll.append([index, ('','boundary')])
				else:
					if e-1 >= 0 and e+1 < len(toParse):
						if 'consonant' not in toParse[e-1][1] and (toParse[e+1][1] == 'vowel' or (x[1] == 'consonant' and 'liquid' in toParse[e+1][1] and mCl)):
							index += 1
							TMPsyll.append([index, ('','boundary')])
					index += 1
					TMPsyll.append([index, x])
		syllables = ''
		for y in sorted(TMPsyll, key=lambda x:x[0]):
			syllables += y[1][0] if y[1][1] != 'boundary' else '|'
		syllables=[s for s in syllables.split('|') if s!='']
		return syllables

	def scan(self, *keepByNature):
		output = []
		corr_idx = {}
		nd_idx = 0
		byNature = '—'
		self.nd = [_ for _ in self.parse]
		for iNd,symbol in enumerate(self.nd):
			if iNd+1 < len(self.nd) and iNd > 0:
				if ((self.nd[iNd-1][0] in ['a','e','h','o','w'] and symbol[0] in ['i','u']) or (self.nd[iNd-1][0] == 'u' and symbol[0] == 'i')) and '+' not in self.letter_diacritics(iNd):
					self.nd[iNd] = (symbol[0],'diacritic')
			if self.nd[iNd][1] != 'diacritic':
				corr_idx.setdefault(iNd,nd_idx)
				nd_idx += 1
		self.nd = [_ for _ in self.nd if _[1] != 'diacritic']
		syllables = self.syllabify()
		syllIdx = 0
		for index, (letter,type) in enumerate(self.parse):
			if letter == '|':
				self.parse[index] = ('i','vowel')
				letter = 'i'
				type = 'vowel'
			if letter in long_vowels:
				output.append([syllables[syllIdx],byNature])
				syllIdx += 1
				if self.next_vowel(index) in ['a','e','h','o','w']: #uocalis ante uocalem
					output[-1] = [output[-1][0],'⏓']
				continue
			if letter in short_vowels:
				scans['anceps'] = '⏒'
				output.append([syllables[syllIdx],'⏑'])
				syllIdx += 1
				if self.shortToLong(index): output[-1] = [output[-1][0],scans[self.shortToLong(index)]]
				continue
			if letter in ancipites:
				scans['anceps'] = '?'
				previous_vowel = self.previous_vowel(index) #second element of diphthong
				if previous_vowel in ['a','e','o','h','w'] and letter in ['i','u'] and '+' not in self.letter_diacritics(index) and not self.parse[index-1][1] == 'diacritic':
					output[-1] = [output[-1][0],byNature]
					if self.next_vowel(index) in ['a','e','i','h','o','u','w']: #diphthong ante uocalem
						output[-1] = [output[-1][0],'⏓']
					continue
				if letter == 'i' and previous_vowel == 'u' and '+' not in self.letter_diacritics(index) and not self.parse[index-1][1] == 'diacritic':
					output[-1] = [self.add_before_coda(output[-1],letter), byNature]
					continue
				if len([_ for _ in ['=','_', '|'] if _ in self.letter_diacritics(index)]): #circumflex,macron, iota subscript
					output.append([syllables[syllIdx], byNature])
					syllIdx += 1
					continue
				if self.shortToLong(index):
					output.append([syllables[syllIdx],scans[self.shortToLong(index)]])
					syllIdx += 1
					continue
				if self.next_vowel(index) in ['a','e','h','o','w']: #uocalis ante uocalem
					if not dictionary.get(self._form.strip(), dictionary.get(self._form.replace('+','').strip(), dictionary.get(re.sub('(.*?[=/].*?)/(.*?)', r'\1\2', self._form).strip(), dictionary.get(self._form.replace('a','h').strip(), None)))):
						output.append([syllables[syllIdx],'⏑'])
						syllIdx += 1
						continue
				if letter == 'a' and self.next_vowel(index) in ['i','u']:
					output.append([syllables[syllIdx],'⏑'])
					syllIdx += 1
					continue
				output.append([syllables[syllIdx],'?'])
				syllIdx += 1
		try: #length of last based on accent
			if output[-1][1] == '?':
				if self.whereIsAccent() == ('=', 2) or self.whereIsAccent() == ('/', 3):
					output[-1] = [output[-1][0], '⏑'] if self.parse[-1][1] != 'consonant' else [output[-1][0],'⏒']
				if self.whereIsAccent() == ('/', 2) and len(output) > 1:
					if output[-2][1] == '—': output[-1] = [output[-1][0], '–']
					if output[-1][1] in ['⏑','⏒'] and output[-2][1] == '?': output[-2] = [output[-2][0], '⏑']
		except:
			pass
		try: #length of penultimate based on accent
			if output[-2][1] == '?' and output[-1][1] == '⏑' and self.whereIsAccent() == ('/', 2):
				output[-2] = [output[-2][0], '⏑']
		except:
			pass
		outputIndexes = [0] + list(itertools.accumulate([len(s[0]) for s in output]))[:-1]
		if dt and (dentry:=dictionary.get(self._form.strip(), dictionary.get(self._form.replace('+','').strip(), dictionary.get(re.sub('(.*?[=/].*?)/(.*?)', r'\1\2', self._form).strip(), dictionary.get(self._form.replace('a','h').strip(), None))))):
			for dSyll in dentry:
				if dSyll[1] == '⏒' and mCl:
					v = [l for l in output[dSyll[0]][0] if self.type(l) == 'vowel'][0]
					index = output[dSyll[0]][0].index(v)+outputIndexes[dSyll[0]]
					if self.shortToLong(index):
						dSyll[1] = scans[self.shortToLong(index)]
				output[dSyll[0]][1] = dSyll[1]
		elif any([True for o in output if o[1] == '?']):
			if dt:
				if hit:=scanTrie.keys(self._form[:-2]):
					model = scanTrie.get(hit[0])
					for dSyll in model:
						if dSyll[0] >= len(output): break
						if dSyll[1] == '⏒' and mCl:
							v = [l for l in output[dSyll[0]][0] if self.type(l) == 'vowel'][0]
							index = output[dSyll[0]][0].index(v)+outputIndexes[dSyll[0]]
							if self.shortToLong(index):
								dSyll[1] = scans[self.shortToLong(index)]
						output[dSyll[0]][1] = dSyll[1]
		if not keepByNature[0]: 
			output = [[o[0],o[1].replace('—','–')] for o in output]

		#test synizesis
		for e,s in enumerate(output):
			if e > 0:
				if (s[0][0] in long_vowels + ancipites + short_vowels or s[0][:2] in diphthongs) and s[1] in ['–','⏓'] and re.sub('[^a-z]','',output[e-1][0])[-1] in short_vowels + ancipites and output[e-1][1] in ['⏑','⏒','⏓']:
					output[e-1][1] += '͜'
		return output
		
def _sandhi(sentence):
	sandhis = []
	for index,[form, scansion, type] in enumerate(sentence[1:]):
		if type != 'word': continue
		previous_word = sentence[index][0].replace('|','i') #rescue iota subscript
		previous_word=re.sub('(.)\+',r'\1\1',previous_word) #rescue diaeresis
		previous_word=re.sub('[^A-z]*','',previous_word)
		pr_final = ','
		pr_final_len = sentence[index][1][-1][1] if len(sentence[index][1]) > 0 else ''
		if len(previous_word) > 0:
				pr_final = previous_word[-1].lower()
				if pr_final in ['i','u'] and previous_word[-2].lower() in ['a','e','h','o','w','u']: pr_final = previous_word[-2:].lower()
		current_word= re.sub('[^A-z]*','',form)
		cu_initial = ','
		cu_second = ''
		if len(current_word) > 0: cu_initial = current_word[0].lower()
		if len(current_word) > 1: cu_second = current_word[1].lower()
		if pr_final_len != '-' and pr_final in short_vowels + ancipites and len(pr_final) == 1: #short vowel sandhi, avoid diphthongs
			if cu_initial in ['c','y','z']: #double consonant
				sandhis.append((index,'long'))
				continue
			if cu_initial not in long_vowels + short_vowels + ancipites and cu_second not in long_vowels + short_vowels + ancipites + ['']:
				if cu_initial not in ['l','r'] and cu_second in ['l','r']: #muta cum liquida in new word
					sandhis.append((index,'anceps'))
					continue
				sandhis.append((index,'long')) #consonant cluster in new word
		if pr_final in ['a','e','o'] and cu_initial in long_vowels + short_vowels + ancipites and sentence[index][1][-1][1] == '⏑': #elision
				sandhis.append((index,'eli/syn'))
		if (pr_final_len != '⏑' and pr_final in long_vowels + ancipites) or len(pr_final) > 1:
			if cu_initial in ['a','e','i','h','o','u','w']: #uocalis ante uocalem, diphthong before vowel
				sandhis.append((index,'inv_anceps'))
				continue
		if pr_final not in long_vowels + short_vowels + ancipites:
			if cu_initial not in long_vowels + short_vowels + ancipites:
				if pr_final == 'k' and cu_initial in ['l','r']:
					sandhis.append((index,'anceps')) #muta cum liquida across words
					continue
				sandhis.append((index,'long')) #consonant cluster across words
				continue
			if re.search('[aehiowu]',sentence[index][0]):
				pre_final = sentence[index][1][-1][1]
				if pre_final == '⏒': sandhis.append((index,'short'))
	return(sandhis)

class doc:
	def __init__(self, **kwargs):
		global mCl
		self._filename = kwargs.get('file',None)
		self._verse = kwargs.get('verse',False)
		self._metre = kwargs.get('metre',False)
		self._form = kwargs.get('form',None)
		mCl = kwargs.get('mCl',False)
		if self._filename:
			if (file:=_externalFile(self._filename, self._verse)):
				self._form = file.text
			else:
				del self
				raise Exception('File not found')
		self._scanDocument()

	def _type(self,form):
		if not re.search('[Α-Ͽἀ-ῼ]', form): return 'punct'
		else: return 'word'

	def _tokenize(self, text, **kwargs):
		document = []
		separator =  ' @' if self._verse else '[\.··;:]'
		if not self._verse: text = re.sub('(%s) '%separator, r'\1\1 ', text)
		sentences = re.split('%s '%separator, text)
		for sentence in sentences:
			tokens = re.split('([,\(\)<>\"“”\{\}\[\]—\-– \.··;:])',sentence)
			tokens = [{"form":utf2beta(t.strip()), "type":self._type(t)} for t in tokens if t not in [' ','']]
			document.append({'sentence':sentence,'tokens':tokens})
		return document

	def _checkMetre(self,metre,data,tmpScansions):
		analysis = '?'
		isMetre = False
		#Dactylic
		arsis = f"({'|'.join(lg)})"
		thesis = f"({'|'.join(lg.union(py))})"
		anceps = f"({'|'.join(lg.union(br))})"
		if metre == 'hex':
			metreRe = re.compile(f"{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{thesis}{arsis}{anceps}")
			size = 12
			correction = ['']*size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'hexameter'
				for i in range(1,size+1):
					if i in [1,3,5,7,9,11]: #arsis positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i < 12: #thesis
						if len(res.group(i)) == 1: correction[i-1] = '–'
						if res.group(i) == '⏑͜⏑': correction[i-1] = '⏑⏑'
						elif len(res.group(i)) > 3 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜⏑⏑'
						elif len(res.group(i)) >= 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜–'
						elif len(res.group(i)) >= 2: correction[i-1] = '⏑⏑'
					else: #final anceps
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == 'pent':
			metreRe = re.compile(f"{arsis}{thesis}{arsis}{thesis}{anceps}{arsis}{thesis}{arsis}{thesis}{anceps}")
			size = 10
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'pentameter'
				for i in range(1,size + 1):
					if i in [1,3,6,8]: #arsis positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i in [2,4,7,9]: #thesis
						if len(res.group(i)) == 1: correction[i-1] = '–'
						if len(res.group(i)) >= 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜–'
						elif len(res.group(i)) >= 2: correction[i-1] = '⏑⏑'
					else: #ancipitia
						correction[i-1] = res.group(i)
				isMetre = True
		#Anapaestic
		anap = f"({arsis}{thesis}|{thesis}{arsis})"
		if metre == '4anap^':
			metreRe = re.compile(f"{anap*7}{anceps}")
			size = 15
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				allFeet = metreRe.findall(data['scansion'])[0]
				analysis = 'catalectic anapaestic tetrameter'
				corrIndex=-2
				for e,i in enumerate(allFeet):
					if e%5 == 0:
						corrIndex +=2
						if e < 35: continue
					f = corrIndex + ((e%5) % 2 == 0)
					if len(i) == 0: continue
					if e in [1,4,6,9,11,14,16,19,21,24,26,29,31,34]: #possible arsis positions
						correction[f] = '–' if len(i) == 1 else i #allow for synizesis
					elif e in [2,3,7,8,12,13,17,18,22,23,27,28,32,33]: #possible thesis positions:
						if len(i) == 1: correction[f] = '–'
						if len(i) >= 2 and i[1] == '͜': correction[f] = '⏑͜–'
						elif len(i) >= 2: correction[f] = '⏑⏑'
					if e == 35: correction[14] = i
				isMetre = True
		#Iambic
		arsis = f"({'|'.join(lg.union(py))})"
		thesis1 = f"({'|'.join(lg.union(py).union(br))})"
		thesis2 = f"({'|'.join(br.union(py))})"
		anceps = f"({'|'.join(br.union(lg))})"
		if metre == '3ia':
			metreRe = re.compile(f"{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{anceps}")
			size = 12
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'iambic trimeter'
				for i in range(1,size + 1):
					if i in [2,4,6,8,10]: #arsis positions
						if len(res.group(i)) == 1: correction[i-1] = '–'
						elif len(res.group(i)) == 2: correction[i-1] = '⏑⏑'
						elif len(res.group(i)) == 3: correction[i-1] = '⏑͜–'
					elif i in [1,3,5,7,9,11]: #thesis
						if res.group(i) in ['–','⏑']: correction[i-1] = res.group(i)
						elif res.group(i) == '⏓': correction[i-1] = '–'
						elif res.group(i) == '⏒': correction[i-1] = '⏑'
						elif len(res.group(i)) > 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜–'
						elif len(res.group(i)) == 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑'
						elif len(res.group(i)) >= 2: correction[i-1] = '⏑⏑'
					else:
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == '3ia/s':
			metreRe = re.compile(f"{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{arsis}{thesis1}")
			size = 12
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'scazon'
				for i in range(1,size + 1):
					if i in [2,4,6,8,10,11]: #arsis positions
						if len(res.group(i)) == 1: correction[i-1] = '–'
						elif len(res.group(i)) == 2: correction[i-1] = '⏑⏑'
						elif len(res.group(i)) == 3: correction[i-1] = '⏑͜–'
					elif i in [1,3,5,7,9]: #thesis
						if res.group(i) in ['–','⏑']: correction[i-1] = res.group(i)
						elif res.group(i) == '⏓': correction[i-1] = '–'
						elif res.group(i) == '⏒': correction[i-1] = '⏑'
						elif len(res.group(i)) > 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜–'
						elif len(res.group(i)) == 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑'
						elif len(res.group(i)) >= 2: correction[i-1] = '⏑⏑'
					else:
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == '4tr^':
			metreRe = re.compile(f"{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{arsis}{thesis1}{arsis}{thesis2}{arsis}")
			size = 15
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'catalectic trochaic tetrameter'
				for i in range(1,size + 1):
					if i in [1,3,5,7,9,11,13]: #arsis positions
						if len(res.group(i)) == 1: correction[i-1] = '–'
						elif len(res.group(i)) == 2: correction[i-1] = '⏑⏑'
						elif len(res.group(i)) == 3: correction[i-1] = '⏑͜–'
					elif i in [2,4,6,8,10,12,14]: #thesis
						if res.group(i) in ['–','⏑']: correction[i-1] = res.group(i)
						elif res.group(i) == '⏓': correction[i-1] = '–'
						elif res.group(i) == '⏒': correction[i-1] = '⏑'
						elif len(res.group(i)) > 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑͜–'
						elif len(res.group(i)) == 2 and res.group(i)[1] == '͜': correction[i-1] = '⏑'
						elif len(res.group(i)) >= 2: correction[i-1] = '⏑⏑'
					else:
						correction[i-1] = res.group(i)
				isMetre = True
		#Aeolic
		longum = f"({'|'.join(lg)})"
		breve = f"({'|'.join(br)})"
		anceps = f"({'|'.join(lg.union(br))})"
		if metre == 'gl':
			metreRe = re.compile(f"{anceps}{anceps}{longum}{breve}{breve}{longum}{breve}{longum}")
			size = 8
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'glyconic'
				for i in range(1,size + 1):
					if i in [3,6,8]: #longum positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i in [2,3,5]: #breve
						correction[i-1] = '⏑'
					else: #ancipitia
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == 'ph':
			metreRe = re.compile(f"{anceps}{anceps}{longum}{breve}{breve}{longum}{longum}")
			size = 7
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'pherecratean'
				for i in range(1,size + 1):
					if i in [3,6,7]: #longum positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i in [2,3,5]: #breve
						correction[i-1] = '⏑'
					else: #ancipitia
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == 'sapph':
			metreRe = re.compile(f"{longum}{breve}{longum}{anceps}{longum}{breve}{breve}{longum}{breve}{longum}{anceps}")
			size = 11
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'sapphic'
				for i in range(1,size + 1):
					if i in [1,3,5,8,10]: #longum positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i in [2,6,7,9]: #breve
						correction[i-1] = '⏑'
					else: #ancipitia
						correction[i-1] = res.group(i)
				isMetre = True
		if metre == 'adon':
			metreRe = re.compile(f"{longum}{breve}{breve}{longum}{anceps}")
			size = 5
			correction = [''] * size
			if (res:=metreRe.match(data['scansion'])):
				analysis = 'adonean'
				for i in range(1,size + 1):
					if i in [1,4]: #longum positions
						correction[i-1] = '–' if len(res.group(i)) == 1 else res.group(i) #allow for synizesis
					elif i in [2,3]: #breve
						correction[i-1] = '⏑'
					else: #ancipitia
						correction[i-1] = res.group(i)
				isMetre = True
		if isMetre:
			syllCount = 0
			data['scansion'] = ''.join(correction)
			tmpAdd = ''
			for w in tmpScansions:
				if w[-1] != 'word': continue
				for s in w[1]:
					if syllCount < len(data['scansion']):
						s[1] = data['scansion'][syllCount]
					else:
						tmpAdd += s[1]
					syllCount += 1
			if len(tmpAdd) > 0: analysis += f" + {tmpAdd}"
		return {'analysis':analysis,'outputScansion':data['scansion'],'scansions':tmpScansions}

	def _scanDocument(self):
		document = self._tokenize(self._form.replace("᾽","'"))
		self.scannedDocument = []
		for sentence in document:
			if not re.search('[aehiowu]',utf2beta(sentence['sentence'])):
				if __name__ == '__main__': input(f'The form/sentence/line {sentence["sentence"]} contains no vowels and cannot be syllabified. Hit return to continue to the next item.')
				continue
			scansions = []
			for token in sentence['tokens']:
				if self._verse and token['type'] != 'word': continue
				form = token['form'].replace('\\','/')
				try:
					tempScan = _word(form).scan(False)
				except:
					if __name__ == '__main__':
						import traceback
						traceback.print_exc()
						continue
					else:
						raise Exception(f'{form} caused an error')
				if '?' in ''.join(t[1] for t in tempScan): tempScan = _word(utf2beta(beta2utf(form).lower())).scan(False)
				if '?' in ''.join(t[1] for t in tempScan):
					howmanyAccents = len(re.findall("[/=]", form))
					if howmanyAccents > 1:
						form=form[::-1].replace("/", "", 1)[::-1]
						tempScan = _word(form).scan(False)
				scansions.append([form, tempScan, token['type']])
			for index, outcome in _sandhi(scansions):
				if len(scansions[index][1]) > 0:
					scans['anceps'] = '?' if scansions[index][1][-1][1] == '?' else '⏒'
					if (scansions[index][1][-1][1] == '⏑' and scans[outcome] != 'short') or (scansions[index][1][-1][1] == '–' and scans[outcome] != 'long') or (scansions[index][1][-1][1] in ['⏒','?'] and scans[outcome] != 'anceps'):
						scansions[index][1][-1][1] = scans[outcome]
			output = {'scansion':''.join([syllable for form,scansion,type in scansions for vowel,syllable in scansion]),'analysis':None}
			#Check for metre
			if self._verse:
				if not self._metre:
					for m in metreCycle:
						tmpMetre = self._checkMetre(m,output,scansions)
						if tmpMetre['analysis'] != '?': break
				else:
					tmpMetre = self._checkMetre(self._metre, output,scansions)
				output['analysis'] = tmpMetre['analysis']
				output['scansion'] = tmpMetre['outputScansion']
				scansions = tmpMetre['scansions']

			#By syllable
			output['syllables'] = []
			sandhiSequence = '#'.join([word[0] for word in scansions])
			sandhiString = _word(sandhiSequence)
			sandhiSequence = [beta2utf(x) for x in sandhiString.syllabify()]
			sandhiSequence = [x.replace('ς','σ' if e<len(sandhiSequence) -1 else 'ς').replace('σ#','ς#') for e,x in enumerate(sandhiSequence)]
			scannedUnits = []
			full_scansion = output['scansion'] + ((output['analysis'].split(' + ')[1] if '+' in output['analysis'] else '') if output['analysis'] else '')
			for e,s in enumerate(full_scansion):
				if s != '͜': scannedUnits.append(s)
				else: scannedUnits[-1]+=s
			output['syllables'] = list(zip(sandhiSequence,scannedUnits))
			self.scannedDocument.append([sentence['sentence'], output])
		self.syllables = [line[1]['syllables'] for line in self.scannedDocument]
		return self.scannedDocument

	def display(self, syll=False, **kwargs):
		lineCount = 0
		if self.scannedDocument is None: self._scanDocument()
		if exportFile:=kwargs.get('export',None):
			if os.path.isfile(exportFile):
				while True:
					ow = input(f'\033[1A\033[KThe file {exportFile} exists. Overwrite? [yn] ')
					if ow == 'y': open(exportFile, 'w',encoding='utf-8')
					if ow in ['y','n']: break
		if syll:
			for (line,data) in self.scannedDocument:
				lineCount += 1
				if kwargs.get('showText',False):
					print(line,'\n', file=open(exportFile,'a+',encoding='utf-8') if exportFile else sys.stdout)
				counter = 0
				syllabified = []
				while True:
					if kwargs.get('above',None): syllabified.append('\t'.join(s[1] for s in data['syllables'][counter*width:(counter+1)*width]))
					syllabified.append('\t'.join(s[0] for s in data['syllables'][counter*width:(counter+1)*width]))
					if not kwargs.get('above',None): syllabified.append('\t'.join(s[1] for s in data['syllables'][counter*width:(counter+1)*width]))
					counter += 1
					if counter*width >= len(data['syllables']): break
				print('\n'.join(syllabified), data['analysis'] if kwargs.get('analysis',False) else '\033[1A' if not exportFile else '', '', sep='\n', file=open(exportFile,'a+',encoding='utf-8') if exportFile else sys.stdout)
		else: 
			for (line,data) in self.scannedDocument:
				if kwargs.get('problems', False) and data['analysis'] != '?': continue
				lineCount += 1
				if exportFile: print(line, data['scansion'],data['analysis'] if self._verse else '',sep='\t', file=open(exportFile,'a+', encoding='utf-8'))
				else:
					print(line)
					print('   {:<40}{}'.format(data['scansion'],data['analysis'] if self._verse else ''))
		print('\nLine count:',lineCount,'\n')
		if exportFile: print(f'Data saved to {exportFile}.')	

if __name__ == '__main__':
	import textwrap
	if '-help' in sys.argv:
		entries = ['-doc','-verse','-syll','-mCl','-above','-showText','-analysis','-metre','-export','-problems']
		descr = ['Load UTF-8 text file into the scanner. The name of the file should include the full path. If it contains spaces, use quotation marks around it.','Specify that the text is verse. Each line in the text is scanned as a separate unit; otherwise, units will be delimited by strong punctuation marks (., ·, ;).', 'Print scansions for each syllable as interlinear text. A number after this command specifies the number of syllables per line (default: 15).','Syllabifies muta-cum-liquida clusters as onsets, which may result in correptio Attica. If left unspecified, the parser returns all possibilities for syllables with a short vowel preceding this type of cluster.','If -syll is active, print the interlinear scansions above the line of text (otherwise scansions are printed below by default)','Print text units (lines/sentences) before their syllable-by-syllable scansion. The metre of each line is not displayed by default.','Display the detected metre (if any) alongside syllable-by-syllable scansions.','Specify what metre the text is in. Available options:'+190* ' '+'· hex            hexameter'+190* ' '+'· pent           pentameter'+190* ' '+'· 3ia            iambic trimeter'+190* ' '+'· 4tr^           catalectic trochaic tetrameter'+190* ' '+'· 4anap^         catalectic anapaestic tetrameter'+190* ' '+'· 3ia(s)         scazon'+190* ' '+'· gl             glyconean'+190* ' '+'· ph             pherecratean'+190* ' '+'· sapph          sapphic endecasyllable'+190* ' '+'· adon           adonean'+190* ' '+'If this option is omitted, metres will be guessed by the parser.','Save the results to a text file. Enter the full path to the file (including the folder).','If -verse is active, only return lines that do not scan.']
		title = "DIORISIS SCAN b`eta"
		print(f'╔{"═"*(len(title)+2)}╗'.center(os.get_terminal_size().columns))
		print(f'║ {title} ║'.center(os.get_terminal_size().columns))
		print(f'╚{"═"*(len(title)+2)}╝'.center(os.get_terminal_size().columns))
		print('Made since 2022 by Alessandro Vatri (alessandro.vatri@crs.rm.it)'.center(os.get_terminal_size().columns))
		print()
		for e,i in enumerate(entries):
			wrapper = textwrap.TextWrapper(initial_indent='{:<30}'.format(i), width=os.get_terminal_size().columns,
							   subsequent_indent=' '*30)
			print(wrapper.fill(descr[e]))
		print()
		sys.exit()
	print('Loading dictionary')
	loadDictionary()
	clear = 'cls' if isWindows else "clear && printf '\e[3J'"
	os.system(clear)
	verse = '-verse' in sys.argv
	metre = False
	if '-metre' in sys.argv:
		if sys.argv.index('-metre')+1 < len(sys.argv):
			metre = metre if (metre:=sys.argv[sys.argv.index('-metre')+1]) in metreCycle else False
	if '-syll' in sys.argv and len(sys.argv) > sys.argv.index('-syll'):
		try:
			n =int(sys.argv[sys.argv.index('-syll')+1])
			width = n
		except:
			pass
	if '-doc' in sys.argv: 
		if sys.argv.index('-doc')+1 < len(sys.argv):
			filename = sys.argv[sys.argv.index('-doc')+1]
			document = doc(file=filename,verse=verse,metre=metre, mCl='-mCl' in sys.argv)
			document.display('-syll' in sys.argv, showText='-showText' in sys.argv, analysis='-analysis' in sys.argv, problems='-problems' in sys.argv, above='-above' in sys.argv)
		else:
			print('Filename missing')
			sys.exit()
	else:
		while True:
			form = input('Enter form/sentence ([e]xit): ')
			if not re.search('[A-Za-z]', form): 
				document = doc(form=form,verse=verse,metre=metre, mCl='-mCl' in sys.argv)
				document.display('-syll' in sys.argv, showText='-showText' in sys.argv, analysis='-analysis' in sys.argv, problems='-problems' in sys.argv, above='-above' in sys.argv)
			elif form == 'e': break
			else: print('Enter text in Unicode Greek')
	if '-export' in sys.argv:
		if sys.argv.index('-export')+1 < len(sys.argv):
			filename = sys.argv[sys.argv.index('-export')+1]
			document.display('-syll' in sys.argv, showText='-showText' in sys.argv, analysis='-analysis' in sys.argv, problems='-problems' in sys.argv, export=filename, above='-above' in sys.argv)
			sys.exit()
		else:
			print('Name of output file missing')
			sys.exit()