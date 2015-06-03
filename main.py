import serverCommunication
import algorithm.Algorithm
import config.config as config

stopped = False
algorithm = algorithm.Algorithm()

def main():
	run_id = 0
	while not stopped:
		run_id+=1
		run_id = run_id % 50000
		for i in range(50000):
			context = serverCommunication.getContext(run_id, i)
			ad_data = algorithm.make_selection(context)
			result  = serverCommunication.proposePage(run_id, i, *ad_data)
			algorithm.learn(context, ad_data, result)
			if i % config.saveinterval == 0:
				algorithm.save()
				print "Saved"

if __name__ == "__main__":
	main()
