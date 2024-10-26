import pandas as pd
import json

def amenitiy_correlation():
    df = pd.read_csv('./data/cleaned_dataset.csv')

    # Drop all columns except 'amenities' and 'availability_365'
    df = df[['amenities', 'availability_365']]

    # Define your cleaning and parsing functions (as before)
    def clean_amenities_string(amenities_str):
        if isinstance(amenities_str, str):
            amenities_str = amenities_str.replace('\u2013', '-')  # Replace en dash
            amenities_str = amenities_str.replace('\u2019', "'")  # Replace right single quote
            amenities_str = amenities_str.replace('\u2018', "'")  # Replace left single quote
            items = amenities_str.strip("[]").split(",")
            items = [item.strip().strip('"') for item in items if item.strip()]  
            cleaned_str = '[{}]'.format(','.join(f'"{item}"' for item in items))  
            return cleaned_str
        return '[]'  

    def parse_amenities(amenities_str):
        amenities_str = clean_amenities_string(amenities_str)
        if isinstance(amenities_str, str):
            try:
                return json.loads(amenities_str)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error parsing amenities: {e} | Problematic string: {amenities_str}")
                return []  
        elif isinstance(amenities_str, list):
            return amenities_str
        return []

    # Parse the amenities
    df['amenities'] = df['amenities'].apply(parse_amenities)

    # Extract unique amenities
    unique_amenities = set(item for sublist in df['amenities'] for item in sublist)

    # Create binary indicator DataFrame for amenities
    amenities_dict = {amenity: df['amenities'].apply(lambda x: 1 if amenity in x else 0) for amenity in unique_amenities}
    amenities_df = pd.DataFrame(amenities_dict)

    # Add the availability_365 column to amenities_df for correlation calculation
    amenities_df['availability_365'] = df['availability_365']

    # Calculate the correlation of amenities with availability_365
    correlation_with_availability = amenities_df.corr()['availability_365'].drop('availability_365')

    # Filter significant amenities based on a correlation threshold
   # significant_amenities = correlation_with_availability[abs(correlation_with_availability) > 0.1]

    # Display the significant amenities
    print("Amenities correlated with availability_365:")
    print(correlation_with_availability)

    # Optionally, save significant amenities to a CSV file
    correlation_with_availability.to_csv('./data/amenity_correlation.csv', index=True)


def main():
    amenitiy_correlation()

if __name__ == "__main__":
    main()