# facebook-auto-poker

###Requirements

This Application runs on Docker

`sudo apt-get install docker.io`

###Install

First Download and build the Image by running the following the command

```
sudo docker build -t fb_autopoker https://github.com/megabytemb/facebook-auto-poker.git
```

###Start
Apply that image to a new Continer

Note: You will need to update this command with your Facebook Username and Password And 2 Step Verification Code
Your 2 Step Verification Code will change every time, so be careful

```
sudo docker run -e FB_USERNAME=username -e FB_PASSWORD=password -e FB_TWO_STEP=123456 --name="fb_autopoker" -d fb_autopoker
```

###Stop
To stop the continer, run the following command
```
sudo docker rm -f fb_autopoker
```
