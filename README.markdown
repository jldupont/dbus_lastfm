Introduction
============

This application offers a DBus API to Last.fm web service API (LFMWS).
Since many of the "write" methods of the LFMWS required authentication,
this application facilitates interfacing to Last.fm by provided a simple
GUI for the user to provision the required parameters (username, api_key, secret_key)
and launch a browser instance for performing the "authorization flow".

Features
========

- Account Settings (username, api_key, secret_key)
- Track related:
  - track.getTags
  - track.addTags
  - track.removeTag


API
===

The API is accessible through DBus. The DBus bus name is *fm.last.api*. There is only one object exposed, the root */* object.

Account related
---------------

Interface: fm.last.api.account
Methods: 

 - getUsername() -> (String username)
 - setUsername( String username )
 - setApiKey( String api_key )
 - setSecretKey( String secret_key )
 - clearSession()
 - authUrl() -> (String URL)

Track related
-------------

Interface: fm.last.api.track
Methods:
 
 - getTags( String artist, String track )
 - addTags( String artist, String track, String[] tags )
 - removeTag( String artist, String track, String tag )

 
Dependencies
============

- `python-notify` Ubuntu package
- GTK+
- Python >=2.6.x, < 3.0
  
Installation
============

A Debian package is available on my Launchpad PPA: https://launchpad.net/~jldupont/+archive/jldupont
