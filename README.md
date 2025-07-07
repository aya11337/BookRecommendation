# BookRecommend

A project for recommending books using Python, Airflow, and Weaviate.

## Features

- Book recommendation logic in Python
- Orchestrated data pipelines using Airflow
- Semantic search and storage with Weaviate
- Interactive analysis with Jupyter Notebooks

## Project Structure

- `airflow/`: Airflow DAGs and configs
- `weaviate/`: Weaviate setup and configs
- `include/`: Book descriptions and supporting files
- `Supressout.py`: Utility scripts
- `BookRecommender.ipynb`, `airflow.ipynb`: Notebooks for analysis and prototyping

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd BookRecommend
   ```

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # (if available)
   ```

3. **Set up Airflow**
   - Install Airflow:  
     `pip install apache-airflow`
   - Initialize Airflow DB:  
     `airflow db init`
   - Start the scheduler and webserver:
     ```bash
     airflow scheduler &
     airflow webserver &
     ```

4. **Set up Weaviate**
   - Navigate to `weaviate/` and run:
     ```bash
     docker-compose up -d
     ```

5. **Run Notebooks**
   - Launch Jupyter:
     ```bash
     jupyter notebook
     ```

## Usage

- Edit and run Airflow DAGs in `airflow/dags/`
- Use Jupyter notebooks for prototyping and analysis
- Store and query semantic data with Weaviate

## License

MIT License
