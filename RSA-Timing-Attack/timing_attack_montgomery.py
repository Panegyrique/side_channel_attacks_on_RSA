import time


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


def montgomery(C, n, d, k):
    """
    Calcule le résultat de l'équation M ≡ C^d mod n avec l'algorithme de montgomery.
    
    Paramètres:
        C (int): Le message à déchiffrer ou à chiffrer.
        n (int): Le module pour les clés publique et privée.
        d (int): L'exposant de chiffrement ou de déchiffrement de la clé RSA.

    Retourne:
        M (int): Le message déchiffré.
    """
    R = 2 ** n.bit_length()
    R_inverse = modinv(R % n, n)
    u = (C * R) % n
    v = R % n
    d = d[::-1]
    for bit in range(k+1):
        if d[bit] == '1':
            v = multiply(R, R_inverse, v, u, n)
        u = multiply(R, R_inverse, u, u, n)
    M = (v * R_inverse) % n
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
    M = montgomery(C, n, d, k)
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