All of these are enforced by the daemon. None depends on the adapter's cooperation. They are constants of the protocol version, not configuration.

| What | Limit | When exceeded |
|---|---|---|
| A line, adapter to daemon | 256 KiB | Skipped without being stored. A violation. |
| A frame the daemon would send | 256 KiB | A request is refused before it is sent (`E_ADAPTER_INVALID`). An answer to an adapter's request that is too large is replaced by `E_REQUEST_TOO_LARGE`. |
| An `event` line | 16 KiB | Trimmed. |
| Requests in flight, each direction | 32 (up to 128 for `host.request`, when the grant asks) | The new request fails at once (`-32029`, `E_ADAPTER_BUSY`). |
| Frames from the adapter | 500 a second sustained, burst 1000; 8 MiB a second | The daemon stops reading, so the adapter blocks on its own pipe. Throttled for 10 seconds without a break is a violation. |
| A write to the adapter's input | No progress for 5 seconds | The connection is closed and the adapter killed. |
| Strikes | 3 in 60 seconds | The adapter is killed and counts as a crash. |
| Expired request ids remembered | 1024, for 5 minutes | A late reply with such an id is dropped without a strike. |
| `initialize` | 10 seconds | The adapter fails the handshake. |
| `ping` | 5 seconds to answer | Three misses in a row kill a service. |

## What is a violation

A violation, also called a strike, is: a line that is not a valid frame, an oversize line, a frame before `initialize`, a response to an id that was never issued or was already answered, a reply that does not have the shape of its method, or being throttled too long.

An adapter request with bad params is not a violation. It gets an error. A line that ends the stream half way, an end of file, or a read error closes the connection.
