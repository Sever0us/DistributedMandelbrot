import tools
from worker import worker

if __name__ == '__main__':
    # Institute a max polling rate for all requests
    tools.GLOBAL_RATE_LIMIT = 0.1

    workerInstance = worker('http://ec2-54-149-191-82.us-west-2.compute.amazonaws.com:80')

    while True:
        break
        result = workerInstance.get_job()
        print(workerInstance.counter)
        if result is False:
            break

    print(workerInstance.get_image_resolution())