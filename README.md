# Animal Sightings Map

- A small Flask application to view the results of animal sightings within range of a postcode area
- Uses the [Postcode IO API](https://postcodes.io) API to get location data for a postcode / random postcode.
  - Random postcode not yet fully implemented within the application but function can be called manually.
- Queries the [NBN Atlas API](https://nbnatlas.org/) to get the animal sightings within a postcode area.
- Only a few taxa have been hard-coded in the application.

TO DO:

- Implement Random postcode funciton.
- Get all taxonomic sightings within a postcode.
