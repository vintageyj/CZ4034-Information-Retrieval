# CZ4034-Information-Retrieval

To use the ElasticSearch Index, you need to have [Docker](https://www.docker.com/products/docker-desktop/) installed to setup the Elastic-Logstash-Kibana (ELK) stack.

After which, clone this repository onto a local directory on the host machine. 
```
git clone https://github.com/deviantony/docker-elk.git
cd docker-elk
```

Before proceeding with the subsequent steps, the passwords inside the **.env** file needs to be changed, otherwise it will default to 'changeme'.


Then inside the root folder where the **docker-compose.yml** is at, initialise the Elasticsearch users and groups required by docker-elk by running:
```
docker-compose up setup
```

If everything ran well and the setup completed without error, start the remaining stack components by running:
```
docker-compose up
```

Optionally, you can access the ElasticSearch server via Kibana:
```
http://localhost:5601/
```

If you have docker desktop, you can start the cluster directly from there instead on future sessions.

Refer to the elasticsearch example noteboook on usage.

Setup Instructions for Dash App

Step 1: Create Conda Environment
To create a new Conda environment with Python 3.11, run the following command in your terminal:

bash
Copy code
conda create --name myenv python=3.11
Replace myenv with your preferred environment name.

Step 2: Install Dependencies
Activate the newly created environment:

bash
Copy code
conda activate myenv
Then, install the project dependencies using pip and the provided requirements.txt file:

bash
Copy code
pip install -r requirements.txt
Step 3: Run the Application
Once the dependencies are installed, you can run the application by executing the app.py file:

bash
Copy code
python app.py
The application will be launched and accessible at http://127.0.0.1:8050/.

