import tools
from worker import worker
import scipy.misc
import os
import random

def write_file(image_array):
	if not os.path.isdir('renders'):
	    os.mkdir('renders') 

	uid = str(random.randint(0, 100000))

	scipy.misc.imsave(os.path.join('renders', 'render_{}.jpg'.format(uid)), image_array)

if __name__ == '__main__':
    # Institute a max polling rate for all requests
    tools.GLOBAL_RATE_LIMIT = 0.1

    workerInstance = worker('http://ec2-54-149-191-82.us-west-2.compute.amazonaws.com:80')

    while True:
        result = workerInstance.get_job()
        print(workerInstance.counter)
        if result is False:
            break

    image_array = workerInstance.get_image()
    write_file(image_array)