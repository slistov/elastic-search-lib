quote_mappings = {
  "properties": {
    "speaker":    {
      "type": "text"
    },
    "quote":  {
      "type": "text",
      "analyzer": "quote"
    }, 
    "movie":   {
      "type": "text",
      "analyzer": "quote",
      "search_analyzer": "quote_search"
    }
  }
}

quote_settings = {
  "analysis": {
    "filter": {
      "substring": {
        "type": "nGram",
        "min_gram": 3
      }
    },
    "analyzer": {
      "quote": {
        "type": "russian",
      },
      "quote_search": {
        "type": "russian",
        "filter": ["substring"],
      },
      "movie": {
        "type": "default",
      },
      "movie_search": {
        "type": "default",
        "filter": ["substring"]        
      }
    }
  }
}
