from airflow.sdk import dag, task, chain

@dag
def my_dag():
    print("Hello World")

my_dag()
