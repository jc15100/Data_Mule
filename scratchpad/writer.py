import time
with open('tmp.txt', 'a') as fout:
	for i in range(10):
		fout.write(str(i)+' !\n')
		time.sleep(1)

