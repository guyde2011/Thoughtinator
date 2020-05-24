
# Thoughtinator
Made as part of the TAU course Advanced System Design

## [Table of Contents]

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
	- [Command Line](#command-line)
	- [Environment](#env)
- [Components](#components)
	- [Client](#client)
	- [Upload Server](#upload-server)
	- [Parsers](#parsers)
	- [Saver](#saver)
	- [API Server](#api-server)
	- [GUI Server](#gui-server)


## Installation

1. Clone the repository:
   ```bash
    git clone git@github.com:guyde2011/thoughtinator.git
   ```
   
	And enter into it:
	  ```bash
	   cd thoughtinator
    ```

2. Setup the work environment via running

   ```bash
    ./scripts/install.sh
    source .env/bin/activate
    $ [thoughtinator] Successfully installed the environment!
   ```


## Getting Started
### Starting the project in docker
To run the project via docker, run 
```bash
 ./scripts/run-pipeline.sh
 $ [thoughtinator] Loading ...
```
When the project will finish loading you will see
```bash
 $ [thoughtinator] Successfully started!
 ```
 At which point you are advised to run a client to upload your sample into the server
 ### Starting a client

```bash
 python -m thoughtinator.client upload-sample 'my_sample_file.gz'
 ```
And that should start the client that uploads the sample file to our application

### Accessing the uploaded files
After the client has finished uploading your sample files, you can access them via the `http://localhost:8080`
Where you will be able to see the uploaded file in the website.
![Image](https://i.imgur.com/MHr4gM9.png)

## Basic Usage
### Command Line
The project has a few modules, each of which has a command line interface.
You can see how to use each component in the command line, via this list:
 - [Client](#client/cli)
 - [Upload Server](#upload-server/cli)
 - [Parsers](#parsers/cli)
 - [Saver](#saver/cli)
 - [API Server](#api-server/cli)
 - [GUI Server](#gui-server/cli)
 
 The project also has a cli module which retrieves saved snapshots.

The usage to the cli is corresponding to the [API's](#api-server) RESTful endpoints, and can also optionally get custom api host and port via `-h/--host` and `-p/--port`.

The `get-result` command also has a flag`-s/--save` flag, which allows to save the result to a given file

### Environment
The project has two configurable environment variables:

1. The save folder, which can be configured by:
    ```bash 
	export SAVE_FOLDER=some/path/to/a/folder
   ```
   Which decides where we will save our Images from the snapshots locally.

2. The config path, which is used to configure the custom logger of the project.
 It can be configured by:
   ```bash
   export CONFIG_PATH=some/path/to/a/config.json
   ```
   If this variable is not defined it will default to `<PROJECT_PATH>/thoughtinator/config.json`
The default configuration is:
   ```json
   {
   "options": []
   }
   ```
   By default the logger only shows errors but you can also add to options to see:
	  - `success`
	  - `info`
	  - `warning`
	  - `hide-errors` (This one hides the default-ly enabled errors)
 
## Components
The project is composed from a few components, each of which is handling a different part of the project.
Those components are:
- The [Client](#client)
- The [Upload Server](#upload-server)
- The [Parsers](#parsers)
- The [Saver](#saver)
- The [API Server](#api-server)
- The [GUI Server](#gui-server)

### Client
The client is the component that reads and uploads sample files from our local environment into our application.
The module is based in `thoughtinator.client`

You can import its upload_sample funcionallity as:
```py
from thoughtinator.client import upload_sample
```
and then run it with:
```py
>>> upload_sample(path='path/to/sample.gz', host='localhost', port=8000, file_format='protobuf') 
```

<h4 id='client/cli'>CLI</h4>   
The command line usage for the client is:

```bash
$ python -m thoughtinator.client upload-sample \
	      -h/--host '127.0.0.1'            \
	      -p/--port 8000                   \
	      'path/to/sample.mind.gz'
 ```

### Upload Server
The server is the component that listens for uploaded samples and sends them to be processed by our application.
The module is based in `thoughtinator.server`

You can import its run_server funcionallity as:
```py
from thoughtinator.server import run_server
```
and then run it with:
```py
>>> run_server(host='localhost', port=8000, mqueue_url='rabbitmq://127.0.0.1:5672') 
```

<h4 id='server/cli'>CLI</h4>   

The command line usage for the server is:
```bash
python -m thoughtinator.server run-server \
	      -h/--host '127.0.0.1'       \
	      -p/--port 8000              \
	      'rabbitmq://127.0.0.1:5672/'
 ```



### Parsers
The parsers are the components that extract and process data sent from the upload server and 
The module is based in `thoughtinator.parsers`

   ```py
from thoughtinator.parsers import run_parser
 ```
and then run it with:
   ```py
>>> run_parser('pose', my_pose_data) 
 ```

<h4 id='parsers/cli'>CLI</h4>   
The command line usage for the parsers is:

1. The `parse` command:

   ```bash
   python -m thoughtinator.parsers parse 'pose' 'path/to/snapshot_raw'
   ```

	Which parses a given raw snapshot file with the 'pose' snapshot.

2. The `run-parser` command:
  
   ```bash
   python -m thoughtinators.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
   ```
	Which runs a project parser which pushes its parsed results (which it gets by parsing server messages) to the message queue (in this case the results of the pose parser to the RabbitMQ message queue).
  

### The Saver


The saver is the component that saves any parser results into the application's database.
The module is based in `thoughtinator.saver`

You can import its run_saver funcionallity as:
```py
from thoughtinator.saver import run_saver
```
and then run it with:
```py
>>> run_saver('mongodb://127.0.0.1:27017', 'rabbitmq://127.0.0.1:5672') 
```
Which runs the saver connecting to the RabbitMQ message queue and the MongoDB.

<h4 id='saver/cli'>CLI</h4>   

The command line usage for the saver is:

```bash
python -m thoughtinator.saver run-saver 'scheme_db://db_host:db_port' \
	                                'scheme_mq://mq_host:mq_port'
  ```


### API Server

This component is the RESTful API server that outsources data from the database.
The module is based in `thoughtinator.api`

You can import its run_saver funcionallity as:
```py
from thoughtinator.api import run_server
```
and then run it with:
```py
>>> run_server('my_api_host', my_api_port, 'my_db_url') 
```

<h4 id='api-server/cli'>CLI</h4>   

The command line usage for the API server is:

```bash
python -m thoughtinator.api run-server    \ 
	      -h/--host '127.0.0.1'       \
              -p/--port 5000              \
              -d/--database 'my_db_url'
  ```

It exposes the following RESTful endpoints:

 `GET HOST:PORT /users`
  The saved users.

`GET HOST:PORT /users/user-id`
 The saved user's data.

`GET HOST:PORT /users/user-id/snapshots`
 The saved user's snapshots.

`GET HOST:PORT /users/user-id/snapshots/snapshot-id`
  The saved snapshot's available results.

`GET HOST:PORT /users/user-id/snapshots/snapshot-id/result-name`
  The saved data of some parsed result.

`GET HOST:PORT /users/user-id/snapshots/snapshot-id/<type_img>-image/data`
The saved Color / Depth Image data.


### GUI Server

This component runs the GUI server.
This module is based in `thoughtinator.gui`.

You can use its run_server functionallity by:
```py
from thoughtinator.gui import run_server
```
and then run it with:
```py
>>> run_server('gui_host', 'gui_port', 'api_host', 'api_port')
```

<h4 id='gui-server/cli'>CLI</h4>  
 
The command line usage for the GUI server is:
 ```bash
  python -m thoughtinator.gui run-server \
		    -h/--host '127.0.0.1'       \
		    -p/--port 8080              \
		    -H/--api-host '127.0.0.1'   \
		    -P/--api-port 5000
 ```


