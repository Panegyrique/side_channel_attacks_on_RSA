import time
TIME = 0.0625


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


def montgomery(C, n, d):
    """
    Calcule le résultat de l'équation M ≡ C^d mod n avec l'algorithme de montgomery.
    
    Paramètres:
        C (int): Le message à déchiffrer.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant de chiffrement de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    R = 2 ** n.bit_length()
    R_inverse = modinv(R % n, n)
    u = (C * R) % n
    v = R % n

    for bit in bin(d)[:1:-1]:
        if bit == '1':
            v = multiply(R, R_inverse, v, u, n)
        u = multiply(R, R_inverse, u, u, n)
        time.sleep(TIME) # Simulation de l'attaque par faute
    M = (v * R_inverse) % n

    return M


def decrypt(C, n, d):
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
    M = montgomery(C, n, d)
    return M


if __name__ == '__main__':
	
    with open('RSA_keys.txt', 'r') as file: # Charge la clé privée depuis le fichier .txt
        line = file.readlines()
    n, d = map(int, line[1].strip('()\n').split(','))

    with open('RSA_message_encrypted.txt', 'r') as file: # Récupération des messages à déchiffer
        all_C_temp = file.readlines()

    print("Begin of the EM attack on Montgomery algorithm !!!\n")

    for i in range(len(all_C_temp)):
        C_temp = int(all_C_temp[i])

        print("TRIGGER")
        start = time.time()
        M = decrypt(C_temp, n, d)
        end = time.time()
        print("UNTRIGGER")

        print("C %s/%s decrypt in %s s\n"%(i, len(all_C_temp), end-start))
        time.sleep(1)