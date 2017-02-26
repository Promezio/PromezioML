##########################
#                        #
# Simple neural network  #
#                        #
# :#/ promezio           #
# www.promezio.it        #
#                        #
##########################

# Import libraries
import numpy

# Activation function
def tanh(x):
    return numpy.tanh(x)

def tanh_prime(x):
    return 1.0 - x**2

# Normalization function 
def step_function(x):
    if x > 0.9 :
        return 1
    else :
        return 0



#################################
## SIMPLE NEURAL NETWORK MODEL ##
#################################
class SimpleNeuralNetwork:
    
    def __init__(self, layers):
        
        # Set activation functions
        self.activation = tanh
        self.activation_prime = tanh_prime
        
        # Set weights
        self.weights = []
        for i in range(1, len(layers) - 1):
            r = 2*numpy.random.random((layers[i-1] + 1, layers[i] + 1)) -1
            self.weights.append(r)

        # Set output layer
        r = 2*numpy.random.random( (layers[i] + 1, layers[i+1])) - 1
        self.weights.append(r)
    
    # LEARNING ROUTINE
    def learn(self, X, y, ml_rate=0.2, n=100000):
        
        # Start learning
        print("Start learning routine . . .")

        # Bias unit
        ones = numpy.atleast_2d(numpy.ones(X.shape[0]))
        X = numpy.concatenate((ones.T, X), axis=1)
        
        # Learning iteration
        for k in range(n):
            i = numpy.random.randint(X.shape[0])
            a = [X[i]]
            
            for l in range(len(self.weights)):
                dot_value = numpy.dot(a[l], self.weights[l])
                activation = self.activation(dot_value)
                a.append(activation)
           
            # Output layer
            error = y[i] - a[-1]
            deltas = [error * self.activation_prime(a[-1])]
            
            # Backpropagation
            for l in range(len(a) - 2, 0, -1):
                deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_prime(a[l]))   
                deltas.reverse()
  
                for i in range(len(self.weights)):
                    layer = numpy.atleast_2d(a[i])
                    delta = numpy.atleast_2d(deltas[i])
                    self.weights[i] += ml_rate * layer.T.dot(delta)
        
        # Finish learning
        print("Finish learning routine.")
                
    # Prediction
    def predict(self, x):
        a = numpy.concatenate((numpy.ones(1).T, numpy.array(x)), axis=1)
        for l in range(0, len(self.weights)):
            a = self.activation(numpy.dot(a, self.weights[l]))
        return float(a)

#################################
#################################
#################################


    


#############################
## TEST THE NEURAL NETWORK ##
#############################
if __name__ == '__main__':
    
    network = SimpleNeuralNetwork([2,2,1])

    ## TRAINING SET ##
    # Training array
    X = numpy.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # Training labels
    y = numpy.array([0, 1, 1, 0])

    # Start learning
    network.learn(X, y)

    # Test result
    test_case = [1,0]
    print("Test case: {} > {}".format(test_case, step_function(network.predict(test_case))))
    
    
