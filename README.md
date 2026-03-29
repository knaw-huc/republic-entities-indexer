
# Republic Entity Indexer

## Purpose
The Republic Entity Indexer (REI) is used to create an ElasticSearch index for the Goetgevonden Entiteiten Browser ([https://entiteiten.goetgevonden.nl/](https://entiteiten.goetgevonden.nl/)).

The REI is a Python application that you can run on a local machine, to create a local or remote ElasticSearch index.

## Data
The origin of the entity data is twofold:

#### 1. The entity files
The entity files is a collection of JSON files of which each contains a distinct set of entities. These entities are extracted from the texts within the corpus of resolutions of the Dutch States General.

The following entities can be distinguished:
1. commissions (commissies)
2. delegates (gedelegeerden)
3. qualities (hoedanigheden)
4. locations (locaties)
5. organisations (organisaties)
6. persons (personen)

The JSON files have the following structures:

*Commissions*
`id: string,`
`name: string,`
`category: string,`
`labels: list[string],`
`comment: string,`
`links: list[string]`

*Delegates*
`id: string,`
`name: string,`
`leefjaren: string,`
`provincie: string,`
`RAA_nr: integer,`
`category: string`

*Qualities*
`id: string,`
`name: string,`
`category: string,`
`labels: list[string]`

*Locations*
`id: string,`
`name: string,`
`geo_data:`
`. region: string,`
`. modern_country: string,`
`. ?modern_province: string,`
`. coordinates: latlon,`
`links: list[type: string, target: string]`
`labels: list[string]`

*Organisations*
`id: string,`
`name: string,`
`category: string,`
`labels: list[string],`
`comment: string,`
`links: list[type: string, target: string, target_category: string, description: string]`

*Persons*
`id: string,`
`name: string,`
`category: string,`
`labels: list[string],`
`raa: list[string, integer],`
`delegates: list[string, string],`
`envoyes: list[string, string]`

#### 2. The years table
This table contains the years of the first and last occurrence per entity in the resolutions. 

The years table is delivered as a csv file or an Excel sheet. It contains the following three columns:
`id: string,`
`first_year: integer,`
`last_year: integer`

Where the id column contains the id's of the several entities. Each entity id has it's own prefix, so matching is quite simple.

## Preprocessing
The six JSON files are manually converted to Python objects. Each of these objects consist of a list of entities.
The six objects are stored in separate python files. These files are imported into the main program.

The years table is converted to a LibreOffice worksheet. This worksheet is imported into a MySQL database.

Current configuration:
`tablename: entity_years,`
`database name: conversie,`
`user: root,`
`host: localhost,`
`port: 3306`

## Scripts
The indexing app consists of the following three scripts:

`create_index.py`
The main script

`mysql_handler.py`
This script contains the MySQL queries

`indexer.py`
Adds the created documents to the ElasticSearch index.

## ElasticSearch
This version of the indexer uses a local Docker version.
After the index is created it's uploaded to the server where the Goetgevonden application is running. Direct indexing to a central ES instance is also an option.

For creating a local index a Docker instance of ES is started with the command
`docker run --name elastic_index  -p 9200:9200 -p 9300:9300  --rm  -v /<LOCAL PATH>/index:/usr/share/elasticsearch/data -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1`

