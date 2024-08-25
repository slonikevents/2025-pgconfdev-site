from invoke import task


@task(help={"relative_to": "render each link absolute with this prefix"})
def render(c, relative_to=None):
    """Render the static site (into `site`)"""

    from jinja2 import Environment, FileSystemLoader
    from pathlib import Path
    import inspect
    import os.path
    import shutil
    import subprocess
    import yaml

    # Add each cached and untracked file to the site
    command = ("git", "ls-files", "-coz", "--exclude-standard")
    output = subprocess.check_output(command, text=True)
    site = set(output.removesuffix("\x00").split("\x00"))

    # Then remove each file with "site-ignore" set
    command = ("git", "check-attr", "-z", "site-ignore", "--", *site)
    output = subprocess.check_output(command, text=True)
    while output:
        name, _, status, output = output.split("\x00", 3)
        if status not in ("no", "unspecified"):
            site.remove(name)

    # Delete each untracked file in the output root
    subprocess.check_call(("git", "clean", "-fqx", "site"))

    def link(target):
        """
        Return the *target* path in accordance to the root path *relative_to*.

        This filter should be used whenever a link or reference to a resource
        within the site itself is made.

        First, *target* is made into an absolute path where "/" is the root of
        the site. If *target* is already an absolute path, it's unchanged.
        Otherwise, it's made into an absolute path by concatenating it to
        parent directory of the template calling this filter. For example,
        within a filter ``some/template.html.j2``::

             {{ "relative.html" | link }}  =>  "/some/relative.html"
            {{ "/absolute.html" | link }}  =>  "/absolute.html"

        Then, if *relative_to* is ``None``, this returns a path relative to the
        parent directory of the template calling this filter. Otherwise, this
        returns *relative_to* joined with *target*. For example, within a
        filter ``some/template.html.j2``, if *target* is ``/some/object.html``,
        then:

            * If *relative_to* is ``None``, this returns ``object.html``.
            * Otherwise, if *relative_to* is ``http://localhost:8000/``, this
              returns ``http://localhost:8000/some/object.html``.
        """

        # Locate the caller of the filter (this should be the most recent
        # template in the call stack). See
        # https://github.com/pallets/jinja/blob/3.1.4/src/jinja2/debug.py#L55
        for info in inspect.stack():
            if (template := info.frame.f_globals.get("__jinja_template__")) is not None:
                break
        else:
            raise RuntimeError("link() must be called from a Jinja2 template")
        origin = Path("/") / Path(template.filename).parent

        if not target.startswith("/"):
            target = origin / target
        target = Path(os.path.normpath(target))

        if relative_to is not None:
            return os.path.join(relative_to, target.relative_to("/"))
        return os.path.relpath(target, origin)

    # Create the Jinja2 environment and context
    environment = Environment(loader=FileSystemLoader("."))
    environment.filters["link"] = link
    context = yaml.safe_load(Path("context.yaml").read_text()) or {}

    # Render each extant source file in sorted order
    for source in sorted(Path(i) for i in site if Path(i).is_file()):
        target = Path("site") / source
        target.parent.mkdir(parents=True, exist_ok=True)

        if source.suffix != ".j2":
            print(f"Copying {str(source)!r} to {str(target)!r} ...")
            shutil.copyfile(source, target)
            continue

        target = target.with_suffix("")
        print(f"Rendering {str(source)!r} to {str(target)!r} ...")
        template = environment.get_template(str(source))
        target.write_text(template.render(context))


@task(help={"port": "port to open the HTTP server on (default: 8000)"})
def server(c, port=8000):
    """Open an HTTP server to serve the rendered site"""

    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    import functools

    site = functools.partial(SimpleHTTPRequestHandler, directory="site")
    with ThreadingHTTPServer(("127.0.0.1", port), site) as server:
        print(f"Opened HTTP server at http://127.0.0.1:{port}/ ...")
        server.serve_forever()
