# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 13:41:34 2015

@author: nitin
"""
from __future__ import division
import numpy as np
from scipy import optimize

class neuralnetwork():
    def __init__(self,reg_lamda=0,epsilon_init=0.12, hidden_layer_size=25,
          opti_method='TNC', maxiter=500):
        self.reg_lamda = reg_lamda
        self.epsilon_init = epsilon_init
        self.hidden_layer_size = hidden_layer_size
        self.activation_func = self.sigmoid
        self.activation_func_prime = self.sigmoid_prime
        self.method = opti_method
        self.maxiter = maxiter
        
    def sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def sigmoid_prime(self,z):
        sig = self.sigmoid(z)
        return sig * (1-sig)
    
    def sumsqr(self,a):
        return np.sum(a**2)

    def rand_init(self, l_in, l_out):
        return np.random.rand(l_in, l_in+1)*2*self.epsilon_init - self.epsilon_init
        
    def pack_thetas(self, t1,t2):
        return np.concatenate((t1.reshape(-1)), t2.reshape(-1))
    
    def unpack_thetas(self, thetas, input_layer_size, hidden_layer_size, num_labels):
        t1_start = 0
        t1_end = hidden_layer_size * (input_layer_size +1)
        t1 = thetas[t1_start:t1_end].reshape(hidden_layer_size, input_layer_size +1)
        t2 = thetas[t1_end:].reshape(num_labels, hidden_layer_size + 1)
        return t1, t2
    
    def _forward(self, X, t1, t2):
        m = X.shape[0]
        once = None
        if len(X.shape) ==1:
            once = np.array(1).reshape(1,)
        else:
            once = np.ones(m).reshape(m,1)
        #InputLayer
        a1 = np.hstack((ones,X))
        #hidden Layer
        z2 = np.dot(t1, a1.T)
        a2 = self.activation_func(z2)
        a3 = np.hstack((ones,a2.T))
        
        #output layer
        z3 = np.dot(t2, a2.T)
        a3 = self.activation_func(z3)
        return a1,z2,a2,z3,a3
    
    def function(self,thetas, input_layer_size, hidden_layer_size, num_labels, X,y,reg_lambda):
        t1,t2 = self.unpack_thetas( thetas, input_layer_size, hidden_layer_size, num_labels)
        m = X.shape[0]
        Y = np.eye(num_labels)[y]
        
        _, _, _, _,h = self._forward(x,t1,t2)
        costPositive = -Y* np.log(h).T
        costNegative = (1-Y)*np.log(1-h).T
        cost = costPositive -costNegative
        J = np.sum(cost)/m
        
        if reg_lambda !=0:
            t1f = t1[:,1:]
            t2f = t2[:,1:]
            reg = (self.reg_lamda/(2*m))*(self.sumsqr(t1f) + self.sumsqr(t2f))
            J = J + reg
        return J
    
    def function_prime(self, thetas, input_layer_size, hidden_layer_size, num_labels, X,y,reg_lambda):
        t1,t2 = self.unpack_thetas(thetas, input_layer_size, hidden_layer_size, num_labels)
        m = X.shape[0]
        t1f = t1[:, 1:]
        t2f = t2[:, 1:]
        Y = np.eye(num_labels)[y]
        
        Delta1, Delta2 = 0,0
        for i, row in enumerate(X):
            a1, z2, a2, z3, a3 = self._forward(row, t1,t2)
            
            d3 = a3 - Y[i,:].T
            d2 = np.dot(t2f.T, d3)* self.activation_func_prime(z2)
            Delta2 += np.dot(d3[np.newaxis].T, a2[np.newaxis])
            Delta1 += np.dot(d2[np.newaxis].T, a1[np.newaxis])
        Theta1_grad = (1/m) * Delta1
        Theta2_grad = (1/m) * Delta2
        
        if reg_lambda !=0:
            Theta1_grad[:,1:] = Theta_grad[:,1:] +(reg_lambda/m)* t1f
            Theta2_grad[:,1:] = Theta_grad[:,1:] +(reg_lambda/m)* t2f
        return self.pack_thetas(Theta1_grad, Thera2_grad)
        
    def fit(self, X,y):
        num_features = X.shape[0]
        input_layer_size = X.shape[1]
        num_labels = len(set(y))
        
        theta1_0 = self.rand_init(input_layer_size, self.hidden_layer_size)
        theta2_0 = self.rand_init(self.hidden_layer_size, num_labels)
        thetas0 = self.pack_thetas(theta1_0, theta2_0)
        options = {'maxiter': self.maxiter}
        _res = optimize.minimize(self.function, thetas0, jac = self.function_prime, method = self.method,
                                 args =(input_layer_size, self.hidden_layer_size, num_labels,X,y,0), options = options)
        self.t1, self.t2 = self.unpack_thetas(_res.x, input_layer_size, self.hidden_layer_size,num_labels)
        
        def predict(self, X):
            return self.predict_proba(X).argmax(0)
        
        def predict_proba(self,X):
            _,_,_,_,h = self._forward(X, self.t1, self.t2)
            return h
import sklearn.datasets as datasets
from sklearn import cross_validation
iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4)
nn = NN_1HL()
nn.fit(X_train, y_train)

        
        