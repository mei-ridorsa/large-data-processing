# Flask and Pandas practice

This is a little project that I made to learn about the Flask framework and the Pandas library.

## _API - Large Data Processing_

## Configuration

This project has been developed using the Flask framework. I have used flask_skeleton as a base. As such, this project has some things that are not really needed for the code, like DB support.

To execute it, you will need to have Python 3 installed. You may need a virtual environment to run this.

Install the required Python packages:
```sh
pip install -r requirements.txt
```

Run:

```sh
flask run
```

## 1 - Large CSV Processing

I have used the Pandas library, as it's very efficient and convenient in reading and processing large files. As it makes it easy to read CSV files in chunks, we can avoid memory problems while processing files larger than our available memory.

Using Panda's methods, we read a CSV file by chunks, we group by the first two columns and calculate the sum of the third.

## 2 - API and Asynchronous Task Processing

Local endpoints can be called via cURL or via software such as Postman.

### API Endpoint 1: Schedule file to processing

The endpoint is: 127.0.0.1:5000/api/v1/reports/process/<filename>

The file will need to be placed inside a folder named 'input'.

Example response:
```sh
{
    "message": "success",
    "report_id": "c23d0b123acb42a2a96ae948029e283c"
}
```

### API Endpoint 2: Download the result

The endpoint is: 127.0.0.1:5000/api/v1/reports/<report_id>

For simplicity's sake, the filename is the same as the task id. In reality, it would be better to save the relation task_id->filename into Redis or similar.

If the CSV processing hasn't finished or the report is does not exist, the endpoint returns:
```sh
{
    "message": "The report does not exist. Please check that the id is correct or try again later",
    "report_id": "c23d0b123acb42a2a96ae948029e283c"
}
```

Otherwise, the report will be downloaded (or shown, if using a client like Postman).
