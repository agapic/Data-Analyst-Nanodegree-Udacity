# Data Visualization with D3
## By Andrew Gapic

## Summary

This data visualization displays data for the top ten 100m and 200m male sprinters in Track and Field. It shows how the most recent records
in the 100m and 200m are significantly faster than those of the past. It also shows how world records in general are becoming harder
to break (naturally of course), but it goes to show how we approaching the limits of mankind. Additionally, users can add their own custom runners, or even
themselves, to see how they pair against the greatest. The data is mostly from here: http://www.webcitation.org/6B6G1X4mj
with the exception of the most recent records which can be found nearly everywhere ([here](http://www.nytimes.com/2009/08/21/sports/21track.html)
and [here](http://www.telegraph.co.uk/sport/othersports/athletics/11703867/Justin-Gatlin-I-can-break-Usain-Bolts-100m-world-record-this-summer.html))

## Design 

I spent a great deal of time figuring out what I wanted to do. Initially, I wanted to display gold medals for countries
in the Olympics but scrapped that idea. Then I wanted to show some sort of graph that displayed positional differences in 
Track and Field events as I always enjoyed seeing the comparisons. 

The initial version was sort of inspired from here: [NY Times Data Visualization](http://www.nytimes.com/interactive/2012/08/05/sports/olympics/the-100-meter-dash-one-race-every-medalist-ever.html?_r=2&)
which displays Olympic record data, but world records don't always occur at the Olympics so I wanted to display _world_ records instead.
There's one major flaw with this idea though. _Of course_ there is a positive correlation between time and world records! But I was curious
how each world record was compared with the previous and it was quite interesting. The amount of world records is decreasing each year, but
in many cases when it actually is broken, it's broken by a larger margin than previously. In fact, the current person in first place (Usain Bolt)
is so far ahead of everyone else in terms of the 100m and 200m events that it's surreal.

The history of my changes is displayed in the commits, but I'll discuss a few of the higher level details here. 

The data is initially displayed via a transition. I decided to use a simple line with small black dots and reserved a red dot for first place. My reasoning for this is straightforward:
I wanted to have a large data-to-ink ratio and I feel I've done a decent job at it. There is no clutter or unnecessary things added (the buttons are arguable)
To see what each "dot" contains, the user can hover over it to display the name, year, and country of the sprinter.

Delving deeper, I wanted to let the user tell their own story as well after I told my own. They can easily add their own personal records (if known) to the 
graph or even add other things such as animals, potentially faster humans, etc. In my opinion, this is what makes the data set fun and interesting.





## Feedback

### Person 1
"There isn't any title and when you add someone who is too slow you can't even see them on the graph. I was sort of confused upon first glance
because I wasn't sure what was happening."

**These changes were taken into account in commit 1/2

### Person 2
"I think it'd make sense if you had an axis that displays the actual years of the runner, no? I mean it looks like you're trying to 
show some sort of relationship between the years of the records based on what you told me. So I think that would be cool."

**These changes were taken into account in commit 2

### Person 3

"It's a bit .. ugly so to speak. Spruce up the buttons a bit and maybe add vertical lines throughout so we can intuitively see the 
distances without hovering over the people. Otherwise, it looks cool. I had fun playing around with it."

**These changes were taken into account in the final commit.**

## Resources

[D3 Documentation](https://github.com/mbostock/d3/wiki/API-Reference)
[NY Times Data Visualization for Track and Field Events (Inspiration](http://www.nytimes.com/interactive/2012/08/05/sports/olympics/the-100-meter-dash-one-race-every-medalist-ever.html?_r=2&)
[Track and Field World Records Data Set](http://www.webcitation.org/6B6G1X4mj)
