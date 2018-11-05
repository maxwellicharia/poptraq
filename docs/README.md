# Population Analyser
## Poptraq - Population Analyser

Potraq is a population analyser aimed to aid the National Government ease
getting population information at the same time ensuring efficient distribution of funds to 
the various county governments


#### Interface


- Python: Framework - Flask
- Bootstrap
- Javascript
- HTML and CSS


#### Database


- Postgresql database
- SQLAlchemy database language


#### System


- Python

## Getting Started


These instructions will get you a copy of the project up and running on 
your local machine for development and testing purposes.


The application has been commented for easy follow through and 
understanding.


### Prerequisites


- Prior knowledge of Git
- Prior knowledge of python programming concepts


The following are tools/libraries needed:


1. Git - To download a copy of the project


- Follow this [git installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to 
successfully install git on your machine


2. PGAdmin III - TO manage migrations and the database.

- Follow this [tutorial](https://www.pgadmin.org/download/) that will aid in installing PGAdmin III


Various database variables will need to be changed in order to suit your 
Development Environment.

### Installing


A step by step series of examples that tell you have to setup and get a 
development environment running.


Prior knowledge of git, installation and setup is assumed.


1. Clone the application and copy the link. Open the terminal and input: 


```
git clone https://github.com/Maxwell-Icharia/poptraq
```

2. Install pip in order to install various requirements needed by the application.


```sudo apt-get install virtualenv```

3. Use pip to install a virtual environment for running the application.

```sudo apt-get install python3-pip```

4. Create a new virtual environment that will be used to run the application without tampering with your system's various installed modules.

``` virtualenv venv```

5. Activate your virtual environment.

```. venv/bin/activate```

6 Install all the requirements needed to run the application found in the requirements.txt file.

```pip install -r requirements.txt```

7. Run the application.

```python run.py```

## Built With

* Python Flask


## Authors

- Maxwell Icharia - [Github](https://github.com/Maxwell-Icharia)

