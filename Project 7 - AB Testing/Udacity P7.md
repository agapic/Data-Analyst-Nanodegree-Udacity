# Experiment Design
### Written by Andrew Gapic for Udacity's A/B Testing Course
## **Metric Choice**

The invariant metrics chosen were: number of cookies, number of clicks, and click-through-probability. We don't expect the number of unique cookies to change as we are operating under the assumption that traffic remains relatively stable over the course of the experiment. Additionally, we expect the number of clicks on the "start free trial" button to remain stable because the experiment takes place _after_ the user clicks it. Since click-through-probability is simply the number of unique cookies to click the button divided by the number of unique cookies to view the page, then this should remain stable as well. 

It should be noted that user IDs was _not_ used as either an invariant or evaluation metric. It doesn't make sense to have user IDs as an invariant because we _expect_ a decrease in users that enroll in the free trial due to the nature of the experiment. As an evaluation metric, user IDs on its own isn't very helpful, as there are many user IDs that existed _prior_ to the experiment. We're more curious to see if the experiment has an effect on new users, so having a ratio of users to unique cookies is more appropriate.

The evaluation metrics chosen were as follows:

* **Gross conversion** - (# of users who enrolled in the free trial / # of unique cookies who clicked the "Start Free Trial" button)

    * We would expect this to change because the experiment inserted in between clicking the button and actually enrolling. Since Udacity provides a warning to users who can't commit the recommended amount of studying time, we would expect this to be slightly lower in the experiment. In the control group however, no warning is presented and so it's likely that *more *people would enroll, thus giving a larger gross conversion. This difference is what makes it attractive as an evaluation metric

* **Net Conversion** - (# of user-ids to remain enrolled past the 14-day boundary (1 payment at least) / # of unique cookies to click the "Start Free Trial" button)

    * This is similar to retention, except that the unit of diversion is the # of unique cookies. In my opinion, this is likely the most relevant metric Udacity would measure over the course of the experiment. We'd expect this number to increase, since realistically only satisfied users (and likely returning users) will make one payment after the 14-day boundary. If the experiment goes out as planned, we should expect this to increase as it filters out all the "bad users", i.e., those that come for a few days and leave.

In summary, arguably the most important statistic to look out for will be net conversion because its unit of diversion is a cookie -- the same as the experiment. It also provides a measurement for people that are completely new to Udacity (this isn't always the case as users can have multiple accounts). While retention is a nice-to-have for Udacity, the required duration is far too long for it to be of any use in _this_ experiment. This is because retention is measured from enrollment onwards, whereas conversion metrics are measured from the click. Therefore, the intervention of this experiment occurs _before_ retention, thereby not making it the most logical metric for this experiment.

For curiosity's sake, I've included retention throughout this report to demonstrate the long duration required for it to have any benefit.

Ideally, Udacity's metric of interest is net conversion -- how many new users actually start a free trial and pay. There are arguably two main goals that this experiment hopes to accomplish:

1. Do not decrease revenue
2. Filter out student's who are unable to make the required time commitment.

For increasing revenue, net conversion will be the metric to watch out for here. In order to align with our goal, we hope that this metric does not decrease. With respect to filtering out students, gross conversion is the metric to scrutinize. This metric will ideally _decrease_ since we expect only committed users to register for the courses. Whether Udacity is satisfied with revenue not changing is a business decision. If revenue stays roughly the same, but there are less users, then I'd say it's a win for Udacity.

## **Measuring Standard Deviation**

Gross Conversion: `sqrt(0.20625*(1-0.20625) / (0.08*5000)) = 0.020231`

Retention: `sqrt(0.53*(1-0.53)/ 5000*(660/40000) ) = 0.0549`

Net Conversion: `sqrt(0.1093*(1-0.1093) / (0.08*5000)) = 0.0156`

The unit of diversion for gross conversion and net conversion is a cookie, and the denominator in each of these is also a cookie, hence why these two metrics have the lowest standard deviations (and variances). Due to this, I can expect the empirical variability to be very close to the analytical variability. Retention's standard deviation/variability is slightly higher since the denominator is the number of users but the unit of diversion is a cookie. Therefore, we can expect that there is a difference between the empirical variability and analytical variability.

## **Sizing**

### **Number of Samples vs. Power**

The Bonferroni correction was not used because it is far too conservative in this case and is prone to Type II errors (false negatives). This is because there is certainly a large amount of correlation between the evaluation metrics.

To calculate the page views, I used this website: [http://www.evanmiller.org/ab-testing/sample-size.html](http://www.evanmiller.org/ab-testing/sample-size.html)

The results were as follows:

* Gross Conversion: 25835

* Retention: 69533

* Net conversion: 27413

Then, dividing each by 0.08 (the click-through-probability on the "start free trial" button), and multiplying by 2 (since we want the amount of views from the experiment and control groups to be equal) we get:

* Gross Conversion: 645875

* Retention: 1738325

* Net Conversion: 685324

The amount of pageviews required for retention is far too high. Additionally, our unit of diversion is cookies and net conversion is higher than gross conversion so 685324 is the final number that we'll work with. 

### **Duration vs. Exposure**

This experiment isn't particularly risky; a message indicating that users should re-evaluate their decision to enroll is likely to make users happier than angrier. Therefore, directing 75% of the traffic to the experiment will allow the experiment to last for approximately 23 days. In the case that Udacity created a riskier experiment, a smaller proportion of traffic should be directed towards the experiment, and then ramped up over time to avoid a learning effect and bad press.

# Experiment Analysis

## **Sanity Checks**

Sanity checks were done on each of the invariant metrics, and the results are shown below:

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Lower Bound</b></td>
    <td><b>Upper Bound</b></td>
    <td><b>Observed</b></td>
    <td><b>Passed?</b></td>
  </tr>
  <tr>
    <td>Number of Cookies</td>
    <td>0.4988</td>
    <td>0.5012</td>
    <td>0.5006</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Number of clicks on "Start free trial"</td>
    <td>0.4959</td>
    <td>0.5041</td>
    <td>0.5005</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Click-through-probability on "Start free trial"</td>
    <td>0.0812</td>
    <td>0.0830</td>
    <td>0.0821</td>
    <td>Yes</td>
  </tr>
</table>


Sample formulae/calculations for each metric are here:

* Number of Cookies:

    * Observed: `#Views Control / (#Views Control + #Views Experiment)`

    * Confidence interval: `0.5 +/- sqrt(0.5*0.5 / (#Views Control + #Views Experiment)) = +/- 0.0012`

* Number of clicks on "Start free trial":

    * Observed: `#Clicks Control / (#Clicks Control + #Clicks Experiment)`

    * Confidence interval: `0.5 +/- sqrt(0.5*0.5 / (#Clicks Control + #Clicks Experiment)) = +/- 0.0041`

* Click-through-probability on "Start free trial":

    * Observed: `#Clicks Control / #Views Control`

    * Confidence interval: `0.0821 +/- sqrt(0.5*0.5/345543) = +/- 0.00085`

## **Result Analysis**

### **Effect Size Tests**

Recall that retention is not a feasible metric to measure over the course of this experiment. Therefore, we perform an effect size test on gross conversion and net conversion. A sample calculation is only shown for gross conversion. 

* Gross Conversion: (-0.0291, -0.0120) statistically significant and practically significant

    * p<sub>pool</sub> = `(# control enrollments + # experiment enrollments) / (# control clicks + # experiment clicks) = 0.208607`

    * Standard Deviation = `sqrt(0.208607 * (1-0.208607)*(1/#clicks control + 1/#clicks experimental)) = 0.004372`

    * Margin of error = `0.004372*1.96 = 0.0085685`

    * D = p<sub>exp</sub> - p<sub>cont</sub> = 0.19832 - 0.218875 = -0.02055

    * Since zero is not in the interval, it is statistically significant. Additionally, 0.02 (practical significance) is not in the interval either so it is practically significant.

* Net Conversion: (-0.0116, 0.0019) not statistically significant and not practically significant

### **Sign Tests**

For gross conversion, the p-value was **0.0026** and it was statistically significant. For net conversion, the p-value was **0.6776** and there was no statistical significance. To calculate the p-values, a binomial test was used as shown here: [http://graphpad.com/quickcalcs/binomial1.cfm](http://graphpad.com/quickcalcs/binomial1.cfm) 

### **Summary**

I decided not to use the Bonferroni correction because net conversion and gross conversion are dependent on each other. More specifically, net conversion is a subset of gross conversion and so applying this correction would make the data too conservative. Delving deeper, Bonferroni controls for type I errors (false positive) at the cost of type II errors (false negative). In our case, we would expect type I errors to be higher and type II errors to be lower without the Bonferroni correction. It is important that ALL the metrics must be satisfied (gross conversion and net conversion) in order to make a decision, therefore our goal would be to minimize type II errors. The reason for this is that if gross conversion doesn't have a significant change but net conversion does, then the experiment likely wasn't the cause for the change in net conversion and it was likely some other factor. If net conversion doesn't have a change but gross conversion does, then we probably shouldn't launch the experiment because we see no change in revenue. This would be more subjective and up to the business team at Udacity. However, if all of the metrics have a change, then the experiment was likely a success and we should move forward with a launch.


The results of net conversion are the most important and thus the p-values related to this test are the most important factor with whether we want to launch or not.

## **Recommendation**

Based on the high level analyses shown above, I would recommend not running the experiment as is. While gross conversion was statistically and practically significant, net conversion was not. In fact, 56.5% of the number payments _decreased_ in the experimental group. This means that Udacity may be losing money from it. I would suggest bootstrapping the data to see if there is a specific demographic that is causing this, or if it's just the experiment overall.

The main issue with this experiment is that it assumes people are actually aware how many hours 5+ hours of studying a week is. Many of the people who didn't pay could be overeager students who overestimate the necessary amount of time commitment. In fact, telling people they are required to study x amount of hours per week may be seen as a challenge by the overconfident and when reality hits, they realize they can't keep up with the lectures (I am guilty of this).

# Follow-Up Experiment

Adding on to the issues that this experiment has, I would suggest lowering the amount of time in a free trial to 7 days or paying a discount up front. 14 days is quite a bit of time and some users might milk what they want out of the experience and decide not to pay. Changing the free trial to 7 days may help, but it also may infuriate users. This would have to be rolled out very slowly to avoid negative press. 

However, a discount seems like a more practical choice to avoid early cancellations. If a user is aware that there are discounts after a certain period of time, it may be a motivating factor going forward because it simulates the effect of "saving money". The implementation of the discount feature would appear after users have enrolled in the course because we are trying to avoid early cancellations.

My hypothesis is that more users will actually complete the course due to the psychological effect of a discount appearing to save the user money (when in reality they're still spending money). 

**It is important that Udacity define what exactly an early cancellation is. Is it one month, two months, six months? This will affect our evaluation metric. **

* Unit of Diversion: user id

    * Only users can enroll in courses, which means only users can see the experiment and make payments. If we were to choose cookies, we'd be overestimating the amount of signups.

* Invariant Metric: user id

    * Since this experiment would only be tracked after the user has enrolled, user id is the appropriate metric of choice. This is because you need to be a user enrolled in the course to see the experiment.

* Evaluation Metric: Cancellation Rate: = # users to cancel early / # userids

    * Recall that the denominator is our unit of diversion -- user ids. We want to track the percentage of users who cancel early relative to the number of user ids enrolled. In our experiment, we should ideally have less users that cancel early (meaning a smaller rate) compared to control.

Our evaluation metric should be smaller for our experimental group since we would expect less users to cancel. If there is no difference between experiment and control, the definition for early cancellation should change. If there are still no differences, the experiment should be scrapped, since Udacity would be making less money for the same result.

