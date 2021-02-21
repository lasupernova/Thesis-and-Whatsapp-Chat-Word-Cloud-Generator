import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.corpus import stopwords as sw
import sys
import argparse
import itertools
import re

def main():
    parser = argparse.ArgumentParser(description='Customize your word cloud!')
    parser.add_argument('-f', action='store', dest='file_path',help='path to text document', type=str)
    parser.add_argument('-hue', action='store', dest='hue',help='color for word cloud', type=int)
    parser.add_argument('-sw', action='store', dest='add_stopwords', nargs='*', help='list of stopwords to add to generic stopwords', type=str)
    parser.add_argument('-bg', action='store', dest='background_color',help='choose background color; check named color options in Python', type=str)
    parser.add_argument('-w', action='store', dest='width',help='image width in pixels', type=int)
    parser.add_argument('-height', action='store', dest='height',help='image height in pixels', type=int)
    parser.add_argument('-maxwords', action='store', dest='maxwords',help='maximum number of different words to display in word cloud', type=int)
    parser.add_argument('-h_ratio', action='store', dest='horizontal_ratio',help='ratio of words that are going to be displayed horizontally', type=float)
    parser.add_argument('-ct', action='store', dest='collocation_threshold',help='collocation threshold', type=int)
    parser.add_argument('-s', action='store', dest='saturation',help='saturation', type=int)
    parser.add_argument('-l', action='store', dest='lightness',help='lightness', type=int)
    parser.add_argument('-o', action='store', dest='output',help='name of output file', type=str)
    parser.add_argument('-x1', action='store', dest='replace_word', nargs='*',help='words to replace with substitutes in text; needs to be used in combination with "-x2"', type=str)
    parser.add_argument('-x2', action='store', dest='with_substitute', nargs='*',help='substitut words; need to be added in order with "-x1"', type=str)
    parser.add_argument('-whatsapp', action='store', dest='whatsapp', nargs='*',help='True if using exported WhatsApp chats; default:False', type=bool)

    args = parser.parse_args()

    # filter out None-values
    all_args = {k:v for k,v in vars(args).items() if v!=None}

    # check if command line arguments were passed
    if len(all_args) > 0:

        print("Word cloud settings customized:")
        
        for k, v in all_args.items():
            print(f"\t{k} set to: {v}")
        print('\n')

        # make sure x1 and x2 command line entries were of the same length if either of these arguments were passed; if not throw error
        if ('replace_word' in all_args.keys() or 'with_substitute' in all_args.keys()):
            try:
                if len(all_args['replace_word']) != len(all_args['with_substitute']):
                    print("Error: '-x1' and '-x2' need to need to be of the same length!")
                    sys.exit()
                else:
                    counter=0
                    for word in all_args['replace_word']:
                        if "_" in word:
                            separate = word.replace("_", " ")
                            all_args['replace_word'][counter] = separate
                        counter+=1

                    counter=0
                    for word in all_args['with_substitute']:
                        if "_" in word:
                            separate = word.replace("_", " ")
                            all_args['with_substitute'][counter] = separate
                        counter+=1

            except Exception as e:
                print(f"{e}\nFix: '-x1' and '-x2' need to be passed together!")
                sys.exit()

    # exclude values passed to -x1 or -x2 from custom_args, as these should not be passed to class constructor - save these values in  
    custom_args = {k:v for k,v in all_args.items() if k not in ["replace_word", "with_substitute"]}
    word_replacements = {k:v for k,v in all_args.items() if k in ["replace_word", "with_substitute"]}

    return custom_args, word_replacements


