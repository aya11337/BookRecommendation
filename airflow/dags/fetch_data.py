from airflow.sdk import dag, task, chain 


@dag
def fetch_data():

    @task
    def create_collection_if_not_exists() -> None:
        pass

    _create_collection_if_not_exists = create_collection_if_not_exists()

    @task
    def list_book_description_files() -> list:
        return []

    _list_book_description_files = list_book_description_files()

    @task
    def transform_book_description_files(book_description_files: list) -> list:
        return []

    _transform_book_description_files = transform_book_description_files(
        book_description_files=_list_book_description_files
    )

    @task
    def create_vector_embeddings(list_of_book_data: list) -> list:
        return []

    _create_vector_embeddings = create_vector_embeddings(
        list_of_book_data=_transform_book_description_files
    )

    @task
    def load_embeddings_to_vectordb(list_of_book_data:list,list_of_description_embeddings:list) ->None:
        pass

    _load_embeddings_to_vectordb = load_embeddings_to_vectordb(
        list_of_book_data=_transform_book_description_files,
        list_of_description_embeddings=_transform_book_description_files
    )

        
    @task
    def print_hello():
        print("hello")
    chain(
        print_hello()
    )

fetch_data()