# Gotchas learned the hard way

## Decisions
- Any rule with `action: deny` that matches wins; otherwise the request is
  allowed and `allow_log` hits are recorded. Two rules can safely overlap if
  the stricter one should win.
- The deny reason shown to the user comes from the highest-severity deny.

## Detectors
- `classification` detector options (`require_marking`,
  `media_type_prefixes`) go under `detector:`, next to `type:`.
- With `require_marking: true` the detector reports only "unmarked" and skips
  typed prompts (not attachments), files it could not read, and media types
  outside `media_type_prefixes`. An empty prefix list means every attachment,
  which would also deny plain notes.
- The `attachment` detector matches only files with no extracted text or that
  were not inspected. `media_type_prefixes: [""]` means every such file.
- A ladder level with `markings: []` can never satisfy a marking check, so a
  document at that level is treated as unmarked.

## Environment
- On Windows, Python's module-level `mimetypes` functions read the registry;
  with Excel installed `.csv` becomes an Office media type. Use a private
  `mimetypes.MimeTypes()` instance so results match on every machine.
- `DLP_*` environment variables must not weaken an admin policy. When one is
  ignored it is recorded in `env_ignored`.

## Reading code while debugging
- `print(repr(x), y)` printing `('closed', []) []` means `x` is a tuple: look
  for a trailing `, something` after a closing parenthesis.
- PowerShell: `Select-String` has no `-Recurse`; pipe `Get-ChildItem -Recurse`
  into it. Run commands one per line; a second command on the same line is
  passed as arguments to the first.
