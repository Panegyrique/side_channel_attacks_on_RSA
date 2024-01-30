# Attaque Side Channel sur RSA

## Attaque temporelle

Pour lancer l'attaque, transférez les fichiers contenus dans le dossier nommé **RSA-Timing-Attack** sur votre carte cible (assurez-vous que votre carte cible peut exécuter des scripts Python3), et lancez le script désiré parmi :
- Attaque sur un algorithme de cryptage RSA utilisant une exponentiation rapide : **timing_attack_square_and_multiply.py**
- Attaque sur un algorithme de cryptage RSA utilisant l'algorithme de Montgomery : **timing_attack_montgomery.py**
- Attaque sur un algorithme de cryptage RSA utilisant le théorème des restes chinois : **timing_attack_CRT.py**

## Attaque EM

Pour réaliser des attaques par ondes électromagnétiques, vous aurez besoin d'une clé RTL-SDR et d'une antenne captant les fréquences du processeur de votre cible. Pour lancer l'attaque, transférez les fichiers contenus dans le dossier nommé **RSA-EM-Attack** sur votre carte cible (assurez-vous que votre carte cible peut exécuter des scripts python3).

- Dans les fichiers python de ce dossier, il y a une constante **TIME** qui peut être ajustée si votre fréquence d'échantillonnage est trop basse.
- Les fichiers texte de ce dossier sont des fichiers de test contenant des données cryptées avec une clé RSA de 32 bits. N'hésitez pas à modifier cet ensemble en utilisant **main.py** dans le dossier **RSA** (rendez vous dans la section **Générer des données**).

> Attention ! !! Plusieurs paramètres dans **data_raw_save.py** doivent être adaptés à votre situation. Pour ce faire, modifiez toutes les variables avec le commentaire suivant : **CHANGE HERE**

Pour démarrer l'acquisition des courbes :

- Sous Linux :
	``` bash
	# Installer GNURadio
	sudo apt-get install gnuradio
	
	# Exécuter le script
	python3 /path/to/data_raw_save.py
	```
- Sous Windows :
	- Télécharger [GNURadio](https://wiki.gnuradio.org/index.php/InstallingGR), l'installer en utilisant radioconda pour ce faire, cliquer sur **Windows Radioconda installer**
	- Exécutez le script depuis un terminal
	``` Bash
	pathto\radioconda\python.exe -u pathto\GNURadio\data_raw_save.py
	```

Pour traiter les données, utilisez les scripts présent dans le dossier **MATLAB**

## Générer des données

Lancez simplement le script **main.py** et suivez les instructions