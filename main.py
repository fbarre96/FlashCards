# coding: utf-8
import json
import random
import sys, locale
from collections import OrderedDict 
def loadFile(path):
	with open(path) as fichier:
		contenu = fichier.read()
		return contenu

if len(sys.argv) != 2:
	print "Usage: python main.py <deck.d>"
	sys.exit(1)

nom=sys.argv[1]
contenu = loadFile(nom)
dicto = json.loads(contenu)
print "Choisi le sens des cartes pour les questions:"
print "1. Recto/Verso"
print "2. Verso/Recto"
print "3. Random"
choix = input()

compteur = 0
c=1
b = list(dicto.items())
random.shuffle(b)
print "Tu peux à tout moment taper 'fuck' si tu estimes avoir mériter le point et que ta réponse a été marqué incorrect."
for key,value in b:

	q = key
	a = value
	b=0
	if choix == 3:
		b=random.getrandbits(1)
	if choix == 2 or b == 1:
		q = value
		a = key
	
	print "Question "+str(c)+"/"+str(len(dicto))+": "+(q)
	print u"Réponse: ",
	answer = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
	if answer.lower() == u"fuck":
		compteur+=1
		print u"La réponse à votre précédant question a été changé à Correct"
		print "Question "+str(c)+"/"+str(len(dicto))+": "+(q)
		print "Réponse: ",
		answer = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
	if answer.lower() == a.lower():
		print "Correct"
		compteur+=1
	else:
		print "Incorrect : réponse correct : "+a
	c+=1

print "\n Score:"+str(compteur)+"/"+str(len(dicto))
