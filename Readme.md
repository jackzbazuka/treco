# Treco

By - Milind and Ibrahim as a project for GUI course.

## A plant searching app

This application is built using tkinter, SQLite and a botanical data source [API](https://trefle.io). It is a single window application, with pages for different functionalities. I've used `ResultPage.py` to render species information for both save and search feature. For searching, the user can enter a common name into the search field though the app supports search via scientific name too. For additional information the user can download the response JSON recieved from the API but the user has to configure the download path (absolute path required) in `ResultPage.py` for this functionality to work. By default, all JSONs will be downloaded in the main directory of the application.

**Prerequisites:** A `.env` file in main directory to hold the access token for API. The environment variable holding the key should be named `APP_TOKEN`. To acquire an access token, follow this [link](https://docs.trefle.io/docs/guides/getting-started/#what-you-need).

`main.py` is the entry point to the application. It creates a database with a table at first instance.

### Features

* PAGINATION: The application has an inbuilt mechanism to restrict page fetching from the API.

* DYNAMIC RESULT RENDERING: The results are rendered and mounted dynamically on a frame after recieving a response for a search from the API.

* BOOKMARK OPTION - The user has the option to bookmark the species for easy access to it later. I've used a SQLite database to implement this feature.

### Bugs

* The whole app is not responsive yet. It has a fixed window size. The issue can be resolved by configuring widgets to scale accordingly.

* The results overflow from the viewport in case of high result count. It has to be mounted on a canvas which enables the scroll mechanism.

* All the requests made to the API are currently *synchronous*. This might cause the application to choke in case of high result count for a search.

* The background color of the buttons doesn't function properly on macOS. The malfunction occurs in Tcl which is the underlying library to tkinter.

### Exceptions

Some species might have some fields set to null due to unavailability of that datapoint. The requisites to display a species in search result are:

- image of the species

- scientific name of the species

- common name of the species
