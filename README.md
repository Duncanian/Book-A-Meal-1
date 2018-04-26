[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Book-A-Meal

Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.

![Home Image](https://raw.github.com/lennykioko/Book-A-Meal/Feature-UI/UI/static/img/image.jpg)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
$ git clone https://github.com/lennykioko/Book-A-Meal.git
$ cd into the created folder
```
  
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Run the development server

```
$ python app.py
```

5. Navigate to [http://localhost:5000](http://localhost:5000)

At the / endpoint you should see Hello world displayed in your browser.

## Running the tests

To run the automated tests simply run

```
nosetests tests
```

### And coding style tests

Coding styles tests are tests that ensure conformity to coding style guides. In our case, they test conformity to
PEP 8 style guides

```
pylint app.py
```

## Deployment

Ensure you use Productionconfig settings which have DEBUG set to False

## Built With

* HTML5
* CSS3
* Python 3.6.4
* Flask - The web framework used

## Github pages link

https://lennykioko.github.io/

## Versioning

Most recent version is version 1

## Authors

Lenny Kioko.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration and encouragement
* etc
