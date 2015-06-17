import serverCommunication
from algorithm import Algorithm
from config import config

stopped = False
algorithm = Algorithm()

def main(max_its=None, verbose=True):
	run_id = 0
	if verbose: print "-- Starting --"
	while not stopped:
		run_id+=1
		run_id = run_id % 50000
		for i in range(50000):
			context = serverCommunication.getContext(run_id, i)
			ad_data = algorithm.make_selection(context)
			datalist = (ad_data['header'], ad_data['adtype'], ad_data['color'],
						ad_data['productid'], ad_data['price'])
			result  = serverCommunication.proposePage(run_id, i, *datalist)
			algorithm.learn(context, ad_data, result)
			if i % config['saveinterval'] == 0:
				algorithm.save()
				if verbose: print "Saved"
				if max_its is not None and run_id * 50000 + i > max_its:
					if verbose: print "-- Stopping --"
					return

if __name__ == "__main__":
	main()
