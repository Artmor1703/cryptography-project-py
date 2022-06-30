import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 1234))
sock.listen(10)

#Asymmetric encryption keys
p_assim = 101
q_assim = 107
e_assim = 113

#Symmetric encryption keys
p_simm = 211
g_simm = 106 #Primitive Root
b_diffi = 102

client,addr = sock.accept()

#Symmetric encryption
def Decrypt():
    global key, decrypted_to_bits
    n = 3

    S = [i for i in range(0, 2 ** n)]

    key_list = [key[i:i + n] for i in range(0, len(key), n)]

    for a in range(len(key_list)):
        key_list[a] = int(key_list[a], 2)


    diff = int(len(S) - len(key_list))

    if diff != 0:
        for i in range(0, diff):
            key_list.append(key_list[i])

    def KSA():
        j = 0
        N = len(S)

        for i in range(0, N):
            j = (j + S[i] + key_list[i]) % N

            # Update S[i] and S[j]
            S[i], S[j] = S[j], S[i]

        initial_permutation_array = S

    KSA()

    def that_PGRA():

        N = len(S)
        i = j = 0
        global key_stream
        key_stream = []

        for k in range(0, len(cipher_text)):
            i = (i + 1) % N
            j = (j + S[i]) % N

            S[i], S[j] = S[j], S[i]

            t = (S[i] + S[j]) % N
            key_stream.append(S[t])

    that_PGRA()

    def that_XOR():
        global original_text
        original_text = []
        for i in range(len(cipher_text)):
            p = key_stream[i] ^ cipher_text[i]
            original_text.append(p)

    that_XOR()

    decrypted_to_bits = ""
    for i in original_text:
        decrypted_to_bits += '0' * (n - len(bin(i)[2:])) + bin(i)[2:]


#Диафонтовое уравнение
def NOD(i, j):
    while i > 0 and j > 0:
        if i >= j:
            i = i % j
        else:
            j = j % i
    return max(i, j)

def table_diophant(i, j):
    p = 1
    q = 0
    r = 0
    s = 1

    while i != 0 and j != 0:
        if i >= j:
            i -= j
            p -= r
            q -= s
        else:
            j -= i
            r -= p
            s -= q
    if i != 0:
        X = p
        Y = q
    else:
        X = r
        Y = s
    return X, Y

def diophantine(a, b, c):
    (u, v) = table_diophant(a, b)
    x = u * (c // NOD(a, b))
    y = v * (c // NOD(a, b))
    return y


def bin_to_dec(digit):
    l = len(digit)
    num_dec = 0
    for i in range(0,l):
        num_dec = num_dec+int(digit[i])*(2**(l-i-1))
    return num_dec

while True:
    client.send(b'How you want to encrypt?\n'
                b'For for symmetric encryption press s'
                b'\nFor asymmetric encryption press a')

    ans = client.recv(1024).decode('utf-8')

    if ans == 'a' or ans == 'A': #Asymmetric encryption
        client.send(b'Please, enter message for RSA encrypt')
        ans = client.recv(1024).decode('utf-8')


        n = p_assim*q_assim
        fi_n = (p_assim-1) * (q_assim-1)
        d = diophantine(fi_n,e_assim,1)

        #Sending to client
        client.send(str(e_assim).encode())
        client.send(str(n).encode())
        #print('From server -> e, n to client')

        #Получаем зашифрованное сообщение
        asimm_decode = ''
        c = list(client.recv(1024).decode('utf-8').split(','))
        #print('Caught encrypt message')
        cnt = 0
        for i in c:
            c[cnt] = int(c[cnt])
            cnt += 1
        for i in c:
            asimm_decode += chr(i**d % n)
        print('Decrypt RSA message -> ' + asimm_decode) #Декодировали сообщение
        client.send(b'process completed')

    if ans == 's' or ans == 'S': #Symmetric encryption
        client.send(str(p_simm).encode())
        client.send(str(g_simm).encode())
        #print('From server -> p, g to client')

        B = g_simm ** b_diffi % p_simm

        A = int(client.recv(1024).decode('utf-8'))
        #print('Caught client open key from client')
        client.send(str(B).encode())
        key = bin(A ** b_diffi % p_simm)[2::] #Private key

        # print('DH key in binary: ' + str(key))

        client.send(b'Please, enter your message for RC4 encrypt')
        ans = client.recv(1024).decode('utf-8')
        #Array with encrypted characters
        decrypt_simm_mess = ''
        simm_cipher = list(client.recv(1024).decode('utf-8').split(','))
        for cipher_text in simm_cipher:
            cipher_text = list(cipher_text)
            for z in range(0, (len(cipher_text))):
                cipher_text[z] = int(cipher_text[z])
            Decrypt()
            decrypted_to_bits = bin_to_dec(decrypted_to_bits)
            decrypt_simm_mess += chr(decrypted_to_bits // 4)

        print('Decrypt RC4 message ->', decrypt_simm_mess)
        client.send(b'process completed')
    cont = client.recv(1024).decode('utf-8')
    if cont == 'Y' or cont == 'y':
        print('establishing a new connection\n')
        continue
    else:
        break