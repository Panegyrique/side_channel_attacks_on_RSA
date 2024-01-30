import random
import os
import numpy as np
from math import gcd
from sympy import isprime, mod_inverse


def generate_prime(bits):
    """
    Génére un nombre premier du bon nombre de bits.
    
    Paramètre:
        bits (int): La longueur en bits du nombre souhaité.

    Retourne:
        num (int): Un nombre premier du nombre de bits souhaité.
    """
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num


def generate_keypair(key_length):
    """
    Génére une paire de clé privé et publique.
    
    Paramètre:
        key_length (int): La longueur de la clé souhaitée.

    Retourne:
        public_key (int, int): Une paire publique (n, e).
        private_key (int, int) : Une paire privé (n, d).
    """
    n = 0
    while n.bit_length() != key_length:
        p = generate_prime(key_length // 2)
        q = generate_prime(key_length // 2)

        n = p * q

    phi_n = (p - 1) * (q - 1)

    # Exposant de chiffrement, e
    e = 65537  # Un choix commun pour e, souvent un nombre de Fermat

    while gcd(e, phi_n) != 1: # Vérifie si e est premier avec ϕ(n)
        e = random.randrange(2, phi_n)

    d = mod_inverse(e, phi_n)

    public_key = (n, e)
    private_key = (n, d)
    p_q = (p, q)

    return p_q, public_key, private_key


def modinv(a, m):
    """
    Calcule l'inverse modulaire de a modulo m.
    
    Paramètres:
        a (int): L'entier dont on veut calculer l'inverse modulaire.
        m (int): Le module pour le calcul de l'inverse modulaire.

    Retourne:
        inv (int): L'inverse modulaire de a modulo m.
    """
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("L'inverse modulaire n'existe pas")
    else:
        inv = x % m
        return inv
    

def multiply(R, R_inverse, a, b, n):
    """
    Effectue une multiplication modulaire en utilisant l'algorithme de Montgomery.
    
    Paramètres:
        R (int): Le réducteur utilisé pour l'opération de réduction de Montgomery.
        R_inverse (int): L'inverse de R modulo n.
        a (int), b (int): Les deux nombres à multiplier.
        n (int): Le module pour les clés publique et privée.

    Retourne:
        mul (int): Le résultat de la multiplication modulaire.
    """
    mask = (((a * b) & (R - 1)) * ((R * R_inverse - 1) // n)) & (R - 1)
    reduced_result = ((a * b) + mask * n) // (2 ** n.bit_length())
    if reduced_result < n:
        mul = reduced_result
    else:
        mul = reduced_result - n
    return mul


def montgomery(Y, n, x):
    """
    Calcule le résultat de l'équation R ≡ Y^x mod n avec l'algorithme de montgomery.
    
    Paramètres:
        Y (int): Le message à déchiffrer ou à chiffrer.
        n (int): Le module pour les clés publique et privée.
        x (int): L'exposant de chiffrement ou de déchiffrement de la clé RSA.

    Retourne:
        A (int): Le message déchiffré ou chiffré.
    """
    R = 2 ** n.bit_length()
    R_inverse = modinv(R % n, n)
    u = (Y * R) % n
    v = R % n
    for bit in bin(x)[:1:-1]:
        if bit == '1':
            v = multiply(R, R_inverse, v, u, n)
        u = multiply(R, R_inverse, u, u, n)
    A = (v * R_inverse) % n
    return A


def square_and_multiply(Y, n, x):
    """
    Calcule le résultat de l'équation R ≡ Y^x mod n avec l'algorithme square and multiply.
    
    Paramètres:
        Y (int): Le message à déchiffrer ou à chiffrer.
        n (int): Le module pour les clés publique et privée.
        x (int): L'exposant de chiffrement ou de déchiffrement de la clé RSA.

    Retourne:
        A (int): Le message déchiffré ou chiffré.
    """
    A = 1
    for bit in bin(x)[2:]:
        A = (A ** 2) % n
        if bit == '1':
            A = (Y * A) % n
    return A


def chinese_remainder_theorem(p, q, Y, n, x):
    """
    Calcule le résultat de l'équation A ≡ Y^x mod n avec le théorème des restes chinois.
    
    Paramètres:
        p (int): nombre premier p.
        q (int): nombre premier q.
        Y (int): Le message à déchiffrer ou à chiffrer.
        n (int): Le module pour les clés publique et privée.
        x (int): L'exposant de chiffrement ou de déchiffrement de la clé RSA.

    Retourne:
        A (int): Le message déchiffré ou chiffré.
    """
    dp = x % (p - 1)
    dq = x % (q - 1)
    qinv = modinv(q, p)
    m1 = pow(Y, dp, p)
    m2 = pow(Y, dq, q)
    h = (qinv * (m1 - m2)) % p
    A = m2 + h * q
    return A


def encrypt(M, n, e):
    """
    Chiffre le message envoyé en paramètre (M).
    
    Paramètres:
        M (int): Le message à chiffrer.
        n (int): Le module pour les clés publique et privée.
        e (int): L'exposant de chiffrement de la clé RSA.

    Retourne:
        C (int): Le message chiffré.
    """
    if M < 0 or M >= n:
        raise ValueError("Le message doit être un entier naturel strictement inférieur à n")
    C = square_and_multiply(M, n, e)
    return C


def decrypt(algo, p, q, C, n, d):
    """
    Déchiffre le message envoyé en paramètre (C).
    
    Paramètres:
        algo (int): Le mode de déchiffrage utilisé.
        p (int): nombre premier p.
        q (int): nombre premier q.
        C (int): Le message chiffré.
        n (int): Le module pour les clés publique et privée (n = pq).
        d (int): L'exposant privé de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    if C < 0 or C >= n:
        raise ValueError("Le message chiffré doit être un entier naturel strictement inférieur à n")
    
    if algo == 1:
        M = montgomery(C, n, d)
    elif algo == 2:
        M = square_and_multiply(C, n, d)
    elif algo == 3:
        M = chinese_remainder_theorem(p, q, C, n, d)

    return M


def get_mode():
    """
    Retourne le mode souhaité par l'utilisateur à savoir Générer des données chiffrée ou déchiffrer ces données.
    
    Paramètres:
        aucun

    Retourne:
        mode (int): Le mode choisi.
    """
    while True:
        try:
            mode = int(input("$>Choose between:\n$>Generate data: 1\n$>Decrypt data : 2\n$>"))
            if mode == 1 or mode == 2:
                return mode
            else:
                print("1 or 2")
        except ValueError:
            print("ValueError")


def launch_mode(mode):
    """
    Retourne le mode souhaité par l'utilisateur à savoir Générer une paire de clé avec des données chiffrée ou déchiffrer ces données.
    
    Paramètres:
        mode (int): Le mode choisi.

    Retourne:
        rien
    """
    if mode == 1: # Générer une paire de clé avec des données chiffrées
        while True:
            try:
                keylength = int(input("\n$>Keylength in bits:\n$>"))
                if keylength > 0:
                    break
                else:
                    print(">0")
            except ValueError:
                print("ValueError")

        p_q, public_key, private_key = generate_keypair(keylength)
        with open("RSA_keys.txt", "w") as file: # Enregistrer les clés dans un fichier .txt (overwrite si déjà existant)
            file.write("%s\n%s\n%s" % (public_key, private_key, p_q))
        for file_name in ["RSA_message_to_encrypt.txt", "RSA_message_encrypted.txt", "RSA_message_decrypted.txt"]: # Vider les fichiers s"ils existent
            if os.path.exists(file_name):
                open(file_name, "w").close()

        n, e = public_key # Paramètres
        number_of_M = 10000
        all_M = np.random.randint(n//100, size=number_of_M)

        for i in range(len(all_M)):
            M_temp = all_M[i]
            C = encrypt(M_temp, n, e)
            with open("RSA_message_to_encrypt.txt","a") as file: # Enregistre le message à chiffrer dans un fichier .txt
                file.write("%s\n"%M_temp)
            with open("RSA_message_encrypted.txt","a") as file: # Enregistre le message chiffré dans un fichier .txt
                file.write("%s\n"%C)
            print("Progression: {:.2f}%".format((i+1)*100/len(all_M)))

    elif mode == 2: # Déchiffrer les données générées
        while True:
            try:
                algo = int(input("\n$>Which algorithm:\n$>Montgomery: 1\n$>Square and multiply: 2\n$>chinese Remainder Theorem: 3\n$>"))
                if algo == 1 or algo == 2 or algo == 3:
                    break
                else:
                    print("1, 2 or 3")
            except ValueError:
                print("ValueError")

        with open("RSA_keys.txt", "r") as file:
            line = file.readlines()
            n, d = map(int, line[1].strip("()\n").split(","))
            p, q = map(int, line[2].strip("()\n").split(","))

        with open("RSA_message_encrypted.txt", "r") as file:
            ciphertexts = [int(line.strip()) for line in file.readlines()]
            
        file_name = "RSA_message_decrypted.txt"
        if os.path.exists(file_name):
                open(file_name, "w").close()

        for i in range(len(ciphertexts)):
            C = ciphertexts[i]
            M = decrypt(algo, p, q, C, n, d)
            with open("RSA_message_decrypted.txt", "a") as file: # Enregistre le message déchiffré dans un fichier .txt
                file.write("%s\n"%M)
            print("Progression: {:.2f}%".format((i+1)*100/len(ciphertexts)))