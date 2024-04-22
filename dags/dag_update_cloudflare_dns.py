from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
import os

# Print Python environment paths right when the module is imported
print("Python Executable:", sys.executable)
print("Python Path:", sys.path)

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 1, 1),
}

# Define the DAG
dag = DAG(
    'update_cloudflare_dns_script',
    default_args=default_args,
    description='This flow updates the DNS records in Cloudflare every 15 minutes',
    schedule_interval='*/15 * * * *',
    catchup=False,
)

# Function to dynamically determine the script path
def get_script_path():
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ip_update_cloudflare_dns.py')
    return script_path

# PythonOperator to print Python executable path
def print_python_path():
    print("Python Executable:", sys.executable)

print_path_task = PythonOperator(
    task_id='print_python_path',
    python_callable=print_python_path,
    dag=dag,
)

# BashOperator to execute the Python script using the absolute path to the Python interpreter
execute_python_script = BashOperator(
    task_id='execute_python_script',
    bash_command=f'/usr/bin/python3 {get_script_path()}',
    dag=dag,
)
