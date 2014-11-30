Dynamic alias creator for system Windows.
====
##Features
- execute program in fork, or in current command line
- custom static invoke arguments

##Requirements:
- python
- folder with script in system PATH

##EXAMPLES:
####1) Register this script as new alias with name 'alias':
```
python C:\path\to\alias.py add alias python C:\path\to\alias.py
```

####2) Register notepad with alias 'n':
```
python C:\path\to\alias.py add n notepad --fork
```    
or if you already registered this script as an 'alias' 
```
alias add n notepad --fork
```
Now in any place you can just type:
```
n text.txt
```    
###And it will work!
Please note that **``--fork``** is important in this case.
It will allow to invoke notepad and do not block console.
In most cases this is useful for GUI applications.

