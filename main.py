import serverCommunication
#import algorithm.Algorithm
import genetic
import config
import time

stopped = False
#algorithm = algorithm.Algorithm()
algorithm = genetic.GeneticAlgorithm()

def main():
    run_id = 0
    while not stopped:
        run_id+=1
        run_id = run_id % 50000
        for i in range(50000):
            print '\rIteration',i,
            # to prevent ddos-attacks?
            time.sleep(0.1)            
            context = serverCommunication.getContext(run_id, i)            
            ad_data = algorithm.make_selection(context)            
            result  = serverCommunication.proposePage(run_id, i, *ad_data)
            algorithm.learn(context, ad_data, result)
            if i % config.config['saveinterval'] == 0:
                algorithm.save()
                print "Saved"

if __name__ == "__main__":
	main()
