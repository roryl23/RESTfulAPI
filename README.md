# RESTfulAPI

An API implementation with FastAPI.

### Notes

I ran into a couple challenges while creating this application,
mostly centered around the usage of MongoDB as the database backend.

First of all, I needed to mock a testing harness to allow unit
tests of the MongoDB functions, which turned out to be a bit more work than anticipated.

Second, if the application has multiple instances such as the
Kubernetes DaemonSet you can see in `deployment/kubernetes.yaml`,
along with round-robin load balancing with HAProxy, then
atomic updates are no longer guaranteed in MongoDB.
I fixed this by adding a retry loop with stochastic delays for
`update_record()` in `app/mongo.py`. You can test this for yourself
by running the stress test against my running instance, instructions
below.

### Usage

* Install dependencies:
  * [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  * [PyCharm](https://www.jetbrains.com/pycharm/)
  * [Docker Compose](https://docs.docker.com/compose/install/)
  * Instead of PyCharm, this will also work with Docker Engine on Linux
    and running shell commands/scripts
* Development
  * Clone the repo: `git clone git@github.com:roryl23/RESTfulAPI.git`
  * Set up a virtualenv however you like
    * [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation): 
      `pyenv install 3.11.9 && pyenv virtualenv 3.11.9 restfulapi && pyenv activate restfulapi && pip install -r requirements.txt`
  * Open PyCharm to the repo directory, or change directory in the shell
  * Activate your virtualenv
  * Run the tests
    * In PyCharm, select the pytest run configuration:

      ![PyCharm](./docs/pytest.png)

    * From the shell, run `pytest`
  * Run the application
    * In PyCharm, select the restfulapi run configuration: 

      ![PyCharm](./docs/restfulapi.png)
    * From the shell, run `docker compose --file deployment/docker-compose.yaml up`
    * Application is up:
      * [API Documentation](http://localhost:8080/docs#/)
      * [Prometheus](http://localhost:9090/)
* Production
  * Install Kubernetes
    * In Docker Desktop, just go to settings and enable the Kubernetes cluster
  * Install [Tilt](https://docs.tilt.dev/)
  * From the shell, run `tilt up`
  * Application is up:
    * [API Documentation](http://localhost:8010/docs#/)
    * [Prometheus](http://localhost:9090/)

### Extras

* Publicly available at:
  * [API Documentation](http://roryl23.ddns.net/docs)
  * [Prometheus](http://roryl23.ddns.net:9090/graph?g0.expr=http_request_duration_milliseconds_bucket&g0.tab=0&g0.display_mode=lines&g0.show_exemplars=0&g0.range_input=5m)
* To make the Prometheus metrics more interesting, run the stress test:
      
  ![PyCharm](./docs/stress.png)
  * From the shell, run `python scripts/stress.py --host roryl23.ddns.net --port 80`
  * Note that the stress test is really only meaningful when run against
    a deployment with multiple instances, with load balancing.
