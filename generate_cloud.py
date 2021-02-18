import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.corpus import stopwords as sw
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Customize your word cloud!')
    parser.add_argument('-f', action='store', dest='file_path',help='path to text document', type=str)
    parser.add_argument('-hue', action='store', dest='hue',help='color for word cloud', type=int)
    parser.add_argument('-sw', action='store', dest='add_stopwords',help='list of stopwords to add to generic stopwords', type=list)
    parser.add_argument('-bg', action='store', dest='background_color',help='choose background color; check named color options in Python', type=str)
    parser.add_argument('-w', action='store', dest='width',help='image width in pixels', type=int)
    parser.add_argument('-height', action='store', dest='height',help='image height in pixels', type=int)
    parser.add_argument('-maxwords', action='store', dest='maxwords',help='maximum number of different words to display in word cloud', type=int)
    parser.add_argument('-h_ratio', action='store', dest='horizontal_ratio',help='ratio of words that are going to be displayed horizontally', type=int)
    parser.add_argument('-ct', action='store', dest='collocation_threshold',help='collocation threshold', type=int)
    parser.add_argument('-s', action='store', dest='saturation',help='saturation', type=int)
    parser.add_argument('-l', action='store', dest='lightness',help='lightness', type=int)
    parser.add_argument('-o', action='store', dest='output',help='name of output file', type=str)

    args = parser.parse_args()

    # filter out None-values
    custom_args = {k:v for k,v in vars(args).items() if v!=None}
    if len(custom_args) > 0:
        print("Word cloud settings customized:")
        for k, v in custom_args.items():
            print(f"\t{k} set to: {v}")
        print('\n')
    return custom_args

class CloudFromDoc(WordCloud):
    def __init__(self, file_path='example.txt', add_stopwords=['said','would','one'], background_color='white', 
                 width=1500, height=1000, maxwords=1000, horizontal_ratio=0.75, 
                 collocation_threshold=30, hue=322, saturation=None, lightness=None, output=None, **kwargs):
        
        self.path = file_path
        self.stopwords = sw.words()
        self.stopwords.extend(add_stopwords)
        self.width = width
        self.height = height
        self.maxwords = maxwords
        self.horizontal = horizontal_ratio
        self.collocation_thresh = collocation_threshold
        self.bg_color = background_color
        self.text = self._read_document()
        self.hue = hue
        self.saturation = saturation
        self.lightness = lightness
        self.output = output 
        
        print(f'Word cloud will be created with a width of {self.width} and a height of {self.height} pixel')
        print(f'Word cloud hsl-color will be: hue-{"random" if self.hue==None else str(self.hue)}, saturation-{"random" if self.saturation==None else str(self.saturation)}, lightness-{"random" if self.lightness==None else str(self.lightness)}')
        print(f'Creating word cloud from {self.path}...')

        self.cloud = WordCloud(background_color=self.bg_color, 
                   width=self.width, 
                   height=self.height,
                   stopwords=self.stopwords,
                   max_words=self.maxwords,
                  prefer_horizontal=self.horizontal,
                  collocation_threshold=self.collocation_thresh)
        
        self.cloud.generate(self.text)
        
        # show
        plt.figure(figsize=[50,30])
        plt.imshow(self.cloud.recolor(color_func = self.custom_color_func), interpolation="sinc")
        plt.axis("off")

        # # store to file
        self.save_wc()

        plt.tight_layout()
        plt.show()
        
        
    def _read_document(self):
        with open(self.path, "r", encoding='utf-8') as myfile:
            data = myfile.readlines()
        text = ','.join(data)
        return text

    def custom_color_func(self, **kwargs):
        return(f"hsl({np.random.randint(0,360) if self.hue==None else self.hue}, {np.random.randint(15,100) if self.saturation==None else self.saturation}%, {np.random.randint(0,60) if self.lightness==None else self.lightness}%)")
    
    def save_wc(self):
        hue = '' if self.hue== None else 'H'+str(self.hue)
        saturation = '' if self.saturation== None else 'S'+str(self.saturation)
        lightness = '' if self.lightness== None else 'L'+str(self.lightness)
        if self.output==None:
            self.output = f"wc_Size{self.width}_{self.height}_hslColor{'Random' if (self.hue==None and self.saturation==None and self.lightness==None) else f'{hue}{saturation}{lightness}'}.png"
        self.cloud.to_file(self.output)
        print(f'Wordcloud image saved in {self.output}')

if __name__ == '__main__':
    custom_args = main()
    CloudFromDoc(**custom_args)