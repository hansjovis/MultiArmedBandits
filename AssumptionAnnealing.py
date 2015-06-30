from config import config
import numpy as np
import itertools
from algorithm import Algorithm
from copy import copy, deepcopy
import serverCommunication
import Converter

class MetaModel:
    """ Metamodels are a kind of ensemble,
        They train models, evaluate which works best,
        And then extend the best one,
        Repeat.
    """
    def __init__(self, opts=None, models=None):
        """ Constructor which prepares for the run
            @param opts {dict} with options.
                    If None or missing values, defaults are used.
            @param models {Model or iterable} models to initialize run.
                    If None, will start with an empty model.
            @return {MetaModel} self
        """
        # Set opts
        metaconf = config['metamodel']
        self.opts = opts if opts is not None else {}
        for key in metaconf:
            if key not in self.opts:
                self.opts.update({key: metaconf[key]})
        # Set models
        self.models = models if models is not None else self.extend(Model())
    
    def run(self):
        """ Starts training until stopping criteria are met.
            The main loop works as follows:
            @return {Model} The winner model
        """
        i = 0
        while True:
            print "Iteration {}".format(i)
            self.train()
            model, stop = self.evaluate()
            if stop:
                return model
            self.models = self.extend(model)
    
    def train(self):
        """ Make the models explore.
            @return {void} This function changes self.models
        """
        run_id = np.random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
        for i in range(self.opts['trainits']):
            context = serverCommunication.getContext(run_id, i, dict)
            context = Converter.context_intify(context)

            choices = [model.choose(context, 1) for model in self.models]
            for model, choice in zip(self.models, choices):
                choice_str = Converter.choice_stringify(choice)
                result = serverCommunication.proposePage(run_id, i,
                    choice_str['header'], choice_str['adtype'], choice_str['color'],
                    choice_str['productid'], choice_str['price'])
                model.learn(context, choice, result)
            if config['verbose'] and i%100 == 0:
                print "Train it {}".format(i)
    
    def evaluate(self):
        """ Evaluate the models by making them exploit and pick the best.
            @return {Model} The best model
                    {Boolean} Have we converged?
        """
        run_id = np.random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
        results = [0]*len(self.models)
        for i in range(self.opts['testits']):
            context = serverCommunication.getContext(run_id, i, dict)
            context = Converter.context_intify(context)
            
            choices = [model.choose(context, 0) for model in self.models]
            for j, choice in enumerate(choices):
                choice_str = Converter.choice_stringify(choice)
                results[j] += serverCommunication.proposePage(run_id, i,
                    choice_str['header'], choice_str['adtype'], choice_str['color'],
                    choice_str['productid'], choice_str['price'])
            if config['verbose'] and i%100 == 0:
                print "Test it {}".format(i)
        return self.models[np.argmax(results)], self.hasconverged(results)
    
    def extend(self, model):
        """ Generate new models by extending model with random variables.
            @param model {Model} The model to extend.
            @return {iterable Model} The extended models.
        """
        if config['verbose']:
            print "-- Extending --"
        # Grab all variables not in model
        variables = list(set(config['variables']).difference(set(model.variables)))
        models = [deepcopy(model) for i in range(len(variables))]
        for v, m in zip(variables, models):
            m.extend(v)
        if config['verbose']:
            print "Finished extending"
        return models

    def hasconverged(self, results):
        """ Check if the results have improved.
            TODO: This can be a lot better.
        """
        mx = np.max(results)
        mn = np.mean(results)
        t = self.opts['conv_threshold']
        if config['verbose']:
            print "Comparing {} to {} with threshold {}".format(mx, mn, t)
        return mx < t * mn

class Model:
    """ Abstract model class
    """

    def __init__(self, lr=0.001):
        """ Generic constructor """
        self.variables = []
        self.estimates = {}
        self.betas = {}
        self.lr = lr
        self.randomChooser = Algorithm()
    
    def choose(self, context, epsilon):
        """ Makes a choice of the five ad variables given context
            With probability epsilon:
                to minimize entropy in the data
            Else:
                to maximize expected gain
            @param context {dict} containing context variables
            @param epsilon {float} exploration probability
            @return {dict} containing choice values
        """
        selection = self.randomChooser.make_selection(context)
        selection = Converter.choice_intify(selection)
        
        if np.random.uniform() > epsilon:
            # Replace the variables we model
            selection.update(self.maximumlikelihood(context))     
        return selection

    def maximumlikelihood(self, context):
        """ Uses expectation maximization to get an estimate of the best variables:
            - Freeze all but one variable
            - Argmax prediction with arg = that one variable
            - Repeat all variables
            - Repeat 'until convergence'
        """
        for i in range(5): # Repeat to improve results
            for var in self.estimates: # Grab previous estimate
                prev = self.predict(context, var, self.estimates[var] + 1)
                curr = self.predict(context, var, self.estimates[var] - 1)
                direction = prev < curr # Go toward the higher value
                if not direction:
                    prev, curr = curr, prev
                while prev < curr: # Until you reached max
                    prev = curr
                    curr = self.predict(context, var, prev + 2*direction - 1)
                self.estimates[var] = prev # Update estimate
        return self.estimates
        
    def predict(self, context, variable=None, estimate=None):
        """ Predicts the value given context variables.
            The method handles two cases:
                variable is provided: then
                    context only contains user context
                    ad context will be grabbed from self.estimates
                    self.estimates[variable] will be estimate
                else
                    context contains all context
        """
        if variable is not None:
            context = copy(context)
            context.update(self.estimates)
            context.update({(variable,): estimate})
        prediction = 0
        for vlist in self.variables:
            prediction += self.betas[tuple(vlist)] * np.prod([context[v] for v in vlist])
        return prediction

    def learn(self, context, choices, result):
        """ Updates the model given the context, choices and result
            @param context {dict} containing context variables
            @param choices {dict} containing variables from last choose
            @param result {float} gain (succes * reward)
            @return {void} this function changes the object
        """
        context.update(choices)
        prediction = self.predict(context)
        update = -self.lr * (prediction - result)
        for vlist in self.variables:
            self.betas[vlist] = self.betas[vlist] + update
        self.randomChooser.learn(result)
    
    def extend(self, var):
        """ Extend the model with variable var
            @param var {string} variable from context or choices
            @return {Model} this method returns self
        """
        variables = copy(self.variables) # Pre-save to prevent infinite loop
        for v in variables:
            b = self.betas[v]
            self.variables.append(v + (var,))
            self.betas.update({v + (var,): 0})
        self.variables.append((var,))
        self.betas.update({(var,): 0})
        self.estimates.update({var: 0})
        return self
