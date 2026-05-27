# First-Time Setup for EXTEND.md

When `EXTEND.md` is missing, setup is blocking. Ask all preference questions in one interaction before creating the file.

## Questions (single interaction)

1. **Media**: How to handle images and videos?
   - Ask each time (`download_media: ask`)
   - Always download (`download_media: 1`)
   - Never download (`download_media: 0`)
2. **Output**: Default output directory?
   - Recommended: `url-to-markdown`
   - Or a custom path
3. **Save location**:
   - User-level: `~/.baoyu-skills/baoyu-url-to-markdown/EXTEND.md`
   - Project-level: `.baoyu-skills/baoyu-url-to-markdown/EXTEND.md`

## File template

```yaml
download_media: ask
default_output_dir: ""
```

## Rules

- Do not silently create defaults without asking.
- Confirm the final path after writing.
- Continue URL conversion only after setup is complete.
