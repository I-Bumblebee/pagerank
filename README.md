## What I Did

I had to implement three functions that were missing:

### 1. The Transition Model

This function figures out where a random web surfer might go next:
- Most of the time (85% by default), they click a random link on the current page
- Sometimes they get bored and just type in a random website address
- If they end up on a page with no links, they just pick another random site to visit

```python
# My approach was pretty simple:
# 1. Set base probability for random jumps
# 2. Add extra probability for following links
# 3. Handle pages with no outgoing links
```

### 2. The Random Sampling Method

This one was fun! It's like simulating a person clicking around the web:
- Start at any random page
- Click links (or occasionally jump randomly) thousands of times
- Count how many times you visit each page
- Pages you visit more often are more "important"

I basically just kept track of where the surfer went and counted visits!

### 3. The Math Way (Iterative)

This one uses the actual PageRank formula instead of simulation:
- Start by giving every page equal importance
- Update each page's rank based on who links to it
- Keep doing this until the ranks stop changing much
- More important pages linking to you = more importance for your page

## My Takeaways

- The code is actually simpler than I expected
