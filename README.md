# listkeeper

- [ ] Option to exclude columns
- [ ] Single-line entries
- [ ] Search multiple input files (synthesis)
- [ ] proper parser in Python

positional
keyed

header [2 or more lines terminated by blank line] -- builds item definition
body [1 or more items delinated by non-indented lines, blank lines between items are ignored]


title
score
:finished

Shall We Dance
  3.2
  finished::2016/05/19
Wild Wild West
  1.2
The Princess Bride
  4.5

==

title
  score
  :finished

Shall We Dance
  3.2
  finished::2016/05/19

Wild Wild West
  1.2

The Princess Bride
  4.5


---------------------

# single-line list, header is terminated by blank line,
# afterwhich blank lines are ignored

title

Shall We Dance
Wild Wild West
The Princess Bride

#--

title
score    #- positional field
:watched #- keyed field

Shall We Dance
  2.3
Star Wars V
  watched::2002/05/31
Another Movie
2 Fast 2 Furious
  9.9

#--

list ->  def items

def -> var vars kvars
vars -> var vars | e
kvars -> kvar kvars | e
kvar -> :var
var -> string

items -> item items | e
item -> prop props kprops
props -> prop props | e
kprops -> kprop kprop | e
kprop -> var::prop
prop -> string
