import pandas as pd
from models import db_storage


class DataProcess:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.db_storage = db_storage

    def read_excel_data(self):
        """Read data from the Excel file using pandas."""
        try:
            data_df = pd.read_excel(self.excel_file_path)
            return data_df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    def process_data(self, data_df):
        """Process the data as needed before storing in the database."""
        # Add your data processing logic here if needed
        # For simplicity, let's assume the data is already in the desired format
        return data_df

    def save_to_database(self, processed_data_df):
        """Save processed data to the database."""
        try:
            with self.db_storage.app.app_context():
                processed_data_df.to_sql('data', self.db_storage.db.engine, if_exists='replace', index=False)
            print("Data saved to the database successfully.")
        except Exception as e:
            print(f"Error saving data to the database: {e}")

    def process_and_save_data(self):
        """Main method to orchestrate the entire process."""
        data_df = self.read_excel_data()
        if data_df is not None:
            processed_data_df = self.process_data(data_df)
            if processed_data_df is not None:
                self.save_to_database(processed_data_df)

if __name__ == "__main__":
    excel_file_path = 'path/to/your/excel/file.xlsx'  # Replace with your Excel file path
    data_processor = DataProcess(excel_file_path)
    data_processor.process_and_save_data()
