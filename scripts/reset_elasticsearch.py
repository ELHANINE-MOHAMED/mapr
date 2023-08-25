from elasticsearch import Elasticsearch

# Define Elasticsearch connection settings
es = Elasticsearch('http://localhost:9200/')

# Define list of indexes to delete and recreate
indexes_to_recreate = [
    "decoded_cdr",
    "raw_cdr",
    "loaded_cdr"
]

# Delete existing indexes
for index in indexes_to_recreate:
    if es.indices.exists(index=index):
        es.indices.delete(index=index)

# Define index mapping
mapping = {
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "properties": {
            "count": {
                "type": "long"
            },
            "date": {
                "type": "date",
                "fields": {
                    "kw": {
                        "type": "keyword",
                        "ignore_above": 256
                    },
                    "text": {
                        "type": "text"
                    }
                }
            },
            "executed_at": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "flux": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "heure": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "path": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "techno": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "type": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }
        }
    }
}

# Create new indexes with the specified mapping
for index in indexes_to_recreate:
    es.indices.create(index=index, body=mapping)

