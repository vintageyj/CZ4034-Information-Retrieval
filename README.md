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