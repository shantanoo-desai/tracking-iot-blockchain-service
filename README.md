# Tracking-IoT-Blockchain Service

This is a Repository to provide __RESTful__ APIs for EPCIS and IoT Information for
[NIMBLE-Platform](https://github.com/nimble-platform). These APIs can provide data related to NIMBLE's Track&Trace services along with IoT Sensor Data Information as well as the platform's Blockchain Network.

## Functionalities

These __RESTful__ APIs communicate with:

* EPCIS Repository (MongoDB Instance)
* Sensor Repository (InfluxDB)
* NIMBLE's HyperLedger Fabric API

### Development

- Written using `python3.6`

- Enable a Virtual Environment

        python -m venv venv

- Activate the Environment

    Linux

        source venv/bin/activate

    Windows

        venv/Scripts/activate.ps1

- Install Dependencies

        pip install -r requirements.txt

- Set `APP_CONFIG` to the configuration file variables e.g. `testing.cfg` or `production.cfg`

    Linux

        export APP_CONFIG=testing.cfg
    
    Windows (PowerShell)

        $env:APP_CONFIG = "testing.cfg"

- enable debugging in the `app.py`:

        app.run(debug=True)

- Run the app using

        python app.py

## Documentation

- Current Swagger Documentation available on http://localhost:5000/api/

## Deployment

- Disable debug mode in production using `debug=False` in `app.py`
- The app is deployed with __uWSGI Server__
- Change the settings for the __uWSGI Server__ in `app.ini`
- Adapt the `APP_CONFIG` variable in the `docker-compose` file to `production.cfg` with all environment variables
  necessary in it
- build using:

        docker-compose up --build

## License
__MIT License__


## Developed and Maintained by

Shantanoo Desai(des@biba.uni-bremen.de)

__University Bremen__ and __BIBA - Bremer Institut für Produktion und Logistik GmbH__, Bremen, Germany