## Goalkeeper Strategic Points
![alt text](goalkeeper_adjust_self.png)
The goalkeeper moves along an elliptical trajectory, where the major axis corresponds to the length of the goal and the minor axis is half the length of the goal area. The goalkeeper endeavors to maintain a position that is centrally aligned with the line connecting the ball to the goal. This strategic position allows the goalkeeper to cover the maximum possible area, enhancing its ability to defend the goal effectively.

## Defender Strategic Points
The main purpose is to defend as comprehensively as possible.
The defination of a strategic point is the midpoint of the line connecting the ball and goalpost to defend. A basic limit is when the strategic point is inside the goal, the x value of the strategic point is modified to leave the goal area.
![alt text](defender_strategic_point.png)
But, for the ball's position is easy to determined, but the goalpost to defend is not so easy to determined, according to the decision tree, there are three major scenarios:
### (1) The ball is not in our half 
Defenders should try to cover both side. In cases where both defenders are on the same side and one taking a longer route around, they should reset to their positions. If defenders are on opposite sides, they choose the nearest goalpost to defend; if on the same side, For instance, if both defenders are on the same side of the pitch and closer to goalpost 1, they should compare their distances to goalpost 2. The one closer to goalpost 2 then moves to defend it, while the other focuses on defending goalpost.

### (2) The ball is in our half, but the opponent has possession
The nearest defender should chase the ball while the other moves to the defensive point, and the player moving to a strategic position must consider the goalpost further from the ball chaser.

### (3) The ball is in our half, our team possesses it but This defender is not the one holding it.
In this scenario, there are two possibilities: either a forward who has dropped back is holding the ball, or another defender has possession. 
#### (3.1) If the forward in the backfield has the ball
The situation is similar to the first scenario: when two defender are on the opposite side, they defend the closest goal post, while on the same side, the player closer to middle guards the far goal post. 
#### (3.2) If another defender has the ball
This defender will cover the goal post that is farther away from the other defender.

## Striker Strategic Points
For strikers, to maximize the threat, it's crucial that the two strikers do not position themselves too close to each other. The ideal scenario is depicted as follows: Player 1 draws the attention of the goalkeeper, thereby creating an opportunity to pass the ball to Player 2. This strategic move gives Player 2 a significant chance to launch an effective attack.
![alt text](striker_strategic_point.png)
The strategic positioning for attackers is defined as follows, with the y-coordinate of the strategic position extending from the penalty area line. The choice of y-coordinate is binary, similar to the above-mentioned scenario: if the two forwards are on opposite sides, they choose the one closer to themselves; if on the same side, they compare both distances to the far ends and choose the closer striker to that side. Note that while this definition prevents players from entering the goal area, the x-coordinate is still regulated to ensure it does not invade the goal area for reasons such as maintaining sufficient maneuvering space. 
The selection of the x-coordinate is discussed through several scenarios:
### (1) Ball is not in attacking area
Simply set x to the edge of the attacking area.
### (2) Ball in attacking area, but our team does not possess it and this striker is far way
 In this case, use the midpoint between the ball and the goal. This maintains an offensive threat.
### (3) Ball in attacking area, another forward has the ball and the ball has not been passed to this forward
This situation encompasses two sub-scenarios:
#### (3.1) If the forward with the ball near the midfield
 The other forward should theoretically be more aggressive to attract attention and create threats. 
#### (3.2)If the forward with the ball is close to a shooting position
 Advancing further would not be appropriate. Hence, the x-coordinate is provisionally set to the midpoint between the ball and the penalty area line. This way, when the forward with the ball is relatively closer to the midfield, one forward can be more forward to pose a threat. Conversely, when the forward with the ball approaches or even enters the penalty area, other forward would hover around the penalty area line, allowing the other forward to have a relatively large space to pass the ball to him.
