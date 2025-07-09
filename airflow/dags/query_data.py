from math import degrees
from airflow.sdk import dag, task

@dag
def query_book():

    @task
    def search_vector_db(search_query:str) -> None:
        pass

    search_vector_db(search_query="Self help books")

query_book()
