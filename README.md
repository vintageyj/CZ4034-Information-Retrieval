# CZ4034-Information-Retrieval

As a group of graduating Computer Science and Data Science students, a common challenge we all face (as do many others) is the sourcing of jobs in the tech industry. However, sourcing for jobs can be quite the ardous process, and we often found ourselves wishing for a way to easily view and explore current job offerings. So why not build it ourselves? Using reviews from Glassdoor, our group worked on building an opinion search engine which is able to retrieve relevant opinions based on user queries. The retrieved documents are supplemented with sentiments classified by a machine learning model, to provide users with a holistic view of the current tech job landscape. We have added some setupn instructions below for those interested in trying out our retrieval system.

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

Refer to the elasticsearch example notebook on usage.

</br></br>
### Setup Instructions for Dash App

Step 1: Create Conda Environment
To create a new Conda environment with Python 3.11, run the following command in your terminal:

```
conda create --name myenv python=3.11
```
Replace myenv with your preferred environment name.

Step 2: Install Dependencies
Activate the newly created environment:

```
conda activate myenv
```
Then, install the project dependencies using pip and the provided requirements.txt file:

```
pip install -r requirements.txt
```
Step 3: Run the Application
Once the dependencies are installed, you can run the application by executing the app.py file:

```
python app.py
```
The application will be launched and accessible at 
```
http://127.0.0.1:8050/
```

<br><br>
### Code for the Classification task
The data files, codes, and results obtained with regards to the Classification task can all be found in _Classification_ folder under /tree/main/Classification
