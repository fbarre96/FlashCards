# coding: utf-8
import json
import random
import sys, locale
import os
from collections import OrderedDict 
def loadFile(path):
	with open(path) as fichier:
		contenu = fichier.read()
		return contenu

def afficheAide(reponse, nbIndiceDonnee):
	if nbIndiceDonnee == 1:
		print "*"*(len(reponse)-1)+reponse[-1]
	elif nbIndiceDonnee == 2:
		print reponse[0]+"*"*(len(reponse)-2)+reponse[-1]
	elif nbIndiceDonnee == 3:
		print reponse[:2]+"*"*(len(reponse)-4)+reponse[-2:]
	elif nbIndiceDonnee >= 4:
		if len(reponse)>=((nbIndiceDonnee-1)*2)+1:
			print reponse[:nbIndiceDonnee-1]+"*"*(len(reponse)-(nbIndiceDonnee-1)*2)+reponse[0-(nbIndiceDonnee-1):]
		else:
			print "Plus d'indice à donné !"
if len(sys.argv) != 2:
	print "Usage: python main.py <deck.d>"
	sys.exit(1)
wrongs = []
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
print "Tu peux à tout moment taper 'fuck' si tu estimes avoir mérité le point et que ta réponse a été marqué incorrect."
print "Tu peux à tout moment taper 'aide' si tu veux un indice (le point ne sera pas accordé)."

for key,value in b:
	nbIndiceDonnee=0
	q = key
	a = value
	b=0
	if choix == 3:
		b=random.getrandbits(1)
	if choix == 2 or b == 1:
		q = value
		a = key
	changeQuestion=False
	while not changeQuestion:
		print "Question "+str(c)+"/"+str(len(dicto))+": "+(q)
		print u"Réponse: ",
		answer = raw_input().decode(sys.stdin.encoding or locale.getpreferredencoding(True))
		if answer.lower() == u"fuck":
			if len(wrongs)>0:
				compteur+=1
				wrongs.pop()
				print u"La réponse à votre précédante question a été changé à Correct"
			else:
				print u"Il n'y a pas de mauvaises réponses."
		elif answer.lower() == u"aide":
			nbIndiceDonnee+=1
			afficheAide(a,nbIndiceDonnee)
		elif answer.lower() == a.lower():
			if nbIndiceDonnee == 0:
				compteur+=1
				print "Correct (+1 point)"
			else:
				print "Correct (+0 point)"
			changeQuestion = True
		else:
			print u"Incorrect : la réponse correct était : "+a
			wrongs.append([q,a])
			changeQuestion = True
	c+=1

print "\n Score:"+str(compteur)+"/"+str(len(dicto))
reponse = ""
if len(wrongs)>0:
	dicoWrongs = {}
	for wrong in wrongs:
		dicoWrongs[wrong[0]] = wrong[1]
	while reponse.lower() != "oui" and reponse.lower() != "non":
		print "Voulez vous stocker vos fautes dans un dictionnaire ? (oui/non)"
		reponse = raw_input()

	if reponse.lower() == "oui":
		nom = sys.argv[1]+"_incorrects"
		if os.path.exists(nom+".d"):
			tentative = 1
			while os.path.exists(nom+"("+str(tentative)+").d"):
				tentative += 1
				if tentative == 100:
					break
			with open(nom+"("+str(tentative)+").d","w") as fichier:
				fichier.write(json.dumps(dicoWrongs))
		else:
			with open(nom+".d","w") as fichier:
				fichier.write(json.dumps(dicoWrongs))