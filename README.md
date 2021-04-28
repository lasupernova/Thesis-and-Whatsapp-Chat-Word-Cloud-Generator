# Word Cloud Generator
Python CLI tool to generate customized word clouds from documents, especially large documents such as dissertations, master and bachelor thesis (or export your __WhatsApp Chat__ and use it on your conversations with different people!). Depending on `wordcloud` and `nltk` <br>
Don't want to work with the command line? Use the jupyter notebook instead (see instructions and examples below)<hr>
![Example of word cloud, Low Height](example_output/example6_width1500_height100.png?raw=true "Custom settings")
### **Example text file for practice:**<br>
Saved as `example.txt`. This is a text file containing the book "The count of Monte Cristo".<br><br>

### **Usage:**<br>
`python generate_cloud.py`<br><br>
By default text information is taken from a file called "doc.txt", so be sure to move a copy of your thesis to you working directory and to rename it to "doc.txt". 
Alternatively, use a command line argument to change the name of the input file.<br><br>
### **Usage - Word Cloud from WhatsApp Chat Exports:**<br>
`python generate_cloud.py - whatsapp`<br><br>
This will pre-process the WhatsApp chat export file, to exclude dates and other text-parts added by WhatsApp to generate export file (e.g. "Media omitted" text that is inserted inplace of media sent). <br><br><br>
### **Customization**:<br>
A number of different parameters can be customized: <br>
Parameter | Command Line Argument | Type
------------ | ------------- | -------------
Name of input file | -file_path | string
Text color | -hue | integer
Stopwords | -sw <br>(NOTE: these stopword will not replace <br>generic stopwords but will be added) | list
Background Color | -bg | string
Image Width (pixel) | -w | integer
Image Heigt (pixel) | -height | integer
Maximum number of words to display | -maxwords | integer
Ratio of words to display horizontally | -h_ratio | integer<br> (from 0-1)
Saturation | -s | integer<br> (from 0-100)
Lightness | -l | integer<br> (from 0-100)
File name to store output | -o | string <br> (NOTE: should end with '.png')
Words to replace in text | -x1 | string <br> (NOTE: can be multiple strings)<br>(NOTE: always needs to be used together with _-x2_)
Substitutes for words passed in -x1 | -x2 | string <br> (NOTE: can be multiple strings)<br>(NOTE: always needs to be used together with _-x1_)
WhatsApp export-file usage | -whatsapp | simply add "-whatsapp"<br> Use when a WhatsApp chat export file is used as text
Matrix Effect | -matrix | simply add "-matrix"<br> The program will then automatically ste all parameters  for a matrix-like word cloud<br> _(see below for example)_


**Example**:<br>
`python generate_cloud.py -file_path my_thesis_final_version.txt -bg black -h_ratio 0.6 -o wordcloud_thesis.png`<br>
 - This example will take a text file named 'my_thesis_final_version.txt' and save the wordcloud to 'wordcloud_thesis.png'. The word cloud will have a black background and only 60% of the words will be displayed horizontally (and 40% vertically).
<br><br><br>
### **Alternative: Jupyter Notebook**:<br>
If you don't want to use the command line, you can use the Jupiter Notebook instead: <br>
 - Install [Jupyter Notebook](https://test-jupyter.readthedocs.io/en/latest/install.html)
 - Download Github repository
 - Open Notebook
 - replace _example.txt_ with the name of your text file / thesis (in the notebook); or save your file in the same folder as the jupyter notebook and rename it _example.txt_
 - go to `Cell` - click `Run all`
 - check you working directory: the word cloud image should be saved there now under a name similar to **wc_Size1500_1000_hslColorH322** (unless you changed the parameter for the output)
<br><br><br>
### **Examples**:<br>
A few examples of different custom settings and the results:<br><br>
* __Regular usage:__ `python generate_cloud.py` <br><br>
<img src="https://github.com/lasupernova/thesis_wordcloud_generator/blob/master/example_output/example_cloud1.png" width="600" height="400"><hr>
Let's change 'count' to 'Simon Basset' ( ...looking at you __Bridgerton__... ) and use a black background <br><br>
* __Custom usage:__ `python generate_cloud.py -x1 count -x2 Simon_Hastings -f example.txt -o bridgerton2.png -bg black`<br><br>
I only replaced one word (count -> simon hastings), but multiple words can be replaced at the same time. <br>E.g: `-x1 count Monte_Cristo -x2 simon_hastings London`  changes "count" to "simon hastings" and "Monte Cristo" to "London". <br> Note that words that belong together, such as "Monte Cristo", should be connected with an underscore.<br><br>
<img src="https://github.com/lasupernova/thesis_wordcloud_generator/blob/master/example_output/bridgerton2.png" width="600" height="400"><hr>
* __Matrix usage:__ `python generate_cloud.py -matrix`<br><br>
Automatically created word cloud with matrix-like style. This specific word cloud was generated using the "-whatsapp" option using a WhatsApp chat export file and I used -x1/-x2 in order to censor names and addresses. You can still specify "-whatsapp", and the input (-f) and output (-o) files.<br><br>
<img src="https://github.com/lasupernova/thesis_wordcloud_generator/blob/master/example_output/matrix.png" width="600" height="400"><hr>
__Custom usage:__ 
<br>* Left (saturation and lightness adjusted): `python generate_cloud.py -s 25 -l 90`<br>
<br>* Right (allow for random word colors): `python generate_cloud.py -hue None`<br><br>
<img src="https://github.com/lasupernova/thesis_wordcloud_generator/blob/master/example_output/example2_saturation25_lightness90.png" width="400" height="266">
<img src="https://github.com/lasupernova/thesis_wordcloud_generator/blob/master/example_output/example3_randomHue.png" width="400" height="266">





