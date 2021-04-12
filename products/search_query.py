
def search_product_query(search_item):
    return {
        "query" : {
            "bool":{
                "must":[
                    {
                        "multi_match":{
                            "query" : search_item,
                            "type" : "phrase_prefix",
                            "fields" : [
                                'name',
                                'category.category_name',
                                'description'
                            ]
                        }
                    },
                    {
                        "term":{
                            "is_draft":False
                        }
                    } 
                ]
            }
        }
    }
