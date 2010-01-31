Introduction
============


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

Track related
-------------

Interface: fm.last.api.track
Methods: 
 - getTags( String artist, String track )
 - addTags( String artist, String track, String[] tags )
 - removeTag( String artist, String track, String tag )
