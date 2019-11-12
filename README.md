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

## Documentation

- Current Swagger Documentation available on http://localhost:5000/api/

## License
__MIT License__


## Developed and Maintained by

Shantanoo Desai(des@biba.uni-bremen.de)

__University Bremen__ and __BIBA - Bremer Institut für Produktion und Logistik GmbH__, Bremen, Germany