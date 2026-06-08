# TSPTW: Travelling Salesman Problem with Time Windows
## I - PROBLEM SPECIFICATION
A delivery worker picks up goods at the depot (point $0$) and needs to deliver them to $N$ customers labeled $1$, $2$, ..., $N$. Customer $i$ is located at point $i$ and requires the delivery to be made within the time window from $e(i)$ to $l(i)$, in which the service for this customer takes $d(i)$ units of time (seconds).

Let $t(i,j)$ denote the travel time from point $i$ to point $j$. The delivery worker departs from the depot at time $t_0 = 0$.

Determine a delivery route for the worker such that the total travel time is minimized while satisfying the time window constraints of all customers. Each solution is represented by a permutation $s[1]$, $s[2]$, ..., $s[N]$ of $1$, $2$, ..., $N$.

### Input
The first line contains an integer $N$.

Line $i + 1$ ($i = 1, 2, ..., N$) contains three integers $e(i)$, $l(i)$ and $d(i)$, separated by a space character.

Line $i + N + 2$ ($i = 0, 1, ..., N$) contains the $i^{th}$ row of the matrix $t$, in which the elements are all integers and separated by a space character.

### Output
The first line contains $N$.

The second line contains $s[1]$, $s[2]$, ..., $s[N]$, separated by a space character.

### Example
#### Input
```
5
50 90 20
300 350 15
215 235 5
374 404 20
107 147 20
0 50 10 100 70 10
50 0 40 70 20 40
10 40 0 80 60 0
100 70 80 0 70 80
70 20 60 70 0 60
10 40 0 80 60 0
```
#### Output
```
5
1 5 3 2 4
```

### Constraints:
- $1 \leq N \leq 1000$
- $0 \leq e(i) \leq l(i)$, $i = 1, 2,..., N$
- $d(i) \geq 0$, $i = 1, 2,..., N$
- $t$ is a square matrix of size $n + 1$ with $t(i, j) > 0$ and $t(i, i) = 0$, $i, j = 0, 1, ..., N$, $i \neq j$

See [here](description.txt) for a Vietnamese version.

## II - CODE USAGE
```
git clone https://github.com/datvt029999/tsptw
cd tsptw
```