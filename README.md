FlickArea
=========

Identify an area box on Google Maps for selected public photos on Flickr

1.	Make sure the following programs are installed:
➢	Python: https://www.python.org/downloads/
➢	Webpy: http://webpy.org/install#install 
➢	Flickr API kit: https://pypi.python.org/pypi/flickrapi 
2.	Go to the FlickArea directory and run the code.py file on command line.
➢	python code.py
The following line will appear upon success of hosting the server.
➢	http://0.0.0.0:8080/
3.	Open the http://localhost:8080/ page on a browser.
4.	Enter the name of a location and submit.
5.	Geotagged photos of your location (first 20) will be displayed.
➢	All photos will be selected initially. Deselect photos that do not represent your desired location.
➢	If you click “Search Again,” the deselected photos will be replaced with next search results.
➢	If you are satisfied with your selection of photos, click “Show Area Box” to display an area box of your location on Google Maps. The area box will be defined by the maximum and minimum longitudes and latitudes
➢	The red markers represent the exact location of each photo used to create the area box. If you click on one, the thumbnail of its photo will appear.
➢	If you wish to fix your selection of photos, you can click “Back” and deselect/select photos again.
➢	You may repeat the process until you obtain the desired area box, and the Google Maps can be navigated by scrolling and dragging.
➢	At any point, click the page title “FlickArea” to go to the home page.
6.	Once you are finished, quit the server on command line.
