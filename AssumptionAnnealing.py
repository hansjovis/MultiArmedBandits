from config import config
import numpy as np
import itertools
from algorithm import Algorithm
from copy import copy, deepcopy
import serverCommunication

def convert(context):
    if 'Language' in context:
        context['Language'] = {'EN': 0, 'NL': 1, 'GE': 2}[context['Language']]
    if 'color' in context:
        context['color']    = {'red':0, 'green':1, 'blue':2, 'white':3, 'black':4}[context['color']]
    if 'Age' in context:
        context['Age'] = int(context['Age'])
    if 'Agent' in context:
        context['Agent'] = {'OSX': 0, 'Linux': 1, 'Windows':2, 'mobile':3}[context['Agent']]
    if 'price' in context:
        context['price'] = float(context['price'])
    if 'header' in context:
        context['header'] = int(context['header'])
    if 'Referer' in context:
        context['Referer'] = {'Bing':0, 'Google': 1, 'NA':2}[context['Referer']]
    if 'adtype' in context:
        context['adtype'] = {'square':0, 'banner':1, 'skyscraper':2}[context['adtype']]
    if 'ID' in context:
        context['ID'] = int(context['ID'])
    if 'productid' in context:
        context['productid'] = int(context['productid'])
    return context



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
            print "Train iteration {}".format(i)
            context = serverCommunication.getContext(run_id, i)
            if type(context) is tuple:
                context = dict((k,v) for k,v in zip(['ID', 'Agent', 'Language', 'Age', 'Referer'], context))
                context = convert(context)
            choices = [convert(model.choose(context, 1)) for model in self.models]
            for model, choice in zip(self.models, choices):
                result = serverCommunication.proposePage(
                                                run_id, i, choice['header'],
                                         choice['adtype'], choice['color'], 
                                      choice['productid'], choice['price'])
                model.learn(context, choice, result)
    
    def evaluate(self):
        """ Evaluate the models by making them exploit and pick the best.
            @return {Model} The best model
                    {Boolean} Have we converged?
        """
        run_id = np.random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
        results = [0]*len(self.models)
        for i in range(self.opts['testits']):
            context = serverCommunication.getContext(run_id, i)
            choices = [model.choose(context, 0) for model in self.models]
            for j, choice in enumerate(choices):
                results[j] += serverCommunication.proposePage(
                                run_id, i, choice['header'],
                         choice['adtype'], choice['color'], 
                      choice['productid'], choice['price'])
        return self.models[np.argmax(results)], self.hasconverged(results)
    
    def extend(self, model):
        """ Generate new models by extending model with random variables.
            @param model {Model} The model to extend.
            @return {iterable Model} The extended models.
        """
        # Grab all variables not in model
        variables = list(set(config['variables']).difference(set(model.variables)))
        models = [deepcopy(model) for i in range(len(variables))]
        for v, m in zip(variables, models):
            m.extend(v)
        return models

    def hasconverged(self, results):
        """ Check if the results have improved.
            TODO: This can be a lot better.
        """
        return max(results) < self.opts['conv_threshold'] * mean(results)

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
        if np.random.uniform() < epsilon:
            return self.randomChooser.make_selection(context)
        else:
            return self.maximumlikelihood(context)
    
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
                self.estimates[tuple(var)] = prev # Update estimate
        
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
            cur_estimates.update({(variable,): estimate})
            context.update(cur_estimates)
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
            @return {void} this function changes the object
        """
        for v in self.variables:
            b = self.betas[v]
            self.variables.append(tuple(v + [var]))
            self.betas.update({tuple(v + [var]): 0})
        self.variables.append((var,))
        self.betas.update({(var,): 0})
        self.estimates.update({var: 0})
