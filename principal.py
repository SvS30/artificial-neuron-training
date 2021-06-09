from tkinter import *
from tkinter import messagebox
import numpy as np
import random
import math

# globals 
root = Tk()
fields = (
    'Lambda',
    'Error permisible',
)

def FAEscalon(U):
    Yc = []
    for i in range(len(U)):
        if U[i] <= 0:
            Yc.append(0)
        else:
            Yc.append(1)
    return np.array(Yc)

def calculateError(E):
    result = 0
    for i in range(len(E)):
        result = result + math.pow(E[i], 2)
    return math.sqrt(result)

def ReadFile():
    f = open('data.txt', 'r')
    data = f.read()
    clean = data.rsplit("\n")
    X = np.matrix(clean[0]) # create matrix X
    y = clean[1].replace(";", ",")
    b = []
    for i in range(0, len(y), 2):
        b.append(y[i])
    Yaux = [int(e) for e in b]
    Y = np.array(Yaux) # create array Y
    f.close()
    return X, Y

def start(entries):
    X, Y = ReadFile()
    lamb = float(entries['Lambda'].get())
    eps = float(entries['Error permisible'].get())
    print('X:\n', X)
    print('Y: ', Y)
    print('Lambda: ', lamb)
    print('Error: ', eps)
    dimensionsX = X.shape
    print('dimensionsX: ', dimensionsX)
    m = dimensionsX[0]
    n = dimensionsX[1]
    W = np.random.rand(n,1)
    print('W:\n', W)
    U = X.dot(W)
    print('U:\n', U)
    Yc = FAEscalon(U)
    print('Yc:', Yc)
    E = Yc - Y
    print('E:', E)
    EtX = np.dot(E.transpose(), X)
    print('Et * X: ',EtX)
    Ne = lamb * EtX
    print('n * Et * X: ', Ne)
    W = W.transpose() - Ne
    print('W: ',W)
    enorm = calculateError(E)
    print('ENorm:', enorm)
    if enorm > eps:
        print('Try again!')

def makeform(root, fields):
    title = Label(root, text="Inicialización", width=20, font=("bold",20))
    title.pack()
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=30, text=field+": ", anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root.title("Entrenamiento Neurona - UPCH IA")
    root.geometry("300x250")
    root.resizable(0,0)
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents:fetch(e)))
    b1 = Button(root, text = 'Iniciar',
        command=(lambda e=ents: start(e)), bg="green",fg='white')
    b1.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    b2 = Button(root, text = 'Quit', command = root.quit, bg="red",fg='white')
    b2.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    root.mainloop()