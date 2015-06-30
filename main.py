import serverCommunication
from algorithm import Algorithm
from config import config
from AssumptionAnnealing import MetaModel, Model
import sys

stopped = False
algorithm = Algorithm()

def meta_model_main(max_its=config['max_its'], verbose=True):
    run_id = 0
    if verbose: print "-- Starting --"
    MM = MetaModel()
    MM.run()

def main(max_its=config['max_its'], verbose=True):
    run_id = 0
    if verbose: print "-- Starting --"
    while not stopped:
        for i in range(50000):
            context = serverCommunication.getContext(run_id, i)
            ad_data = algorithm.make_selection(context)
            datalist = (ad_data['header'], ad_data['adtype'], ad_data['color'],
                        ad_data['productid'], ad_data['price'])
            result = serverCommunication.proposePage(run_id, i, *datalist)
            algorithm.learn(context, ad_data, result)
            if verbose and i % config['updateinterval'] == 0:
                print "Iteration #{}".format(i)
                print "Result: {}".format(result)
            if i % config['saveinterval'] == 0:
                algorithm.save()
                if verbose: print "Saved"
            if max_its is not None and run_id * 50000 + i >= max_its:
                if verbose: print "-- Stopping --"
                algorithm.save()
                if verbose: print "Saved"
                return
        run_id += 1
        run_id = run_id % 50000

if __name__ == "__main__":
    if len(sys.argv) > 0 and sys.argv[1] == 'meta':
        meta_model_main()
    else:
        main()
