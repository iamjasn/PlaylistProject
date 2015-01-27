PlaylistProject
==============

http://54.191.28.219/concert_preview/

A RESTful application built with Django and AngularJS

This is my final project for PDX Code Guild. It is an API mashup that generates a "playlist" based on upcoming concerts in the client's geographical area. I use the Songkick API to get the events, and then match them to additional metadata using the Echo Nest music intelligence platform. I then match them to a streaming track in Rdio and display a limited number on the page. I'm using the rdio-python library to access the Rdio API. 
