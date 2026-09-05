
## Running the dev server

```bash
cd ~/Projects/auralab-astro
env -u NODE_ENV npx astro dev --port 4321 --host 127.0.0.1
```

`NODE_ENV` **must not** be `production`. If it is, Astro refuses to serve
`/_image/` — every optimised image 500s with "The dev image endpoint can only be
used in dev mode" and the site renders with all portraits and figures missing,
while every page still returns 200. A shell that inherits `NODE_ENV=production`
from a parent process is the usual cause.
