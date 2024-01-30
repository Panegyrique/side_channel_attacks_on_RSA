import time
TIME = 0.00625


def square_and_multiply(C, n, d):
    """
    Calcule le résultat de l'équation M = C^d mod n avec l'algorithme square and multiply.
    
    Paramètres:
        C (int): Le message chiffré.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant privé de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    M = 1
    for bit in bin(d)[2:]: # parcourt chaque bit de d
        M = (M ** 2) % n # opération de carré
        if bit == '1':
            M = (C * M) % n # opération de multiplication
        time.sleep(TIME) # Simulation de l'attaque par faute
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
    M = square_and_multiply(C, n, d)
    return M


if __name__ == '__main__':
	
    with open('RSA_keys.txt', 'r') as file: # Charge la clé privée depuis le fichier .txt
        line = file.readlines()
    n, d = map(int, line[1].strip('()\n').split(','))

    with open('RSA_message_encrypted.txt', 'r') as file: # Récupération des messages à déchiffer
        all_C_temp = file.readlines()

    print("Begin of the EM attack on Square and Multiply algorithm !!!\n")

    for i in range(len(all_C_temp)):
        C_temp = int(all_C_temp[i])

        print("TRIGGER")
        start = time.time()
        M = decrypt(C_temp, n, d)
        end = time.time()
        print("UNTRIGGER")

        print("C %s/%s decrypt in %s s\n"%(i, len(all_C_temp), end-start))
        time.sleep(1)