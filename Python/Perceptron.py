#  Simple python perceptron
#  :#/ promezio.it

from random import choice
from numpy import array, dot, random

#  Training data for AND logic operator
training_data = [
    (array([0,0,1]), 0),
    (array([0,1,1]), 0),
    (array([1,0,1]), 0),
    (array([1,1,1]), 1),
]

#  Step function
def step_function(x):
    if x < 0 :
        return 0
    else :
        return 1

#  Random Weights
calculated_w= random.rand(3)

#  Learning Rate
ml_rate = 0.2

#  Learning iteration
n = 100

#  Learning cycle
for i in xrange(n):
    #  Choice a random training data
    x, expected = choice(training_data)
    #  Calculate the scalar product
    result = dot(calculated_w, x)
    #  Evaluate the error
    error = expected - step_function(result)
    #  Update wheights to fit training data value
    calculated_w += ml_rate * error * x

# Check if perceptron has learned
test_case = [1,0,1]
test_result = step_function(dot(test_case, calculated_w))
print("{} -> {}".format(test_case, test_result))
