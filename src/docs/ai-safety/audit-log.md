Everything an AI or an adapter asks for is recorded, and so is every caution or dangerous request by anyone.

## The files

The log is two JSON-lines files in `~/.oxidepm/audit/` (the directory is mode 0700, the files 0600, created when the first line is written):

- `audit.jsonl`: every recorded request.
- `audit-security.jsonl`: the denials, the dangerous requests, and what a non-human actor changed. A chatty but permitted actor cannot rotate this file's evidence away.

Each request leaves a `decision` line (who asked, the operation and its tier, the selector and the apps it reached, `allow` or `deny` with the reason) and, if it ran, a `result` line (`ok`, the error code, how many apps changed or failed, the milliseconds). The two share a `req` number the daemon assigns. The id the client chose is kept as `client_req`. A start also records the program, the number of arguments and a digest of them. `seq` counts up across rotation, so a gap shows a lost line.

```term wrap="yes" label="Lines of audit-security.jsonl" cap="audit-json"
```

## What is recorded

- Every request of a non-human actor. Repeated `ping`, `hello` and `status` are one line per actor and operation per minute, with a count. `show`, `describe` and `logs` are one line each, with the app, because they are how arguments and logs are read.
- A person's caution and dangerous requests.
- Every denial, whoever asked.

## What is never written

Environment values, hook and probe scripts, the arguments themselves, log lines, the app spec and adapter configuration. The record is a fixed set of fields with no place for them, and free text is cut to a fixed length.

## Written before it runs

A non-human actor's caution or dangerous request is written to disk before it runs. If the log cannot be written (the directory is a file, the disk is full, the writer is stuck), the request is refused with `E_AUDIT_UNAVAILABLE` and nothing happens. A read still goes through, and the lost line is counted. A person is never held up: a stop works while the log is broken, which is how a full-disk incident is handled. The lines that could not be written are counted. `oxidepm status --daemon` shows `audit: ok` or `degraded`, how many lines were lost, and what is wrong.

## Read it

```term cap="audit" label="Terminal output of oxidepm audit"
```

```sh
oxidepm audit --tail 50
oxidepm audit --actor ai:assistant        # or just `ai`, or just `assistant`
oxidepm audit --op restart
oxidepm audit --since 30m              # or an RFC 3339 time
oxidepm audit --security               # the second file
oxidepm --json audit                   # one JSON object per line
```

`oxidepm audit` reads the files directly, so it works with the daemon down. A request that matches keeps its result line. Every string an actor could have written (labels, reasons, notes) is printed with control characters replaced, so a label cannot move the cursor or paint over the lines around it.

## Rotation and limits

The files rotate at 10 MiB (5 MiB for the security file) and keep ten each. There is no tamper evidence beyond the file mode: a process with your rights can rewrite the files, as it can rewrite the database.
