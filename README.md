# mmdata
ESO Master Merchant data in ELK

Requirements:

- docker
- docker-compose
- python 2.7 virtualenv

start ELK:

- `docker pull sebp/elk`
- `docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --name elk sebp/elk`

https://elk-docker.readthedocs.io/

run mmdata:

- `pip install elasticsearch`
- `pip install git+https://github.com/SirAnthony/slpp`
- `python mm-prepare.py`
- `python mm-import.py`

view mmdata:

- web browser to `localhost:5601`
- configure index
- browse data

README to be expanded...

<img src="owl.png" />