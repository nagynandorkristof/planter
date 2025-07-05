# Plant Watering Management Application

Addresses the following problems:
- Multiple people may water the plant at the same time, leading to overwatering.
- Plants may be neglected and die from lack of water.

This is a multi-site Django application, allowing you to host several sites with a single application instance. For example, you can manage both office.org and home.com, each with separate data, all from the same server.

Visit images folder for screenshots.

## Plans

- [] Figure out how to configure multiple sites: https://docs.djangoproject.com/en/5.2/ref/contrib/sites/
- [] Improved UI code and add node package manager. Single Page Application or Multi Page Application?
- [] Add multi tenant authorization. (permissions to sites)
- [] Add permissions. (archive, edit plant in the site)
- [] Add authentication mehtods like SSO - Single Sign On - so people can access the site with microsoft/google email addresses without storing password.
- [] Deployment Docker image and add pipeline.
- [] Subscribe to all plants with one click.
- [] Add email notification if a plant needs watering.
- [] Send heartbreaking email if you forget to water a plant for long time.
- [] Add basic tests.
- [] Add common type of plants. So it is easier to add new ones with the same watering requirements.
- [] Add seasonal watering requirements change.
- [] QR code identifications for plants. So you can print out QR codes and access the plant in the system easly.
- [] Add charts to show watering trends.
- [] Add multiple properties to follow plant health. E.g: Add dry leafs tag when watering.
- [] Add rooms and maps.
- [] Add lighting requirements and add windows to the map.
- [] Make a drag and drop editor to edit the map.