class CloudFromDoc(WordCloud):
    def __init__(self, file_path='doc.txt', add_stopwords=['said','would','one'], background_color='white', 
                 width=1500, height=1000, maxwords=1000, horizontal_ratio=0.75, 
                 collocation_threshold=30, hue=322, saturation=None, lightness=None, output=None, whatsapp=None, **kwargs):
        
        self.path = file_path
        self.stopwords = sw.words()
        self.stopwords.extend(add_stopwords)
        self.width = width
        self.height = height
        self.maxwords = maxwords
        self.horizontal = horizontal_ratio
        self.collocation_thresh = collocation_threshold
        self.bg_color = background_color
        self.whatsapp = whatsapp #NOTE: self.whatsapp is referenced in self._read_document(), so it needs to be defined prior to calling this funtion
        self.text = self._read_document()
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness
        self.output = output 

        print(self.whatsapp)

        self.cloud = WordCloud(
            background_color=self.bg_color, 
            width=self.width, 
            height=self.height,
            stopwords=self.stopwords,
            max_words=self.maxwords,
            prefer_horizontal=self.horizontal,
            collocation_threshold=self.collocation_thresh)
 
    def mk_cloud(self):
        
        print(f'Word cloud will be created with a width of {self.width} and a height of {self.height} pixel')
        print(f'Word cloud hsl-color will be: hue-{"random" if self.hue==None else str(self.hue)}, saturation-{"random" if self.saturation==None else str(self.saturation)}, lightness-{"random" if self.lightness==None else str(self.lightness)}')
        print(f'Creating word cloud from {self.path}...')

        self.cloud.generate(self.text)
        
        # output name 
        cwd = self.set_output()

        # show
        plt.figure(f"Don't worry, this word cloud was saved in {cwd} as:      '{self.output}'", figsize=[50,30])
        plt.imshow(self.cloud.recolor(color_func = self.custom_color_func), interpolation="sinc")
        plt.axis("off")

        # # store to file
        self.save_wc()

        plt.tight_layout()
        plt.show()

    def replace_words(self, replace_word:list, with_substitute:list):
        '''
        Function taking to lists and passing them to the string method .replace();
        Saves new string with replaced values in self.text
        '''
        # add lower-case versio, the capitalized version and the title version for each word in list to new list --> to account for words at beginning of the sentence
        to_replace = [x for i in replace_word for x in (i.lower() ,i.capitalize(),i.title())]
        substitute = [x for i in with_substitute for x in (i ,i , i)] #tuple of 3 i's because to_replace and substitue need to be of same length, BUT I only want given spelling here (defined by me)

        for word, subs in zip(to_replace, substitute): 
            self.text = self.text.replace(word, subs) 
        return self
        
        
    def process_text(self, text):
        '''
        Processes text in order to filter out punctuation
        '''
        from nltk.tokenize import RegexpTokenizer

        tokenizer = RegexpTokenizer(r'\w+')
        processed_text = " ".join(tokenizer.tokenize(text))

        return processed_text
        
        
    def _read_document(self):

        with open(self.path, "r", encoding='utf-8') as myfile:
            data = myfile.readlines()

        text = ','.join(data) 

        if self.whatsapp!=None: #not "if self.whatsapp:" - because this will be an empty list and if self.whatsapp will be False
            text = self.preprocess_whatsapp(text) 

        text = self.process_text(text)

        return text

    def custom_color_func(self, **kwargs):
        if self.bg_color == 'white':
            return(f"hsl({np.random.randint(0,360) if self.hue==None else self.hue}, {np.random.randint(15,100) if self.saturation==None else self.saturation}%, {np.random.randint(0,60) if self.lightness==None else self.lightness}%)")
        elif self.bg_color == 'black':
            return(f"hsl({np.random.randint(0,360) if self.hue==None else self.hue}, {np.random.randint(15,100) if self.saturation==None else self.saturation}%, {np.random.randint(7,65) if self.lightness==None else self.lightness}%)")

    def set_output(self):  
        cwd = os.getcwd()
        hue = '' if self.hue== None else 'H'+str(self.hue)
        saturation = '' if self.saturation== None else 'S'+str(self.saturation)
        lightness = '' if self.lightness== None else 'L'+str(self.lightness)
        if self.output==None:
            self.output = f"cloud_Size{self.width}_{self.height}_hslColor{'Random' if (self.hue==None and self.saturation==None and self.lightness==None) else f'{hue}{saturation}{lightness}'}.png"
        return cwd

    def save_wc(self):
        print(self.output)
        self.cloud.to_file(self.output)
        print(f'Wordcloud image saved in {self.output}')
    
    def preprocess_whatsapp(self, text):
        """
        Pre-processing of WhatsApp text exports, to make them suitable for inout into wordcloud.
        Text files from WhatsApp chat export start every message with the following format '[m]m/[d]d/yy, hh:mm - sender_name:'.
        Additionally WhatsApp-specific text like 'Missed voice call' or '<Media omitted>' are within the text.
        In order to create a wordcloud that does not display these text parts (date/time, Whatsapp text, contact name) as frequent words, 
        these parts will be filtered out and removed from text.
        """
        regx = r'(\d+/\d+/\d+,\s\d{2}\:\d{2}\s-\s[\s\w.]*:)' #regex for '[m]m/[d]d/yy, hh:mm - sender_name:' - the beginning of every Whatsapp chat export entry
        pattern = re.compile(regx)

        # list with pattern filtered out
        filtered_list = [x for x in re.compile(regx).split(text) if not pattern.match(x)] #splits text on regex pattern and only keeps npn-pattern chunks
        # join list into string
        filtered_text = " ".join(filtered_list)

        # remove WhatsApp export information, such as 'Media omitted', 'Missed voice call' or 'Video call'
        processed_text = filtered_text.replace("Media omitted","").replace("Missed voice call","").replace("Missed video call","").replace("Video call","").replace("Voice call","")

        return processed_text

if __name__ == '__main__':
    custom_args, word_replacements = main()
    if word_replacements:
        CloudFromDoc(**custom_args).replace_words(**word_replacements).mk_cloud()

    else:
        CloudFromDoc(**custom_args).mk_cloud() 