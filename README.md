# domain-rank-history-chrome-extension




rank changes report 


https://tranco-list.eu/methodology

## last 30 days

https://tranco-list.eu/query

## last 2 years

https://github.com/zakird/crux-top-lists/tree/main/data/global





## tranco rank

Sure, let's break it down into simpler terms:

### Understanding the Tranco List Configuration

1. **Purpose**:
   The goal is to create a consistent and stable ranking of domain popularity over time using data from several ranking providers.

2. **Data Sources**:
   The Tranco list uses rankings from five different providers. 

3. **Averaging Ranks**:
   - **Over Time**: They look at rankings from the past 30 days.
   - **Across Providers**: They combine the rankings from all five providers.

4. **Scoring Method**:
   - **Dowdall Rule**: This is a method to give scores to domains based on their ranks. For instance, if a domain is ranked 1st, it gets 1 point; if 2nd, it gets 0.5 points; if 3rd, it gets 0.33 points; and so on.
   - **Purpose**: This rule helps to score and rank the domains in a way that reflects their relative popularity more fairly.

5. **Handling "Bucketed" Ranks**:
   Sometimes, rankings are given in broad ranges or "buckets" (e.g., "top 10,000"). To make these buckets more precise:
   - **Normalize Buckets**: They use the geometric mean (a type of average) of the range’s boundaries. For example, for a bucket of "10,000 to 20,000", they use the geometric mean of 10,000 and 20,000 to estimate a more accurate "virtual" rank within the range.

### Summary

- **Objective**: To create a stable and accurate ranking of domains by averaging rankings from multiple providers over 30 days.
- **Method**: Use the Dowdall rule to score domains and normalize bucketed ranks to provide a more precise ranking within broader categories.
