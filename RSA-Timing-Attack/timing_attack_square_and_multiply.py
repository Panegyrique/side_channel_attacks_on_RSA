import time


def square_and_multiply(C, n, d, k):
    """
    Calcule le résultat de l'équation M = C^d mod n avec l'algorithme square and multiply.
    
    Paramètres:
        C (int): Le message chiffré.
        n (int): Le module pour les clés publique et privée.
        d (list): L'exposant privé de la clé RSA sous forme de liste binaire.
        k (int): La limite de bit testé.

    Retourne:
        M (int): Le message déchiffré.
    """
    M = 1
    for bit in range(k+1): # parcourt chaque bit de d
        M = (M ** 2) % n # opération de carré
        if d[bit] == 1:
            M = (C * M) % n # opération de multiplication
    return M


def elapsed_time(C, n, d, k):
    """
    Mesure le temps d'éxécution de l'algorithme square and multiply.
    
    Paramètres:
        C (int): Le message chiffré.
        n (int): Le module pour les clés publique et privée.
        d (list): L'exposant privé de la clé RSA sous forme de liste binaire.
        k (int): La limite de bit testé.

    Retourne:
        ti (int): Le message écoulé pour déchiffré C.
    """
    ti = 0
    start = time.perf_counter()
    M = square_and_multiply(C, n, d, k)
    end = time.perf_counter()
    ti = end - start
    return ti


def kocher_attack(ciphertexts, n, d):
    """
    Réalise l'attaque décrite par Kocher en 1996.
    
    Paramètres:
        ciphertexts (liste): L'ensemble des messages chiffrés.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant privé de la clé RSA.

    Retourne:
        d_found (list): L'exposant privé d trouvé après l'attaque.
    """
    keylength = d.bit_length()
    d_binary = [int(bit) for bit in bin(d)[2:]]
    d_found = [1]
    d0 = [d_found[0]]
    d1 = [d_found[0]]

    for k in range(keylength - 1):
        print("# bit: %s/%s\tNumber of ciphertexts: %s"%(k + 2, keylength, len(ciphertexts)))

        delta0 = [0] * len(ciphertexts)
        delta1 = [0] * len(ciphertexts)

        for i, C in enumerate(ciphertexts):
            T = elapsed_time(C, n, d_binary, k+1)
            T0 = elapsed_time(C, n, d0+[0], k+1)
            T1 = elapsed_time(C, n, d1+[1], k+1)
            delta0[i] = abs(T - T0)
            delta1[i] = abs(T - T1)

        mean0 = sum(delta0) / len(delta0)
        mean1 = sum(delta1) / len(delta1)

        if mean0 < mean1:
            d_found.append(0)
        else:
            d_found.append(1)

        d0 = d_found
        d1 = d_found

    return d_found


def verify(d, d_found, start):
    """
    Vérifie si la clé privé à bien été trouvée et si non, combien de % trouvé.
    
    Paramètres:
        d (int): L'exposant privé de la clé RSA.
        d_found (list): L'exposant privé trouvé de la clé RSA sous forme de liste binaire.

    Retourne:
        rien
    """
    keylength = d.bit_length()
    d_binary = [int(bit) for bit in bin(d)[2:]]
    d_binary_str = bin(d)[2:]
    d_found_binary_str = ''.join(map(str, d_found))
    if(d_binary_str == d_found_binary_str):
        print("\nKey found at 100%\nd: {}\nd_found: {}".format(d_binary_str, d_found_binary_str), end="")
    else:
        ratio = 0
        for i in range(keylength):
            if d_binary[i] == d_found[i]:
                ratio += 1
        print("Found only {:.2f}%".format(ratio*100/keylength), end="")
    print(" in {:.2f} s".format(time.perf_counter() - start))


if __name__ == "__main__":

    with open('RSA_keys.txt', 'r') as file:
        lines = file.readlines()
        n, d = map(int, lines[1].strip('()\n').split(','))

    with open('RSA_message_encrypted.txt', 'r') as file: # Récupération des messages à déchiffer
        ciphertexts = [int(line.strip()) for line in file.readlines()]

    start = time.perf_counter()
    d_found = kocher_attack(ciphertexts, n, d)
    verify(d, d_found, start)