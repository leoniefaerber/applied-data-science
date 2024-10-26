import pandas as pd
from datetime import datetime

def clean_columns():
    df = pd.read_csv('./data/cleaned_dataset.csv')

    # Date columns
    df['host_since'] = pd.to_datetime(df['host_since'], errors='coerce')
    df['host_since'] = (datetime.now() - df['host_since']).dt.days


    # Drop the review-related columns (because these probably don't exist for our case data???)
    review_columns = [col for col in df.columns if 'review' in col.lower()]
    df = df.drop(columns=review_columns)

    # Converting percentage to float
    df['host_response_rate'] = df['host_response_rate'].astype(str).str.replace('%', '', regex=False).astype(float) / 100

    # Converting boolean fields
    boolean_cols = ['host_is_superhost', 'host_has_profile_pic', 'host_identity_verified', 'instant_bookable']
    df[boolean_cols] = df[boolean_cols].replace({'t': 1, 'f': 0})

    # TODO: not sure this is the best way to use this sort of data
    # Converting latitude and longitude to float
    df['latitude'] = df['latitude'].astype(str).str.replace(',', '.').astype(float)
    df['longitude'] = df['longitude'].astype(str).str.replace(',', '.').astype(float)

    # Converting price to float
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)


    # Convert bathrooms to numeric, handle any non-numeric values
    df['bathrooms'] = pd.to_numeric(df['bathrooms'].astype(str).str.replace(',', '.'), errors='coerce')
    df['shared_bathroom'] = df['bathrooms_text'].str.contains('shared', case=False, na=False)
    df.drop(columns=['bathrooms_text'], inplace=True)


    # TODO: one-hot encoding is too inefficient for these categories. find better metric
    # One-hot encoding for categorical variables
    # df = pd.get_dummies(df, columns=['neighbourhood_cleansed', 'host_response_time', 'property_type', 'room_type'], drop_first=True)
    # drop for now. CHANGE LATER! These columns are very important
    df.drop(columns=['neighbourhood_cleansed', 'host_response_time', 'property_type', 'room_type'], inplace=True)

    # Turn bool to 1 / 0
    bool_cols = df.select_dtypes(include='bool').columns
    df[bool_cols] = df[bool_cols].astype(int)

    # TODO: group and clean amenities
    # Drop the amenities column for now
    df.drop(columns=['amenities'], inplace=True)

    # TODO: process description and name in a way that we can use it
    df.drop(columns=['name', 'description', 'id'], inplace=True)

    # Display cleaned data types to verify
    print("Data types after cleaning:")
    print(df.dtypes)

    # Save the processed DataFrame to a file
    df.to_csv('./data/processed_data.csv', index=False)

    print("Data processing complete. Data saved to 'processed_data.csv'.")


def main():
    clean_columns()

if __name__ == "__main__":
    main()