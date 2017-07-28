# Django-RESTful-Backend[![Build Status](https://travis-ci.org/ESCAE/Django-RESTful-Backend.svg?branch=master)](https://travis-ci.org/ESCAE/Django-RESTful-Backend)[![Coverage Status](https://coveralls.io/repos/github/ESCAE/Django-RESTful-Backend/badge.svg?branch=master)](https://coveralls.io/github/ESCAE/Django-RESTful-Backend?branch=master)
This is the Django-Backend that holds the game-ai logic along with the neural net framework.
***
**Contributors-**
Eric Enderlein, Chris Hudson, Alex Short, W. Ely Paysinger, Sean Beseler
***
**About-**
Neural.py has holds the class framework necessary to make a neural network instance. This is a blank slate neural net that is in essence modular by design.
Genetic.py calls an inherited Neural class as Network, modifies the class to have tic-tac-toe specific methods. Along with Network, Genetic also has Game, Generation, and Individual as classes. Game translates board states from the front-end into data readable for Neural. Generation holds methods for exports and import, generating test boards, selecting a random individual neural network within a generation, and several run methods, which create different fitness programs for neural networks. Individual holds all of the mutation/reproduction code for neural networks. Individual also has evaluate and class attributes have unique neural network stats.
