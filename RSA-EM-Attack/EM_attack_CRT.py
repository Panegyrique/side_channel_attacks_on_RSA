import time
TIME = 0.00625


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
    

def chinese_remainder_theorem(p, q, C, n, d):
    """
    Calcule le résultat de l'équation M ≡ C^d mod n avec le théorème des restes chinois.
    
    Paramètres:
        p (int): nombre premier p.
        q (int): nombre premier q.
        C (int): Le message à déchiffrer.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant de chiffrement de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)
    m1 = pow(C, dp, p)
    m2 = pow(C, dq, q)
    h = (qinv * (m1 - m2)) % p
    M = m2 + h * q
    return M


def decrypt(p, q, C, n, d):
    """
    Déchiffre le message envoyé en paramètre (C).
    
    Paramètres:
        C (int): Le message chiffré.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant privé de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    if C < 0 or C >= n: # Vérifie que le message est entre 0 et n
        raise ValueError("Le message chiffré doit être un entier naturel strictement inférieur à n")
    M = chinese_remainder_theorem(p, q, C, n, d)
    return M


if __name__ == '__main__':
	
    with open('RSA_keys.txt', 'r') as file: # Charge la clé privée depuis le fichier .txt
        line = file.readlines()
        n, d = map(int, line[1].strip('()\n').split(','))
        p, q = map(int, line[2].strip("()\n").split(","))

    with open('RSA_message_encrypted.txt', 'r') as file: # Récupération des messages à déchiffer
        all_C_temp = file.readlines()

    print("Begin of the EM attack on CRT algorithm !!!\n")

    for i in range(len(all_C_temp)):
        C_temp = int(all_C_temp[i])

        print("TRIGGER")
        start = time.time()
        M = decrypt(p, q, C_temp, n, d)
        end = time.time()
        print("UNTRIGGER")

        print("C %s/%s decrypt in %s s\n"%(i, len(all_C_temp), end-start))
        time.sleep(1)