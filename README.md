# Spec

Create a tombola web application, which enables the following
1. A web front end
2. A API
3. A database

As a user, I want to be able to enter a tombola, the value of my bet where each ticket costs £1, but the price of the bet increase with every 100 bets paced in the game by 1%.

When I place my bet, the response tells me what the odds are of me winning, and the ticket IDS I have purchased.

I can either enter the value in the front end or Via and API.

The event lasts 5 mins (configurable) and at the end of the timer a random ticket is drawn and displayed this is the winner and I should be notified of my prise draw.

# Decisions
- I built the app trying where possible to adhere to TDD methodology. The app has very good test coverage

- I have enabled the creation of multiple and concurrent tombolas. Tombolas can be run in seconds. (5 minutes=300 seconds) All tombolas and their statuses can be found on the home page.

- Every ticket has a completely unique id derived from its primary key. This means that a given tombola may not have consecutive id numbers if there are multiple tombolas running simultaneously.

- The web app has more functionality than the api. I have just kept to the specification for api functionality. It can just buy tickets for a given tombola id.

- web app can
  - Create new tombola
  - See winners of all tombolas
  - see time remaining of all tombolas
  - buy tickets
  - see price off tickets once bought

# Web front end (web app) & database

Web front end is located at http://tombola.diveondown.com
There is also a staging server at http://tombola.staging.diveondown.com

The app is built using django, which uses templates to serve the web front end. I've used no javascript, templates are all generated server side.

I have used django's built in ORM to write out models for database. This is compatible with most SQL db, I have tested on postgres and sqlite

# Testing

The app contains functional tests running selenium testing the web front end using geckdriver and firefox. These are located in the folder functional_tests

The app contains unit tests running using django's built in test client. All unit tests for models and views are located at tombola/tests

To run all tests, clone the repo and then inside python virtualenv or venv:
```
pip install -r requirements.txt
python manage.py test
```
You can run the tests on the staging sever as follows:
```
STAGING_SERVER=tombola.diveondown.com python manage.py test.functional_tests
```

# API
As per spec, API works for buy view.

It is a POST request which accepts "ticket_quantity" as an integer and a TOMBOLA_ID as follows:
http://tombola-staging.diveondown.com/api/tombolas/TOMBOLA_ID/buy/

It will return the following data
```
{
  "total_cost": INT (DENOTING PRICE IN £),
  "ticket_ids": lIST OF INT (DENOTING ALL TICKET IDS BOUGHT),
  "ticket_odds": FLOAT (% CHANCE OUT OF 100)}
```
for example:
##### input:
```
curl -d '{"ticket_quantity": 5} ' -H "Content-Type: application/json" -X POST http://tombola-staging.diveondown.com/api/tombolas/49/buy/
```
##### output:
```
{
  "total_cost": 5,
  "ticket_ids": [2563, 2564, 2565, 2566, 2567],
  "ticket_odds": 100.0
}
```

# Deployment

I am running this on an Ubuntu 18.04.3 (LTS) x64 VPS.
reqs:
```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```
This app can then be deployed automatically to a server by ssh using fabric3.
```
cd deploy_tools
fab deploy:host=user@domain
```
Then, follow the provisioning instructions in provisioning_notes.md
