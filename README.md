# Diorisis Scan
A Python module for the metrical scansion of Ancient Greek prose and verse texts.

If run in Windows, the module loads a custom font in the terminal for the correct display of metrical symbols.

# Standalone

Run `python prosodyScanner.py -help` for the user guide.
# Module
Copy all files to the same folder as your script and import it as follows:

`import prosodyScanner as ps`

## The `doc` class

Texts or forms/sentences to be scanned are loaded into a `doc` object:

`document = doc(file=filename,verse=verse,metre=metre)`

or 

`document = doc(form=form,verse=verse,metre=metre)`

### Options
| option | accepted values |
| ----------- | ----------- |  
| *form* | String. Word/sentence in Unicode Polytonic Greek. |
| *file* | String. Full path to text file to be parsed (plain text, Unicode Polytonic Greek).|
| | *form* and *file* may not be used at the same time |
| *verse* | Boolean. Specify that the text is verse. If used with *file*, each line in the text is scanned as a separate unit; otherwise, units will be delimited by strong punctuation marks (., ·, ;). |
| *metre* | String. Specify what metre the text is in. See table below for options. If this option is omitted, metres will be guessed by the parser. |

#### Supported metres
|  code | metre |
| --- | --- |
| hex | hexameter |
|pent | pentameter |
|3ia | iambic trimeter |
|4tr^ |catalectic trochaic tetrameter |
|4 anap^ | catalectic anapaestic tetrameter |
| 3ia(s) | scazon |
| gl | glyconean |
| ph | pherecratean |
| sapph | sapphic endecasyllable |
|adon | adonean |


### Methods
#### scanAndDisplay(_syll_=`Boolean`, _showText_=`Boolean`, _analysis_=`Boolean`, _problems_=`Boolean`, _above_=`Boolean`,_export_=`String`)
This method scans the input text or form/sentence and outputs the results of the scansion to screen and/or to an external file.

| option | values |
| ----------- | ----------- |  
|*syll* | optional (default `False`). Print scansions for each syllable as interlinear text. |
|*showText*|optional (default `False`). Print text units (lines/sentences) before their syllable-by-syllable scansion. The metre of each line is not displayed by default.|
|*analysis*|optional (default `False`). Display the detected metre (if any) alongside syllable-by-syllable scansions.|
|*problems*|optional (default `False`). Use with `verse = True`. Only display lines/sentences that are not analysable as a supported metre.|
|*above*|optional (default `False`). Use with `syll = True`. Print the interlinear scansions above the line of text (otherwise scansions are printed below by default).|
|*export*|optional. Full path to text file to which to save the results. If blank, the results are only printed to screen.|

### Properties
#### scannedDocument
`List` containing a `list` for each sentence/line. The elements of each sublist are:

`[0]`: `String` containing the scanned unit.

`[1]`: `Dictionary` with the following items:
- _scansion_: the scansion of the whole unit.
- _analysis_: the result of the metrical analysis (if requested)
- _syllables_: a `List` containing a `list` for each syllable. The first element in each `list` is the syllable itself; the second element is its scansion.

## The `syllabify` class

This class returns syllabified texts or forms/sentences.

The class requires one parameter to be instantiated. The parameter is a `String` containing either the form/sentence to be syllabified or the full path to a text file to be parsed (plain text, Unicode Polytonic Greek).

### Properties
#### syllables
A `List` containing a `list` for each syllable. The first element in each `list` is the syllable itself; the second element is its scansion.
