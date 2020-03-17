from nimble_iot_bc import app

entrypoint = app.main()

if __name__ == "__main__":
    entrypoint.run(debug=False)
