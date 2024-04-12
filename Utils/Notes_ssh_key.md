# Set ssh key

### Step 1  Creating the Key Pair

```
$ ssh-keygen
```

```
Output
Generating public/private rsa key pair.
Enter file in which to save the key (/your_home/.ssh/id_rsa):
```

If you choose to overwrite the key on disk, you will not be able to authenticate using the previous key anymore. 
Be very careful when selecting yes, as this is a destructive process that cannot be reversed.

### Step 2  Copying the Public Key to Your Ubuntu Server

```
$ ssh-copy-id username@remote_host
```

```
Output
The authenticity of host '203.0.113.1 (203.0.113.1)' can't be established.
ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.
Are you sure you want to continue connecting (yes/no)? yes
```
This means that your local computer does not recognize the remote host.
This will happen the first time you connect to a new host. 
Type “yes” and press ENTER to continue.

Type in the password (your typing will not be displayed, for security purposes) and press ENTER. 
The utility will connect to the account on the remote host using the password you provided. 
It will then copy the contents of your ~/.ssh/id_rsa.pub key into a file 
in the remote account’s home ~/.ssh directory called authorized_keys.