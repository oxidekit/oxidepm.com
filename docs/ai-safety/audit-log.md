# Audit log

What is written to the audit log, what is not, and how to read it.

Source: https://oxidepm.com/docs/ai-safety/audit-log/

Everything an AI or an adapter asks for is recorded, and so is every caution or dangerous request by anyone.

## The files

The log is two JSON-lines files in `~/.oxidepm/audit/` (the directory is mode 0700, the files 0600, created when the first line is written):

- `audit.jsonl`: every recorded request.
- `audit-security.jsonl`: the denials, the dangerous requests, and what a non-human actor changed. A chatty but permitted actor cannot rotate this file's evidence away.

Each request leaves a `decision` line (who asked, the operation and its tier, the selector and the apps it reached, `allow` or `deny` with the reason) and, if it ran, a `result` line (`ok`, the error code, how many apps changed or failed, the milliseconds). The two share a `req` number the daemon assigns. The id the client chose is kept as `client_req`. A start also records the program, the number of arguments and a digest of them. `seq` counts up across rotation, so a gap shows a lost line.

*Lines of audit-security.jsonl*

```text
{"v":1,"seq":5,"ts":"2026-11-25T21:35:24.051Z","phase":"decision","req":"r103","client_req":"3af779-1","actor":{"class":"ai","label":"assistant","via":"agent","pid":3864441,"uid":1001},"op":"restart","tier":"caution","selector":"db","decision":"deny","deny":{"code":"E_PROTECTED","why":"ai:assistant may not restart protected app(s): db. A protected app is read-only for anything but a person"},"dry_run":false}
{"v":1,"seq":6,"ts":"2026-11-25T21:35:24.057Z","phase":"decision","req":"r104","client_req":"3af7a3-1","actor":{"class":"ai","label":"assistant","via":"agent","pid":3864483,"uid":1001},"op":"delete","tier":"dangerous","selector":"api","decision":"deny","deny":{"code":"E_POLICY_DENIED","why":"ai:assistant may not make the request 'delete': it is a dangerous request. Ask a person to run it"},"dry_run":false}
{"v":1,"seq":7,"ts":"2026-11-25T21:35:24.062Z","phase":"decision","req":"r105","client_req":"3af7cc-1","actor":{"class":"ai","label":"assistant","via":"agent","pid":3864524,"uid":1001},"op":"stop","tier":"caution","selector":"all","decision":"deny","deny":{"code":"E_POLICY_DENIED","why":"ai:assistant may not use 'all' or a tag with 'stop': name the apps"},"dry_run":false}
```

## What is recorded

- Every request of a non-human actor. Repeated `ping`, `hello` and `status` are one line per actor and operation per minute, with a count. `show`, `describe` and `logs` are one line each, with the app, because they are how arguments and logs are read.
- A person's caution and dangerous requests.
- Every denial, whoever asked.

## What is never written

Environment values, hook and probe scripts, the arguments themselves, log lines, the app spec and adapter configuration. The record is a fixed set of fields with no place for them, and free text is cut to a fixed length.

## Written before it runs

A non-human actor's caution or dangerous request is written to disk before it runs. If the log cannot be written (the directory is a file, the disk is full, the writer is stuck), the request is refused with `E_AUDIT_UNAVAILABLE` and nothing happens. A read still goes through, and the lost line is counted. A person is never held up: a stop works while the log is broken, which is how a full-disk incident is handled. The lines that could not be written are counted. `oxidepm status --daemon` shows `audit log: ok` or `degraded`, how many lines were lost, and what is wrong.

## Read it

*Terminal output of oxidepm audit*

```text
$ oxidepm audit --tail 7
2026-11-25T21:35:24.039Z #7      ai:assistant stop [caution] allow web (dry run)
2026-11-25T21:35:24.046Z #8      result r102 ok changed=0 failed=0 0ms
2026-11-25T21:35:24.051Z #9      ai:assistant restart [caution] DENIED E_PROTECTED: ai:assistant may not restart protected app(s): db. A protected app is read-only for anything but a person db
2026-11-25T21:35:24.057Z #10     ai:assistant delete [dangerous] DENIED E_POLICY_DENIED: ai:assistant may not make the request 'delete': it is a dangerous request. Ask a person to run it api
2026-11-25T21:35:24.062Z #11     ai:assistant stop [caution] DENIED E_POLICY_DENIED: ai:assistant may not use 'all' or a tag with 'stop': name the apps all
2026-11-25T21:35:24.065Z #12     human:cli set_policy [dangerous] allow web
2026-11-25T21:35:24.067Z #13     result r106 ok changed=1 failed=0 1ms
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
