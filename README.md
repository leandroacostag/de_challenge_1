# README

To get started with the `de_challenge` project, follow these steps:

## Run Locally

1. Open a terminal and navigate to the project directory: `/home/ubuntu/de_challenge/`

2. Activate the project environment. Depending on your operating system, you can use either `venv` or `conda`:

   - For `venv`, run:
     ```
     python -m venv .venv
     ```
   - For `conda`, run:
     ```
     conda create -n de_challenge
     ```

3. Activate the project environment. Depending on your operating system, you can use either `venv` or `conda`:

   - For `venv`, run:
     ```
     source .venv/bin/activate
     ```
   - For `conda`, run:
     ```
     conda activate de_challenge
     ```

4. Install the project dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

5. Rename the `.env.example` file to `.env` and update the environment variables as needed.

6. Run the following command to execute the project:
   ```
   python -m app/main.py
   ```

## Run on Docker

1. Open a terminal and navigate to the project directory: `/home/ubuntu/de_challenge/`

2. Build the Docker image by running the following command:

   ```
   docker build -t de_challenge .
   ```

3. Run the Docker container by executing the following command:

   ```
    docker run --env-file /home/ubuntu/de_challenge/.env -v /home/ubuntu/de_challenge/data:/app/data de_challenge
   ```

   Replace `/home/ubuntu/de_challenge/data` with the path to the data directory on your local machine.

## Partitioning of the data

For partitioning the data in the `de_challenge` we use the following directory structure:

```
/book=book_name/year=year/month=month/day=day/hour=hour/minute=minute/order_book.csv
```

This partitioning scheme is hierarchical and based on the timestamp of the data.
This approach is well-suited for easy analysis and querying of the data using tools like Amazon Athena.
The data is partitioned by the following columns:

- `book`: The name of the book.
- `year`: The year of the timestamp.
- `month`: The month of the timestamp.
- `day`: The day of the timestamp.
- `hour`: The hour of the timestamp.
- `minute`: The minute of the timestamp.

For example, the following directory structure shows how the data is partitioned:

```
/book=mxn_btc/year=2024/month=07/day=15/hour=00/minute=00/order_book.csv
/book=mxn_btc/year=2024/month=07/day=15/hour=00/minute=10/order_book.csv
/book=mxn_btc/year=2024/month=07/day=15/hour=00/minute=20/order_book.csv
...
```

### Advantages of this partitioning scheme:

- **Query performance**: The hierarchical partitioning aligns well with typical query patterns in Athena, allowing for efficient time-based filtering and analysis.

- **Scalability**: Keeps partitions small and manageable, which is crucial for maintaining query performance in Athena.

- **Organization**: The deep directory structure creates a clear hierarchy, making it easier to navigate and understand the organization of your data.

## Assumptions

This process relies on the following assumptions:

- Latency is not a concern. If it were, we would need to consider a different approach to api calls.
