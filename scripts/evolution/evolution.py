# Evolución Diferencial aleatoria de una resta binaria
# ED/rand/1/bin
import numpy as np
from random import choice, randint, random
from numpy.core.fromnumeric import reshape

def gen_population(a, b, N, m):
    X = (b-a)*np.random.random_sample((N, m)) - a
    return X


# Class in construction
class Evolution(): 
    def __init__(self, Gm, C, F):
        self.Gm = Gm
        self.C = C
        self.Fr = F
    
    def set_population(self, a, b, N, m):
        """
        a = lower bound 
        b = upper bound
        N = number of individuals
        m = number of gens per individuals
        """
        self.a = a
        self.b = b
        self.N = N
        self.m = m
        self.X = np.zeros((N, m+1))

        for i in range(self.N):
            for j in range(self.m):
                self.X[i][j] = (self.b-self.a)*np.random.random_sample() - self.a
    
    def get_population(self):
        return self.X

    #def get_FO(self):
    #    return self.FO

    # TODO: update FO (num_individuo, error)
    def update_FO(self, pos, value):
        self.X[pos][self.m] = value

    #def X_concat_FO(self):
    #    self.FO = self.FO.reshape(-1,1)
        # Add FO results to X matrix
    #    self.X = np.concatenate((self.X, self.FO),axis=1)

    def set_sons(self):
        self.U = np.zeros((self.N, self.m+1))
        #self.FO_h = np.zeros((self.N, self.m-2)) # no m porque ahora m incluye la columna de la FO 

    def get_sons(self):
        return self.U

    def evolute(self, function):
        g = 0
        while(g <= self.Gm):
            # Crear matriz de hijos
            self.set_sons()

            for i in range(self.N):
                # generate 3 random integers for selecting the 3 individuals for 1st gen
                r1 = choice([n for n in range(self.N) if n != i])
                r2 = choice([n for n in range(self.N) if n not in [i, r1]])
                r3 = choice([n for n in range(self.N) if n not in [i, r1, r2]])
                
                # vector mutante
                Vi = np.zeros(self.m)
                Vi = self.X[r1][0:self.m] + self.F*(self.X[r2][0:self.m] - self.X[r3][0:self.m])
                
                # verificar cotas:
                # algunas veces los valores se salen del rango 
                # (ej.[-3,3]), esto debido al producto con el 
                # factor F, para ello hay que ajustar los resultados
                for w in range(self.m):
                    if (Vi[w] > self.b):
                        Vi[w] = 2*self.b - Vi[w]
                    if (Vi[w] < self.a):
                        Vi[w] = 2*self.a - Vi[w]
                # factor binomial
                Fr = randint(0, self.m-1) # randint(0,m) llega hasta 2, j no llegará hasta 2 porque range(m) da 0 y 1

                for j in range(self.m):
                    # rcj decide si se mutará o no el gen
                    rcj = random()
                    
                    # Cruce
                    if (rcj < self.C) or (j == Fr): 
                        # Copiar gen de Vi al hijo
                        self.U[i][j] = Vi[j]
                    else:
                        self.U[i][j] = self.X[i][j]

            # TODO: evaluar hijos
            function(self.U)

            for i in range(self.N):
                if self.U[i][3] < self.X[i][3]:
                    self.X[i][:] = self.U[i][:]

            g += 1
            print("Fin {} generación".format(g))

        print(self.X) 

    def update_FO_h(self, pos, value):
        self.FO_h[pos] = value
    
    def U_concat_FO_h(self):
        self.FO_h = self.FO_h.reshape(-1,1)
        # Add FO results to X matrix
        self.U = np.concatenate((self.U, self.FO_h),axis=1)
