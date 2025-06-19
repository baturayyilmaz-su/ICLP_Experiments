
% Helpers based on input
acceptable(A1,A2) :- arank(A1,A2,_), arank(A2,A1,_). % if a A1 and A2, then A1 != A2 is a consequence of this rule because agents dont rank themselves.
aPrefers(A,A1,A2) :- arank(A,A1,R1), arank(A,A2,R2), R1<R2. % A1!=A2 may not be needed. Every agent ranks other agents once in the input

% Generate a matching
0{matched(A1,A2) : agent(A1), acceptable(A1,A2)}1 :- agent(A2). % Agent cannot be matched with itself. Because it is not acceptable to itself
:- matched(A1,A2), not matched(A2,A1). % If A1 is matched with A2, A2 is matched with A1.
aSingle(A) :- not matched(A,_), agent(A).
:- matched(A,A1), matched(A,A2), A1!=A2. % Every agent can be matched at most once

blockingPair(A1,A2) :- aSingle(A1), aSingle(A2), acceptable(A1,A2).%, A1!=A2.
blockingPair(A1,A2) :- aSingle(A2), matched(A1,X), aPrefers(A1,A2,X), acceptable(A1,A2).%, A1!=A2.
blockingPair(A1,A2) :- aSingle(A1), matched(A2,X), aPrefers(A2,A1,X), acceptable(A1,A2).%, A1!=A2.
blockingPair(A1,A2) :- matched(A1,X), matched(A2,Y), aPrefers(A1,A2,X), aPrefers(A2,A1,Y).%, acceptable(A1,A2), A1!=A2. 


:- blockingPair(A1,A2), agent(A1), agent(A2).


#show matched/2.
#show aSingle/1.