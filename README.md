# Python Computer Vision

<div style="text-align: right"> 
This repository is a usage example for the computer vision library OpenCv. I followed the 
tutorial https://www.youtube.com/watch?v=01sAkU_NvOY&t=815s to replicate the gesture volume
control. 

The program works by detecting key points in the hand and by tracking the distance between 
the points at the tip of the index and thumb (pinch_separation). One problem that I kept running
into was the sensibility of depth, since the measurements where going to be affected
if my hand was closer of farther.

To try and fix this issue I measured the distance of the tip of the index and
the medial phalanx points (screen_separation). If you look closely, the farther you are from the 
screen the greater the pinch separation distance becomes. Because of this, if we
divide the pinch separation distance by the screen separation distance the value stops
depending on the separation of the screen and becomes accurate despite this distance as the
relationship between the decibels and screen distance is inversely proportional.

Now, to convert the value of the division we stated above, to decibels y measured the max
value given by my open hand, and interpolated it to range from the decibels my pc has. You of course
may be thinking that this approach would not work for larger or smaller hands, and you are correct. 
As of now, I am working on an statistics approach that would modify these values depending on the variance
of the pinch distance.
</div>

