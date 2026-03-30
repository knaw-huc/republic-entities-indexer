
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

The index is created with the name * entities * . 

It has the following mapping:

`{
  "entities" : {
    "mappings" : {
      "properties" : {
        "RAA_nr" : {
          "type" : "long"
        },
        "category" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "comment" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "delegate_name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "delegates" : {
          "properties" : {
            "id" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "envoyes" : {
          "properties" : {
            "link" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "first_year" : {
          "type" : "long"
        },
        "geo_data" : {
          "properties" : {
            "coordinates" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "lat" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "lon" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "modern_country" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "modern_province" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "region" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "geslachtsnaam" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "id" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "id_persoon" : {
          "type" : "long"
        },
        "labels" : {
          "properties" : {
            "label" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "last_year" : {
          "type" : "long"
        },
        "leefjaren" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "links" : {
          "properties" : {
            "description" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "target" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "target_category" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "type" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "name" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "provincie" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "raa" : {
          "properties" : {
            "id" : {
              "type" : "long"
            },
            "name" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        }
      }
    }
  }
}
`

## Creating the index
To create an entity index follow this procedure:

1. Check out the Republic Entity Indexer on GitHub ([https://github.com/knaw-huc/republic-entities-indexer](https://github.com/knaw-huc/republic-entities-indexer)) to a locale directory on your computer.
2. Go to that directory
3. Create a virtual environment of choice
4. Install the requirements from `requirements.txt`
5. Create a subfolder for the ES index
6. Create a subfolder `data` for the entities as Python objects
7. Import the years table into MySQL (in my case is was a file called `entity-session-year-range.csv` )
8. Create the Python object files from the entity-JSON files and place them into the `data` subfolder
9. Start a local Docker instance of ElasticSearch. Mount your local index folder to `/usr/share/elasticsearch/data` in the Docker container
10. Activate your local environment
11. Run `python create_index.py`
12. When the index is created, move the index to the server where * Goetgevonden * is running
13. Copy the index to folder where the current index is stored
14. Restart ElasticSearch
