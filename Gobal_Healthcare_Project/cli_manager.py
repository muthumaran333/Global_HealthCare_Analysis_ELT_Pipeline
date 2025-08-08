import argparse
import logging
import os
import pandas as pd
from datetime import datetime
from etl.data_transformer import DataTransformer
from etl.load_data import DataLoader
from tabulate import tabulate


class CLIManager:
    def __init__(self, api_client, db_handler):
        self.api_client = api_client
        self.db_handler = db_handler

        # Setup logging
        logging.basicConfig(
            filename='etl.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("CLIManager initialized")

        # Setup CLI
        self.parser = argparse.ArgumentParser(description="Global Healthcare Data ETL & Analysis CLI")
        self._setup_parser()

    def _setup_parser(self):
        subparsers = self.parser.add_subparsers(dest='command', help='Available commands')

        # Fetch and Load
        fetch_parser = subparsers.add_parser('fetch_data', help='Fetch, transform, and load healthcare data.')
        fetch_parser.add_argument('country', type=str, help='Country to fetch data for (e.g., "India")')
        fetch_parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        fetch_parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')

        # Queries
        query_parser = subparsers.add_parser('query_data', help='Query loaded data.')
        query_subparsers = query_parser.add_subparsers(dest='query_type')

        total_cases_parser = query_subparsers.add_parser('total_cases', help='Get total cases for a country.')
        total_cases_parser.add_argument('country', type=str)

        daily_trends_parser = query_subparsers.add_parser('daily_trends', help='Get daily trends for a metric.')
        daily_trends_parser.add_argument('country', type=str)
        daily_trends_parser.add_argument('metric', type=str)
        daily_trends_parser.add_argument('--export', action='store_true', help='Export results to CSV')

        top_n_parser = query_subparsers.add_parser('top_n_countries_by_metric', help='Top N countries by a metric.')
        top_n_parser.add_argument('n', type=int)
        top_n_parser.add_argument('metric', type=str)

        # Admin
        subparsers.add_parser('list_tables', help='List tables in the database.')
        subparsers.add_parser('drop_tables', help='Drop all tables (Use with caution).')

        # Raw SQL
        sql_parser = subparsers.add_parser('run_sql', help='Run a raw SQL command.')
        sql_parser.add_argument('sql', type=str)

    def run(self):
        args = self.parser.parse_args()
        command = args.command

        if command == 'fetch_data':
            self._handle_fetch(args)
        elif command == 'query_data':
            self._handle_query(args)
        elif command == 'list_tables':
            self._list_tables()
        elif command == 'drop_tables':
            self._drop_tables()
        elif command == 'run_sql':
            self._run_sql(args)
        else:
            self.parser.print_help()

    def _handle_fetch(self, args):
        logging.info(f"Fetching data for {args.country} from {args.start_date} to {args.end_date}")
        print(f" Fetching data for {args.country}...")

        try:
            raw_cases = self.api_client.fetch_cases()
            raw_vacc = self.api_client.fetch_vaccinations()

            transformer = DataTransformer()
            transformed_cases = transformer.transform_cases(raw_cases)
            transformed_vacc = transformer.transform_vaccinations(raw_vacc)

            loader = DataLoader(self.db_handler)
            loader.load_cases(transformed_cases)
            loader.load_vaccinations(transformed_vacc)

            print(" ✅ Data fetched and loaded successfully.")
            logging.info("Data fetch & load complete.")
        except Exception as e:
            logging.error(f"Failed during fetch/load: {e}")
            print(f"❌ Error during fetch/load: {e}")

    def _handle_query(self, args):
        try:
            if args.query_type == 'total_cases':
                sql = f"""
                    SELECT country_name, SUM(total_cases) as total_cases
                    FROM daily_cases 
                    WHERE country_name = '{args.country}'
                    GROUP BY country_name;
                """
                result = self.db_handler.run_query(sql)
                if result:
                    print(tabulate(result, headers=["Country", "Total Cases"], tablefmt="grid"))
                else:
                    print("No results found.")
                logging.info(f"Total cases queried for {args.country}")

            elif args.query_type == 'daily_trends':
                sql = f"""
                    SELECT report_date, {args.metric}
                    FROM daily_cases
                    WHERE country_name = '{args.country}'
                    ORDER BY report_date
                    LIMIT 10;
                """
                result = self.db_handler.run_query(sql)
                if result:
                    headers = ["Date", args.metric]
                    print(tabulate(result, headers=headers, tablefmt="grid"))

                    if getattr(args, 'export', False):
                        df = pd.DataFrame(result, columns=headers)
                        os.makedirs("reports", exist_ok=True)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"reports/{args.country}_{args.metric}_trends_{timestamp}.csv"
                        df.to_csv(filename, index=False)
                        print(f"✅ Report exported to: {filename}")
                else:
                    print("No trends found.")
                logging.info(f"Daily trends for {args.metric} in {args.country} queried.")

            elif args.query_type == 'top_n_countries_by_metric':
                sql = f"""
                    SELECT country_name, SUM({args.metric}) AS total
                    FROM daily_cases
                    GROUP BY country_name
                    ORDER BY total DESC
                    LIMIT {args.n};
                """
                result = self.db_handler.run_query(sql)
                if result:
                    print(tabulate(result, headers=["Country", f"Total {args.metric}"], tablefmt="grid"))
                else:
                    print("No countries found.")
                logging.info(f"Top {args.n} countries by {args.metric} queried.")

            else:
                print("Unknown query type.")
                self.parser.print_help()
        except Exception as e:
            logging.error(f"Query failed: {e}")
            print(f"❌ Error running query: {e}")

    def _list_tables(self):
        try:
            tables = self.db_handler.run_query("SHOW TABLES;")
            if tables:
                print(tabulate(tables, headers=["Tables"], tablefmt="grid"))
            else:
                print("No tables found.")
            logging.info("Listed tables.")
        except Exception as e:
            logging.error(f"Error listing tables: {e}")
            print(f"❌ Error listing tables: {e}")

    def _drop_tables(self):
        print("Dropping all tables...")
        try:
            drop_queries = [
                "DROP TABLE IF EXISTS daily_cases;",
                "DROP TABLE IF EXISTS vaccination_data;"
            ]
            for query in drop_queries:
                self.db_handler.run_query(query)
            print("✅ All tables dropped.")
            logging.info("All tables dropped.")
        except Exception as e:
            logging.error(f"Failed to drop tables: {e}")
            print(f"❌ Error dropping tables: {e}")

    def _run_sql(self, args):
        print(f"🧾 Running SQL: {args.sql}")
        try:
            results = self.db_handler.run_query(args.sql)
            if results:
                column_names = [desc[0] for desc in self.db_handler.cursor.description]
                print(tabulate(results, headers=column_names, tablefmt="grid"))
            else:
                print("SQL executed. No results to display.")
            logging.info(f"Executed SQL: {args.sql}")
        except Exception as e:
            logging.error(f"Error running raw SQL: {e}")
            print(f"❌ Error running SQL: {e}")
