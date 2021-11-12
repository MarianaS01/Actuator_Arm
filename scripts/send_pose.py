#! /usr/bin/env python3
# Sinusoidal function trajectory

import rospy
from rospy.timer import Rate
from std_msgs.msg import Float64
from dynamic_reconfigure.msg import Config
from control_msgs.msg import JointControllerState
import numpy as np
from random import choice, randint, random
from evolution.evolution import Evolution
import dynamic_reconfigure.client

error = Float64()
t = np.arange(0, 60, 0.6)

def sine(t):
    sine = np.sin(t/10)
    return sine

s = sine(t)

# Generate population [-3, 3)
# a = lower bound
# b = upper bound
a = -3
b = 3
N = 20
m = 3
X = (b-a)*np.random.random_sample((N, m)) - a 
FO = np.zeros((X.shape[0], 1)) # aquí X.shape[1]-1 es 2-1
X = np.concatenate((X, FO.reshape(-1,1)),axis=1)
X = X.astype("float64")
# Set:
# Gm = maximum number of generations
# F = mutation factor (bipartition of genes) [0,1]
# C = crossing factor [0,1]
Gm = 1000 #TODO: Change Gm
F = 0.65
C = 0.8
g = 0


def error_callback(data):
    #rospy.loginfo("Error: {}".format(data.error))
    global error 
    error += data.error
    return error

def talker():
    global error, client, pub1, rate
    rospy.init_node("sine_pose")
    
    client = dynamic_reconfigure.client.Client("/arm/motor_end_effector_position_controller/pid")
    command_path = "/arm/motor_end_effector_position_controller/command"
    state_path = "/arm/motor_end_effector_position_controller/state"

    # pub1: publishes end_effector's position
    # pub2: publishes pid gains to pid_parameter_updates to update pid
    # sub = subscribes to state_path to get error
    pub1 = rospy.Publisher(command_path, Float64, queue_size=10)
    sub = rospy.Subscriber(state_path, JointControllerState, error_callback)
    rate = rospy.Rate(1.66)

    
    while not rospy.is_shutdown():
        for w,x in zip(range(N), X):
            rospy.loginfo("\nIndividuo: {}".format(w))
            params = {'p' : x[0], 'i' : x[1], 'd' : x[2]}
            rospy.loginfo(params)
            config = client.update_configuration(params)
            error = Float64(0.0)
            for i in s:
                pub1.publish(i)
                rate.sleep()
            
            # add error to individual (m = 3 (pos3 0,1,2,3))
            X[w][m] = error
        
        # evolution 
        g = 0  
        while(g <= Gm):
            # Crear matriz de hijos
            U = np.zeros((N,m))
            FO_h = np.zeros((N, 1)) # no m porque ahora m incluye la columna de la FO 
            U = np.concatenate((U, FO_h.reshape(-1,1)),axis=1)
            U = U.astype("float64")

            for i in range(N):
                # generate 3 random integers for selecting the 3 individuals for 1st gen
                r1 = choice([n for n in range(N) if n != i])
                r2 = choice([n for n in range(N) if n not in [i, r1]])
                r3 = choice([n for n in range(N) if n not in [i, r1, r2]])
                
                # vector mutante
                Vi = np.zeros(m)
                Vi = X[r1][0:m] + F*(X[r2][0:m] - X[r3][0:m])
                
                # verificar cotas:
                # algunas veces los valores se salen del rango 
                # (ej.[-3,3]), esto debido al producto con el 
                # factor F, para ello hay que ajustar los resultados
                for w in range(m):
                    if (Vi[w] > b):
                        Vi[w] = 2*b - Vi[w]
                    if (Vi[w] < a):
                        Vi[w] = 2*a - Vi[w]
                # factor binomial
                Fr = randint(0, m-1) # randint(0,m) llega hasta 2, j no llegará hasta 2 porque range(m) da 0 y 1

                for j in range(m):
                    # rcj decide si se mutará o no el gen
                    rcj = random()
                    
                    # Cruce
                    if (rcj < C) or (j == Fr): 
                        # Copiar gen de Vi al hijo
                        U[i][j] = Vi[j]
                    else:
                        U[i][j] = X[i][j]

            # evaluar a los hijos en la FO
            for w,u in zip(range(N), U):
                rospy.loginfo("\Hijo: {}".format(w))
                params = {'p' : u[0], 'i' : u[1], 'd' : u[2]}
                rospy.loginfo(params)
                config = client.update_configuration(params)
                error = 0
                for i in s:
                    pub1.publish(i)
                    rate.sleep()

                # add error to son (m = 3 (pos3 0,1,2,3))
                U[w][m] = error

            # Padres vs hijos
            for i in range(N):
                if U[i][3] < X[i][3]:
                    X[i][:] = U[i][:]
                    
            g += 1
            print("Fin {} generación".format(g))

        print(X)
            

       
def eval_FO(X):
    global pub1, rate

    for w,x in zip(range(N), X):
        rospy.loginfo("\nIndividuo: {}".format(w))
        params = {'p' : x[0], 'i' : x[1], 'd' : x[2]}
        rospy.loginfo(params)
        config = client.update_configuration(params)
        error = 0
        for i in s:
            pub1.publish(i)
            rate.sleep()
        
        # add error to individual (m = 3 (pos3 0,1,2,3))
        X[w][m] = error

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass