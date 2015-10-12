# hipshare
Share yr shell output via XMPP

## y
Issue resolution. By multiplexing information to yr team in realtime you can:

+ Democratize the analysis of a situation
+ Avoid feeling helpless while someone else investigates a problem
+ Annoy people & satisfy yr boundless hatred of humanity via spam

## do et
+ python 3 pls
+ ```pip install -r requirements.txt```
+ ```./run <strategy>```

Look at the config samples for more details

## caveat
This is buggy yo

## todo (halp!)
+ pty has no idea when to exit since bash never sends EOF, tl;dr right now you have to hit enter twice to exit pty, it might be smarter to use a higher level interface like pexpect
+ timeouts
+ reconnection
+ support DMs (no more pasting shell output!)
+ if you send messages too fast they may arrive out of order (is order guaranteed by the spec?)
+ output is truncated at 80 chars
+ interactive programs do weird stuff (try ```sl```)

## thx
Inspired by ppl at devopsdays boston who already do something like this.
