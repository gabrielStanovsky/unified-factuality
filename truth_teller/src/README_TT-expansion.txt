Analysis of expandedPredicateList.properties:
This lexicon assigns exactly ONE signature to each single-word predicate:

wc -l predicateSignatures.srt
1811 predicateSignatures.srt

wc -l ttLemmas.srt 
1811 ttLemmas.srt

#######################################################################

How TruthTeller encodes the signatures (mapping from paper terminology to implementation terminology):

Clause Truth ct
ct+ -> P (positive)
ct- -> N (negative)
ct? -> U (unknown)

Signature in Table 1 mapped to signature used in  expandedPredicateList.properties:

+/-	P_N
+/?	P_U
?/-	U_N
-/+	N_P
-/?	N_U
?/+	U_P

+/+	P_P (factives)
-/-	N_N (counterfactives)

?/?	U_U (regular)

#######################################################################

##########################################
# Mapping of noun classes to TT signatures
##########################################

**** wh_factual nouns ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh_factual_N ttLemmas.srt | wc -l
103

nouns expressing sentiment towards a fact: map to P_P_FinP

nouns expressing an opinion about anything: U_U
accusation
argument
consideration
counterposition
faith
interest
interpretation
misunderstanding
motivation
motive
objection
opinion
statement
vote

nouns mapped to N_U
inability
incapability

nouns mapped to U_P
uncertainty



overlapping nouns wrt Truthteller
adventure
bad
convention
difficulty
doubt
enjoyment
excuse	 P_P_FinP
force
form
fun
game
grounds
pleasure
position
power
practice
problem
reason
risk	 P_N_InfP 
sense
shame	 P_P_FinP 
stress	 P_P 
theme
topic
view	 P_P_FinP 
wise
wonder
wrong	 N_P 



**** future-oriented nouns ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 future-oriented_N ttLemmas.srt | wc -l
122

nouns expressing modal meanings: map to U_U

nouns correponding to negated modals: map to N_U 
ban
impossibility
refusal

map to P_U
inevitability


overlapping nouns and their signatures:
- permission U_N, offer U_U
?? opportunity	 P_N_InfP
- order
- ability
- necessity



**** wh-if_factual nouns ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh-if_factual_N ttLemmas.srt | wc -l
53

default: map to P_N

map to P_P
awareness
conflict
controversy
discrimination
struggle
disputation
scramble

map to U_U
discussion
discourse


overlapping nouns
case
conclusion	 P_P_FinP 
estimate	 U_P 
idea
judgement	 P_P_FinP 
list
matter
note
probability	 P_N_InfP 
process
project
result	 P_U 
sentence
situation
talk
view	 P_P_FinP 


**** non-factual nouns ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 non-factual_N ttLemmas.srt | wc -l
19



###############################################
# Mapping of adjective classes to TT signatures
###############################################


**** wh_factual adjectives ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh_factual_A ttLemmas.srt | wc -l
192

default: map to P_P 

map to N_P:
unreal


overlapping adjectives and their signatures
risky	 P_P 



**** future-oriented adjectives ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 future-oriented_A ttLemmas.srt | wc -l
67

default: map to U_U

adjectives corresponsing to negated modals: map to N_U
impossible
late
unthinkable

map to P_P:
grateful
sufficient
suitable
tired


overlapping adjectives and their signatures:
bound
curious
daring
eager
endeavor
free
inevitable
light
obvious
practiced
proud
ready
ripe
sure
unable


**** wh-if_factual adjectives ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh-if_factual_A ttLemmas.srt | wc -l
37

default: map to P_P

map to U_U
controllable
estimated

map to P_U
foreseeable
predictable


map to U_P
doubtful
questionable
skeptical
uncertain
unclear
undecided
unproven


**** non-factual adjectives ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 non-factual_A ttLemmas.srt 
confident
convinced

default: map to U_U


###############################################
# Mapping of verb classes to TT signatures
###############################################


**** future-oriented verbs ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 future-oriented_V ttLemmas.srt | wc -l
98

strategy to deal with verbs belonging to more than one class:
map all future-oriented verbs with top priority

default mapping: U_U

map to N_U
boycott
cancel
hamper
reject
suspend
waive

map to P_U
enforce


NOT MAPPED:
compare
comprehend
contribute
coordinate
count
deserve
document
enjoy
equal
exceed
fit
gain
honor ### also wh_factual
judge
keep
learn
modest
monitor
need
obtain
pending
praise
pray
preach
problematize
proper
save
shiver
stand
sue
teach
test
thematize



**** wh_factual verbs ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh_factual_V ttLemmas.srt | wc -l
55

default mapping: P_P

overlap with future-orientation: appeal, honor

only add a verb, if no overlap with future-oriented

not added:
admit
affirm
answer
attribute
clarify
contradict
cover
dawn
decrease
deduce
draw
dream
elaborate
enumerate
exemplify
grasp
hide
hush
illustrate
imagine
match
present
reaffirm
scourge
sign
smile
suppose
symbolize



**** wh-if_factual verbs ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 wh-if_factual_V ttLemmas.srt | wc -l
44

default mapping: P_U

map to P_P_FinP
overlook


not mapped
announce
appear
argue
bequeath
brood
capture
conceal
definite
differ
establish
hand
hide
imagine
include
judge
present
reckon
save
stick
veil
worry



**** non-factual verbs ****
eckle@desktop-155:~/Dropbox/factualityMarkers$ comm -23 non-factual_V ttLemmas.srt | wc -l
32

default: map to U_U

map to N_P
lie

not mapped:
admit
affirm
aim
blackjack
complain
exclude
give
harm
hope
justify
name
recognise
reproach
require
suggest
unacceptable
worth









