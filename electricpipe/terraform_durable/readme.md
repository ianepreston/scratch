# Why have two terraform folders?

The infrastructure in my main terraform folder is stateless, and some of it can run up compute costs while it's active.
Since this is just for learning I want to be able to destroy and provision it at will. But since this is a data project, I do want somewhere more persistent to store my data and some other state information so I don't have to completely restart my data generating process every time.