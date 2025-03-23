# RESTfulAPI

An API implementation with FastAPI.

### Usage

* Install dependencies:
  * Everything is smoothest with:
    * [Docker Desktop](https://www.docker.com/products/docker-desktop/)
    * [PyCharm](https://www.jetbrains.com/pycharm/)
  * However, this will also work with Docker Engine on Linux
    and running shell commands/scripts
  * [Docker Compose](https://docs.docker.com/compose/install/)
* Development
  * Clone the repo: `git clone git@github.com:roryl23/RESTfulAPI.git`
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
  * [Prometheus](http://roryl23.ddns.net:9090)
* To make the Prometheus metrics more interesting, run the stress test:
      
  ![stress](./docs/stress.png)
  * From the shell: `python scripts/stress.py`
  
