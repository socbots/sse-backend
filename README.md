# API for making Sanbot move
![Sanbot running](docs/dlg_loading2.png)

*Make Alf do your biddings without touching Java code.*

### How dis work?

**sse_backend** is a Flask app that serves an [SSE](https://en.wikipedia.org/wiki/Server-sent_events) stream on the endpoint **/stream**.
It listens for a POST request to **/move**, which then sends off the JSON data to be emitted at /stream => **MobileSDK** is connected and listens for changes at /stream
=> this event gets parsed and sends move commands to **Sanbot**.

## Usage
**NOTE:** direction and distance aren't supported yet

POST to /move accepts the following JSON properties:

```
{
  bodyPart: String
  gesture: String
  direction: String
  distance: int
}
```
bodyPart is:
- head
- left_hand
- right_hand
- feet

direction is:
- left
- right
- up
- down
- stop

gesture accepts currently:
- wave

All properties aren't needed, it depends what you want the robot to do

### Make Alf wave
```
POST http://<sse_backend_url>/move HTTP/1.1
content-type: application/json


{
  "gesture": "wave",
  "bodyPart": "left_hand"
}
```
Waving requires just the gesture and which bodypart.

Alf can wave any part of his body! Even the feet! Try it out :)


### Can't be bothered with postman?
For quick testing, slam this into chromes console:
```
fetch('http://<sse_backend_url:5000/move', {
  method: 'POST',
  body: JSON.stringify({
    gesture: 'wave',
    bodyPart: 'left_hand'
  }),
  headers: {
    'Content-type': 'application/json; charset=UTF-8'
  }
})
.then(res => res.json())
.then(console.log)
```
Remember you need to have the MobileSDK running to see the results, but this will get you a json response if your sse_server is working.

- - -

Other emotes should be easy to implement now that we have the framework on MobileSDK setup.
Moving bodyparts a specific direction and distance aren't supported yet!


# Deployment to CSC Rahti
Docs https://docs.csc.fi/<br/>
Create user account on https://my.csc.fi/<br/>
Create project + enable Rahti service for the project.
## Setup build & deployment pipeline
Follow Fredrik's instructions https://github.com/welandfr/rahti-flask
### Additional notes
If the repo is private:
- 	you must choose advanced options and supply the ssh repo url instead.
	- **Source Secret**: Create new secret->SSH key authentication
		- Create new key pair and upload private key `ssh-keygen -t ed25519 -C "spam@ham.eggs"` etc...
	- Add the public key to your github account
- The github webhook secret is found in the build's editing page. Use it while configuring the webhook in GitHub.
- Choose to add a secure route as well. The https setup is painless
- Define pip dependencies in requirements.txt

The docker container will be default try to run `app.py` in the repo's root directory! If the main script is a different name or folder, add an environment variable `APP_FILE` with the main script's path.

## Data storage
https://docs.csc.fi/cloud/rahti/storage/ Tells what storage options are available
- Persistent volume was the simplest option since you don't need any additional python libraries. The mounted volume is accessed like any other directory in the file system.
- Object storage is like AWS's buckets. It's accessed with s3 compatible libraries.

### Create and attach volume
On Rahti
- Storage->Create Storage
- Set a name, access mode to shared access, give appropriate size. Ignore storage class.
- Applications->Deployments->{name}->Configuration->Add Storage
- Mount path to /data and give the volume a name
	- Subpath is not necessary, but "foo/" would turn into `/data/foo`

### Sync data
https://docs.csc.fi/cloud/rahti/tutorials/transfer_data_rahti/ Gives instructions for syncing data, we already made the persistent volume through the web interface.

The `oc` tool is needed to sync, so follow instructions here for installation: https://docs.csc.fi/cloud/rahti/usage/cli/

In order to upload files you must first authenticate the `oc` program with csc.
The secret token and `oc` login command is found in https://registry-console.rahti.csc.fi/registry
```
$ oc login --token {foobartoken} rahti.csc.fi:8443
```

There must be an online pod with the mounted volume to sync data to the persistent storage. The data will not only be bound to that pod, it'll get saved to the storage and every new deployment will also automatically mount the volume.

Find the pod with `oc get pods` 
Example output:
```
fredde-example-1-build              0/1       Init:Error   0          21h
fredde-example-1-pmbs8              1/1       Running      0          21h
fredde-example-2-build              0/1       Completed    0          21h
socbots-flask-production-1-build    0/1       Init:Error   0          1d
socbots-flask-production-12-s9bpb   1/1       Running      0          50m
socbots-flask-production-2-build    0/1       Init:Error   0          1d
socbots-flask-production-2-deploy   0/1       Error        0          1d
socbots-flask-production-3-build    0/1       Init:Error   0          1d
```
"socbots-flask-production-12-s9bpb" is the current deployment here.

A local directory and its files within is uploaded with
```
oc rsync ./local/dir/ POD:/remote/dir
```
`POD` is the pod name, followed by where it should be uploaded to. `/data` in our case.
So servings the local directory "models" to the pod's "/data" looks like
```
oc rsync ./models socbots-flask-production-12-s9bpb:/data
```
oc might output an error about failing to set permissions, but the data still got synced. Setting the path to /data/foo allows oc to set permissions, just not in the root directory apparently.
## Access persistent storage through Flask
As per the example above, the data exists in `/data/models`, so the Python app can now access the content like any other file on the filesystem.

*ps. for Flask, use `send_from_directory()` instead of `send_file()` for security reasons. `send_file` allows for access to any file in the system if the path is user-provided*
