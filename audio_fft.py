from scipy.io.wavfile import *
from scipy.fftpack import fft
import numpy as np
from matplotlib import pyplot as plt
import json
import os
import re

from scipy.signal import hanning
from scipy.signal.windows import hamming

N=128*2
T=1.0/10000.0
data: dict = {"N":N, "fichiers":[]}
def wav_coefs(nom_fichier: str, classe:str= "inconnu"):
    fe, audio = read(nom_fichier)#on lit chaque fichier audio
    window = hamming(len(audio))
    coefs = np.abs(fft(audio*window, N)[0:N//2]) #partie réelle positive
    sortie = {
        "nom": nom_fichier,
        "coefs":coefs.tolist(),
        "classe":classe
    }
    return sortie

#for i in range(1, 9):
#    print(i)
#    fichier = wav_coefs('bonjour p2i/{}.wav'.format(i))
#    x, y = [], []
#    j = 0
#    for v in fichier['coefs']:  # présentation jolie du graph fourier
#        x.append(j)
#        x.append(j)
#        x.append(j)
#        y.append(0)
#        y.append(v)
#        y.append(0)
#        j += 1
#    plt.plot(x, y)
#    plt.ylabel('amplitude')
#    plt.xlabel('fréquence')
#    plt.show()
#    data['fichiers'].append(fichier)
wav_file = re.compile('^.+wav$')
from pathlib import Path
for dos in os.listdir('bonjour p2i'):
    try:
        for fichier in os.listdir("bonjour p2i/"+dos):
            if wav_file.match(fichier):
                print(dos+"/"+fichier)
                donnees = wav_coefs(nom_fichier="bonjour p2i/{}/{}".format(dos, fichier), classe=dos)
                data['fichiers'].append(donnees)
                x, y, j = [], [],0
                for v in donnees['coefs']:  # présentation jolie du graph fourier
                    x.append(j)
                    x.append(j)
                    x.append(j)
                    y.append(0)
                    y.append(v)
                    y.append(0)
                    j += 1
                plt.plot(x, y)
                plt.ylabel('amplitude')
                plt.xlabel('fréquence')
                plt.show()
    except NotADirectoryError:
        pass

with open('data.json', 'w+') as f:
    json.dump(data, f, sort_keys=True, indent=4)
f.close()

def analyze(audio,window):
    """
    Fonction à coller dans la console pour faire des tests et voir direct le grapghique de fourier
    """
    x, y, j, N = [], [], 0, 256
    coefs = np.abs(fft(window * audio, N)[0:N // 2])
    for v in coefs:  # présentation jolie du graph fourier
        x.append(j)
        x.append(j)
        x.append(j)
        y.append(0)
        y.append(v)
        y.append(0)
        j += 1
    plt.plot(x, y)
    plt.ylabel('amplitude')
    plt.xlabel('fréquence')
    plt.show()