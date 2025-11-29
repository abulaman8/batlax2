# Comments extracted from remove_comments.py

- Line 107: # Vue files can have HTML comments in template, and JS/CSS comments in script/style
- Line 108: # We'll run both. HTML first, then JS/CSS.
- Line 109: # Note: This might be slightly risky if JS strings contain <!--, but unlikely.
- Line 149: # Append if file exists (for iterative runs)? No, overwrite is safer to avoid dupes.
- Line 150: # But wait, if we re-run, the source file has no comments, so comments list will be empty.
- Line 151: # So we shouldn't overwrite if comments is empty, but here comments is NOT empty.
- Line 152: # If we re-run on ALREADY processed file, comments will be empty, so we won't overwrite docs.
- Line 153: # That's good.
