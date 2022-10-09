def convertBeta(text):
	import re
	text = text.upper()
	
	# 4 chars	
	text = text.replace("A)\\|",   u"\u1F82")
	text = text.replace("A(\\|",   u"\u1F83")
	text = text.replace("A)/|",   u"\u1F84")
	text = text.replace("A(/|",   u"\u1F85")
	text = text.replace("A)=|",   u"\u1F86")
	text = text.replace("A(=|",   u"\u1F87")
	text = text.replace("H)\\|",   u"\u1F92")
	text = text.replace("H(\\|",   u"\u1F93")
	text = text.replace("H)/|",   u"\u1F94")
	text = text.replace("H(/|",   u"\u1F95")
	text = text.replace("H)=|",   u"\u1F96")
	text = text.replace("H(=|",   u"\u1F97")
	text = text.replace("W)\\|",   u"\u1FA2")
	text = text.replace("W(\\|",   u"\u1FA3")
	text = text.replace("W)/|",   u"\u1FA4")
	text = text.replace("W(/|",   u"\u1FA5")
	text = text.replace("W)=|",   u"\u1FA6")
	text = text.replace("W(=|",   u"\u1FA7")
	text = text.replace("*)\\A",	u"\u1F0A")
	text = text.replace("*(\\A",	u"\u1F0B")
	text = text.replace("*A)/",	u"\u1F0C")
	text = text.replace("*)/A",	u"\u1F0C")
	text = text.replace("*A(/",	u"\u1F0D")
	text = text.replace("*(/A",	u"\u1F0D")
	text = text.replace("*A(=",	u"\u1F0F")
	text = text.replace("*(=A",	u"\u1F0F")
	text = text.replace("*A)=",	u"\u1F0E")
	text = text.replace("*)=A",	u"\u1F0E")
	text = text.replace("*)\\E",	u"\u1F1A")
	text = text.replace("*(\\E",	u"\u1F1B")
	text = text.replace("*E)/",	u"\u1F1C")
	text = text.replace("*)/E",	u"\u1F1C")
	text = text.replace("*E(/",	u"\u1F1D")
	text = text.replace("*(/E",	u"\u1F1D")
	text = text.replace("*H)\\",   u"\u1F2A")
	text = text.replace(")\\*H",   u"\u1F2A")
	text = text.replace("*)\\H",	u"\u1F2A")
	text = text.replace("*H(\\",   u"\u1F2B")
	text = text.replace("(\\*H",   u"\u1F2B")
	text = text.replace("*(\\H",	u"\u1F2B")
	text = text.replace("*H)/",	u"\u1F2C")
	text = text.replace("*)/H",	u"\u1F2C")
	text = text.replace("*H(/",	u"\u1F2D")
	text = text.replace("*(/H",	u"\u1F2D")
	text = text.replace("*)=H",	u"\u1F2E")
	text = text.replace("(=*H",	u"\u1F2F")
	text = text.replace("*(=H",	u"\u1F2F")
	text = text.replace("*I)\\",   u"\u1F3A")
	text = text.replace(")\\*I",   u"\u1F3A")
	text = text.replace("*)\\I",	u"\u1F3A")
	text = text.replace("*I(\\",   u"\u1F3B")
	text = text.replace("(\\*I",   u"\u1F3B")
	text = text.replace("*(\\I",	u"\u1F3B")
	text = text.replace("*I)/",	u"\u1F3C")
	text = text.replace("*)/I",	u"\u1F3C")
	text = text.replace("*I(/",	u"\u1F3D")
	text = text.replace("*(/I",	u"\u1F3D")
	text = text.replace("*I)=",	u"\u1F3E")
	text = text.replace("*)=I",	u"\u1F3E")
	text = text.replace("*I(=",	u"\u1F3F")
	text = text.replace("*(=I",	u"\u1F3F")
	text = text.replace("*)\\O",	u"\u1F4A")
	text = text.replace("*(\\O",	u"\u1F4B")
	text = text.replace("*O)/",	u"\u1F4C")
	text = text.replace("*)/O",	u"\u1F4C")
	text = text.replace("*O(/",	u"\u1F4D")
	text = text.replace("*(/O",	u"\u1F4D")
	text = text.replace("*(\\U",	u"\u1F5B")
	text = text.replace("*U(\\",	u"\u1F5B")
	text = text.replace("*(/U",	u"\u1F5D")
	text = text.replace("*U(/",	u"\u1F5D")
	text = text.replace("*(=U",	u"\u1F5F")
	text = text.replace("*W)\\",	u"\u1F6A")
	text = text.replace("*)\\W",	u"\u1F6A")
	text = text.replace("*W(\\",	u"\u1F6B")
	text = text.replace("*(\\W",	u"\u1F6B")
	text = text.replace("*W)/",	u"\u1F6C")
	text = text.replace("*)/W",	u"\u1F6C")
	text = text.replace("*W(/",	u"\u1F6D")
	text = text.replace("*(/W",	u"\u1F6D")
	text = text.replace("*W)=",	u"\u1F6E")
	text = text.replace("*)=W",	u"\u1F6E")
	text = text.replace("*W(=",	u"\u1F6F")
	text = text.replace("*(=W",	u"\u1F6F")
	
	
	#3 chars
	text = text.replace("A)\\",   u"\u1F02")
	text = text.replace("A(\\",   u"\u1F03")
	text = text.replace("A)/",	u"\u1F04")
	text = text.replace("A(/",	u"\u1F05")
	text = text.replace("E)\\",   u"\u1F12")
	text = text.replace("E(\\",   u"\u1F13")
	text = text.replace("E)/",	u"\u1F14")
	text = text.replace("E(/",	u"\u1F15")
	text = text.replace("H)\\",   u"\u1F22")
	text = text.replace("H(\\",   u"\u1F23")
	text = text.replace("H)/",	u"\u1F24")
	text = text.replace("H(/",	u"\u1F25")
	text = text.replace("I)\\",   u"\u1F32")
	text = text.replace("I(\\",   u"\u1F33")
	text = text.replace("I)/",	u"\u1F34")
	text = text.replace("I(/",	u"\u1F35")
	text = text.replace("O)\\",   u"\u1F42")
	text = text.replace("O(\\",   u"\u1F43")
	text = text.replace("O)/",	u"\u1F44")
	text = text.replace("O(/",	u"\u1F45")
	text = text.replace("U)\\",   u"\u1F52")
	text = text.replace("U(\\",   u"\u1F53")
	text = text.replace("U)/",	u"\u1F54")
	text = text.replace("U(/",	u"\u1F55")
	text = text.replace("W)\\",   u"\u1F62")
	text = text.replace("W(\\",   u"\u1F63")
	text = text.replace("W)/",	u"\u1F64")
	text = text.replace("W(/",	u"\u1F65")
	text = text.replace("A)=",	u"\u1F06")
	text = text.replace("A(=",	u"\u1F07")
	text = text.replace("H)=",	u"\u1F26")
	text = text.replace("H(=",	u"\u1F27")
	text = text.replace("I)=",	u"\u1F36")
	text = text.replace("I(=",	u"\u1F37")
	text = text.replace("U)=",	u"\u1F56")
	text = text.replace("U(=",	u"\u1F57")
	text = text.replace("W)=",	u"\u1F66")
	text = text.replace("W(=",	u"\u1F67")

	text = text.replace("*A)",	 u"\u1F08")
	text = text.replace("*)A",	 u"\u1F08")
	text = text.replace("*A(",	 u"\u1F09")
	text = text.replace("*(A",	 u"\u1F09")
	text = text.replace("*E)",	 u"\u1F18")
	text = text.replace("*)E",	 u"\u1F18")
	text = text.replace("*E(",	 u"\u1F19")
	text = text.replace("*(E",	 u"\u1F19")
	text = text.replace("*H)",	 u"\u1F28")
	text = text.replace("*)H",	 u"\u1F28")
	text = text.replace("*H(",	 u"\u1F29")
	text = text.replace("*(H",	 u"\u1F29")
	text = text.replace("*I)",	 u"\u1F38")
	text = text.replace("*)I",	 u"\u1F38")
	text = text.replace("*I(",	 u"\u1F39")
	text = text.replace("*(I",	 u"\u1F39")
	text = text.replace("*O)",	 u"\u1F48")
	text = text.replace("*)O",	 u"\u1F48")
	text = text.replace("*O(",	 u"\u1F49")
	text = text.replace("*(O",	 u"\u1F49")
	text = text.replace("*U(",	 u"\u1F59")
	text = text.replace("*(U",	 u"\u1F59")
	text = text.replace("*W)",	 u"\u1F68")
	text = text.replace("*)W",	 u"\u1F68")
	text = text.replace("*W(",	 u"\u1F69")
	text = text.replace("*(W",	 u"\u1F69")
	
	text = text.replace("I\\+",   u"\u1FD2")
	#text = text.replace("I/+",	u"\u1FD3")
	#text = text.replace("I+/",	u"\u1FD3")
	text = text.replace("I+/",	u"\u0390")
	text = text.replace("I/+",	u"\u0390")
	text = text.replace("I=+",	u"\u1FD7")
	text = text.replace("U\\+",   u"\u1FE2")
	#text = text.replace("U/+",	u"\u1FE3")
	text = text.replace("U/+",	u"\u03B0")
	text = text.replace("U=+",	u"\u1FE7")
	
	text = text.replace("A/|",	u"\u1FB4")
	text = text.replace("H/|",	u"\u1FC4")
	text = text.replace("W|/",	u"\u1FF4")
	text = text.replace("W/|",	u"\u1FF4")
	text = text.replace("A\\|",	u"\u1FB2")
	text = text.replace("H\\|",	u"\u1FC2")
	text = text.replace("W|\\",	u"\u1FF2")
	text = text.replace("W\\|",	u"\u1FF2")
	text = text.replace("A=|",	u"\u1FB7")
	text = text.replace("H=|",	u"\u1FC7")
	text = text.replace("W=|",	u"\u1FF7")
	text = text.replace("R)",	 u"\u1FE4")
	text = text.replace("R(",	 u"\u1FE5")
	text = text.replace("*R(",	u"\u1FEC")
	text = text.replace("*(R",	u"\u1FEC")
	
	text = text.replace("A)|",	u"\u1F80")
	text = text.replace("A(|",	u"\u1F81")
	text = text.replace("H)|",	u"\u1F90")
	text = text.replace("H(|",	u"\u1F91")
	text = text.replace("W)|",	u"\u1FA0")
	text = text.replace("W(|",	u"\u1FA1")

	
	#2 chars
	text = text.replace("*A",	  u"\u0391")
	text = text.replace("*B",	  u"\u0392")
	text = text.replace("*G",	  u"\u0393")
	text = text.replace("*D",	  u"\u0394")
	text = text.replace("*E",	  u"\u0395")
	text = text.replace("*Z",	  u"\u0396")
	text = text.replace("*H",	  u"\u0397")
	text = text.replace("*Q",	  u"\u0398")
	text = text.replace("*I",	  u"\u0399")
	text = text.replace("*K",	  u"\u039A")
	text = text.replace("*L",	  u"\u039B")
	text = text.replace("*M",	  u"\u039C")
	text = text.replace("*N",	  u"\u039D")
	text = text.replace("*C",	  u"\u039E")
	text = text.replace("*O",	  u"\u039F")
	text = text.replace("*P",	  u"\u03A0")
	text = text.replace("*R",	  u"\u03A1")
	text = text.replace("*S",	  u"\u03A3")
	text = text.replace("*T",	  u"\u03A4")
	text = text.replace("*U",	  u"\u03A5")
	text = text.replace("*V",	 u"\u03DC")
	text = text.replace("*F",	  u"\u03A6")
	text = text.replace("*X",	  u"\u03A7")
	text = text.replace("*Y",	  u"\u03A8")
	text = text.replace("*W",	  u"\u03A9")
	
	text = text.replace("S ",	 u"\u03C2 ")
	text = text.replace("S,",	 u"\u03C2,")
	text = text.replace("S.",	 u"\u03C2.")
	text = text.replace("S:",	 u"\u03C2:")
	text = text.replace("S;",	 u"\u03C2;")
	text = text.replace("S]",	 u"\u03C2]")
	text = text.replace("S)",	 u"\u03C2)")
	text = text.replace("S@",	 u"\u03C2@")
	text = text.replace("S_",	 u"\u03C2_")
	text = text.replace("S%",	 u"\u03C2%")
	text = text.replace("S\"",	 u"\u03C2\"")
	text = re.sub("S$",	 u"\u03C2", text)
	
	text = text.replace("I+",	 U"\u03CA")
	text = text.replace("U+",	 U"\u03CB")
	
	text = text.replace("A)",	 u"\u1F00")
	text = text.replace("A(",	 u"\u1F01")
	text = text.replace("E)",	 u"\u1F10")
	text = text.replace("E(",	 u"\u1F11")
	text = text.replace("H)",	 u"\u1F20")
	text = text.replace("H(",	 u"\u1F21")
	text = text.replace("I)",	 u"\u1F30")
	text = text.replace("I(",	 u"\u1F31")
	text = text.replace("O)",	 u"\u1F40")
	text = text.replace("O(",	 u"\u1F41")
	text = text.replace("U)",	 u"\u1F50")
	text = text.replace("U(",	 u"\u1F51")
	text = text.replace("W)",	 u"\u1F60")
	text = text.replace("W(",	 u"\u1F61")
	
	text = text.replace("A\\",	u"\u1F70")
	#text = text.replace("A/",	 u"\u1F71")
	text = text.replace("A/",	 u"\u03AC")
	text = text.replace("E\\",	u"\u1F72")
	#text = text.replace("E/",	 u"\u1F73")
	text = text.replace("E/",	 u"\u03AD")
	text = text.replace("H\\",	u"\u1F74")
	#text = text.replace("H/",	 u"\u1F75")
	text = text.replace("H/",	 u"\u03AE")
	text = text.replace("I\\",	u"\u1F76")
	#text = text.replace("I/",	 u"\u1F77")
	text = text.replace("I/",	 u"\u03AF")
	text = text.replace("O\\",	u"\u1F78")
	#text = text.replace("O/",	 u"\u1F79")
	text = text.replace("O/",	 u"\u03CC")
	text = text.replace("U\\",	u"\u1F7A")
	#text = text.replace("U/",	 u"\u1F7B")
	text = text.replace("U/",	 u"\u03CD")
	text = text.replace("W\\",	u"\u1F7C")
	#text = text.replace("W/",	 u"\u1F7D")
	text = text.replace("W/",	 u"\u03CE")
	
	text = text.replace("A|",	 u"\u1FB3")
	text = text.replace("H|",	 u"\u1FC3")
	text = text.replace("W|",	 u"\u1FF3")
	
	text = text.replace("A=",	 u"\u1FB6")
	text = text.replace("H=",	 u"\u1FC6")
	text = text.replace("I=",	 u"\u1FD6")
	text = text.replace("U=",	 u"\u1FE6")
	text = text.replace("W=",	 u"\u1FF6")
	text = text.replace("*V",	 u"\u03DC")
			
	#1 char
	text = text.replace("A",	  u"\u03B1")
	text = text.replace("B",	  u"\u03B2")
	text = text.replace("G",	  u"\u03B3")
	text = text.replace("D",	  u"\u03B4")
	text = text.replace("E",	  u"\u03B5")
	text = text.replace("Z",	  u"\u03B6")
	text = text.replace("H",	  u"\u03B7")
	text = text.replace("Q",	  u"\u03B8")
	text = text.replace("I",	  u"\u03B9")
	text = text.replace("K",	  u"\u03BA")
	text = text.replace("L",	  u"\u03BB")
	text = text.replace("M",	  u"\u03BC")
	text = text.replace("N",	  u"\u03BD")
	text = text.replace("C",	  u"\u03BE")
	text = text.replace("O",	  u"\u03BF")
	text = text.replace("P",	  u"\u03C0")
	text = text.replace("R",	  u"\u03C1")
	text = text.replace("S",	  u"\u03C3")
	text = text.replace("T",	  u"\u03C4")
	text = text.replace("U",	  u"\u03C5")
	text = text.replace("F",	  u"\u03C6")
	text = text.replace("X",	  u"\u03C7")
	text = text.replace("Y",	  u"\u03C8")
	text = text.replace("V",	 u"\u03DD")
	text = text.replace("W",	  u"\u03C9")
	
	text = text.replace(":",	  u"\u00B7")
	text = text.replace("'",	  u"\u2019")
	text = text.replace("_",	  u"\u2014")
	text = text.replace("?",	  u"\u0323")
	
	return text