# Points of Interest (POI) Manager

A Django application that manages Points of Interest (POI) data from various file formats (CSV, JSON, XML). The application provides functionality to import POI data, view it through the Django admin interface, and filter/search based on different criteria.

## Requirements

- Python 3.10 or above
- Django 4.2.0 or above
- Additional dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:

```bash
git clone https://github.com/dan-super/test-ss.git
cd test-ss
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
./venv/Scripts/activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser for admin access:

```bash
python manage.py createsuperuser
# Use these credentials for development:
# Username: admin
# Email: admin@example.com
# Password: admin123!
```

Note: For production environments, always use strong, unique passwords.

## Running the Application

1. Start the Django development server:

```bash
python manage.py runserver
```

2. Access the admin interface at: http://localhost:8000/admin

## Importing POI Data

The application includes a management command to import POI data from various file formats. The command supports CSV, JSON, and XML files with the following specifications:

### File Format Specifications

- CSV Format:

  ```
  poi_id,poi_name,poi_latitude,poi_longitude,poi_category,poi_ratings
  ```
- JSON Format:

  ```json
  {
    "id": "...",
    "name": "...",
    "coordinates": [latitude, longitude],
    "category": "...",
    "ratings": [...],
    "description": "..." (optional)
  }
  ```
- XML Format:

  ```xml
  <RECORDS>
    <DATA_RECORD>
      <pid>123456789</pid>
      <pname>Point of Interest Name</pname>
      <platitude>48.8566</platitude>
      <plongitude>2.3522</plongitude>
      <pcategory>restaurant</pcategory>
      <pratings>1,2,3,4,5</pratings>
    </DATA_RECORD>
  </RECORDS>
  ```

  Notes:
  - The XML importer handles special characters (like &, <, >) automatically
  - Ratings should be comma-separated integers
  - Coordinates must be valid decimal degrees
  - Categories should match the supported types (e.g., restaurant, park, bus-stop)

### Import Command Usage

```bash
python manage.py import_poi_data path/to/file.csv path/to/file.json path/to/file.xml
```

You can import multiple files at once by providing multiple file paths.

## Features

1. **Data Import**
   - CSV, JSON, and XML format support
   - Single or multiple POI import
   - Data validation and conversion
   - Unicode character support
   - Duplicate handling

2. **Admin Interface**
   - POI listing and details view
   - Search and filtering
   - Average rating display
   - Category management
   - Coordinate validation

## Project Structure

```
SearchSmartly/
├── poi/                    # Main application directory
│   ├── management/        # Custom management commands
│   │   └── commands/   
│   │       └── import_poi_data.py
│   ├── migrations/        # Database migrations
│   ├── admin.py          # Admin interface configuration
│   ├── models.py         # Data models
│   └── views.py          # Views (if needed)
├── poi_manager/           # Project settings directory
├── requirements.txt       # Project dependencies
└── manage.py             # Django management script
```

## Testing

The application includes a comprehensive test suite that covers core functionality:

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test poi.tests
```

### Test Coverage

The test suite includes:

1. **Model Tests**

   - POI creation and validation
   - Coordinate validation (latitude/longitude bounds)
   - Average rating calculation
   - Unicode character handling
   - Duplicate external ID prevention
2. **Import Tests**

   - JSON data import validation
   - Data format handling
   - Error handling for invalid data

### Running Tests with Coverage Report

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run manage.py test

# Generate coverage report
coverage report
```

## Implementation Details

### Core Features
- Django admin interface for POI management
- Command-line data import tool
- SQLite database storage
- Coordinate and rating validation
- Database indexing for performance

### Data Import
- Supports CSV, JSON, and XML formats
- Handles Unicode and special characters
- Prevents duplicate entries
- Validates data before import
- Supports multiple file import

### Data Validation
- Latitude range: -90 to 90
- Longitude range: -180 to 180
- Unique external IDs
- UTF-8 file encoding
- Numeric rating values

## Security
- Password-protected admin interface
- Input validation
- Secure credential handling
