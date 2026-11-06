# Clusters

Run several instances of one app, with a port for each.

Source: https://oxidepm.com/docs/configuration/clusters/

```sh
oxidepm start ./server -i 4 --port 3000
```

or in a config file:

*oxidepm.config.toml*

```toml
[[apps]]
name = "web"
mode = "node"
script = "server.js"
instances = 4
port = 3000
```

## The shape of a cluster

A cluster is a parent (`web`, with no process) and one app per instance (`web-0`, `web-1`, and so on). There are at most 256 instances. Instance `i` gets port `port + i`, or the start of `port_range` plus `i`. The range must hold every instance, and `port` and `port_range` together are refused.

## Starting and stopping

- The cluster is created all at once. A name that is already taken (`web-1` included) refuses the start with `E_APP_EXISTS` and writes nothing. If an instance cannot launch on the first start, the whole cluster is deleted again and the instance's error is returned.
- Starting a cluster that exists starts only the instances that are at rest: after `stop web-1`, `start web` brings back `web-1` and leaves the others running.
- The number of instances cannot change (`E_INVALID_SPEC`). Delete and recreate. That includes starting an existing single app with more than one instance, or an existing cluster with one.
- `delete web` removes the parent and all instance rows in one transaction, before any instance is stopped.
- A tag or `all` that matches a cluster and its instances acts on the cluster once. `web-1` by name acts on that instance only.

## Policy

The markers `protected` and `ai_control` of a cluster apply to every instance. An instance created later takes the markers of its cluster. An instance can be set on its own, but it counts as protected when its cluster is, and as open to AI control only when both are.
