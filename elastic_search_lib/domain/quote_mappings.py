quote_mappings = {
  "dynamic_templates": [
    {
      "stuffs_as_strings": {
        "match_mapping_type": "string",
        "match":   "stuff*",
        "mapping": {
          "type": "text",
          "analyzer": "quote",
          "search_analyzer": "quote_search"      
        }
      }
    }
  ],
  "properties": {
    "movie":   {
      "type": "text",
      "analyzer": "movie",
      "search_analyzer": "movie_search"
    },
    "speaker":    {
      "type": "text",
      "analyzer": "speaker",
      "search_analyzer": "speaker_search"
    },
    "quote":  {
      "type": "text",
      "analyzer": "quote",
      "search_analyzer": "quote_search"      
    },
  }
}

quote_settings = {
  "analysis": {
    "filter": {
      "substring": {
        "type": "ngram",
        "min_gram": 3,
        "max_gram": 3
      }
    },
    "analyzer": {
      "movie": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"]        
      },
      "movie_search": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"]
      }, 
      "quote": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"]
      },
      "quote_search": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"],
      },
      "speaker": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"]
      },
      "speaker_search": {
        "tokenizer": "whitespace",        
        "filter": ["lowercase", "substring"]
      }
    }
  }
}
