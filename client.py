import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

input('To connect to server press any key\n')

try:
    sock.connect(('127.0.0.1', 1234))
except OSError:
    print('No connection to server')

while sock.getsockname()[0] == '0.0.0.0':
    input('To connect to server press any key\n')
    try:
        sock.connect(('127.0.0.1', 1234))
    except OSError:
         print('No connection to server')

#Symmetric encryption (Diffie hellman)
a_diffi = 101

def Encrypt():
    global key, plain_text, encrypted_to_bits
    n = 3
    S = [i for i in range(0, 2 ** n)]
    key_list = [key[i:i + n] for i in range(0, len(key), n)]
    for i in range(len(key_list)):
        key_list[i] = int(key_list[i], 2)

    global pt

    pt = [plain_text[i:i + n] for i in range(0, len(plain_text), n)]

    for i in range(len(pt)):
        pt[i] = int(pt[i], 2)

    diff = int(len(S) - len(key_list))

    if diff != 0:
        for i in range(0, diff):
            key_list.append(key_list[i])

    def KSA():
        j = 0
        N = len(S)

        for i in range(0, N):
            j = (j + S[i] + key_list[i]) % N

            S[i], S[j] = S[j], S[i]

        initial_permutation_array = S

    KSA()

    def PGRA():

        N = len(S)
        i = j = 0
        global key_stream
        key_stream = []

        for k in range(0, len(pt)):
            i = (i + 1) % N
            j = (j + S[i]) % N

            S[i], S[j] = S[j], S[i]
            t = (S[i] + S[j]) % N
            key_stream.append(S[t])

    PGRA()

    def that_XOR():
        global cipher_text
        cipher_text = []
        for i in range(len(pt)):
            c = key_stream[i] ^ pt[i]
            cipher_text.append(c)

    that_XOR()

    encrypted_to_bits = ""
    for i in cipher_text:
        encrypted_to_bits += '0' * (n - len(bin(i)[2:])) + bin(i)[2:]
while True:
    print(sock.recv(1024).decode('utf-8'))
    ans = input()
    sock.send(str(ans).encode());


    if ans == 'a' or ans == 'A':
        print(sock.recv(1024).decode('utf-8'))
        m_asimm = input()
        sock.send(str(m_asimm).encode())

        e_assim = int(sock.recv(1024).decode('utf-8'))
        n = int(sock.recv(1024).decode('utf-8'))
        #print('From server -> receive e, n')

        c = []
        for z in range(len(m_asimm)):
            c.append(str((ord(m_asimm[z]) ** e_assim) % n))
        c = ','.join([str(z) for z in c])
        sock.send(str(c).encode())
        print(sock.recv(1024).decode('utf-8'))
        #print('Encrypt message -> to server')

    if ans == 's' or ans == 'S':
        P = int(sock.recv(1024).decode('utf-8'))
        G = int(sock.recv(1024).decode('utf-8'))
        # print('From server -> receive p, g')
        A = G ** a_diffi % P

        sock.send(str(A).encode())
        #print('Send client open key')
        B = int(sock.recv(1024).decode('utf-8'))

        key = bin(B ** a_diffi % P)[2::] #Private key
        # print('DH key in binary: ' + str(key))

        print(sock.recv(1024).decode('utf-8'))
        mes = input()
        sock.send(str(mes).encode())

        sym_cipher = list()
        for i in mes:
            plain_text = bin(ord(i))[2::]+'00'
            while len(plain_text) < 9:
                plain_text = '0' + plain_text
            Encrypt()
            cipher_text = ''.join([str(i) for i in cipher_text])
            sym_cipher.append(cipher_text)

        sym_cipher = ','.join([str(i) for i in sym_cipher])
        sock.send(str(sym_cipher).encode())

        print(sock.recv(1024).decode('utf-8'))
    cont = input("Want to continue? Y/N \n")
    sock.send(str(cont).encode());
    if cont == 'Y' or cont == 'y':
        print('establishing a new connection\n')
        continue
    else:
        break