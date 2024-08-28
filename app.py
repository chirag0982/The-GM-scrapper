from flask import Flask, render_template, request
from src.gmaps import Gmaps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
from flask import Flask, render_template, request, redirect, url_for
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    places = Gmaps.places([query], max=5)
    
    # Replace spaces with hyphens in the query
    query_for_file = query.replace(' ', '-')
    
    # Construct the file path based on the modified query
    file_path = f'output/{query_for_file}/csv/places-of-{query_for_file}.csv'
    
    # Check if the CSV file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and write the data
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for place in places:
                csv_writer.writerow([place['place_id'], place['name'], place['description'], place['featured_image']])
    
    # Render the template with the query and places
    return redirect(url_for('display_csv', file_path=file_path))
import csv,os
@app.route('/display_csv')
def display_csv():
    # Get the file path from the query parameters
    file_path = request.args.get('file_path')
    
    # Read the required fields from the CSV file
    csv_data = []
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Extract only the required fields from each row
            data = {
                'name': row['name'],
                'reviews': row['reviews'],
                'rating': row['rating'],
                'owner_name': row['owner_name'],
                'phone':row['phone'],
                'featured_image': row['featured_image']
            }
            csv_data.append(data)
    
    # Pass the extracted data to the template
    return render_template('display_csv.html', csv_data=csv_data)

if __name__ == '__main__':
    app.run(debug=True)
