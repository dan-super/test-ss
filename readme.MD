# Points of Interest (POI) Manager

A Django application that manages Points of Interest (POI) data from various file formats (CSV, JSON, XML). The application provides functionality to import POI data, view it through the Django admin interface, and filter/search based on different criteria.

## Requirements

- Python 3.10 or above
- Django 4.2.0 or above
- Additional dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:

```bash
git clone git@github.com:dan-super/test-ss.git
cd test-ss
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
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
  <poi>
    <pid>...</pid>
    <pname>...</pname>
    <platitude>...</platitude>
    <plongitude>...</plongitude>
    <pcategory>...</pcategory>
    <pratings>[...]</pratings>
  </poi>
  ```

### Import Command Usage

```bash
python manage.py import_poi_data path/to/file.csv path/to/file.json path/to/file.xml
```

You can import multiple files at once by providing multiple file paths.

## Features

1. **Data Import**

   - Support for CSV, JSON, and XML file formats
   - Handles both single and multiple POI entries
   - Automatic data validation and type conversion
2. **Admin Interface**

   - Display of POI internal ID
   - POI name
   - POI external ID
   - POI category
   - Average rating calculation
   - Search functionality for internal and external IDs
   - Category filtering

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

- Uses Django's built-in admin interface for data visualization
- Implements custom management command for data import
- Uses SQLite as the database (can be easily changed to other databases)
- Includes data validation for coordinates and ratings
- Provides efficient database indexing for search operations

## Assumptions Made

1. POI ratings are stored as JSON arrays in the database
2. External IDs are unique across all data sources
3. Coordinates are provided in decimal degrees format
4. File encodings are UTF-8
5. Rating values are numeric

## Potential Improvements

1. Add API endpoints for programmatic access to POI data
2. Implement batch processing for large data files
3. Add data export functionality
4. Add more detailed validation for imported data
5. Implement caching for frequently accessed data
6. Add unit tests and integration tests
7. Add user authentication and authorization beyond admin interface
8. Add support for more file formats
9. Implement geographic queries and proximity search
10. Add data versioning and history tracking

## Security Considerations

- Admin interface is password protected
- Input data is validated before storage
- Database credentials are not exposed in version control
- File uploads are validated for format and content
