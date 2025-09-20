# In your populate_spots.py script

import csv
from django.core.management.base import BaseCommand, CommandError
# Remove 'Region' from the import statement
from apps.tourism.models import TouristSpot, Category, Location, Province

class Command(BaseCommand):
    help = 'Populates the TouristSpot database from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file.')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Attempting to populate data from: {csv_file_path}'))

        try:
            try:
                with open(csv_file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self._process_csv_rows(reader)
            except UnicodeDecodeError:
                self.stdout.write(self.style.WARNING("UTF-8 decoding failed, trying cp1252..."))
                with open(csv_file_path, 'r', encoding='cp1252') as file:
                    reader = csv.DictReader(file)
                    self._process_csv_rows(reader)
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file_path}" does not exist.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

        self.stdout.write(self.style.SUCCESS('Database population complete.'))

    def _process_csv_rows(self, reader):
        for row in reader:
            try:
                # Get or create Category
                category_name = row.get('category_name')
                if not category_name:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to missing category_name: {row}"))
                    continue
                category, created = Category.objects.get_or_create(name=category_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new category: {category.name}'))

                # Get or create Province (No Region needed)
                province_name = row.get('province', '')
                if not province_name:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to missing province: {row}"))
                    continue

                province_obj, created = Province.objects.get_or_create(name=province_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new province: {province_obj.name}'))

                # Get or create Location, now linking directly to Province
                location_name = row.get('location_name')
                if not location_name:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to missing location_name: {row}"))
                    continue

                location, created = Location.objects.get_or_create(
                    name=location_name,
                    defaults={
                        # Assign the province object directly
                        'province': province_obj,
                        # If you removed the 'region' field from the Location model,
                        # you can also remove this line:
                        # 'region': row.get('region', ''),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new location: {location.name}'))

                # Create TouristSpot
                is_featured_str = row.get('is_featured', 'FALSE').upper()
                is_featured = is_featured_str == 'TRUE'

                TouristSpot.objects.create(
                    name=row['name'],
                    description=row.get('description', ''),
                    category=category,
                    location=location,
                    image=row.get('image', 'tourist_spots/default.jpg'),
                    is_featured=is_featured,
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully added tourist spot: {row["name"]}'))

            except KeyError as e:
                self.stdout.write(self.style.ERROR(f"Missing column in CSV: {e} in row: {row}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))