# RESTfulAPI

A RESTful API implementation with FastAPI.

### Usage

* Install dependencies:
  * Docker, [Docker Desktop](https://www.docker.com/products/docker-desktop/) is the easiest option
  * [Docker Compose](https://docs.docker.com/compose/install/)
* Development
  * Clone the repo: `git clone git@github.com:roryl23/RESTfulAPI.git`
  * Install [PyCharm](https://www.jetbrains.com/pycharm/)
  * Set up a virtualenv however you like and activate it in PyCharm or otherwise
    * [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation): 
      `pyenv install 3.11.9 && pyenv virtualenv 3.11.9 restfulapi && pyenv activate restfulapi && pip install -r requirements.txt`
  * Run the tests
    * In PyCharm, select the pytest run configuration:

      ![pytest](./docs/pytest.png)

    * From the shell, run `pytest`
  * Run the application
    * In PyCharm, select the restfulapi run configuration: 

      ![restfulapi](./docs/restfulapi.png)
    * Application is up:
      * [API Documentation](http://127.0.0.1:8080/docs#/)
      * [Performance metrics](http://127.0.0.1:8080/metrics/)
* Production
  * Install Kubernetes
    * In Docker Desktop, just go to settings and enable the Kubernetes cluster
  * Install [Tilt](https://docs.tilt.dev/)
  * From the shell, run `tilt up` 
  * Application is up:
    * [API Documentation](http://127.0.0.1:8010/docs#/)
    * [Performance metrics](http://127.0.0.1:8010/metrics/)

### Extras

* To make the performance metrics more interesting, run the stress test:
      
  ![stress](./docs/stress.png)
  * From the shell: `python scripts/stress.py`
  
