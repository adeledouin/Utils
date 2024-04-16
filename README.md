# Utils : Good to Know

## Gestion des paths pour projets communs 

Chemin du projet : 

    path_root_to_project = '{}/Documents/GitHub/NomProjet'.format(os.path.expanduser('~/')))

Chemin des datas - dépend très souvent des ordi... - par exemple :
    
    dict_path_from_root = {'path_from_root_data': '/data1'}
    
    # dict_path_from_root = {'path_from_root_data': '/data12To'}
    
    # dict_path_from_root = {'path_from_root_data': '/media/sf_vm_share'}

## Gestion des environnements virtuels

1) Dans Settings => Project NomProjet => Python Interpreter
2) Add Interpreter => Add Local Interpreter
3) Choose Conda (if needed suivre les steps d'installation https://docs.anaconda.com/free/anaconda/install/linux/)

        name = NomProjet
        version python = 3.8

4) run commande suivante

```bash
cd Utils
pip install -r requirements.txt
```

et si jamais il manque quand meme un package ```(nom_env) adele@anima: pip install {nom du package}``` dans le terminal

ASTUCE : le nom de l'environnement virtuel devrait apparaitre ```(nom_env)```
dans le terminal - par exemple ```(LabQuakes_Localisation) adele@anima:```

si ce n'est pas le cas => environement root (celui de l'OS)

Pour activer un environnement virtuel :

```bash
conda activate nom_env
```

5) attention a la version opencv : si necessaire effectuer

```bash
pip uninstall opencv 
pip install scikit_image==0.19.3 ##ou 0.17.2
pip install opencv-contrib-python==4.6.0.66
pip install imutils==0.5.4
pip install imageio==2.32.0
conda install scipy==1.10.1
```

6) Save un environnement dans un .txt

```bash
pip freeze > requirements.txt
```

pour lister les package d'un env ```(nom_env) adele@anima: pip list``` dans le terminal.

7) Install de latex NECESSAIRE pour clean plot avec CMU font 
   - windows : install MikTex (https://miktex.org/download)
   - ubuntu : 
```bash
sudo apt install texlive texlive-latex-extra texlive-fonts-recommended dvipng
pip install latex
```

## Git Repo

Quand on veut update les changements effectués en local vers le serveur git :

1) Commit : (cerle sur ligne) comment les changements effectués
2) Push : (flèche pleine vers le haut) envoyer les changements en remote

Quand on veut update le repo local à partir de changements sur le serveur git:

1) synchroniser (flèche pointillée vers le bas)
2) Fetch : (flèche pleine vers le bas) importe les changements en local
3) Merge : choisir la methode Merge

## Astuces IDE (PycharmPro => licence gratuite pour étudiants/enseignants)

1) click droit on toolbar => "Customize toolbar"
2) Settings (engrenage)/Tool/plots => de cliquer plots
3) Edit configuration (toolbar) => Edit configuration template => python => modifi option => run in python consol
