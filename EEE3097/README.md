# Welcome to the IoT Smart Alarm Clock
## MBRSHI002 & MZBNJA002

## API Specification
#### Hardware API
Due to the high volume of the GPIO pins on a raspberry pi it allows us the project to be scalable and use various interfaces depending on the module being used. From I2c, UART, SPI as the mpst ubiqutous.
The display uses an I2C interface

The soundtracks stored on the SD-card of the raspberry pi are stored in digital form.

For the sound to be audible to the user and get various degrees of pitch and volume there is a need for digital to analogue conversion. 
The pins that connect directly to the LPF is converted from the General Purpose digital pins to PWM. This is applied to the LDR as well as it contains a spectrum of values

The button is connected in the normal binary mode as they only have two states. A debounce value is set such that its a convenience to the user and long enough to ensure that they are fully awake


#### Software API 
For us to store our states there is need for a server and the one used for this project is the Apache Web Server.
It hosts the website which was developed using the 3 languages: HTML for the content, CSS for the styles, JavaScript for the interactivity

The server provides the pi with a local-netwerk viable website correspomding to its IP address or hostname

For the Apache Server to work with python script an interface module called WSGI was used.

The interface between software is bidirectional just like the SPI characteristic (the webiste affects the speaker, the button affects the website)



