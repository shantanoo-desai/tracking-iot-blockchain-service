# Tracking-IoT-Blockchain Service

This is a Repository to provide __RESTful__ APIs for EPCIS and IoT Information for
[NIMBLE-Platform](https://github.com/nimble-platform). These APIs can provide data related to NIMBLE's Track&Trace services along with IoT Sensor Data Information as well as the platform's Blockchain Network.

## Functionalities

These __RESTful__ APIs communicate with:

* EPCIS Repository (MongoDB Instance)
* Sensor Repository (InfluxDB)
* NIMBLE's HyperLedger Fabric API

### Development

- Written using `python3.x`

- Enable a Virtual Environment

        python -m venv venv

- Activate the Environment

    Linux

        source venv/bin/activate

    Windows

        venv/Scripts/activate.ps1

- Install Dependencies

        pip install -r requirements.txt

    or

        python setup.py develop

- Set `APP_CONFIG` to the configuration file variables e.g. `testing.cfg` or `production.cfg` in the 
   `nimble_iot_bc` directory:

    Linux

        export APP_CONFIG=testing.cfg
    
    Windows (PowerShell)

        $env:APP_CONFIG = "testing.cfg"

- enable debugging in the `main.py`:

        entrypoint.run(debug=True)

- Run the app using

        python main.py

### Development with Docker

        docker build -t nimble-iot-blockchain-api .

(see __Deployment__ section for setting up environment file)

## Documentation

- Current Swagger Documentation available on http://localhost:5000/api/doc/

## Deployment

- Disable debug mode in production using `debug=False` in `main.py`
- The app is deployed with __uWSGI Server__
- Change the settings for the __uWSGI Server__ in `app.ini`
- Adapt the `APP_CONFIG` variable in the `docker-compose` file to `production.cfg` with all environment variables
  necessary in it.
- The `production.cfg` file __MUST__ be in the `nimble_iot_bc` directory. Else, adapt the compose file with 
  the path to the configuration accordingly (see `volumes`).
- build using:

        docker-compose up --build

### Docker

        docker --name=iot-tnt-bc-microservice -e APP_CONFIG=production.cfg  -p 5000:5000 shantanoodesai/nimble-iot-blockchain-api:latest

## License
__MIT License__


## Developed and Maintained by

Shantanoo Desai(des@biba.uni-bremen.de)

__Faculty of Production Engineering, University Bremen__. In collaboration with __BIBA - Bremer Institut für Produktion und Logistik GmbH__, Bremen, Germany