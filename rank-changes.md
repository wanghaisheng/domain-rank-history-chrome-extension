Tranco
Home
Download
Configure
Methodology(current)
About us
Log in
Register
Methodology
Full details on the methodology behind the Tranco list are available in our paper. You can also browse the source code.

Construction of the Tranco list
We designed the standard configuration of the Tranco list to improve agreement on the popularity of domains and stability over time, using the available rankings from (currently) five providers as our source data. To achieve this, we average ranks over the lists of all four providers over the past 30 days. We apply the Dowdall rule (scoring items with 1, 1/2, ..., 1/(N-1), 1/N points) to calculate the new score on which domains are ranked.

Where ranks are "bucketed", meaning that only a coarse range is given (e.g., a domain is in the top 10,000), we first normalize each bucket to the geometric mean of its boundaries, and use this as its 'virtual' rank in the rest of the computation.

Properties of source lists
Chrome User Experience Report (CrUX)
The Chrome User Experience Report (CrUX) is a monthly updated ranking published by Google, since March 9, 2021 (for data of February 2021). It consists of a variable number of entries, with the June 2023 list having around 18 million entries. Only websites are included. The original data set on BigQuery contains origins; we normalize these to their respective subdomain. Because of this normalization, the number of entries that we take into account is slightly lower than the number of entries in the CrUX data set, as some subdomains (in the order of a few thousand) appear under multiple origins (http vs. https, or with different ports).

The ranks are based on browser traffic contributed by opt-in Chrome users. Only "sufficiently popular" origins are included. The published ranks are bucketed, in buckets of 1000, 5000, 10000, 50000, 100000, 500000, 1 million, 5 million, 10 million, and the remaining ~8 million origins. A more detailed description of CrUX's methodology is available on this page.

The Chrome User Experience Report was considered the most accurate ranking in a 2022 study by Ruth et al.

Cloudflare Radar
Cloudflare publishes a list called 'Radar', consisting of one million entries, The list is updated weekly, except for the top 100, which is updated daily. The list is available since September 26, 2022. Both websites and infrastructural domains are included. Only pay-level domains are ranked.

The ranks are based on DNS traffic to Cloudflare's 1.1.1.1 resolver. Ranks are computed based on a popularity metric that is designed to reflect "the estimated relative size of the user population that accesses a domain over some period of time", calculated using a machine learning model on the aggregated resolver data. The published ranks are bucketed, in buckets of 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, and 1 million. except for the top 100, which is individually ranked. A more detailed description of Radar's methodology is available on this page.

Farsight
Farsight Security, part of DomainTools, provides a daily updated list consisting of one million entries. Both websites and infrastructural domains are included. Only pay-level domains are ranked. This list is available since May 1, 2022.

The ranks calculated by Farsight are based on passive DNS traffic from its DNSDB dataset. This data originates from a certain set of organizations (or ISPs) who share their "above-resolver" DNS traffic with Farsight Security, meaning the DNS queries for domains that are not present in the cache of the organization's recursive DNS resolver and that therefore are sent over the Internet to the authoritative nameservers of those domains (cache misses).

Majestic
Majestic publishes the daily updated 'Majestic Million' list consisting of one million websites. The list comprises mostly pay-level domains, but includes subdomains for certain very popular sites (e.g. plus.google.com, en.wikipedia.org).

The ranks calculated by Majestic are based on backlinks to websites, obtained by a crawl of around 450 billion URLs over 120 days. Sites are ranked on the number of class C (IPv4 /24) subnets that refer to the site at least once. Majestic's data collection method means only domains linked to from other websites are considered, implying a bias towards browser-based traffic, however without counting actual page visits. Similarly to search engines, the completeness of their data is affected by how their crawler discovers websites.

Cisco Umbrella
Cisco Umbrella publishes a daily updated list consisting of one million entries. Both websites and infrastructural domains are included. Any domain name may be included, with it being ranked on the aggregated traffic counts of itself and all its subdomains.

The ranks calculated by Cisco Umbrella are based on DNS traffic to its two DNS resolvers (marketed as OpenDNS), claimed to amount to over 100 billion daily requests from 65 million users. Domains are ranked on the number of unique IPs issuing DNS queries for them Not all traffic is said to be used: instead the DNS data is sampled and "data normalization methodologies" are applied to reduce biases, taking the distribution of client IPs into account. Umbrella's data collection method means that non-browser-based traffic is also accounted for. A side effect is that invalid domains are also included (e.g. internal domains such as *.ec2.internal for Amazon EC2 instances, or typos such as google.conm).

Deprecated lists
Alexa
Alexa, a subsidiary of Amazon, published a daily updated list consisting of up to one million websites, until August 1, 2023. Usually only pay-level domains are ranked, except for subdomains of certain sites that provide "personal home pages or blogs" (e.g. tmall.com, wordpress.com).

The ranks calculated by Alexa are based on traffic data from a "global data panel", with domains being ranked on a proprietary measure of unique visitors and page views, where one visitor can have at most one page view count towards the page views of a URL. Alexa states that it applies "data normalization" to account for biases in their user panel. The panel is claimed to consist of millions of users, who have installed one of "many different" browser extensions that include Alexa's measurement code. However, through a crawl of all available extensions for Google Chrome and Firefox, we found only Alexa's own extension ('Alexa Traffic Rank') to report traffic data. Moreover, this extension is only available for the desktop version of these two browsers. Chrome's extension is reported to have around 570,000 users; no user statistics are known for Firefox, but extrapolation based on browser usage suggests at most one million users for two extensions, far less than Alexa's claim.

In addition, sites can install an 'Alexa Certify' tracking script that collects traffic data for all visitors; the rank can then be based on these actual traffic counts instead of on estimates from the extension. This service is estimated to be used by 1.06% of the top one million and 4% of the top 10,000.

The rank shown in a domain's profile on Alexa's website is based on data over three months, while the downloadable list was based on data over one month. However, since January 30, 2018 the list is based on data for one day; this was confirmed to us by Alexa but was otherwise unannounced.

Alexa's data collection method leads to a focus on sites that are visited in the top-level browsing context of a web browser (i.e. HTTP traffic). They also indicate that ranks worse than 100,000 are not statistically meaningful, and that for these sites small changes in measured traffic may cause large rank changes, negatively affecting the stability of the list.

Quantcast
Quantcast published a list of the websites visited the most in the United States until April 1, 2020. The size of the list varied daily, but usually was around 520,000 mostly pay-level domains; subdomains reflected sites that publish user content (e.g. blogspot.com, github.io). The list also included 'hidden profiles', where sites are ranked but the domain is hidden.

The ranks calculated by Quantcast were based on the number of people visiting a site within the previous month, and comprised 'quantified' sites where Quantcast directly measured traffic through a tracking script as well as sites where Quantcast estimated traffic based on data from 'ISPs and toolbar providers'. These estimates were only calculated for traffic in the United States, with only quantified sites being ranked in other countries; the list of top sites also only considered US traffic. Moreover, while quantified sites saw their visit count updated daily, estimated counts were only updated monthly, which may have inflated the stability of the list.

Privacy policy
