# Troubleshooting notes

Four things broke on the way to a working agent. Writing them down while I still
remember why.

## Container exits immediately

`latest` gave me 3.1.4, which doesn't start at all. Three errors: a LangChain
uuid subpath that isn't exported anymore, a missing `@smithy/eventstream-codec`,
and `this.db.exec is not a function` out of connect-sqlite3. Reported upstream
already. Pinned to `3.1.3`, starts fine.

The log is worth reading properly. The first two errors look fatal and aren't,
the server carries on past them and even prints a success line. The real cause
is the last thing before the process dies. Read it bottom up.

## "qwen2.5:7b does not support thinking"

Reasoning is a training property, not a setting. qwen2.5 was never trained for
it, so Ollama refuses the request. Switched the option off on the Agent node.

## "fetch is not defined" inside the tool

Tool code runs in a vm2 sandbox. Makes sense once you think about who can write
that code: anyone with access to the UI, executing JavaScript on the server.
So globals and imports are restricted until you say otherwise.

`TOOL_FUNCTION_BUILTIN_DEP=*` and `TOOL_FUNCTION_EXTERNAL_DEP=axios,node-fetch`,
then rewrote the tool on axios. Note that axios throws on 404 instead of handing
back `ok: false`, so the 404 handling moved into the catch block.

## "isDeniedIP: Access to this host is denied by policy"

SSRF protection. Flowise resolves the hostname, checks the IP against a deny
list, and blocks private ranges. `host.docker.internal` resolves to
192.168.65.254, which is inside that list.

I wasted a good half hour here assuming `HTTP_DENY_LIST` replaces the default
list. It doesn't. It appends to it, so nothing I put in there could ever help.
Ended up grepping `httpSecurity.js` inside the container, where a comment says
the built-in list is only skipped when `HTTP_SECURITY_CHECK=false`. Also worth
knowing: that check compares against the string `'false'`, so `False` or `0`
silently leaves protection on.

Running locally with the check disabled and the cloud metadata endpoint
(169.254.169.254) still denied by hand. Not what I'd do on a server. There the
API goes in the same Docker network and the check stays where it is.

## Final run command

```
docker run -d --name flowise \
  -p 3100:3000 \
  -v flowise_data:/root/.flowise \
  -e TOOL_FUNCTION_BUILTIN_DEP=* \
  -e TOOL_FUNCTION_EXTERNAL_DEP=axios,node-fetch \
  -e HTTP_SECURITY_CHECK=false \
  -e HTTP_DENY_LIST=169.254.169.254/32 \
  flowiseai/flowise:3.1.3
```

Port 3100 because Grafana already owns 3000 on this machine.
