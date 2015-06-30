from config import config
import numpy as np
import itertools
from algorithm import Algorithm
from copy import copy, deepcopy
import serverCommunication

def convert(context, num=True):
    print "CONVERTING: ", context
    context = copy(context)
    if type(context) is list or type(context) is tuple:
        context = context2dict(context)
    if num:
        if 'Language' in context and type(context['Language']) is str:
            context.update('Language',{'EN': 0, 'NL': 1, 'GE': 2}[context['Language']]) ## CONTINUE DIS
        if 'color' in context and type(context['color']) is str:
            context['color']    = {'red':0, 'green':1, 'blue':2, 'white':3, 'black':4}[context['color']]
        if 'Age' in context and type(context['Age']) is str:
            context['Age'] = int(context['Age'])
        if 'Agent' in context and type(context['Agent']) is str:
            context['Agent'] = {'OSX': 0, 'Linux': 1, 'Windows':2, 'mobile':3}[context['Agent']]
        if 'price' in context and type(context['price']) is str:
            context['price'] = float(context['price'])
        if 'header' in context and type(context['header']) is str:
            context['header'] = {'5':0, '15':1, '35':2}[context['header']]
        if 'Referer' in context and type(context['Referer']) is str:
            context['Referer'] = {'Bing':0, 'Google': 1, 'NA':2}[context['Referer']]
        if 'adtype' in context and type(context['adtype']) is str:
            context['adtype'] = {'square':0, 'banner':1, 'skyscraper':2}[context['adtype']]
        if 'ID' in context and type(context['ID']) is str:
            context['ID'] = int(context['ID'])
        if 'productid' in context and type(context['productid']) is str:
            context['productid'] = int(context['productid'])
        print "CONVERTED TO NUM: ", context
        return context
    else:
        if 'Language' in context and type(context['Language']) is not str:
            context['Language'] = ['EN', 'NL', 'GE'][int(context['Language'])]
        if 'color' in context and type(context['color']) is not str:
            context['color']    = ['red', 'green', 'blue', 'white', 'black'][int(context['color'])]
        if 'Age' in context and type(context['Age']) is not str:
            context['Age'] = str(context['Age'])
        if 'Agent' in context and type(context['Agent']) is not str:
            context['Agent'] = ['OSX', 'Linux', 'Windows', 'mobile'][int(context['Agent'])]
        if 'price' in context and type(context['price']) is not str:
            context['price'] = str(context['price'])
        if 'header' in context and type(context['header']) is not str:
            context['header'] = str(context['header'])
        if 'Referer' in context and type(context['Referer']) is not str:
            context['Referer'] = ['Bing', 'Google', 'NA'][int(context['Referer'])]
        if 'adtype' in context and type(context['adtype']) is not str:
            context['adtype'] = ['square', 'banner', 'skyscraper'][int(context['adtype'])]
        if 'ID' in context and type(context['ID']) is not str:
            context['ID'] = str(context['ID'])
        if 'productid' in context and type(context['productid']) is not str:
            context['productid'] = str(int(context['productid']))
        print "CONVERTED TO STR: ", context
        return context
    

def context2dict(context):
    return dict((k,v) for k,v in zip(['ID', 'Agent', 'Language', 'Age', 'Referer'], context))

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
            context = convert(serverCommunication.getContext(run_id, i))

            choices = [model.choose(context, 1) for model in self.models]
            for model, choice in zip(self.models, choices):
                result = serverCommunication.proposePage(run_id, i,
                    *[convert(choice, False)[k] for k in ['header', 'adtype', 'color', 'productid', 'price']]
                )
                model.learn(convert(context), choice, result)
    
    def evaluate(self):
        """ Evaluate the models by making them exploit and pick the best.
            @return {Model} The best model
                    {Boolean} Have we converged?
        """
        run_id = np.random.randint(self.opts['run_id_min'], self.opts['run_id_max'])
        results = [0]*len(self.models)
        for i in range(self.opts['testits']):
            context = convert(serverCommunication.getContext(run_id, i))
            
            choices = [model.choose(context, 0) for model in self.models]
            print choices
            for j, choice in enumerate(choices):
                results[j] += serverCommunication.proposePage(run_id, i,
                    *[convert(choice, False)[k] for k in ['header', 'adtype', 'color', 'productid', 'price']])
            print "Result: {}".format(np.max(results))
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
        selection = convert(self.randomChooser.make_selection(context))
        if np.random.uniform() > epsilon:
            # Replace the variables we model
            selection.update(self.maximumlikelihood(context))     
        print "CHOSE:", selection
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
        print context
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
        print "CONTEXT W", context, choices, result
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
        for v in self.variables:
            b = self.betas[v]
            self.variables.append(tuple(v + [var]))
            self.betas.update({tuple(v + [var]): 0})
        self.variables.append((var,))
        self.betas.update({(var,): 0})
        self.estimates.update({var: 0})
        return self
