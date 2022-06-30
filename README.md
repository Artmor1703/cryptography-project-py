#### РУС

Данный проект занимается  передачей сообщения в зашифрованном виде. Реализован в архитектуре клиент сервер на **Python**. <br>

После запуска клиента и сервера, на стороне клиента появится сообщение после чего у пользователя будет возможность подключиться к серверу. Если сервер будет неактивен, клиент предупредит об этом и предложит подключится еще раз. <br>

Далее сервер предлагает клиенту выбрать формат шифрования для передачи сообщения. В ассиметричном шифровании используется  метод RCA. В симметричном, передача закрытого ключа происходит с помощью метода Диффи Хелмана, а само шифрование через RC4. <br>

После выбора шифрования клиенту предлагается написать сообщение, которое, в дальнейшем, в зашифрованном виде будет передано серверу и расшифровано на стороне сервера. <br>

Затем клиент оповестит о корректной передаче зашифрованного сообщения, а сервер выведет само сообщение. <br>

В конце сервер спросит у клиента, желает ли он проделать операцию еще раз. Если ответ положительный, то клиент должен будет заново выбрать шифрование и сообщение. В случае отказа программа перестает работать.
___
#### ENG

This project transmits messages in encrypted form. It is implemented in client-server architecture on **Python**. <br>

After starting the client and the server, the client will display a message and the user will be able to connect to the server. If the server is inactive the client will warn the user and offer to connect again. <br>

Then the server offers the client to choose the encryption format to send the message. Asymmetric encryption uses the RCA method. In symmetric encryption, the transmission of the private key is using the Diffie-Helman method, and the encryption itself through RC4.  <br>

After selecting the encryption client is prompted to write a message that will be transmitted to the server in encrypted form and decrypted on the server side.  <br>

The client will then inform the user that the encrypted message has been correctly transmitted. The server will display the message itself.  <br>

At the end, the server will ask the client if it is willing to do the operation again. If the answer is affirmative, the client will have to reselect the encryption and the message. In case of refusal the program stops working.