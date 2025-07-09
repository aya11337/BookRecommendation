from airflow.sdk import dag, task, chain 
from airflow.providers.weaviate.hooks.weaviate import WeaviateHook

collection_name='Books'
book_description_folder="include/data"
embedding_model='BAAI/bge-small-en-v1.5'


@dag(
    start_date=datetime(2025, 7, 11),
    schedule_interval='@daily',
   
    
)
def fetch_data():

    @task
    def create_collection_if_not_exists() -> None:
        from airflow.providers.weaviate.hooks.weaviate import WeaviateHook

    hook = WeaviateHook("my_weaviate_conn")
    client = hook.get_conn()
    existing_collection=client.collections.list_all()
    existing_collection_names=existing_collection.keys()
    if collection_name not in existing_collection_names:
        print(f"Collection does not exist, creating collection {collection_name}")
        collection=client.collections.create(name=collection_name)
        print(f"Collection {collection_name} created successfully")
        print(f"collection details{collection}")
        

    _create_collection_if_not_exists = create_collection_if_not_exists()

    @task
    def list_book_description_files() -> list:
        import os
        book_description_files= [f for f in os.listdir(book_description_folder) if f.endswith('.txt')]
        return book_description_files

    _list_book_description_files = list_book_description_files()

    @task
    def transform_book_description_files(book_description_files: list) -> list:
        import json
        import os

        with open(
            os.path.join(book_description_folder, book_description_files[0]),
            "r",
            encoding="utf-8",
        )as f:
            book_descriptions=f.readlines()
        titles=[book_description.split(":::")[1].strip()for book_decription in book_descriptions]
        authors=[book_description.split(":::")[2].strip()for book_decription in book_descriptions]
        descriptions=[book_description.split(":::")[3].strip()for book_decription in book_descriptions]
        list_of_book_data=[
            {
                "title":title,
                "author":author,
                "description":description
            }
            for title,author,description in zip(titles,authors,descriptions)
        ]
        return list_of_book_data


    _transform_book_description_files = transform_book_description_files.expand(
        book_description_files=_list_book_description_files
    )

    @task
    def create_vector_embeddings(list_of_book_data: list) -> list:
        from fastembed import TextEmbedding
        embedding_model=TextEmbedding(embedding_model=embedding_model)
        book_descriptions = [book["description"] for book in book_data]
        description_embeddings = [
            list(map(float, next(embedding_model.embed([desc]))))
            for desc in book_descriptions
        ]
        return description_embeddings

    _create_vector_embeddings = create_vector_embeddings.expand(
        list_of_book_data=_transform_book_description_files
    )

    @task
    def load_embeddings_to_vectordb(list_of_book_data:list,list_of_description_embeddings:list) ->None:
        from airflow.providers.weaviate.hooks.weaviate import WeaviateHook
        hook=WeaviateHook("my_weaviate_conn")
        client=hook.get_conn()
        collection=client.collections.get(collection_name)

        for book_data_list, emb_list in zip(list_of_book_data,list_of_description_embeddings):
            items=[]
            for book_data,emb in zip(book_data_list,emb_list):
                item=DataObject(
                    properties={
                        "title":book_data["title"],
                        "author":book_data["author"],
                        "description":book_data["description"],
                    

                    },
                    vector=emb,
                )
                items.append(item)
            collection.data.insert_many(items)
                
            


    _load_embeddings_to_vectordb = load_embeddings_to_vectordb(
        list_of_book_data=_transform_book_description_files,
        list_of_description_embeddings=_create_vector_embeddings,
    )

        
    chain(_create_collection_if_not_exists,_load_embeddings_to_vectordb)

fetch_data()